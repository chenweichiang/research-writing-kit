#!/usr/bin/env python3
"""overclaim_lint.py — bilingual (English / Traditional Chinese) overclaim scan.
A fixed station in the de-AI pass, not an optional extra.

Why: AI-polished prose has two fingerprints, not one. Style tools catch the first
(convergence words, cadence, em-dash rhythm). The second is saying more than the
data supports** — "all", "never", "the only", "proves", "clearly", "significantly"
used non-statistically. Strip the convergence words and leave the overclaims, and
the draft still reads like a model wrote it. Worse, an overclaim survives review as
a *substantive* problem: a reviewer who reads "this proves" for a study with n=12
stops trusting the rest of the paper.

Position: report-only. It never edits and never blocks delivery. Every hit needs
a human decision — does the evidence carry this word?
  - It does  → keep it. Real 0/72 or 100% results ARE absolutes; do not soften data.
  - It doesn't → converge:
      all → most            never → rarely        the only → one of the few
      prove → show/suggest  clearly → (delete)    the most X → a more X
      significantly (non-statistical) → markedly, or delete
      完全 → 幾乎/多半      永遠 → 往往           唯一 → 之一
      證明了 → 顯示         一致顯示 → 多數研究顯示   最 → 較
  - Quoted source text and object-language in quotation marks are out of scope:
    skip them by hand; the scanner cannot tell whose words they are.

Two categories behave differently from the rest:
  - nobody-did-it / 沒人做過 ("to the best of our knowledge", "no prior research", "fills a gap",
    就作者所知, 尚無研究): reported even when a citation is nearby. A citation cannot carry
    "nobody has done this"; only a search trail can (databases, query strings, date).
  - official-doc-undated / 官方文件未標年 (a guideline, regulation or policy cited without a
    year): skipped when a year sits next to it. These documents are revised often, and an
    undated citation does not say which version is meant.

Where it sits in the pipeline:
  English : ai_style_diag → Harper / LanguageTool / Vale → overclaim_lint →
            de-cadencing pass (agents/de-cadencing-scholar.md, tic #6 is this list)
  Chinese : voice_lint (hard rules to zero) → overclaim_lint → zh_ai_style →
            zh_localize (+ zh_term_check if you have the Taiwan add-on)

Usage:
  python3 overclaim_lint.py <file.md|.txt|.tex|.typ|.qmd> [--lang auto|en|zh]
                            [--json report.json] [--strict] [--max N]
Exit codes: 0 always (this is a report), unless --strict, which exits 1 when
candidates remain — use that only if you deliberately want a CI gate.

Zero-install: Python 3 standard library only.
"""
import argparse
import json
import re
import sys
from pathlib import Path

