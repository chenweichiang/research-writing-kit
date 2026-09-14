#!/usr/bin/env python3
"""Parenthetical-gloss inventory for Chinese drafts — local, no upload, report-only.

Lists every full-width parenthetical 「（…）」 of N+ characters that is neither a
citation (year + author / 等人) nor a cross-reference (見／附件／第 N 節／本節), so a
human can decide what each one is:
  - a plain-language explanation of a term  → rewrite as a defining sentence, in place
  - a specification list (values, settings)  → may stay
  - pure restatement                          → delete

Why it exists: a senior co-author's verdict on a grant proposal was "too many
parenthetical asides, not academic enough". The fix that read best was NOT a
collected glossary at the end (harder to read) but defining each term once, where
it first appears — one sentence, then the term is used bare. This tool only finds
the candidates; the decision is yours.

No dependencies (Python 3 standard library). Markdown / Typst / plain text.

Usage:
    python3 zh_gloss_scan.py <draft.md|.typ|.txt> [--min 12]
"""
import pathlib
import re
import sys


def main():
    args = sys.argv[1:]
    if not args or any(a in ("-h", "--help") for a in args):
        print(__doc__.strip())
        sys.exit(0 if args else 2)
    n_min = 12
    if "--min" in args:
        i = args.index("--min")
        n_min = int(args[i + 1])
        del args[i:i + 2]
    text = pathlib.Path(args[0]).expanduser().read_text(encoding="utf-8", errors="ignore")
    lines = text.split("\n")
    in_code = False
    hits = 0
    for i, l in enumerate(lines, 1):
        if l.startswith("```"):
            in_code = not in_code
            continue
        # skip code, tables, definition lists, headings, blank lines
        if in_code or l.startswith("|") or l.startswith(": ") or l.startswith("#") or not l.strip():
            continue
        for m in re.finditer(r"（([^（）]{%d,})）" % n_min, l):
            t = m.group(1)
            # citation: has a year, plus an author-ish token; short; no 「；」 chain
            if re.search(r"\d{4}", t) and re.search(r"[A-Za-z]|等人|與", t) and "；" not in t and len(t) < 60:
                continue
            # cross-reference / pointer
            if re.search(r"^(見|另見|詳見)|附件|第[一二三四五六七八九十\d]+節|本節", t):
                continue
            hits += 1
            s = max(0, m.start() - 16)
            print(f"L{i}: …{l[s:m.start()]}【{t}】")
    print(f"\n{hits} gloss candidate(s) of ≥{n_min} chars (citations and cross-references skipped).")
    print("Plain-language notes → a defining sentence at first mention, in place; "
          "do not collect them into a glossary.")


if __name__ == "__main__":
    main()
