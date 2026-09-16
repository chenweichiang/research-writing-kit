#!/usr/bin/env python3
"""method_decision_check.py — format gate for a method-decision memo (does NOT judge whether the method is right)

Why this exists: "research the field's methods before deciding" is easy to fake — a comparison
table with three studies, abstracts-only, one option, or claims the chosen method can't actually
support. This gate blocks those shortcuts; whether the *chosen* method is the right one is still
a human call (see `method/RIGOR_PROCESS.md` and `method/METHOD_DECISION.md`).

Bilingual: this script reads BOTH the English template (`templates/method-decision.template.md`)
and the Traditional-Chinese-Taiwan template (`setup/addons/zh-tw/templates/method-decision.zh-TW.md`)
— section numbers ("## 1.", "## 4b.", …) are the anchor, and every field name is checked against
an English/Chinese alias pair, so a filled-in copy of either template passes the same rules.

Usage:
    python3 method_decision_check.py <project>/method-decision.md
    python3 method_decision_check.py --selftest

Rules (mirror `templates/method-decision.template.md` / the zh-TW template):
    §1 at least one research question; every RQ tagged with a question shape; the claims table
       has at least one row and every claim's type is on the list
    §2 all six fields filled
    §3 comparison table has at least 8 studies; each row carries a DOI/permalink/URL (or a
       volume(issue), page citation — common for venues without DOIs) and a source mark;
       at most half may be "[abstract only]"; the analysis-method comparison has at least 5 rows
       that reference the comparison table by #, and the search trail is not empty
    §4 default judgment before checking literature, what changed after checking, and approaches
       dropped after checking must all be written down (2026 decision: check the literature even
       when you already think you know the answer)
    §5 at least two options, each with all nine fields filled (added after a blind test: core
       construct + alternative explanations, and an independent check beyond the author);
       "Analysis method" must point at a comparison-table row by #, or say explicitly that no
       comparable study does this
    §6 adopted / rationale / rejected-and-why all filled; every §1 claim appears in the claim
       alignment table
    §7 at least three premortem items
    §8 all seven fields filled (including whether a pre-data-collection plan is needed)
Exit codes: 0 = pass; 1 = something missing; 2 = file not found
"""
import argparse
import pathlib
import re
import sys

# ---------------------------------------------------------------------------
# Bilingual vocabulary. Every list pairs (English, 繁體中文) so a filled-in
# English or zh-TW template is checked by the exact same rules.
# ---------------------------------------------------------------------------

SHAPES = [
    ("Difference and degree", "差異與程度"),
    ("Relationship and prediction", "關係與預測"),
    ("Prevalence and distribution", "盛行與分布"),
    ("Experience and meaning", "經驗與意義"),
    ("Process and mechanism", "過程與機制"),
    ("Feasibility and design knowledge", "可行性與設計知識"),
    ("Interpretation and critique", "詮釋與批評"),
    ("Preservation and reconstruction", "保存與重建"),
]
CLAIM_TYPES = [
    ("causal", "因果"),
    ("correlational", "相關"),
    ("prevalence", "盛行率"),
    ("experiential interpretation", "經驗詮釋"),
    ("mechanistic understanding", "機制理解"),
    ("design-mediating knowledge", "中介設計知識"),
    ("feasibility", "可行性"),
    ("interpretive argument", "詮釋論證"),
]
SHAPES_MSG = "; ".join(f"{en} ({zh})" for en, zh in SHAPES)
CLAIM_TYPES_MSG = "; ".join(f"{en} ({zh})" for en, zh in CLAIM_TYPES)

# English source marks per the port spec; zh-TW keeps the original four plus the shorter
# [原文]/[摘要] some authors use instead of [本機原文]/[網路原文]/[僅摘要].
SOURCE_MARKS = ["[full text]", "[full text, web]", "[abstract only]",
                "[本機原文]", "[網路原文]", "[僅摘要]", "[原文]", "[摘要]"]
ABSTRACT_MARKS = {"[abstract only]", "[僅摘要]", "[摘要]"}

MIN_STUDIES = 8
MIN_ANALYSIS_ROWS = 5

