"""tools/claims (overclaim_lint, uncited_claims_scan) and tools/common/md_prose."""
import json
import time

from conftest import load_tool, run_tool


def test_overclaim_lint_en(tmp_path):
    f = tmp_path / "draft.md"
    f.write_text("This result proves that all participants improved.\n"
                 "<!-- this comment clearly proves nothing -->\n", encoding="utf-8")
    out = tmp_path / "hits.json"
    r = run_tool("claims/overclaim_lint.py", f, "--json", out)
    assert r.returncode == 0, "report-only by default"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["lang"] == "en"
    assert {h["line"] for h in data["hits"]} == {1}
    assert run_tool("claims/overclaim_lint.py", f, "--strict").returncode == 1


def test_overclaim_lint_zh_and_clean(tmp_path):
    f = tmp_path / "draft.md"
    f.write_text("這個結果證明了教學介入完全有效。\n", encoding="utf-8")
    r = run_tool("claims/overclaim_lint.py", f)
    assert "lang=zh" in r.stdout and "0 candidate" not in r.stdout
    f.write_text("The scores rose in the second session.\n", encoding="utf-8")
    r = run_tool("claims/overclaim_lint.py", f, "--strict")
    assert r.returncode == 0 and "0 candidate(s)" in r.stdout


def test_uncited_claims_scan(tmp_path):
    f = tmp_path / "paper.md"
    f.write_text("# Results\n\nScores improved by 23% after the workshop.\n\n"
                 "Prior work reported similar gains (Chen, 2024).\n", encoding="utf-8")
    out = tmp_path / "r.json"
    r = run_tool("claims/uncited_claims_scan.py", "--src", f, "--json", out)
    assert r.returncode == 1
    res = json.loads(out.read_text(encoding="utf-8"))
    assert len(res["findings"]) == 1 and "23%" in res["findings"][0]["text"]
    assert res["findings"][0]["line"] == 3 and "quant" in res["findings"][0]["categories"]


def test_uncited_claims_scan_waiver(tmp_path):
    f = tmp_path / "paper.md"
    f.write_text("Scores improved by 23% after the workshop. <!--uncited-ok: own data run3.csv-->\n",
                 encoding="utf-8")
    r = run_tool("claims/uncited_claims_scan.py", "--src", f)
    assert r.returncode == 0, r.stdout


def test_md_prose_strip_and_mask():
    mp = load_tool("common/md_prose.py")
    src = "---\ntitle: x\n---\n# Head\n\nReal sentence here.<!-- note; note -->\n```\ncode;\n```\n"
    stripped = mp.strip_markup(src)
    assert "Real sentence here." in stripped
    assert "note" not in stripped and "code;" not in stripped and "title" not in stripped
    masked = mp.mask_nonprose(src)
    assert masked.count("\n") == src.count("\n"), "masking keeps line numbers"
    assert "note; note" not in masked and "code;" not in masked


def _cats(tmp_path, text, lang):
    f = tmp_path / "gap.md"
    f.write_text(text, encoding="utf-8")
    out = tmp_path / "gap.json"
    run_tool("claims/overclaim_lint.py", f, "--lang", lang, "--json", out)
    return [h["category"] for h in json.loads(out.read_text(encoding="utf-8"))["hits"]]


def test_overclaim_lint_nobody_did_it(tmp_path):
    for s in ["就作者所知，這是第一個把聲音原型放進課堂的研究。", "目前尚無研究探討這個問題。",
              "國內外均未見相關研究。", "本研究填補了這一領域的空白。", "迄今缺乏實證支持。"]:
        assert "沒人做過" in _cats(tmp_path, s, "zh"), s
    # reported even with a citation next to it: a citation cannot carry "nobody has done this"
    assert "沒人做過" in _cats(tmp_path, "就筆者所知（王，2020），尚無研究處理此事。", "zh")
    for s in ["To the best of our knowledge, this is the first study of its kind.",
              "No prior research has examined voice prototyping in class.",
              "This question has not yet been investigated.",
              "Our work fills an important gap in the literature.",
              "The topic remains understudied."]:
        assert "nobody-did-it" in _cats(tmp_path, s, "en"), s
    assert "沒人做過" not in _cats(tmp_path, "我們以三個資料庫查詢，結果列於附錄。", "zh")
    assert "nobody-did-it" not in _cats(
        tmp_path, "We searched three databases; results are listed in Appendix A.", "en")


def test_overclaim_lint_undated_official_document(tmp_path):
    assert "官方文件未標年" in _cats(tmp_path, "依據教育部《教學實踐研究計畫申請要點》辦理。", "zh")
    for s in ["依據教育部《教學實踐研究計畫申請要點》（2025）辦理。",
              "依據 114 年度《教學實踐研究計畫申請要點》辦理。",
              "依據民國 113 年修正之《著作權法》。"]:
        assert "官方文件未標年" not in _cats(tmp_path, s, "zh"), s
    assert "official-doc-undated" in _cats(
        tmp_path, "UNESCO guidance on generative AI in education stresses age limits.", "en")
    assert "official-doc-undated" not in _cats(
        tmp_path, "UNESCO (2023) guidance on generative AI in education stresses age limits.", "en")


def test_md_prose_multi_key_citation_is_fast():
    mp = load_tool("common/md_prose.py")
    assert mp.strip_markup("見 [@a; @b ; -@c] 一文。") == "見 [CITES] 一文。"
    t = time.monotonic()
    mp.strip_markup("[@a" + " ; @a" * 40 + " x")  # unterminated: used to backtrack exponentially
    assert time.monotonic() - t < 2
