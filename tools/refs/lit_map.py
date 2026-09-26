#!/usr/bin/env python3
"""lit_map.py — a literature map: who a batch of same-topic papers co-cite, as a starting point
for judging "classics" (OpenAlex, stdlib only)

Why this exists: "classic" cannot be judged from global citation count alone -- citation counts
can be inflated by citation distortion (Greenberg 2009). A better starting point is: within "this
topic's batch of literature," how many papers co-cite a given work, and how many different
journals or venues cite it. This script counts both, and lists recent high-cited work too.
The result is only a candidate list: each candidate still needs a human check for whether it is
cited by different camps, whether it has been replicated or overturned, and whether it has been
retracted.

Usage:
  lit_map.py --query "research through design" --from-year 2007 --limit 200
  lit_map.py --dois seeds.txt                      # one DOI per line = this batch of literature
  common: --top 25  --recent-years 3  --out map.md  --csv refs.csv  --save-json corpus.json
          --email you@example.org   (or set OPENALEX_MAILTO — see below)
  lit_map.py --selftest                            # offline check of the counting logic

The raw OpenAlex data saved with --save-json can be handed to R's bibliometrix for a full
science map:
  Rscript -e 'library(bibliometrix); works <- jsonlite::fromJSON("corpus.json", simplifyVector=FALSE);
              save(works, file="corpus.RData"); M <- convert2df("corpus.RData", dbsource="openalex_api", format="api")'
  GUI: Rscript -e 'bibliometrix::biblioshiny()'

Gotchas:
  - The query uses title_and_abstract.search, not full-text search -- full-text search pulls in
    cross-field mega-cited papers like PRISMA that have nothing to do with your topic (checked
    2026).
  - OpenAlex has been usage-metered (with a daily free quota) since Feb 2026; 429 = quota wall,
    resets midnight UTC — do not read it as "no results."
  - "distinct citing venues" is only a rough proxy for "cited by different camps," not a
    replacement for reading the papers.
  - --email is required (or set the OPENALEX_MAILTO environment variable) so OpenAlex can put you
    in its faster, polite request pool; this script never assumes an address for you.
"""
import argparse
import collections
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

OA = "https://api.openalex.org"
SELECT = "id,doi,title,publication_year,cited_by_count,referenced_works,primary_location"


def oa_headers(url):
    """Optional OpenAlex key: set OPENALEX_API_KEY to use your free account's daily budget
    ($1/day; $0.10/day without a key). Sent as a header, never in the URL, and only to api.openalex.org."""
    k = os.environ.get("OPENALEX_API_KEY", "").strip()
    return {"Authorization": "Bearer " + k} if k and urllib.parse.urlsplit(url).netloc == "api.openalex.org" else {}


def oa_search_text(s):
    """Blank out the characters OpenAlex search reads as syntax (checked 2026-09): `,` separates
    filters (HTTP 400, even sent as %2C), `?` and `*` are wildcards (400 on a stemmed field),
    `!` is NOT and `|` is OR (no error, but the query silently means something else)."""
    return " ".join(re.sub(r"[,?*!|]", " ", s or "").split())


def get(url, email, retries=2):
    sep = "&" if "?" in url else "?"
    full = f"{url}{sep}mailto={urllib.parse.quote(email)}"
    req = urllib.request.Request(full, headers={"User-Agent": f"lit_map.py (mailto:{email})", **oa_headers(full)})
    for i in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                sys.exit("OpenAlex 429: today's quota is used up (resets midnight UTC) — not \"no results\"")
            if i == retries:
                raise
        except urllib.error.URLError:
            if i == retries:
                raise
        time.sleep(2 * (i + 1))
    raise RuntimeError(f"OpenAlex query failed: {url}")


def venue(w):
    loc = w.get("primary_location") or {}
    src = loc.get("source") or {}
    return src.get("display_name") or ""


