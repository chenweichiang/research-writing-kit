#!/usr/bin/env python3
"""Taiwan-Mandarin localization check — mainland-vs-Taiwan term list + 台/臺
consistency + a false-positive whitelist. Local-only, never uploads. Report-only.

Why not OpenCC: OpenCC's s2twp over-corrects text that is *already* Traditional
(it "fixes" 文件→檔案, 參考→引…), so the noise drowns the signal. This tool uses a
precise mainland-term table + a 台/臺 check with a whitelist, and only reports real
hits — you decide each one by hand.

The term table lives next to this file in `zh_tw_terms.tsv` (read by
`zh_tw_terms.py`). Each row can carry context rules: `skip_near` (don't report
when one of these words is within 10 characters) and `need_near` (only report
when one is), plus `allow` rows that are masked out before matching (演算法,
平均值, 交互作用, brand names that officially use 台…). Entries were checked
against Taiwan-authored journal papers: a term that 3+ Taiwanese authors use is
normal Taiwan usage and is left out. Extend the TSV for your own field.

No dependencies (Python 3 standard library only).

Usage:
    python3 zh_localize.py <file.md|.txt|.tex>     # or pipe via stdin
"""
import re
import sys
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent / "common"))
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent))
from md_prose import mask_nonprose
import zh_tw_terms
from pathlib import Path

TERMS, ALLOW = zh_tw_terms.load()


def check_terms(text: str):
    hits = []
    for i, line in enumerate(text.split("\n"), 1):
        for pos, t in zh_tw_terms.find(line, TERMS, ALLOW):
            ctx = line[max(0, pos - 8): pos + len(t.cn) + 8]
            hits.append((i, t.cn, t.tw + (f"({t.note})" if t.note else ""), ctx))
    return hits


def check_tai(text: str):
    """台→臺 consistency (formal documents prefer 臺; brand names already masked)."""
    hits = []
    for i, line in enumerate(text.split("\n"), 1):
        masked = zh_tw_terms.mask(line, ALLOW)
        for m in re.finditer("台", masked):
            ctx = line[max(0, m.start() - 6): m.start() + 7]
            hits.append((i, ctx))
    return hits


def report(text: str) -> str:
    L = ["=== 1. Mainland terms (context-sensitive, judge each) ==="]
    th = check_terms(text)
    if not th:
        L.append("  OK — no hits.")
    else:
        for i, cn, tw, ctx in th:
            L.append(f"  L{i}  「{cn}」→{tw}   …{ctx}…")

    L.append("\n=== 2. 台→臺 (formal docs prefer 臺; brand names auto-excluded) ===")
    ta = check_tai(text)
    if not ta:
        L.append("  OK — no non-brand 台.")
    else:
        for i, ctx in ta[:40]:
            L.append(f"  L{i}  台→臺   …{ctx}…")
        if len(ta) > 40:
            L.append(f"  … {len(ta)} total, first 40 shown.")
    L.append(f"\nSummary: {len(th)} mainland-term hits, {len(ta)} 台→臺. "
             f"Report-only; judge each by hand. (table: {len(TERMS)} terms + {len(ALLOW)} whitelist rows)")
    return "\n".join(L)


def main():
    if any(a in ("-h", "--help") for a in sys.argv[1:]):
        print(__doc__.strip() if __doc__ else "usage: see the header of this file")
        return
    arg = sys.argv[1] if len(sys.argv) > 1 else "-"
    text = sys.stdin.read() if arg == "-" else \
        Path(arg).expanduser().read_text(encoding="utf-8", errors="ignore")
    # 🔴 Mask HTML comments and code fences: internal notes never reach the
    #    submitted paper, so flagging terms inside them is a false alarm.
    #    MASK rather than delete — this tool reports line numbers, and deleting
    #    lines would shift every one of them.
    #    ⚠️ Deliberately does NOT mask tables and headings: readers see that text,
    #    so its terminology must still be checked.
    text = mask_nonprose(text)
    print(report(text))


if __name__ == "__main__":
    main()