S2_FIELDS = [
    ("participants", "Participants and access", "研究對象與取得管道"),
    ("relationship", "Researcher's relationship to participants", "研究者與對象的關係"),
    ("data_status", "Data status", "資料現況"),
    ("time_budget", "Time, personnel, and budget", "時間、人力、經費"),
    ("ethics", "Ethics review", "倫理審查"),
    ("venue", "Target venue", "目標場域"),
]
S4_FIELDS = [
    ("prior", "Default judgment before checking", "查證前的預設判斷"),
    ("post", "What changed after checking", "查證後的差異"),
    ("dropped", "Approaches considered before checking but dropped after, and why", "查證前有、查證後放棄的做法與理由"),
    ("mainstream", "Mainstream approach", "主流做法"),
    ("weaknesses", "Recurring weaknesses in comparable studies", "同類研究反覆出現的弱點"),
    ("diff", "Differences from this study's conditions", "與本題條件的差異"),
]
OPTION_FIELDS = [
    ("card", "Corresponding method card", "對應分析卡"),
    ("can_support", "Claims it can support", "能支撐的宣稱"),
    ("cannot_support", "Claims it cannot support", "不能支撐的宣稱"),
    ("analysis", "Analysis method", "分析方法"),
    ("construct", "How the core construct is measured or observed", "核心構念怎麼測或觀察"),
    ("indep", "Independent check beyond the author", "作者以外的獨立檢核"),
    ("sample", "Sample justification", "樣本正當化方式"),
    ("feasibility", "Feasibility and cost", "可行性與成本"),
    ("objections", "Likely reviewer objections", "審稿人可能質疑"),
]
S6_FIELDS = [
    ("adopted", "Adopted", "採用"),
    ("rationale", "Rationale", "理由"),
    ("rejected", "Rejected options and why", "不採用的選項與理由"),
]
S8_FIELDS = [
    ("s0", "Design diagnostics (S0)", "設計診斷 S0"),
    ("power", "Sample size or information power calculation", "樣本數或資訊力的計算"),
    ("guideline", "Reporting guideline", "報告準則"),
    ("prereg", "Preregistration", "預註冊"),
    ("ethics_timeline", "Ethics submission timeline", "倫理審查送件時程"),
    ("checkpoints", "Data collection checkpoints", "資料收集檢查點"),
    ("preplan", "Pre-data-collection plan", "資料收集前計畫"),
]

Q_SHAPES_H = ["Question shapes", "問題形狀"]
CLAIMS_H = ["Claims to make", "想提出的宣稱"]
ANALYSIS_CMP_H = ["Analysis method comparison", "分析方法比對"]
SEARCH_TRAIL_H = ["Search trail", "檢索留痕"]
CLAIM_ALIGN_H = ["Claim alignment table", "宣稱對齊表"]

# Taiwan journals often lack a DOI; "31(1), 67–90" (or with a colon / 頁) is checkable evidence.
CITATION_RE = r"10\.\d{4,}/|https?://|arXiv|\d+\s*[\(（]\d+[\)）]\s*[:：，,、]?\s*(?:pp?\.?\s*|頁\s*)?\d+"


def strip_comments(text):
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def sections(text):
    """Split on "## N." into {N: body}; language-neutral (only the digit matters)."""
    out = {}
    parts = re.split(r"^## (\d)\.\s*.*$", text, flags=re.M)
    for i in range(1, len(parts) - 1, 2):
        out[int(parts[i])] = parts[i + 1]
    return out


def field_value(body, names):
    """Value of "- name(optional parenthetical): value"; None if not found.

    `names` may be a single string or a list/tuple of aliases (e.g. an English/Chinese pair) —
    the first alias that matches wins. The value can sit on the same line, or be written as an
    indented sub-list/paragraph underneath (read until the next same-level "- " or heading) —
    a real blind-test case: "- Data status:" followed by three indented sub-items was
    misread as empty until this was added.
    """
    if isinstance(names, str):
        names = [names]
    alt = "|".join(re.escape(n) for n in sorted(names, key=len, reverse=True))
    m = re.search(r"^(\s*)-\s*(?:" + alt + r")[^:：\n]*[:：][ \t]*(.*)$", body, flags=re.M)
    if m is None:
        return None
    val = m.group(2).strip()
    if val:
        return val
    indent = len(m.group(1))
    extra = []
    for line in body[m.end():].split("\n")[1:]:
        if not line.strip():
            if extra:
                break
            continue
        lead = len(line) - len(line.lstrip())
        if line.lstrip().startswith("#") or (line.lstrip().startswith("-") and lead <= indent):
            break
        extra.append(line.strip())
    return " ".join(extra).strip()