def fetch_query(query, from_year, to_year, limit, email):
    flt = [f"title_and_abstract.search:{oa_search_text(query)}"]
    if from_year:
        flt.append(f"from_publication_date:{from_year}-01-01")
    if to_year:
        flt.append(f"to_publication_date:{to_year}-12-31")
    works, cursor = [], "*"
    while len(works) < limit and cursor:
        url = (f"{OA}/works?filter={urllib.parse.quote(','.join(flt), safe=':,')}"
               f"&select={SELECT}&per-page={min(200, limit)}&cursor={urllib.parse.quote(cursor)}")
        d = get(url, email)
        works += d.get("results", [])
        cursor = (d.get("meta") or {}).get("next_cursor")
        if not d.get("results"):
            break
    return works[:limit]


def fetch_dois(dois, email):
    works = []
    for i in range(0, len(dois), 50):
        chunk = "|".join(f"https://doi.org/{d}" for d in dois[i:i + 50])
        d = get(f"{OA}/works?filter=doi:{urllib.parse.quote(chunk, safe=':/|')}&select={SELECT}&per-page=50", email)
        works += d.get("results", [])
    return works


def resolve(ids, email):
    out = {}
    ids = list(ids)
    for i in range(0, len(ids), 50):
        chunk = "|".join(x.rsplit("/", 1)[-1] for x in ids[i:i + 50])
        d = get(f"{OA}/works?filter=openalex:{chunk}&select={SELECT}&per-page=50", email)
        for w in d.get("results", []):
            out[w["id"]] = w
    for x in ids:   # merged/renumbered works aren't found in a batch filter — retry one by one
        if x not in out:  # (OpenAlex auto-redirects /works/{id} to the new id)
            try:
                out[x] = get(f"{OA}/works/{x.rsplit('/', 1)[-1]}?select={SELECT}", email)
            except Exception:
                pass
    return out


