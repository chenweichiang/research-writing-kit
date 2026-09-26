"""tools/register (register_profile, polish_check), tools/zh-tw/zh_register, the register
options of the English corpus tools, and voice_lint's paper mode. Every corpus and draft here
is synthetic: generated from fixed word lists, never real writing."""
import json

import pytest

from conftest import english_text, load_tool, make_corpus, run_tool

DASH = chr(0x2014)
ZH_DRAFT = "# 合成測試稿\n\n" + "\n\n".join(
    "本文以問卷蒐集資料。本文分析結果。本文討論意義。受訪者提供回饋。" * 12 for _ in range(4)) + "\n"


@pytest.fixture
def zh_corpus(tmp_path):
    return load_tool("zh-tw/zh_register.py").synthetic_corpus(tmp_path / "zh", venue="JX")


@pytest.fixture
def zh_draft(tmp_path):
    f = tmp_path / "draft_zh.md"
    f.write_text(ZH_DRAFT, encoding="utf-8")
    return f


@pytest.fixture
def en_corpus(tmp_path):
    root = make_corpus(tmp_path / "en", venue="venA")
    make_corpus(root, n=5, venue="venB")
    return root


@pytest.fixture
def en_draft(tmp_path):
    f = tmp_path / "draft_en.md"
    f.write_text(english_text(999, 1000), encoding="utf-8")
    return f


# ---- zh_register -------------------------------------------------------------------------

def test_zh_register_selftest():
    r = run_tool("zh-tw/zh_register.py", "--selftest")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "FAIL" not in r.stdout


def test_zh_register_profile_flags_high_feature(zh_corpus, zh_draft):
    r = run_tool("zh-tw/zh_register.py", zh_draft, "--corpus", zh_corpus, "--venue", "JX", "--json")
    assert r.returncode == 0, r.stdout + r.stderr
    p = json.loads(r.stdout)
    assert p["n_docs"] == 30 and p["venue"] == "JX"
    assert p["feats"]["本文"]["status"] == "high"


def test_zh_register_small_venue_falls_back(zh_corpus, zh_draft):
    load_tool("zh-tw/zh_register.py").synthetic_corpus(zh_corpus, n=4, venue="JY")
    r = run_tool("zh-tw/zh_register.py", zh_draft, "--corpus", zh_corpus, "--venue", "JY", "--json")
    assert r.returncode == 0, r.stdout + r.stderr
    p = json.loads(r.stdout)
    assert p["n_docs"] == 34 and "fewer than" in p["venue"]


# ---- register_profile --------------------------------------------------------------------

