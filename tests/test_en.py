"""tools/en: ai_style_diag, bundle_diag, metadiscourse_en, biber_diag, lt_check.sh.
The corpus tools run against a synthetic 30-paper corpus built in a temp dir."""
import pathlib
import shutil

import pytest

from conftest import english_text, load_tool, make_corpus, run_tool


@pytest.fixture
def corpus(tmp_path):
    return make_corpus(tmp_path / "corpus")


@pytest.fixture
def draft(tmp_path):
    f = tmp_path / "draft.md"
    f.write_text(english_text(999, 1000), encoding="utf-8")
    return f


def test_ai_style_diag_selftest():
    r = run_tool("en/ai_style_diag.py", "--selftest")
    assert r.returncode == 0, r.stdout + r.stderr


def test_ai_style_diag_contrast_counts():
    A = load_tool("en/ai_style_diag.py")
    c = A.contrast_counts("We chose interviews rather than surveys. It was a probe, not a product.")
    assert c["rather"] == 1 and c["commanot"] == 1 and c["contrast"] == 2


def test_ai_style_diag_against_corpus(corpus, draft, tmp_path):
    r = run_tool("en/ai_style_diag.py", draft, "--corpus", corpus, home=tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "baseline 30 field papers" in r.stdout


def test_ai_style_diag_refuses_small_corpus(tmp_path, draft):
    small = make_corpus(tmp_path / "small", n=5)
    r = run_tool("en/ai_style_diag.py", draft, "--corpus", small, home=tmp_path)
    assert r.returncode != 0 and "need ≥30" in r.stderr


def test_bundle_diag(corpus, draft, tmp_path):
    r = run_tool("en/bundle_diag.py", draft, "--lang", "en", "--corpus", corpus, home=tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "baseline 30 field papers" in r.stdout


def test_metadiscourse_en(corpus, draft, tmp_path):
    r = run_tool("en/metadiscourse_en.py", draft, "--corpus", corpus, "--matches", home=tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "baseline 30 field papers" in r.stdout
    assert (tmp_path / ".cache" / "metadiscourse_en_kit_baseline.json").is_file()


def test_biber_diag_needs_corpus(tmp_path, draft):
    r = run_tool("en/biber_diag.py", draft, home=tmp_path)
    assert r.returncode != 0 and "baseline corpus" in r.stderr
    r = run_tool("en/biber_diag.py", draft, "--corpus", tmp_path / "missing", home=tmp_path)
    assert r.returncode != 0 and "Corpus dir not found" in r.stderr


def test_lt_check_argument_handling(tmp_path, draft):
    assert run_tool("en/lt_check.sh").returncode == 2
    assert run_tool("en/lt_check.sh", tmp_path / "missing.md").returncode == 2
    assert run_tool("en/lt_check.sh", draft, "--bogus").returncode == 2
    r = run_tool("en/lt_check.sh", draft, env={"LT": str(tmp_path / "no-languagetool")})
    assert r.returncode == 3 and "languagetool not found" in r.stderr
    r = run_tool("en/lt_check.sh", "--help")
    assert r.returncode == 0 and "LanguageTool" in r.stdout


def _run_lt_check(tmp_path, *args):
    """Run lt_check.sh with the stub LanguageTool and a private TMPDIR, so the test
    can see exactly what the script leaves behind."""
    tmpdir = tmp_path / "tmpdir"
    tmpdir.mkdir(exist_ok=True)
    r = run_tool("en/lt_check.sh", *args, home=tmp_path,
                 env={"LT": str(_fake_languagetool(tmp_path)), "TMPDIR": str(tmpdir)})
    return r, tmpdir


def test_lt_check_runs_with_system_mktemp_and_cleans_up(tmp_path):
    f = tmp_path / "draft.txt"
    f.write_text("Plain text.\n", encoding="utf-8")
    r, tmpdir = _run_lt_check(tmp_path, f)
    assert r.returncode == 0, r.stderr
    assert "Plain text." in r.stdout
    assert list(tmpdir.iterdir()) == [], "lt_check.sh left temp files behind"


def test_lt_check_keep_leaves_the_file_it_checked(tmp_path):
    f = tmp_path / "draft.txt"
    f.write_text("Kept text.\n", encoding="utf-8")
    r, tmpdir = _run_lt_check(tmp_path, f, "--keep")
    assert r.returncode == 0, r.stderr
    kept = pathlib.Path(r.stderr.split("[intermediate plain text: ", 1)[1].split("]", 1)[0])
    assert kept.suffix == ".txt" and tmpdir in kept.parents
    assert kept.read_text(encoding="utf-8") == "Kept text.\n"
    # the path LanguageTool was given is the path that was kept
    assert f"ARGS -l en-US {kept}" in r.stdout


def _fake_languagetool(tmp_path):
    """Stand-in for the LanguageTool binary: prints its arguments and the text it got."""
    lt = tmp_path / "languagetool"
    lt.write_text('#!/usr/bin/env bash\necho "ARGS $*"\ncat "${@: -1}"\n', encoding="utf-8")
    lt.chmod(0o755)
    return lt


def test_lt_check_plain_text_with_stub(tmp_path):
    f = tmp_path / "draft.txt"
    f.write_text("Their results was clear.\n", encoding="utf-8")
    r, _ = _run_lt_check(tmp_path, f, "--variant", "en-GB")
    assert r.returncode == 0, r.stderr
    assert "ARGS -l en-GB" in r.stdout and "Their results was clear." in r.stdout


def test_lt_check_markdown_filter_strips_code_and_math(tmp_path):
    if not shutil.which("pandoc"):
        pytest.skip("pandoc not installed")
    f = tmp_path / "draft.md"
    f.write_text("Prose stays here.\n\n```\ncode_block_text\n```\n\nInline `inline_code` and $x_math$ "
                 "and [@citekey2024].\n", encoding="utf-8")
    r, tmpdir = _run_lt_check(tmp_path, f, "--json")
    assert r.returncode == 0, r.stderr
    assert "Prose stays here." in r.stdout and "--json" in r.stdout
    for gone in ("code_block_text", "inline_code", "x_math", "citekey2024"):
        assert gone not in r.stdout
    assert list(tmpdir.iterdir()) == []
