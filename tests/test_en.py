"""tools/en: ai_style_diag, bundle_diag, metadiscourse_en, biber_diag, lt_check.sh.
The corpus tools run against a synthetic 30-paper corpus built in a temp dir."""
import os
import pathlib
import shutil
import subprocess

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


def _gnu_mktemp_rejects_bare_template():
    r = subprocess.run(["mktemp", "-t", "ltcheck"], capture_output=True, text=True)
    if r.returncode == 0:
        pathlib.Path(r.stdout.strip()).unlink(missing_ok=True)
    return r.returncode != 0


def _path_with_mktemp_shim(tmp_path):
    """lt_check.sh calls `mktemp -t ltcheck`, which only BSD mktemp (macOS) accepts.
    On GNU systems put a shim first on PATH that adds the X's, so the rest of the
    script can still be exercised. The bug itself is pinned by the xfail test below."""
    if not _gnu_mktemp_rejects_bare_template():
        return {}
    real = shutil.which("mktemp")
    shim_dir = tmp_path / "shim"
    shim_dir.mkdir()
    shim = shim_dir / "mktemp"
    shim.write_text(f'#!/usr/bin/env bash\nexec {real} "${{@:1:$#-1}}" "${{@: -1}}.XXXXXX"\n',
                    encoding="utf-8")
    shim.chmod(0o755)
    return {"PATH": f"{shim_dir}:{os.environ['PATH']}"}


@pytest.mark.xfail(_gnu_mktemp_rejects_bare_template(), strict=True,
                   reason="existing bug: lt_check.sh uses `mktemp -t ltcheck`, rejected by GNU mktemp")
def test_lt_check_runs_with_system_mktemp(tmp_path):
    f = tmp_path / "draft.txt"
    f.write_text("Plain text.\n", encoding="utf-8")
    r = run_tool("en/lt_check.sh", f, home=tmp_path, env={"LT": str(_fake_languagetool(tmp_path))})
    assert r.returncode == 0, r.stderr


def _fake_languagetool(tmp_path):
    """Stand-in for the LanguageTool binary: prints its arguments and the text it got."""
    lt = tmp_path / "languagetool"
    lt.write_text('#!/usr/bin/env bash\necho "ARGS $*"\ncat "${@: -1}"\n', encoding="utf-8")
    lt.chmod(0o755)
    return lt


def test_lt_check_plain_text_with_stub(tmp_path):
    f = tmp_path / "draft.txt"
    f.write_text("Their results was clear.\n", encoding="utf-8")
    r = run_tool("en/lt_check.sh", f, "--variant", "en-GB", home=tmp_path,
                 env={"LT": str(_fake_languagetool(tmp_path)), **_path_with_mktemp_shim(tmp_path)})
    assert r.returncode == 0, r.stderr
    assert "ARGS -l en-GB" in r.stdout and "Their results was clear." in r.stdout


def test_lt_check_markdown_filter_strips_code_and_math(tmp_path):
    if not shutil.which("pandoc"):
        pytest.skip("pandoc not installed")
    f = tmp_path / "draft.md"
    f.write_text("Prose stays here.\n\n```\ncode_block_text\n```\n\nInline `inline_code` and $x_math$ "
                 "and [@citekey2024].\n", encoding="utf-8")
    r = run_tool("en/lt_check.sh", f, "--json", home=tmp_path,
                 env={"LT": str(_fake_languagetool(tmp_path)), **_path_with_mktemp_shim(tmp_path)})
    assert r.returncode == 0, r.stderr
    assert "Prose stays here." in r.stdout and "--json" in r.stdout
    for gone in ("code_block_text", "inline_code", "x_math", "citekey2024"):
        assert gone not in r.stdout