def analyse(works, top):
    """Return (co-citation ranking, set of citing venues per work). Pure counting, no network —
    this is what --selftest checks."""
    counts = collections.Counter()
    venues = collections.defaultdict(set)
    for w in works:
        v = venue(w) or "(unknown venue)"
        for r in set(w.get("referenced_works") or []):
            counts[r] += 1
            venues[r].add(v)
    return counts.most_common(top), venues


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--query")
    g.add_argument("--dois", help="a file with one DOI per line")
    ap.add_argument("--from-year", type=int)
    ap.add_argument("--to-year", type=int)
    ap.add_argument("--limit", type=int, default=200)
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--recent-years", type=int, default=3)
    ap.add_argument("--out")
    ap.add_argument("--csv")
    ap.add_argument("--save-json")
    ap.add_argument("--email", default=os.environ.get("OPENALEX_MAILTO", ""),
                    help="your email for OpenAlex's polite pool (required; or set OPENALEX_MAILTO)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        fake = [
            {"id": "W1", "primary_location": {"source": {"display_name": "CHI"}}, "referenced_works": ["R1", "R2"]},
            {"id": "W2", "primary_location": {"source": {"display_name": "DIS"}}, "referenced_works": ["R1", "R1", "R3"]},
            {"id": "W3", "primary_location": {"source": {"display_name": "CHI"}}, "referenced_works": ["R1", "R2"]},
            {"id": "W4", "primary_location": None, "referenced_works": None},
        ]
        rank, venues = analyse(fake, 3)
        checks = [
            ("R1 is co-cited by 3 papers (a repeat within one paper counts once)", rank[0] == ("R1", 3)),
            ("R2 ranks second with 2 papers", rank[1] == ("R2", 2)),
            ("R1 comes from 2 distinct venues", venues["R1"] == {"CHI", "DIS"}),
            ("a paper with no references doesn't crash the count", True),
        ]
        bad = 0
        for label, ok in checks:
            bad += not ok
            print(("✅ " if ok else "❌ ") + label)
        print("all passed" if not bad else f"{bad} check(s) failed")
        sys.exit(1 if bad else 0)

    if not (a.query or a.dois):
        ap.error("give --query or --dois")
    if not a.email:
        ap.error("give --email or set the OPENALEX_MAILTO environment variable "
                 "(needed for OpenAlex's polite request pool — no address is assumed for you)")
    if a.query:
        works = fetch_query(a.query, a.from_year, a.to_year, a.limit, a.email)
        scope = f"title_and_abstract.search \"{a.query}\"" + (
            f", {a.from_year}-{a.to_year or ''}" if a.from_year or a.to_year else "")
    else:
        dois = [l.strip().removeprefix("https://doi.org/") for l in open(a.dois, encoding="utf-8") if l.strip()]
        works = fetch_dois(dois, a.email)
        scope = f"{len(dois)} DOI(s) (found {len(works)})"
    if not works:
        sys.exit("this batch of literature is empty")
    if a.save_json:
        json.dump(works, open(a.save_json, "w", encoding="utf-8"), ensure_ascii=False)

    rank, venues = analyse(works, a.top)
    meta = resolve([r for r, _ in rank], a.email)
    n = len(works)
    now = time.localtime().tm_year
    recent = sorted([w for w in works if (w.get("publication_year") or 0) >= now - a.recent_years],
                    key=lambda w: -(w.get("cited_by_count") or 0))[:15]
    with_refs = sum(1 for w in works if w.get("referenced_works"))

    lines = [f"# Literature map ({time.strftime('%Y-%m-%d')})", "",
             f"- This batch: {scope}; {n} papers total, {with_refs} with reference data from OpenAlex",
             "- How to read it: \"co-cited\" = how many papers in this batch cite it; \"citing venues\" = "
             "how many distinct journals or venues cite it, only a rough proxy for \"cited by different "
             "camps.\" Every candidate classic still needs a human check for whether it's cited by "
             "different camps, whether it's been replicated or overturned, and whether it's been "
             "retracted (see `method/RIGOR_PROCESS.md`, stage 3).", "",
             "## Candidate classics: most co-cited within this batch", "",
             "| Rank | Co-cited | Share | Citing venues | Year | Global citations | Title | DOI |",
             "|---|---|---|---|---|---|---|---|"]
    rows = []
    for i, (rid, c) in enumerate(rank, 1):
        w = meta.get(rid, {})
        title = (w.get("title") or f"(title not found in OpenAlex: {rid.rsplit('/', 1)[-1]})").replace("|", "/")
        doi = (w.get("doi") or "").removeprefix("https://doi.org/")
        rows.append([i, c, f"{c / n:.0%}", len(venues[rid]), w.get("publication_year", ""),
                    w.get("cited_by_count", ""), title, doi])
        lines.append("| " + " | ".join(str(x) for x in rows[-1]) + " |")
    lines += ["", f"## Most-cited work from the last {a.recent_years} years within this batch", "",
              "| Year | Citations | Venue | Title | DOI |", "|---|---|---|---|---|"]
    for w in recent:
        lines.append(f"| {w.get('publication_year')} | {w.get('cited_by_count')} | {venue(w).replace('|', '/')} | "
                     f"{(w.get('title') or '').replace('|', '/')} | {(w.get('doi') or '').removeprefix('https://doi.org/')} |")
    lines += ["", "Log your search trail in `search-log.md`: query string, year range, date, hit count."]
    text = "\n".join(lines) + "\n"
    if a.out:
        open(a.out, "w", encoding="utf-8").write(text)
        print(f"written to {a.out}")
    else:
        print(text)
    if a.csv:
        with open(a.csv, "w", newline="", encoding="utf-8") as f:
            wr = csv.writer(f)
            wr.writerow(["rank", "co_cited", "share", "citing_venues", "year", "cited_by_count", "title", "doi"])
            wr.writerows(rows)


if __name__ == "__main__":
    main()