# Word lists are deliberately over-inclusive: a false positive costs one glance,
# a miss ships an unsupported claim. Categories exist so you can read the report
# in passes rather than as one undifferentiated list.
EN = [
    ("absolute", r"\b(?:all (?:of )?(?:the |these |such )?(?:studies|cases|models|participants|texts|results)|in all cases|every (?:study|case|model|participant|text|reader)|always|never|none of|no one|nobody|entirely|completely|fully|wholly|totally|universally|invariably|without exception|the only|unique(?:ly)?|the first (?:to|study|time)|unprecedented|impossible|guarantees?)\b"),
    ("intensifier", r"\b(?:extremely|highly|vastly|dramatically|drastically|enormously|hugely|massively|overwhelmingly|far (?:more|less|higher|lower|greater)|substantially|significantly(?! \(p)|remarkable|striking(?:ly)?|profound(?:ly)?|revolutionary|groundbreaking|critical(?:ly)?|crucial(?:ly)?|essential(?:ly)?|fundamental(?:ly)?)\b"),
    ("evidence", r"\b(?:prove[sd]?|proof|demonstrates? conclusively|conclusively|establish(?:es|ed)|reveals?|confirms?|clearly|obviously|undoubtedly|unquestionably|it is well known|widely (?:accepted|recognised|recognized)|consensus)\b"),
    ("superlative", r"\b(?:the most (?:important|effective|direct|robust|precise|reliable|common|widely)|the best|the strongest|the largest|the cleanest|the clearest)\b"),
]
ZH = [
    ("絕對化", r"完全(?!相同|一致|不同|沒有)|全然|永遠|從未|從不|毫無|沒有任何|所有的|全部都|一律|必然|必定|勢必|無疑|毫無疑問|不可能|唯一|首次|首度|第一個|前所未有|史無前例|徹底|根本上|本質上"),
    ("程度誇大", r"極為|極其|極度|極大|高度(?=[敏感相關依賴共享一致重要])|遠遠|遠多於|遠高於|遠低於|大幅|巨大|劇烈|關鍵性|決定性|革命性|突破性|壓倒性"),
    ("證據強度", r"證明了|證實了|確立了|揭示了|一致顯示|一致認為|普遍認為|眾所周知|不言而喻|顯而易見|顯然|無可否認|毋庸置疑"),
    ("最高級", r"最(?:重要|關鍵|核心|有效|佳|好|強|大|直接|明確|乾淨|精確|標準|常見|成熟)"),
    ("無出處歸屬", r"(?<!「)(?:研究顯示|研究表明|有研究指出|許多研究(?:顯示|指出|表明)|許多學者認為|學者普遍認為|專家認為|業界普遍認為)(?!」)"),
    ("沒人做過", r"[就據](?:作者|筆者|我們|本研究)所知|尚無(?:研究|文獻|相關研究|實證)|(?:目前|迄今|至今|過去)(?:仍|尚)?(?:沒有|缺乏|未見|未有|少有)(?:研究|文獻|相關(?:研究|文獻)|實證)|國內外(?:均|皆)?(?:尚無|未見|缺乏)|填補.{0,8}(?:空白|缺口)"),
    ("官方文件未標年", r"《[^》\n]{2,40}(?:要點|辦法|準則|指引|指南|計畫|政策|白皮書|綱要|規定|條例|法|規範|方案|報告)》"),
]
EN.append(("nobody-did-it", r"\bto the best of (?:our|my|the authors?'?) knowledge\b|\bno (?:prior|previous|existing|published) (?:research|work|studies|study|literature)\b|\b(?:has|have) (?:never|not (?:yet )?)been (?:studied|examined|explored|investigated|addressed|reported)\b|\b(?:little|no) (?:research|attention|work) has (?:been|examined|addressed)\b|\bfills? (?:a|the|this|an important) (?:gap|void)\b|\bremains? (?:unexplored|understudied|largely unknown)\b"))
EN.append(("official-doc-undated", r"\b(?:UNESCO|OECD|European Commission|the EU|Ministry of [A-Z]\w+|Department of [A-Z]\w+|National [A-Z]\w+ (?:Council|Foundation|Agency))\b[^.\n]{0,60}?\b(?:guidelines?|guidance|policy|policies|framework|white paper|act|regulations?|recommendations?)\b"))
EN.append(("unattributed", r"\b(?:studies|research|experts?|scholars|many (?:researchers|scholars|studies))\s+(?:have\s+|has\s+)?(?:shown|shows?|suggests?|suggested|indicates?|agree|argue|found)\b|\bit is (?:generally|commonly|widely) (?:believed|known|agreed)\b"))
# Attribution to unnamed authorities ("studies show", 研究顯示) is only an overclaim when nothing
# is cited. A citation in the window around the hit (year + bracket, [n], et al.) = sourced, skip.
ATTRIB = {"無出處歸屬", "unattributed"}
# "To the best of our knowledge", "no prior research", 就作者所知, 尚無研究: the claim reviewers most
# often knock down with one line ("you missed X"). It only stands with a search trail behind it
# (search-log.md: databases, query strings, date), so these are reported even when a citation is near.
# Official documents (guidelines, regulations, policies) are revised every year or two; cited without
# a year, nobody can tell which version is meant. A year in the window around the hit (Western,
# ROC era, academic year) = dated, skip.
GAP = {"沒人做過", "nobody-did-it"}
UNDATED = {"官方文件未標年", "official-doc-undated"}
YEAR_RX = re.compile(r"(?:19|20)\d{2}|民國\s*\d{2,3}|\d{2,3}\s*(?:學)?年度?|\d{3}\s*年")
CITE_RX = re.compile(r"\d{4}[a-z]?\s*[）)]|\[\d+(?:\s*[,，–-]\s*\d+)*\]|et al\.|\[@")
HAN = re.compile(r"[一-鿿]")

CONVERGE_EN = ("all → most, never → rarely, prove → show/suggest, the only → one of the few, "
               "clearly → (delete), significantly (non-statistical) → markedly or delete, "
               "the most X → a more X")
