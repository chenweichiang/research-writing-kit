#!/usr/bin/env python3
"""Fetch Coxhead's Academic Word List (AWL) from the official Victoria University of
Wellington pages and write it as a local TSV (headword, sublist, related_forms).

Why this script exists: the AWL is licensed CC BY-NC-ND 3.0. The ND (no-derivatives)
term means the kit must not redistribute a re-formatted copy. So the kit ships this
fetcher instead of the data: you download the list from the source yourself, for your
own non-commercial use, and the TSV stays on your machine (it is git-ignored).

Sources (official, Victoria University of Wellington):
  primary  https://www.wgtn.ac.nz/lals/resources/academicwordlist/publications/awlsublists.rtf
           (the "AWL Sublist Families" document; one file, headwords + family members)
  fallback https://www.wgtn.ac.nz/lals/resources/academicwordlist/sublist/sublist01 ... sublist10
           (HTML pages; note the site's own page for sublist 7 merges "confirm" into "comprise",
           so the RTF is preferred; --source html forces the pages)

Usage:
  python3 tools/vocab/fetch_awl.py                       # writes data/academic-vocab/awl_families.tsv
  python3 tools/vocab/fetch_awl.py --out /path/to/awl.tsv
  python3 tools/vocab/fetch_awl.py --check existing.tsv  # compare against an existing TSV

Cite the list as: Coxhead, A. (2000). A new academic word list. TESOL Quarterly, 34(2), 213-238.
Standard library only.
"""
import argparse
import html
import re
import sys
import time
import urllib.request
from pathlib import Path

BASE = "https://www.wgtn.ac.nz/lals/resources/academicwordlist/sublist/sublist{:02d}"
RTF_URL = "https://www.wgtn.ac.nz/lals/resources/academicwordlist/publications/awlsublists.rtf"
# The VUW site answers 410 Gone to unfamiliar User-Agents; a plain browser string works.
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0 Safari/537.36"
DEFAULT_OUT = Path(__file__).resolve().parents[2] / "data" / "academic-vocab" / "awl_families.tsv"
EXPECTED = {n: (30 if n == 10 else 60) for n in range(1, 11)}


