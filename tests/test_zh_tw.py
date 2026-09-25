"""tools/zh-tw: zh_localize, zh_tw_terms, voice_lint, zh_ai_style, zh_gloss_scan."""
from conftest import load_tool, run_tool

SENTENCE = "本研究的{}很重要。"


def _reported_term(mode=None):
    """A term from the shipped table that the matcher reports in a plain sentence.
    Read from the TSV at test time so this file never spells a mainland term out."""
    zt = load_tool("zh-tw/zh_tw_terms.py")
    terms, allow = zt.load()
    for t in terms:
        if mode and t.mode != mode:
            continue
        if [x.cn for _, x in zt.find(SENTENCE.format(t.cn), terms, allow)] == [t.cn]:
            return t
    raise AssertionError("no term in zh_tw_terms.tsv matches in a plain sentence")


def test_terms_table_loads():
    zt = load_tool("zh-tw/zh_tw_terms.py")
    terms, allow = zt.load()
    assert len(terms) > 50 and allow
    assert all(t.mode in ("fix", "flag") for t in terms)


def test_terms_fix_replaces_fix_mode_term():
    zt = load_tool("zh-tw/zh_tw_terms.py")
    t = _reported_term("fix")
    new, done = zt.fix(SENTENCE.format(t.cn))
    assert new == SENTENCE.format(t.tw)
    assert done == [f"{t.cn}→{t.tw}"]


def test_zh_localize_reports_term(tmp_path):
    t = _reported_term()
    f = tmp_path / "draft.md"
    f.write_text(SENTENCE.format(t.cn) + "\n", encoding="utf-8")
    r = run_tool("zh-tw/zh_localize.py", f)
    assert r.returncode == 0
    assert f"「{t.cn}」" in r.stdout
    assert "Summary: 1 mainland-term hits" in r.stdout


def test_zh_localize_clean_text_and_comment_masking(tmp_path):
    t = _reported_term()
    f = tmp_path / "draft.md"
    f.write_text(f"本研究以訪談蒐集資料。\n<!-- {t.cn} -->\n", encoding="utf-8")
    r = run_tool("zh-tw/zh_localize.py", f)
    assert "Summary: 0 mainland-term hits, 0 台→臺" in r.stdout


def test_zh_localize_reads_stdin():
    r = run_tool("zh-tw/zh_localize.py", "-", stdin="台灣的研究。\n")
    assert r.returncode == 0 and "1 台→臺" in r.stdout


def test_voice_lint_flags_em_dash(tmp_path):
    f = tmp_path / "draft.md"
    f.write_text("本研究以訪談蒐集資料" + chr(0x2014) + "並以主題分析整理結果。\n", encoding="utf-8")
    r = run_tool("zh-tw/voice_lint.py", f)
    assert r.returncode == 1
    assert "Em-dash" in r.stdout and "NOT PASSED" in r.stdout


def test_voice_lint_clean_and_custom_rules(tmp_path):
    f = tmp_path / "draft.md"
    f.write_text("本研究以訪談蒐集資料，並以主題分析整理結果。\n", encoding="utf-8")
    r = run_tool("zh-tw/voice_lint.py", f)
    assert r.returncode == 0 and "CLEAN" in r.stdout
    rules = tmp_path / "rules.json"
    rules.write_text('{"hard": [["no 訪談", "訪談"]], "soft": [], "report": [], "headings": ""}',
                     encoding="utf-8")
    r = run_tool("zh-tw/voice_lint.py", f, "--rules", rules)
    assert r.returncode == 1 and "no 訪談: 1" in r.stdout


def test_zh_ai_style_selftest():
    r = run_tool("zh-tw/zh_ai_style.py", "--selftest")
    assert r.returncode == 0 and "all passed" in r.stdout


def test_zh_ai_style_report(tmp_path, monkeypatch):
    f = tmp_path / "draft.md"
    body = "本研究以半結構訪談蒐集十二位教師的經驗，並以主題分析整理資料。" \
           "結果顯示，教師在課程設計上面臨時間與資源的限制，但也發展出各自的調適策略。"
    f.write_text("\n\n".join([body] * 6), encoding="utf-8")
    r = run_tool("zh-tw/zh_ai_style.py", f, home=tmp_path)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip()


def test_zh_gloss_scan(tmp_path):
    f = tmp_path / "draft.md"
    f.write_text("本研究採用半結構訪談（研究者依預先擬定的大綱提問，並視受訪者回應彈性追問）蒐集資料。\n"
                 "此觀點已有討論（Chen, 2024）。\n", encoding="utf-8")
    r = run_tool("zh-tw/zh_gloss_scan.py", f)
    assert r.returncode == 0
    assert "1 gloss candidate(s)" in r.stdout
    assert run_tool("zh-tw/zh_gloss_scan.py").returncode == 2