CONVERGE_ZH = ("完全→幾乎/多半、永遠→往往、證明了→顯示、唯一→之一、一致顯示→多數研究顯示、最→較")


def mask(text: str) -> str:
    """Blank out non-prose regions, preserving line numbers.

    HTML comments, fenced code, YAML frontmatter, table rules, and Typst/LaTeX
    command lines are not prose you are accountable for — flagging "critical" in
    a code comment wastes the reader's attention and erodes trust in the report.
    """
    def blank(m):
        return "".join("\n" if c == "\n" else " " for c in m.group(0))

    text = re.sub(r"<!--.*?-->", blank, text, flags=re.S)
    text = re.sub(r"```.*?```", blank, text, flags=re.S)
    text = re.sub(r"\A\s*---\n.*?\n---[ \t]*(?=\n)", blank, text, flags=re.S)
    text = re.sub(r"(?m)^[ \t]*\|[\s:|-]+\|[ \t]*$", blank, text)
    text = re.sub(r"(?m)^\s*(?:#set|#show|#let|\\[a-zA-Z]+\{).*$", blank, text)
    return text


def scan(path: Path, lang: str):
    raw = mask(path.read_text("utf-8", "ignore"))
    lines = raw.split("\n")
    if lang == "auto":
        lang = "zh" if len(HAN.findall(raw)) > len(raw) * 0.15 else "en"
    rules = ZH if lang == "zh" else EN
    flags = 0 if lang == "zh" else re.I
    hits = []
    for cat, pat in rules:
        rx = re.compile(pat, flags)
        for n, line in enumerate(lines, 1):
            s = line.strip()
            # table rows, images, and indented example quotations are not your prose
            if not s or s.startswith("|") or s.startswith("![") or s.startswith("> ("):
                continue
            for m in rx.finditer(line):
                if cat in ATTRIB and CITE_RX.search(line[max(0, m.start() - 40):m.end() + 80]):
                    continue
                if cat in UNDATED and YEAR_RX.search(line[max(0, m.start() - 40):m.end() + 60]):
                    continue
                ctx = line[max(0, m.start() - 30):m.end() + 30].strip()
                hits.append({"line": n, "category": cat, "match": m.group(), "context": ctx})
    return lang, hits


def main():
    ap = argparse.ArgumentParser(description="Bilingual overclaim scan (report-only).")
    ap.add_argument("path")
    ap.add_argument("--lang", default="auto", choices=["auto", "en", "zh"])
    ap.add_argument("--json", help="also write the findings as JSON")
    ap.add_argument("--strict", action="store_true", help="exit 1 while candidates remain")
    ap.add_argument("--max", type=int, default=60, help="max lines printed per category")
    a = ap.parse_args()

    lang, hits = scan(Path(a.path), a.lang)
    print(f"overclaim_lint | {a.path} | lang={lang} | {len(hits)} candidate(s) "
          f"— report only, judge each one by hand")
    by = {}
    for h in hits:
        by.setdefault(h["category"], []).append(h)
    for cat, hs in by.items():
        print(f"\n[{cat}] {len(hs)}")
        for h in hs[:a.max]:
            print(f"  L{h['line']:<5} {h['match']:<18} …{h['context']}…")
        if len(hs) > a.max:
            print(f"  … {len(hs) - a.max} more (raise --max or use --json)")
    if any(h["category"] in GAP for h in hits):
        print("\nNobody-did-it claims: keep one only with a search trail (search-log.md or venue-notes.md: "
              "which databases, the query strings, the date), rewritten as a checkable statement "
              "(\"searching Scopus and Web of Science for X and Y up to October 2026 found no ...\"); "
              "without a trail, cut it or soften it to \"few studies\".")
    if any(h["category"] in UNDATED for h in hits):
        print("Undated official documents: add the year of issue or of the last amendment, and check on the "
              "official page that the version you cite is the current one.")
    print(f"\nDisposition: evidence carries it → keep (real 0/72 or 100% results are data, "
          f"do not soften them); it doesn't → converge ({CONVERGE_EN if lang == 'en' else CONVERGE_ZH}). "
          f"Quoted source text and object-language in quotes: skip by hand.")
    if a.json:
        Path(a.json).write_text(
            json.dumps({"path": a.path, "lang": lang, "hits": hits}, ensure_ascii=False, indent=1),
            "utf-8")
    sys.exit(1 if (a.strict and hits) else 0)


if __name__ == "__main__":
    main()