def table_rows(body):
    """Data rows of a Markdown table (header + separator skipped), as a list of cell lists."""
    rows, seen_sep = [], False
    for line in body.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", c) for c in cells if c):
            seen_sep = True
            continue
        if seen_sep:
            rows.append(cells)
    return [r for r in rows if any(c for c in r[1:] if c)]


def _find_heading(text, alts):
    pat = re.compile(r"^### (?:" + "|".join(re.escape(a) for a in alts) + r")\s*$", re.M)
    m = pat.search(text)
    return m


def before(text, alts):
    m = _find_heading(text, alts)
    return text if m is None else text[: m.start()]


def after(text, alts):
    m = _find_heading(text, alts)
    return "" if m is None else text[m.end():]


def between(text, start_alts, end_alts):
    m = _find_heading(text, start_alts)
    if m is None:
        return ""
    body = text[m.end():]
    m2 = _find_heading(body, end_alts)
    return body if m2 is None else body[: m2.start()]


def check(text):
    text = strip_comments(text)
    sec = sections(text)
    probs = []
    for n in range(1, 9):
        if n not in sec:
            probs.append(f"Section {n} is missing (heading must read \"## {n}. ...\")")
    if probs:
        return probs

    # §1
    s1 = sec[1]
    rqs = re.findall(r"^-\s*RQ\d+[:：][ \t]*(.*)$", before(s1, Q_SHAPES_H), flags=re.M)
    if not any(r.strip() for r in rqs):
        probs.append("§1 has no research question")
    shape_part = between(s1, Q_SHAPES_H, CLAIMS_H)
    shape_vals = [v.strip() for v in re.findall(r"^-\s*RQ\d+[:：][ \t]*(.*)$", shape_part, flags=re.M)]
    if not shape_vals or any(not v for v in shape_vals):
        probs.append("§1 every RQ needs a question shape")
    for v in shape_vals:
        if v and not any(s.lower() in v.lower() for pair in SHAPES for s in pair):
            probs.append(f"§1 question shape \"{v}\" is not on the list: {SHAPES_MSG}")
    claim_part = after(s1, CLAIMS_H)
    claims = [(r[0], r[1] if len(r) > 1 else "") for r in table_rows(claim_part) if r and r[0]]
    if not claims:
        probs.append("§1 the claims table is empty")
    for c, t in claims:
        if not any(k.lower() in t.lower() for pair in CLAIM_TYPES for k in pair):
            probs.append(f"§1 claim \"{c[:20]}\" has type \"{t}\", not on the list: {CLAIM_TYPES_MSG}")

    # §2
    for _, en, zh in S2_FIELDS:
        if not field_value(sec[2], [en, zh]):
            probs.append(f"§2 missing: {en} ({zh})")

    # §3
    s3 = sec[3]
    table_part = re.split(
        r"^### (?:" + "|".join(re.escape(x) for x in ANALYSIS_CMP_H + SEARCH_TRAIL_H) + r")\s*$",
        s3, flags=re.M)[0]
    studies = table_rows(table_part)
    if len(studies) < MIN_STUDIES:
        probs.append(f"§3 comparison table has only {len(studies)} studies, need at least {MIN_STUDIES}")
    abstract_only = 0
    for r in studies:
        joined = " ".join(r)
        cite = r[1] if len(r) > 1 else ""
        if not re.search(CITATION_RE, cite):
            probs.append(f"§3 row #{r[0]} has no DOI/permalink/URL/volume-issue-page: {cite[:30]}")
        marks = [m for m in SOURCE_MARKS if m in joined]
        if not marks:
            probs.append(f"§3 row #{r[0]} has no source mark (full text / full text, web / abstract only)")
        if any(m in ABSTRACT_MARKS for m in marks):
            abstract_only += 1
        empty = [i for i, c in enumerate(r[2:10], start=2) if not c]
        if empty:
            probs.append(f"§3 row #{r[0]} has {len(empty)} empty method column(s)")
    if studies and abstract_only * 2 > len(studies):
        probs.append(f"§3 {abstract_only}/{len(studies)} rows are abstract-only — more than half")
    study_ids = {r[0].lstrip("#") for r in studies}
    ana_part = between(s3, ANALYSIS_CMP_H, SEARCH_TRAIL_H)
    ana = [r for r in table_rows(ana_part) if r and r[0]]
    if len(ana) < MIN_ANALYSIS_ROWS:
        probs.append(f"§3 analysis-method comparison has only {len(ana)} rows, need at least "
                     f"{MIN_ANALYSIS_ROWS} (check how comparable studies analyze this, whether or not "
                     "you already knew)")
    for r in ana:
        if r[0].lstrip("#") not in study_ids:
            probs.append(f"§3 analysis-method comparison row #{r[0]} does not match any comparison-table row")
        if len(r) < 3 or not r[2]:
            probs.append(f"§3 analysis-method comparison row #{r[0]} has no analysis method")
    log = after(s3, SEARCH_TRAIL_H)
    if not re.search(r"^-\s*\S", log, flags=re.M):
        probs.append("§3 the search trail is empty")

    # §4
    for _, en, zh in S4_FIELDS:
        if not field_value(sec[4], [en, zh]):
            probs.append(f"§4 missing: {en} ({zh})")

    # §5
    opts = re.split(r"^### (?:Option|選項)", sec[5], flags=re.M)[1:]
    if len(opts) < 2:
        probs.append(f"§5 only {len(opts)} candidate method(s); need at least two, including a rejected one")
    for o in opts:
        name = o.splitlines()[0].strip(" :：") or "(unnamed)"
        if not re.sub(r"^[A-Z]?[:：]?", "", name).strip():
            probs.append("§5 an option has no method name")
        for _, en, zh in OPTION_FIELDS:
            if not field_value(o, [en, zh]):
                probs.append(f"§5 option {name[:20]!r} missing: {en} ({zh})")
        am = field_value(o, ["Analysis method", "分析方法"]) or ""
        refs = set(re.findall(r"#(\d+)", am))
        if am and not (refs & study_ids) and not re.search(
                r"not in the comparison table|no comparable stud|比較表(中|裡)?沒有|沒有同類研究", am, re.I):
            probs.append(f"§5 option {name[:20]!r}'s analysis method does not cite a comparison-table row (#n)")

    # §6
    s6 = sec[6]
    for _, en, zh in S6_FIELDS:
        if not field_value(s6, [en, zh]):
            probs.append(f"§6 missing: {en} ({zh})")
    align_body = after(s6, CLAIM_ALIGN_H)
    align = table_rows(align_body) if align_body else []
    align_claims = " ".join(r[0] for r in align)
    align_ids = {m.group(1) for r in align
                 for m in [re.match(r"\s*([A-Za-z]+\d+)(?:\s+|\s*[:：.、])", r[0])] if m}
    for c, _t in claims:
        cid = re.match(r"\s*([A-Za-z]+\d+)(?:\s+|\s*[:：.、])", c)
        if cid and cid.group(1) in align_ids:
            continue  # matching by claim id (S1, C2, …) is enough; the wording may be abbreviated
        if c and c not in align_claims:
            probs.append(f"§6 claim alignment table is missing the §1 claim \"{c[:20]}\"")
    for r in align:
        if len(r) < 2 or not r[1]:
            probs.append(f"§6 claim \"{r[0][:20]}\" has no yes/no on whether the method supports it")
        elif re.search(r"(?i)\bno\b|\bcannot\b|\bpartial(?:ly)?\b|不能|否|部分", r[1]) and (len(r) < 3 or not r[2]):
            probs.append(f"§6 claim \"{r[0][:20]}\" — the method can't support it, but no downgraded wording is given")

    # §7
    items = [x for x in re.findall(r"^\s*\d+\.\s*(.*)$", sec[7], flags=re.M) if x.strip()]
    if len(items) < 3:
        probs.append(f"§7 premortem has only {len(items)} item(s), need at least three")

    # §8
    for _, en, zh in S8_FIELDS:
        if not field_value(sec[8], [en, zh]):
            probs.append(f"§8 missing: {en} ({zh})")
    return probs


