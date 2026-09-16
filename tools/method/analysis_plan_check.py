#!/usr/bin/env python3
"""analysis_plan_check.py — gate for a pre-data-collection plan (analysis-plan.md)

Why this exists: of the thirteen stages in `method/RIGOR_PROCESS.md`, only "before data
collection" is a step you cannot fix after the fact — preregistration must precede the data
(Nosek et al. 2019), analytic flexibility inflates false positives (Simmons et al. 2011), and
ethics approval must precede data collection. Other stages (synthesis quality, problematization)
are guided by templates without a script gate, so they don't become box-ticking.

Bilingual: reads both the English template (`templates/analysis-plan.template.md`) and the
Traditional-Chinese-Taiwan template (`setup/addons/zh-tw/templates/analysis-plan.zh-TW.md`) —
section numbers are the anchor and every field name is checked against an English/Chinese
alias pair.

Usage:
    python3 analysis_plan_check.py <project>/analysis-plan.md
    python3 analysis_plan_check.py <project>/analysis-plan.md --phase6   # pre-delivery: deviation log too
    python3 analysis_plan_check.py --selftest

Rules (mirror `templates/analysis-plan.template.md` / the zh-TW template):
    §1 all five fields filled; start date must be YYYY-MM-DD; finalization evidence is a commit
       hash (must exist in the repo, and its date must not be after the start date) or an OSF link
    §2 at least one research question or claim
    §3 all five fields filled
    By study type: quantitative → §4 fully filled; qualitative → §4b fully filled; mixed → both;
       practice-based → §5 fully filled
    --phase6: §6 deviation log has at least one row, or explicitly says "no deviations"
Exit codes: 0 = pass; 1 = something missing; 2 = file not found
"""
import argparse
import datetime as dt
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from method_decision_check import field_value, strip_comments, table_rows  # noqa: E402

S1 = [
    ("kind", "Study type", "研究類型"),
    ("decision", "Corresponding method decision", "對應的方法決策"),
    ("ethics", "Ethics review", "倫理審查"),
    ("start", "Planned data-collection start date", "資料收集預定開始日"),
    ("evidence", "Finalization evidence", "定稿證據"),
]
S3 = [
    ("checkpoints", "Data collection checkpoints", "資料收集檢查點"),
    ("indep", "Independent check beyond the author", "作者以外的獨立檢核"),
    ("changemind", "What result would change my mind", "什麼結果會讓我改變看法"),
    ("reviewer", "Who reviewed this plan", "審過這份計畫的人"),
    ("devlog", "Where deviations are logged", "偏離紀錄放在哪裡"),
]
S4 = [
    ("primary", "Primary outcome variable and scoring", "主要結果變項與計分方式"),
    ("secondary", "Secondary outcome variables", "次要結果變項"),
    ("samplesize", "Sample size and justification", "樣本數與依據"),
    ("stop", "Data collection stopping rule", "資料收集停止規則"),
    ("exclusion", "Exclusion rules", "排除規則"),
    ("model", "Primary analysis model", "主要分析模型"),
    ("multiple", "Multiple comparisons handling", "多重比較的處理"),
    ("sensitivity", "Sensitivity or multiverse analysis", "敏感度分析或多重宇宙分析"),
    ("exploratory", "Scope of exploratory analyses", "探索性分析的範圍"),
]
S4B = [
    ("sources", "Data sources and collection instruments", "資料來源與蒐集工具"),
    ("approach", "Analytic approach", "分析取向"),
    ("samplejust", "Sample size justification", "樣本量正當化方式"),
    ("reflexivity", "Reflexivity practices", "反身性做法"),
    ("adjustments", "Anticipated scope of adjustments", "預期可能調整的範圍"),
]
S5 = [
    ("docplan", "Documentation plan", "文件化計畫"),
    ("lens", "Evaluation lens", "評估鏡頭"),
    ("audience", "Who besides the author will see the work and process", "作者以外誰會看作品與歷程"),
]


def split_sections(text):
    out = {}
    parts = re.split(r"^## (\d+b?)\.\s*.*$", text, flags=re.M)
    for i in range(1, len(parts) - 1, 2):
        out[parts[i]] = parts[i + 1]
    return out