def fetch(url, timeout=30, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", errors="replace")


def parse_sublist(page):
    """Return [(headword, [members...]), ...] from one sublist HTML page.
    Headwords are <p>word</p>; a following <ul> (if any) holds the family members.
    Some headwords (e.g. 'adjacent', 'albeit') have no <ul> at all."""
    i = page.find("<main")
    body = page[i:] if i >= 0 else page
    j = body.find("The Academic Word List")
    if j >= 0:
        body = body[j:]
    fams = []
    for kind, inner in re.findall(r"<(p|ul)>(.*?)</\1>", body, re.S):
        if kind == "p":
            head = html.unescape(re.sub(r"<[^>]+>", "", inner)).strip().lower()
            if head and re.fullmatch(r"[a-z'\- ]+", head):
                fams.append((head, []))
        elif fams:
            members = [html.unescape(re.sub(r"<[^>]+>", "", x)).strip().lower()
                       for x in re.findall(r"<li>\s*(.*?)\s*</li>", inner, re.S)]
            fams[-1] = (fams[-1][0], sorted(set(m for m in members if m)))
    return fams


def rtf_to_text(raw):
    """Minimal RTF -> text: keep \\par as newline and \\tab as tab, drop groups/control words."""
    raw = re.sub(r"\{\\\*[^{}]*\}", "", raw)                  # \*-groups (metadata)
    raw = re.sub(r"\\(par|line)\b", "\n", raw)                  # \b: do not split \\pard into \\par + d
    raw = re.sub(r"\\tab\b", "\t", raw)
    raw = raw.replace("\\_", "-").replace("\\-", "").replace("\\~", " ")  # non-breaking hyphen / optional hyphen / nbsp
    raw = re.sub(r"\\'[0-9a-f]{2}", "", raw)                       # hex escapes (none expected in words)
    raw = re.sub(r"\\[A-Za-z]+-?\d* ?", "", raw)                   # control words
    raw = raw.replace("{", "").replace("}", "")
    return raw


def parse_rtf(raw):
    """Return [(headword, sublist, [members...]), ...] from the official AWL Sublist Families RTF."""
    text = rtf_to_text(raw)
    rows, cur, sub, started = [], None, 0, False
    for line in text.splitlines():
        m = re.search(r"Sublist (\d+)\s+of\s+(?:the\s+)?Academic Word List", line)
        if m:
            sub, started = int(m.group(1)), True
            continue
        if not started:
            continue
        if line.lstrip(" ").startswith("\t"):          # member lines are tab-indented (RTF emits "\par \tab word")
            w = line.strip().lower()
            if cur is not None and re.fullmatch(r"[a-z'\-]+", w):
                cur[2].append(w)
            continue
        w = line.strip().lower()
        if re.fullmatch(r"[a-z'\-]+", w):
            cur = [w, sub, []]
            rows.append(cur)
    return [(h, n, sorted(set(m))) for h, n, m in rows]


def build_rtf(verbose=True):
    try:
        raw = fetch(RTF_URL, binary=True).decode("latin-1")
    except Exception as e:
        print(f"[WARN] RTF source unavailable ({e}); falling back to HTML pages", file=sys.stderr)
        return None
    rows = parse_rtf(raw)
    per = {n: sum(1 for r in rows if r[1] == n) for n in EXPECTED}
    bad = {n: c for n, c in per.items() if c != EXPECTED[n]}
    if verbose:
        print(f"[OK] RTF: {len(rows)} families " + ", ".join(f"s{n}={c}" for n, c in per.items()))
    if bad:
        print(f"[WARN] RTF counts differ from the published 60x9+30 layout: {bad}", file=sys.stderr)
    return sorted(rows, key=lambda r: (r[1], r[0]))


def build_html(sleep=0.5, verbose=True):
    rows = []
    for n in range(1, 11):
        url = BASE.format(n)
        try:
            page = fetch(url)
        except Exception as e:  # network / HTTP
            print(f"[FAIL] sublist {n}: {e}", file=sys.stderr)
            return None
        fams = parse_sublist(page)
        if len(fams) != EXPECTED[n]:
            print(f"[WARN] sublist {n}: parsed {len(fams)} families, expected {EXPECTED[n]} "
                  f"(page layout may have changed; check {url})", file=sys.stderr)
        if verbose:
            print(f"[OK] sublist {n}: {len(fams)} families")
        rows.extend((head, n, members) for head, members in fams)
        time.sleep(sleep)
    return sorted(rows, key=lambda r: (r[1], r[0]))


def build(source="auto", sleep=0.5, verbose=True):
    if source in ("auto", "rtf"):
        rows = build_rtf(verbose=verbose)
        if rows is not None or source == "rtf":
            return rows
    return build_html(sleep=sleep, verbose=verbose)


def write_tsv(rows, out):
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write("headword\tsublist\trelated_forms\n")
        for head, n, members in rows:
            f.write(f"{head}\t{n}\t{', '.join(members)}\n")


def read_tsv(path):
    d = {}
    with open(path, encoding="utf-8") as f:
        next(f)
        for line in f:
            head, n, forms = line.rstrip("\n").split("\t")
            d[head] = (int(n), sorted(x.strip() for x in forms.split(",") if x.strip()))
    return d


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT, help=f"output TSV (default: {DEFAULT_OUT})")
    ap.add_argument("--check", type=Path, help="compare the fetched list against this TSV instead of writing")
    ap.add_argument("--source", choices=["auto", "rtf", "html"], default="auto",
                    help="auto = official RTF document, HTML pages as fallback")
    ap.add_argument("--sleep", type=float, default=0.5, help="seconds between page requests (html source)")
    args = ap.parse_args()

    rows = build(source=args.source, sleep=args.sleep)
    if rows is None:
        print("[FAIL] fetch incomplete; nothing written", file=sys.stderr)
        return 2
    total = len(rows)
    if total != sum(EXPECTED.values()):
        print(f"[WARN] total families {total}, expected {sum(EXPECTED.values())}", file=sys.stderr)

    if args.check:
        ref = read_tsv(args.check)
        got = {h: (n, m) for h, n, m in rows}
        missing = sorted(set(ref) - set(got)); extra = sorted(set(got) - set(ref))
        diff = [h for h in ref if h in got and ref[h] != got[h]]
        print(f"families: fetched {len(got)} / reference {len(ref)}; missing {len(missing)}, extra {len(extra)}, differing {len(diff)}")
        for h in diff[:10]:
            print(f"  {h}: ref={ref[h]} got={got[h]}")
        return 0 if not (missing or extra or diff) else 1

    write_tsv(rows, args.out)
    print(f"[OK] wrote {total} families to {args.out}")
    print("AWL is CC BY-NC-ND 3.0 (Coxhead 2000, Victoria University of Wellington). "
          "Keep it local; do not redistribute this file.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
