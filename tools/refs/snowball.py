#!/usr/bin/env python3
"""snowball.py — forward/backward citation snowballing (OpenAlex primary, Semantic Scholar fallback)

Fills fetch-refs' blind spot: collecting reference PDFs is *backward* (what you
cite). This script answers "who cites X" (forward — for related work and for
"you missed recent work" reviews), "what does X cite" (backward), and "what is
similar to X" (related). With multiple seeds it aggregates: the more seeds a
paper hits (`seed_hits`), the more likely it's something you should have read.

Zero-install: Python 3 standard library only. Free APIs, no keys, no signup.

Usage:
  snowball.py --doi 10.1145/1240624.1240704 --direction forward --limit 100
  snowball.py --bib references.bib --direction forward --limit 50   # per-seed limit, aggregated+deduped
  snowball.py --doi ... --direction backward|related
  Common: --out out.csv (default: print top 30) --email you@example.org
          (--email is optional but polite: it puts you in OpenAlex's faster pool)

Output columns: seed_hits (sort key) / cited_by_count / year / venue / title / doi / oa_url
Gotchas: OpenAlex 429 = daily quota wall (resets midnight UTC). forward falls
    back to Semantic Scholar automatically (fewer fields; seed_hits still works);
    backward/related need OpenAlex itself — on 429 report "quota", never "no results".
"""
import argparse, csv, json, re, sys, time, urllib.error, urllib.parse, urllib.request

OA = "https://api.openalex.org"
S2 = "https://api.semanticscholar.org/graph/v1"


def http_json(url, email):
    if email and "openalex" in url:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}mailto={urllib.parse.quote(email)}"
    ua = f"snowball.py (mailto:{email})" if email else "snowball.py (research-writing-kit)"
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def oa_get(url, email, retries=2):
    for i in range(retries + 1):
        try:
            return http_json(url, email), None
        except urllib.error.HTTPError as e:
            if e.code == 429:
                if i < retries:
                    time.sleep(3 * (i + 1)); continue
                return None, "429"
            return None, f"http {e.code}"
        except Exception as e:  # noqa: BLE001
            if i < retries:
                time.sleep(2); continue
            return None, str(e)
    return None, "unreachable"


def resolve_seed(doi, email):
    """DOI → OpenAlex work (with id/referenced_works/related_works)."""
    data, err = oa_get(f"{OA}/works/doi:{urllib.parse.quote(doi)}", email)
    if data is None:
        return None, err
    return data, None


def norm_row(w, seed_doi):
    loc = (w.get("best_oa_location") or {}) or {}
    return {
        "seed_hits": 1, "seeds": seed_doi,
        "cited_by_count": w.get("cited_by_count", 0),
        "year": w.get("publication_year", ""),
        "venue": ((w.get("primary_location") or {}).get("source") or {}).get("display_name", "") or "",
        "title": (w.get("title") or "").strip(),
        "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
        "oa_url": loc.get("pdf_url") or loc.get("landing_page_url") or "",
    }


def forward_oa(work_id, seed_doi, limit, email):
    rows, cursor, got = [], "*", 0
    wid = work_id.rsplit("/", 1)[-1]
    while got < limit and cursor:
        n = min(200, limit - got)
        data, err = oa_get(
            f"{OA}/works?filter=cites:{wid}&per-page={n}&cursor={urllib.parse.quote(cursor)}"
            f"&sort=cited_by_count:desc", email)
        if data is None:
            return rows, err
        for w in data.get("results", []):
            rows.append(norm_row(w, seed_doi))
        got += len(data.get("results", []))
        cursor = (data.get("meta") or {}).get("next_cursor")
        if not data.get("results"):
            break
    return rows, None


def forward_s2(doi, seed_doi, limit, email):
    """Fallback when OpenAlex hits 429 (S2 is keyless; fewer fields)."""
    rows, offset = [], 0
    while len(rows) < limit:
        n = min(100, limit - len(rows))
        try:
            data = http_json(
                f"{S2}/paper/DOI:{urllib.parse.quote(doi)}/citations"
                f"?fields=title,year,venue,externalIds,citationCount,openAccessPdf"
                f"&limit={n}&offset={offset}", email)
        except Exception as e:  # noqa: BLE001
            return rows, f"S2: {e}"
        batch = data.get("data", [])
        for it in batch:
            p = it.get("citingPaper", {}) or {}
            rows.append({
                "seed_hits": 1, "seeds": seed_doi,
                "cited_by_count": p.get("citationCount", 0),
                "year": p.get("year", ""), "venue": p.get("venue", "") or "",
                "title": (p.get("title") or "").strip(),
                "doi": (p.get("externalIds") or {}).get("DOI", "") or "",
                "oa_url": (p.get("openAccessPdf") or {}).get("url", "") or "",
            })
        if len(batch) < n:
            break
        offset += n
        time.sleep(1.2)  # S2 keyless rate limit
    return rows, None