def commit_date(repo_dir, sha):
    r = subprocess.run(["git", "-C", str(repo_dir), "show", "-s", "--format=%cs", sha],
                       capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def check(text, repo_dir=None, phase6=False):
    text = strip_comments(text)
    sec = split_sections(text)
    probs = []
    for k in ["1", "2", "3", "6"]:
        if k not in sec:
            probs.append(f"Section {k} is missing")
    if probs:
        return probs

    vals = {}
    for key, en, zh in S1:
        v = field_value(sec["1"], [en, zh])
        vals[key] = v
        if not v:
            probs.append(f"§1 missing: {en} ({zh})")
    kind = vals["kind"] or ""
    start = vals["start"] or ""
    if start and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", start):
        probs.append(f"§1 data-collection start date \"{start}\" must be written YYYY-MM-DD")
        start = ""
    ev = vals["evidence"] or ""
    if ev:
        m = re.search(r"\b[0-9a-f]{7,40}\b", ev)
        if "osf.io" in ev:
            pass
        elif m and repo_dir is not None:
            d = commit_date(repo_dir, m.group(0))
            if d is None:
                probs.append(f"§1 finalization-evidence commit {m.group(0)} was not found in the repo")
            elif start and d > start:
                probs.append(f"§1 plan finalized {d}, after the data-collection start date {start} — "
                             "finalize before collecting data")
        elif not m:
            probs.append("§1 finalization evidence must be a commit hash or an OSF link")

    if not re.search(r"^-\s*\S", sec["2"], flags=re.M):
        probs.append("§2 has no research question or claim")
    for _, en, zh in S3:
        if not field_value(sec["3"], [en, zh]):
            probs.append(f"§3 missing: {en} ({zh})")

    kl = kind.lower()
    need = []
    if "混合" in kind or "mixed" in kl:
        need = [("4", S4), ("4b", S4B)]
    elif "量化" in kind or "quantitative" in kl:
        need = [("4", S4)]
    elif "質性" in kind or "qualitative" in kl:
        need = [("4b", S4B)]
    elif "實踐" in kind or "創作" in kind or "practice" in kl or "creative" in kl:
        need = [("5", S5)]
    elif kind:
        probs.append(f"§1 study type \"{kind}\" must be one of: quantitative / qualitative / mixed / "
                     "practice-based (量化／質性／混合／實踐研究)")
    for key, fields in need:
        body = sec.get(key, "")
        for _, en, zh in fields:
            if not field_value(body, [en, zh]):
                probs.append(f"§{key} missing: {en} ({zh}) (study type = {kind})")

    if phase6:
        rows = table_rows(sec["6"])
        low6 = sec["6"].lower()
        if not rows and "無偏離" not in sec["6"] and "no deviation" not in low6:
            probs.append("§6 deviation log is empty: fill it in before delivery, or write "
                         "\"no deviations\" if there were none")
        for r in rows:
            if len(r) < 4 or not all(r[:4]):
                probs.append(f"§6 deviation entry \"{r[0][:12]}\" needs all four columns filled")
    return probs


def _example(lang="en", kind=None, start="2026-10-01", evidence="osf.io/abcd1", fill_quant=True,
             fill_qual=True, dev_rows=True, drop_change=False):
    if lang == "zh":
        kind = kind or "量化"
        q = "\n".join(f"- {zh}:已寫" for _, _en, zh in S4) if fill_quant else ""
        qq = "\n".join(f"- {zh}:已寫" for _, _en, zh in S4B) if fill_qual else ""
        p5 = "\n".join(f"- {zh}:已寫" for _, _en, zh in S5)
        change = "" if drop_change else "效果量小於 0.2 就改寫成無明顯差異"
        dev = "| 2026-10-05 | 少一場 | 颱風 | 樣本少 4 人,功效下降 |" if dev_rows else ""
        return f"""# 計畫
## 1. 基本資料
- 研究類型:{kind}
- 對應的方法決策:受試者內實驗
- 倫理審查:核可字號 X-123,2026-09-20
- 資料收集預定開始日:{start}
- 定稿證據:{evidence}
## 2. 研究問題與宣稱
- RQ1:A 比 B 好嗎
## 3. 每一種研究都要寫
- 資料收集檢查點:每場結束當場點收
- 作者以外的獨立檢核:第二編碼者抽 20%
- 什麼結果會讓我改變看法:{change}
- 審過這份計畫的人:同系教師,2026-09-25
- 偏離紀錄放在哪裡:本檔第 6 節
## 4. 量化研究
{q}
## 4b. 質性研究
{qq}
## 5. 實踐研究
{p5}
## 6. 偏離紀錄
| 日期 | 偏離了什麼 | 為什麼 | 對結論可能的影響 |
|---|---|---|---|
{dev}
"""
    kind = kind or "quantitative"
    q = "\n".join(f"- {en}: filled in" for _, en, _zh in S4) if fill_quant else ""
    qq = "\n".join(f"- {en}: filled in" for _, en, _zh in S4B) if fill_qual else ""
    p5 = "\n".join(f"- {en}: filled in" for _, en, _zh in S5)
    change = "" if drop_change else "an effect size below 0.2 would be rewritten as no clear difference"
    dev = "| 2026-10-05 | one session dropped | typhoon | 4 fewer participants, lower power |" if dev_rows else ""
    return f"""# Plan
## 1. Basic information
- Study type: {kind}
- Corresponding method decision: within-subjects experiment
- Ethics review: approval no. X-123, approved 2026-09-20
- Planned data-collection start date: {start}
- Finalization evidence: {evidence}
## 2. Research questions and claims
- RQ1: is A better than B
## 3. Every study writes this
- Data collection checkpoints: checked off at the end of each session
- Independent check beyond the author: second coder codes 20%
- What result would change my mind: {change}
- Who reviewed this plan: a colleague in the department, 2026-09-25
- Where deviations are logged: section 6 of this file
## 4. Quantitative research
{q}
## 4b. Qualitative research
{qq}
## 5. Practice-based research
{p5}
## 6. Deviation log
| Date | What deviated | Why | Possible effect on conclusions |
|---|---|---|---|
{dev}
"""


def _kit_root():
    return pathlib.Path(__file__).resolve().parent.parent.parent


def selftest():
    root = _kit_root()
    en_tpl = root / "templates" / "analysis-plan.template.md"
    zh_tpl = root / "setup" / "addons" / "zh-tw" / "templates" / "analysis-plan.zh-TW.md"
    here = pathlib.Path(__file__).resolve().parent
    head = subprocess.run(["git", "-C", str(here), "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    head_date = commit_date(here, head) if head else None
    bad = 0

    def run(label, text, want, **kw):
        nonlocal bad
        probs = check(text, **kw)
        got = not probs
        ok = got == want
        bad += not ok
        print(f"{'✅' if ok else '❌'} {label}  expected {'pass' if want else 'block'}, "
              f"got {'pass' if got else 'block'}" + ("" if ok or not probs else f"  ({probs[0]})"))

    run("[en] blank template is blocked", en_tpl.read_text(encoding="utf-8"), False)
    run("[zh-TW] blank template is blocked", zh_tpl.read_text(encoding="utf-8"), False)

    cases = [
        ("quantitative filled in passes", dict(fill_qual=False), True),
        ("quantitative missing §4 is blocked", dict(fill_quant=False), False),
        ("qualitative only needs §4b",
         dict(kind_zh="質性", kind_en="qualitative", fill_quant=False), True),
        ("mixed needs both sections",
         dict(kind_zh="混合", kind_en="mixed", fill_qual=False), False),
        ("practice-based only needs §5",
         dict(kind_zh="實踐研究", kind_en="practice-based", fill_quant=False, fill_qual=False), True),
        ("missing 'what would change my mind' is blocked", dict(drop_change=True), False),
        ("bad start-date format is blocked", dict(start="10/1"), False),
    ]
    for label, kw, want in cases:
        kind_zh = kw.pop("kind_zh", None)
        kind_en = kw.pop("kind_en", None)
        for lang, kind in (("en", kind_en), ("zh", kind_zh)):
            run(f"[{lang}] {label}", _example(lang, kind=kind, **kw), want)

    run("[en] commit not found is blocked", _example("en", evidence="deadbeefdeadbeef"), False, repo_dir=here)
    run("[zh] commit not found is blocked", _example("zh", evidence="deadbeefdeadbeef"), False, repo_dir=here)
    run("[en] no deviation log before delivery is blocked", _example("en", dev_rows=False), False, phase6=True)
    run("[en] writing 'no deviations' passes",
        _example("en", dev_rows=False).replace("|---|---|---|---|\n", "|---|---|---|---|\nno deviations\n"),
        True, phase6=True)
    run("[zh] writing 「無偏離」 passes",
        _example("zh", dev_rows=False).replace("|---|---|---|---|\n", "|---|---|---|---|\n無偏離\n"),
        True, phase6=True)

    if head and head_date:
        early = (dt.date.fromisoformat(head_date) - dt.timedelta(days=1)).isoformat()
        run("[en] commit before the start date passes", _example("en", evidence=head, start=head_date),
            True, repo_dir=here)
        run("[en] finalizing after the start date is blocked", _example("en", evidence=head, start=early),
            False, repo_dir=here)

    print("all cases passed" if not bad else f"{bad} case(s) failed")
    return 0 if not bad else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", nargs="?")
    ap.add_argument("--phase6", action="store_true", help="pre-delivery: deviation log must be filled too")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if not a.target:
        ap.error("give the path to analysis-plan.md")
    p = pathlib.Path(a.target).resolve()
    if not p.is_file():
        print(f"cannot read {p}")
        sys.exit(2)
    probs = check(p.read_text(encoding="utf-8"), repo_dir=p.parent, phase6=a.phase6)
    if probs:
        print(f"pre-data-collection plan is missing {len(probs)} item(s):")
        for x in probs:
            print(f"  - {x}")
        sys.exit(1)
    print("pre-data-collection plan is complete" + (" (including the deviation log)" if a.phase6
          else "; data collection may begin now that it is finalized"))


if __name__ == "__main__":
    main()
