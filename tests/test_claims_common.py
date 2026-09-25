"""tools/claims (overclaim_lint, uncited_claims_scan) and tools/common/md_prose."""
import json

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
