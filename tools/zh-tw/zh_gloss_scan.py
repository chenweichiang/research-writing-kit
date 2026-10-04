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
    python3 zh_gloss_scan.py <draft> --en        # English glosses and bare English words

--en mode (for Chinese prose where English should appear only when necessary):
  1. English glosses after a Chinese term, e.g. 感性工學(Kansei engineering),
     grouped by normalized English. The first occurrence of each is listed for a
     human to judge (a field term at first mention may stay; a common word glossed
     in English should go). Every later occurrence is flagged "already glossed at
     first mention", and those are almost always deletable.
  2. Bare English words in the prose (no parentheses), ranked by frequency,
     lowercase-initial words first (ordinary words, usually better in Chinese)
     then capitalised ones (proper nouns, acronyms, names; usually fine).
  Skipped: code, tables, headings, citations, URLs, YAML front matter, HTML
  comments; scanning stops at a References heading. Report-only.
"""
import pathlib
import re
import sys
from collections import Counter, defaultdict

EN_GLOSS = re.compile(r"[（(]\s*([A-Za-z][A-Za-z0-9 ,.;:'&/+\-]{1,80}?)\s*[）)]")
EN_WORD = re.compile(r"(?<![A-Za-z0-9_./@#-])[A-Za-z][A-Za-z'-]{2,}(?![A-Za-z0-9_./@-])")
CJK = re.compile(r"[\u4e00-\u9fff]")


def is_citation(t):
    return bool(re.search(r"(19|20)\d{2}", t)) or bool(re.search(r"\bet al\b|\bpp?\.", t))


def scan_en(lines):
    groups = defaultdict(list)          # normalized English -> [(line no, context, text)]
    bare = Counter()
    bare_where = {}
    in_code = in_cmt = False
    in_fm = bool(lines) and lines[0].strip() == "---"   # YAML front matter and HTML comments are not prose
    for i, l in enumerate(lines, 1):
        if in_fm:
            if i > 1 and l.strip() == "---":
                in_fm = False
            continue
        if in_cmt:
            in_cmt = "-->" not in l
            continue
        if l.lstrip().startswith("<!--"):
            in_cmt = "-->" not in l
            continue
        if re.match(r"^#+\s*(參考文獻|引用文獻|References|Bibliography)", l):
            break                                       # English titles in a bibliography are not stray English
        if l.startswith("```"):
            in_code = not in_code
            continue
        if in_code or l.startswith("|") or l.startswith("#") or not CJK.search(l):
            continue
        body = re.sub(r"`[^`]*`|https?://\S+|\[[^\]]*\]\([^)]*\)|@[A-Za-z0-9_:-]+", " ", l)
        spans = []
        for m in EN_GLOSS.finditer(body):
            t = m.group(1).strip()
            before = body[max(0, m.start() - 12):m.start()]
            if is_citation(t) or not CJK.search(before[-3:] if before else ""):
                continue
            groups[re.sub(r"\s+", " ", t.lower()).strip(" ,.;")].append((i, before, t))
            spans.append((m.start(), m.end()))
        rest = "".join(ch if not any(a <= k < b for a, b in spans) else " " for k, ch in enumerate(body))
        rest = re.sub(r"[（(][^（）()]*(19|20)\d{2}[^（）()]*[）)]", " ", rest)   # citation parentheses
        # narrative citations: author names before "(2004)" ("Borsboom 等人(2004)", "A 與 B(2004)")
        rest = re.sub(r"[A-Za-z][A-Za-z' -]*(?:\s*(?:與|和|、|&|and)\s*[A-Za-z][A-Za-z' -]*)*\s*(?:等人|等)?\s*[（(]\s*(?:19|20)\d{2}", " ", rest)
        rest = re.sub(r"[A-Za-z][A-Za-z' -]*\s*等人", " ", rest)
        for w in EN_WORD.findall(rest):
            bare[w] += 1
            bare_where.setdefault(w, i)
    first = sorted(((v[0], k) for k, v in groups.items()), key=lambda x: x[0][0])
    print("== 1. English glosses: first occurrence (a human judges whether it is needed) ==")
    for (i, before, t), _ in first:
        print(f"L{i}: ...{before}({t})")
    dup = [(k, v[1:]) for k, v in groups.items() if len(v) > 1]
    n_dup = sum(len(v) for _, v in dup)
    print(f"\n== 1. Repeated glosses: already glossed at first mention, suggest deleting ({n_dup}) ==")
    for k, rest_ in sorted(dup, key=lambda x: x[1][0][0]):
        print(f"  ({k}) first at L{groups[k][0][0]}; repeated at " + ", ".join(f"L{i}" for i, _, _ in rest_))
    low = [(w, c) for w, c in bare.most_common() if w[0].islower()]
    cap = [(w, c) for w, c in bare.most_common() if not w[0].islower()]
    print("\n== 2. Bare English in prose, lowercase-initial (ordinary words; most should become Chinese) ==")
    for w, c in low[:40]:
        print(f"  {w} x{c} (first at L{bare_where[w]})")
    print("\n== 2. Capitalised (proper nouns, acronyms, names; mostly fine, skim) ==")
    print("  " + ", ".join(f"{w} x{c}" for w, c in cap[:40]))
    print(f"\n{len(groups)} glossed term(s), {n_dup} repeated gloss(es); "
          f"{len(bare)} distinct bare English word(s), {sum(bare.values())} occurrence(s). "
          "Proper nouns, model and software names, and file names may stay; "
          "translate the rest. A field term may keep its gloss at first mention.")


def main():
    args = sys.argv[1:]
    if not args or any(a in ("-h", "--help") for a in args):
        print(__doc__.strip())
        sys.exit(0 if args else 2)
    en_mode = "--en" in args
    if en_mode:
        args = [a for a in args if a != "--en"]
    n_min = 12
    if "--min" in args:
        i = args.index("--min")
        n_min = int(args[i + 1])
        del args[i:i + 2]
    text = pathlib.Path(args[0]).expanduser().read_text(encoding="utf-8", errors="ignore")
    lines = text.split("\n")
    if en_mode:
        scan_en(lines)
        return
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