def test_register_profile_selftest(tmp_path):
    r = run_tool("register/register_profile.py", "--selftest", home=tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "FAIL" not in r.stdout


def test_register_profile_zh_deviation_list(zh_corpus, zh_draft, tmp_path):
    out = tmp_path / "deviations.md"
    r = run_tool("register/register_profile.py", zh_draft, "--lang", "zh", "--corpus", zh_corpus,
                 "--venue", "JX", "--out", out)
    assert r.returncode == 0, r.stdout + r.stderr
    md = out.read_text(encoding="utf-8")
    assert "To fix" in md and "本文" in md and "Inside the band" in md


def test_register_profile_en_without_biber(en_corpus, en_draft, tmp_path):
    r = run_tool("register/register_profile.py", en_draft, "--lang", "en", "--corpus", en_corpus,
                 "--venue", "venA", "--no-biber", "--json", home=tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert json.loads(r.stdout)["feats"]


def test_register_profile_refuses_binary_formats(tmp_path):
    f = tmp_path / "draft.docx"
    f.write_bytes(b"PK")
    r = run_tool("register/register_profile.py", f, "--lang", "zh", "--corpus", tmp_path)
    assert r.returncode != 0 and "Convert" in (r.stdout + r.stderr)


# ---- polish_check ------------------------------------------------------------------------

def test_polish_check_selftest(tmp_path):
    r = run_tool("register/polish_check.py", "--selftest", home=tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "FAIL" not in r.stdout


def _polish(tmp_path, draft, edits, *extra):
    e = tmp_path / "edits.py"
    e.write_text("E = [\n" + "".join(f"    ({a!r}, {b!r}),\n" for a, b in edits) + "]\n",
                 encoding="utf-8")
    return run_tool("register/polish_check.py", "--draft", draft, "--edits", e, "--lang", "zh",
                    *extra, env={"ZH_CORPUS_DIR": ""})


ZH_SMALL = "# 合成測試稿\n\n本文以問卷蒐集十二位教師的資料。\n\n受訪者提供回饋，共 12 位教師。\n"


def test_polish_check_pass_and_apply(tmp_path):
    d = tmp_path / "d.md"
    d.write_text(ZH_SMALL, encoding="utf-8")
    r = _polish(tmp_path, d, [("本文以問卷蒐集", "本研究以問卷蒐集")], "--grow-budget", "2", "--apply")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "overall: PASS" in r.stdout
    assert "本研究以問卷蒐集" in d.read_text(encoding="utf-8")


def test_polish_check_blocks_dash_number_and_budget(tmp_path):
    d = tmp_path / "d.md"
    d.write_text(ZH_SMALL, encoding="utf-8")
    for edits, extra in (
        ([("受訪者提供回饋", "受訪者提供回饋" + DASH * 2 + "包括建議")], ("--allow-grow",)),
        ([("共 12 位教師", "共 13 位教師")], ()),
        ([("本文以問卷蒐集", "本研究以問卷蒐集")], ()),   # +1 character with a budget of 0
    ):
        r = _polish(tmp_path, d, edits, *extra, "--apply")
        assert r.returncode == 1 and "overall: FAIL" in r.stdout, r.stdout
        assert d.read_text(encoding="utf-8") == ZH_SMALL


def test_polish_check_never_runs_the_edits_file(tmp_path):
    d = tmp_path / "d.md"
    d.write_text(ZH_SMALL, encoding="utf-8")
    marker = tmp_path / "ran"
    e = tmp_path / "evil.py"
    e.write_text(f"E = [(open({str(marker)!r}, 'w').write('x') and 'a', 'b')]\n", encoding="utf-8")
    r = run_tool("register/polish_check.py", "--draft", d, "--edits", e, "--lang", "zh",
                 env={"ZH_CORPUS_DIR": ""})
    assert r.returncode != 0 and "literal" in r.stderr
    assert not marker.exists()


# ---- English corpus tools: --groups / --json ----------------------------------------------

def test_metadiscourse_groups_and_json(en_corpus, en_draft, tmp_path):
    r = run_tool("en/metadiscourse_en.py", en_draft, "--corpus", en_corpus, "--groups", "venA",
                 "--json", home=tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    p = json.loads(r.stdout)
    assert p["n_docs"] == 30
    assert {f["status"] for f in p["feats"].values()} <= {"high", "low", "ok"}
    r = run_tool("en/metadiscourse_en.py", en_draft, "--corpus", en_corpus, "--groups", "venB",
                 "--json", home=tmp_path)
    assert r.returncode == 0, r.stdout + r.stderr
    assert json.loads(r.stdout)["n_docs"] == 35   # venB has 5 papers: falls back to the whole corpus


def test_biber_diag_offers_groups_and_json():
    r = run_tool("en/biber_diag.py", "--help")
    assert r.returncode == 0
    assert "--groups" in r.stdout and "--json" in r.stdout


# ---- voice_lint paper mode ---------------------------------------------------------------

def test_voice_lint_paper_mode(tmp_path):
    f = tmp_path / "p.md"
    f.write_text("本研究以訪談蒐集資料；研究者則是依紀錄整理。綜上所述，此一方式可行。\n", encoding="utf-8")
    r = run_tool("zh-tw/voice_lint.py", f)
    assert r.returncode == 1 and "Semicolon" in r.stdout
    r = run_tool("zh-tw/voice_lint.py", f, "--paper")
    assert r.returncode == 1 and "(paper mode)" in r.stdout
    assert "Semicolon" not in r.stdout and "此一" in r.stdout
    f.write_text("本研究以訪談蒐集資料；研究者依紀錄整理，綜上所述，方式可行。\n", encoding="utf-8")
    assert run_tool("zh-tw/voice_lint.py", f, "--paper").returncode == 0