def _filled_example(lang="en", n_studies=8, abstract_only=0, drop_claim=False, one_option=False,
                     n_analysis=5, prior=True, cite_ref=True, indep=True):
    if lang == "zh":
        rows = []
        for i in range(1, n_studies + 1):
            mark = "[僅摘要]" if i <= abstract_only else "[本機原文]"
            rows.append(f"| {i} | Author {i} 2020; 10.1000/x{i} | DIS | 差異與程度 | 受試者內實驗 | "
                        f"24 人 | 評分 | clmm | 效果量 | 便利樣本 | {mark} |")
        opt_b = "" if one_option else """
### 選項 B:準實驗(等候名單)
- 對應分析卡:A-2
- 能支撐的宣稱:有限的因果
- 不能支撐的宣稱:長期效果
- 分析方法:DiD,參照 #2、#5
- 核心構念怎麼測或觀察:同 A
- 作者以外的獨立檢核:不知情評分者兩位
- 樣本正當化方式:S0 設計診斷
- 可行性與成本:需兩個班
- 審稿人可能質疑:非隨機分派
"""
        prior_lines = ("- 查證前的預設判斷:問卷前後測\n- 查證後的差異:同類研究多用受試者內實驗\n"
                       "- 查證前有、查證後放棄的做法與理由:無\n") if prior else ""
        am_a = "clmm,參照 #1、#3" if cite_ref else "clmm"
        indep_txt = "第二編碼者抽 20% 獨立編碼" if indep else ""
        align2 = "" if drop_claim else "| 學生偏好 A | 部分 | 本班學生偏好 A |\n"
        ana_rows = "\n".join(f"| {i} | 7 點量表 | clmm,報 OR 與 95% CI | 表格 | 未校正多重比較 |"
                             for i in range(1, n_analysis + 1))
        return f"""# 方法決策備忘:測試
## 1. 問題與宣稱
### 研究問題
- RQ1:A 比 B 好嗎
### 問題形狀
- RQ1:差異與程度
### 想提出的宣稱
| 宣稱 | 類型 |
|---|---|
| A 提升創意 | 因果 |
| 學生偏好 A | 相關 |
## 2. 條件與限制
- 研究對象與取得管道:自己授課班級
- 研究者與對象的關係(是否為自己授課的學生):是,評分者
- 資料現況:要新收
- 時間、人力、經費:一學期
- 倫理審查:需要
- 目標場域與它對方法的期待:DIS,標準量表
## 3. 同類研究方法比較表
| # | 文獻 | 場域 | 問題形狀 | 設計 | 樣本 | 資料 | 分析 | 品質判準 | 被批評處 | 來源標記 |
|---|---|---|---|---|---|---|---|---|---|---|
{chr(10).join(rows)}
### 分析方法比對
| # | 資料型態 | 分析方法 | 報告方式 | 批評 |
|---|---|---|---|---|
{ana_rows}
### 檢索留痕
- lit-map:creativity support evaluation,12 筆
## 4. 比較表的觀察
{prior_lines}- 主流做法:受試者內實驗
- 少數做法與它們的理由:田野
- 同類研究反覆出現的弱點:便利樣本
- 與本題條件的差異:無法隨機
## 5. 候選方法
### 選項 A:受試者內實驗
- 對應分析卡:A-1
- 能支撐的宣稱:短期差異
- 不能支撐的宣稱:學習遷移
- 分析方法:{am_a}
- 核心構念怎麼測或觀察:CSI 量表;替代解釋=新奇效應
- 作者以外的獨立檢核:{indep_txt}
- 樣本正當化方式:功效分析
- 可行性與成本:一週
- 審稿人可能質疑:順序效應
{opt_b}
## 6. 決策
- 採用:A
- 理由:對回比較表主流
- 不採用的選項與理由:B 需兩個班
### 宣稱對齊表
| 宣稱 | 採用的方法能否支撐 | 撐不起時改寫成 |
|---|---|---|
| A 提升創意 | 能 | |
{align2}
## 7. 事前驗屍
1. 順序效應
2. 樣本太小
3. 教師兼研究者
## 8. 後續動作
- 設計診斷 S0(跑／不跑,理由):跑
- 樣本數或資訊力的計算:simr
- 報告準則:CONSORT
- 預註冊:OSF
- 倫理審查送件時程:10 月
- 資料收集檢查點(誰、何時、怎麼確認資料真的收到且可用):每週匯出
- 資料收集前計畫(analysis-plan.md 需要／不需要,理由):需要,要收新資料
"""
    rows = []
    for i in range(1, n_studies + 1):
        mark = "[abstract only]" if i <= abstract_only else "[full text]"
        rows.append(f"| {i} | Author {i} 2020; 10.1000/x{i} | DIS | Difference and degree | "
                    f"Within-subjects experiment | n=24 | Ratings | clmm | Effect size | "
                    f"Convenience sample | {mark} |")
    opt_b = "" if one_option else """
### Option B: Quasi-experiment (waitlist)
- Corresponding method card: A-2
- Claims it can support: limited causal claim
- Claims it cannot support: long-term effects
- Analysis method: DiD, cf. #2, #5
- How the core construct is measured or observed: same as A
- Independent check beyond the author: two blinded raters
- Sample justification: S0 design diagnosis
- Feasibility and cost: needs two classes
- Likely reviewer objections: non-random assignment
"""
    prior_lines = ("- Default judgment before checking: pre/post questionnaire\n"
                   "- What changed after checking: comparable studies mostly use within-subjects experiments\n"
                   "- Approaches considered before checking but dropped after, and why: none\n") if prior else ""
    am_a = "clmm, cf. #1, #3" if cite_ref else "clmm"
    indep_txt = "second coder independently codes 20%" if indep else ""
    align2 = "" if drop_claim else "| Students prefer A | Partially | students in this class prefer A |\n"
    ana_rows = "\n".join(f"| {i} | 7-point scale | clmm, report OR and 95% CI | table | "
                         f"uncorrected multiple comparisons |" for i in range(1, n_analysis + 1))
    return f"""# Method decision memo: Test
## 1. Questions and claims
### Research questions
- RQ1: is A better than B
### Question shapes
- RQ1: Difference and degree
### Claims to make
| Claim | Type |
|---|---|
| A improves creativity | causal |
| Students prefer A | correlational |
## 2. Conditions and constraints
- Participants and access: my own class
- Researcher's relationship to participants: yes, I am the rater
- Data status: new collection
- Time, personnel, and budget: one semester
- Ethics review: required
- Target venue: DIS, standard scales
## 3. Comparable-study method comparison table
| # | Reference | Venue | Question shape | Design | Sample | Data | Analysis | Quality criteria | Critique or self-reported limits | Source mark |
|---|---|---|---|---|---|---|---|---|---|---|
{chr(10).join(rows)}
### Analysis method comparison
| # | Data type | Analysis method | Reporting | Critique |
|---|---|---|---|---|
{ana_rows}
### Search trail
- lit-map: creativity support evaluation, 12 hits
## 4. Observations from the comparison table
{prior_lines}- Mainstream approach: within-subjects experiment
- Minority approaches and their rationale: field studies
- Recurring weaknesses in comparable studies: convenience samples
- Differences from this study's conditions: cannot randomize
## 5. Candidate methods
### Option A: Within-subjects experiment
- Corresponding method card: A-1
- Claims it can support: short-term difference
- Claims it cannot support: transfer of learning
- Analysis method: {am_a}
- How the core construct is measured or observed: CSI scale; alternative explanation = novelty effect
- Independent check beyond the author: {indep_txt}
- Sample justification: power analysis
- Feasibility and cost: one week
- Likely reviewer objections: order effects
{opt_b}
## 6. Decision
- Adopted: A
- Rationale: matches the mainstream approach in the comparison table
- Rejected options and why: B needs two classes
### Claim alignment table
| Claim | Can the adopted method support it | Rewritten if it cannot |
|---|---|---|
| A improves creativity | Yes | |
{align2}
## 7. Premortem
1. Order effects
2. Sample too small
3. Teacher-as-researcher conflict
## 8. Next steps
- Design diagnostics (S0) (run/skip, why): run
- Sample size or information power calculation: simr
- Reporting guideline: CONSORT
- Preregistration: OSF
- Ethics submission timeline: October
- Data collection checkpoints (who, when, how you confirm data actually arrived and is usable): weekly export
- Pre-data-collection plan (analysis-plan.md needed/not needed, why): needed, collecting new data
"""