def backward_or_related(seed, seed_doi, email, field):
    ids = [i.rsplit("/", 1)[-1] for i in seed.get(field) or []]
    rows = []
    for chunk in (ids[i:i + 50] for i in range(0, len(ids), 50)):
        data, err = oa_get(f"{OA}/works?filter=openalex_id:{'|'.join(chunk)}&per-page=50", email)
        if data is None:
            return rows, err
        rows.extend(norm_row(w, seed_doi) for w in data.get("results", []))
    return rows, None


def bib_dois(path):
    txt = open(path, encoding="utf-8", errors="replace").read()
    dois = re.findall(r"^\s*doi\s*=\s*[{\"]\s*([^}\"\s]+)", txt, re.I | re.M)
    return list(dict.fromkeys(d.replace("https://doi.org/", "").rstrip(",") for d in dois))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--doi"); src.add_argument("--bib")
    ap.add_argument("--direction", choices=["forward", "backward", "related"], default="forward")
    ap.add_argument("--limit", type=int, default=100, help="per-seed cap (default 100)")
    ap.add_argument("--out", help="CSV output path (omit = print top 30 to terminal)")
    ap.add_argument("--email", default="", help="your email — optional, puts you in OpenAlex's polite pool")
    a = ap.parse_args()

    seeds = [a.doi] if a.doi else bib_dois(a.bib)
    if not seeds:
        sys.exit("no doi fields found in the bib file")
    print(f"{len(seeds)} seed(s) | direction={a.direction} | per-seed cap {a.limit}", file=sys.stderr)

    agg, errors = {}, []
    for doi in seeds:
        seed, err = resolve_seed(doi, a.email)
        # 🔴 429 is a DAILY QUOTA wall, and when you hit it the very FIRST OpenAlex
        #    call — seed resolution — already returns 429. This used to `continue`
        #    past the whole seed, which meant the Semantic Scholar fallback below was
        #    **never reached even once** (measured: 0 S2 calls). forward_s2 only needs
        #    the DOI, not OpenAlex's seed id, so skip resolution and go straight to it.
        if seed is None:
            if err == "429" and a.direction == "forward":
                print(f"  OpenAlex 429 (seed resolution) → Semantic Scholar fallback ({doi})",
                      file=sys.stderr)
                rows, err = forward_s2(doi, doi, a.limit, a.email)
                if err:
                    errors.append(f"{doi}: fallback also failed ({err}) (got {len(rows)} rows)")
            else:
                # backward/related need OpenAlex itself — there is no fallback for them.
                why = "OpenAlex daily quota wall — NOT 'no results'" if err == "429" else err
                errors.append(f"{doi}: seed resolution failed ({why})")
                continue
        elif a.direction == "forward":
            rows, err = forward_oa(seed["id"], doi, a.limit, a.email)
            if err == "429":
                print(f"  OpenAlex 429 → Semantic Scholar fallback ({doi})", file=sys.stderr)
                rows, err = forward_s2(doi, doi, a.limit, a.email)
        else:
            fld = "referenced_works" if a.direction == "backward" else "related_works"
            rows, err = backward_or_related(seed, doi, a.email, fld)
            if err == "429":
                err = "OpenAlex daily quota wall — NOT 'no results' (no fallback for backward/related)"
        if err:
            errors.append(f"{doi}: {err} (got {len(rows)} rows)")
        for r in rows:
            key = r["doi"] or r["title"].lower()[:80]
            if not key or key in {d.lower() for d in seeds}:
                continue  # drop the seeds themselves
            if key in agg:
                agg[key]["seed_hits"] += 1
                agg[key]["seeds"] += ";" + r["seeds"]
            else:
                agg[key] = r

    out = sorted(agg.values(), key=lambda r: (-r["seed_hits"], -(r["cited_by_count"] or 0)))
    cols = ["seed_hits", "cited_by_count", "year", "venue", "title", "doi", "oa_url", "seeds"]
    if a.out:
        with open(a.out, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(out)
        print(f"{len(out)} rows → {a.out}", file=sys.stderr)
    for r in out[: 30 if not a.out else 10]:
        print(f"[{r['seed_hits']} seed|cited {r['cited_by_count']:>5}] {r['year']} {r['title'][:70]}  {r['doi']}")
    if errors:
        print("\n⚠️ incomplete (429 = daily quota, resets midnight UTC — rerun then; NOT 'no results'):", file=sys.stderr)
        for e in errors:
            print("  " + e, file=sys.stderr)


if __name__ == "__main__":
    main()