def _kit_root():
    return pathlib.Path(__file__).resolve().parent.parent.parent


def selftest():
    root = _kit_root()
    en_tpl = root / "templates" / "method-decision.template.md"
    zh_tpl = root / "setup" / "addons" / "zh-tw" / "templates" / "method-decision.zh-TW.md"
    bad = 0

    def run(label, text, want):
        nonlocal bad
        probs = check(text)
        got = not probs
        ok = got == want
        bad += not ok
        print(f"{'✅' if ok else '❌'} {label}  expected {'pass' if want else 'block'}, "
              f"got {'pass' if got else 'block'}" + ("" if ok or not probs else f"  ({probs[0]})"))

    run("[en] blank template is blocked", en_tpl.read_text(encoding="utf-8"), False)
    run("[zh-TW] blank template is blocked", zh_tpl.read_text(encoding="utf-8"), False)

    cases = [
        ("filled memo passes", {}, True),
        ("only 7 studies is blocked", {"n_studies": 7}, False),
        ("over half abstract-only is blocked", {"n_studies": 8, "abstract_only": 5}, False),
        ("exactly half abstract-only passes", {"n_studies": 8, "abstract_only": 4}, True),
        ("claim missing from the alignment table is blocked", {"drop_claim": True}, False),
        ("a single option is blocked", {"one_option": True}, False),
        ("only 4 analysis-comparison rows is blocked", {"n_analysis": 4}, False),
        ("missing the prior default judgment is blocked", {"prior": False}, False),
        ("option's analysis method missing a table reference is blocked", {"cite_ref": False}, False),
        ("option missing the independent check is blocked", {"indep": False}, False),
    ]
    for label, kw, want in cases:
        for lang in ("en", "zh"):
            run(f"[{lang}] {label}", _filled_example(lang, **kw), want)

    run("[zh] field value wrapped onto sub-bullets still passes",
        _filled_example("zh").replace("- 資料現況:要新收", "- 資料現況:\n  - 要新收\n  - 無既有資料"), True)
    run("[en] field value wrapped onto sub-bullets still passes",
        _filled_example("en").replace("- Data status: new collection",
                                       "- Data status:\n  - new collection\n  - no existing data"), True)

    run("[zh] claim referenced by id in the alignment table passes",
        _filled_example("zh").replace("| A 提升創意 | 因果 |", "| S1:A 提升創意 | 因果 |")
                              .replace("| A 提升創意 | 能 | |", "| S1:A 讓作品較有創意 | 能 | |"), True)
    run("[zh] claim id followed by a space is also recognised",
        _filled_example("zh").replace("| A 提升創意 | 因果 |", "| C1 A 提升創意 | 因果 |")
                              .replace("| A 提升創意 | 能 | |", "| C1 A 讓作品較有創意 | 能 | |"), True)
    run("[zh] mismatched claim id is blocked",
        _filled_example("zh").replace("| A 提升創意 | 因果 |", "| S1:A 提升創意 | 因果 |")
                              .replace("| A 提升創意 | 能 | |", "| S9:其他 | 能 | |"), False)
    run("[en] claim referenced by id in the alignment table passes",
        _filled_example("en").replace("| A improves creativity | causal |", "| S1: A improves creativity | causal |")
                              .replace("| A improves creativity | Yes | |",
                                       "| S1: A makes work more creative | Yes | |"), True)

    run("[zh] a Taiwanese journal's volume/issue/page can replace a DOI",
        _filled_example("zh").replace("Author 1 2020; 10.1000/x1", "孔垂暉 2026；設計學報 31(1), 67–90"), True)
    run("[en] a volume(issue), page citation can replace a DOI",
        _filled_example("en").replace("Author 1 2020; 10.1000/x1", "Author 1 2020; Design Journal 31(1), 67-90"), True)

    print("all cases passed" if not bad else f"{bad} case(s) failed")
    return 0 if not bad else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", nargs="?")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if not a.target:
        ap.error("give the path to method-decision.md")
    p = pathlib.Path(a.target)
    if not p.is_file():
        print(f"cannot read {p}")
        sys.exit(2)
    probs = check(p.read_text(encoding="utf-8"))
    if probs:
        print(f"method-decision memo is missing {len(probs)} item(s):")
        for x in probs:
            print(f"  - {x}")
        sys.exit(1)
    print("method-decision memo is complete (whether the method itself is the right choice is still "
          "a human call — see method/RIGOR_PROCESS.md)")


if __name__ == "__main__":
    main()
