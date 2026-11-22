#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""snowball.py: forward/backward citation snowballing (OpenAlex primary, Semantic Scholar fallback,
OpenCitations as an independent second source)

Fills fetch-refs' blind spot: collecting reference PDFs is *backward* (what you
cite). This script answers "who cites X" (forward — for related work and for
"you missed recent work" reviews), "what does X cite" (backward), and "what is
similar to X" (related). With multiple seeds it aggregates: the more seeds a
paper hits (`seed_hits`), the more likely it's something you should have read.

Zero-install: Python 3 standard library only. Free APIs, no signup. Optional free keys:
OPENALEX_API_KEY raises the OpenAlex daily budget from $0.10 to $1; S2_API_KEY gives you
your own Semantic Scholar rate limit instead of the shared keyless pool, which is often
full. Keys are read from the environment, sent only as a header to their own host, and
never printed or written to disk.

Usage:
  snowball.py --doi 10.1145/1240624.1240704 --direction forward --limit 100
  snowball.py --bib references.bib --direction forward --limit 50   # per-seed limit, aggregated+deduped
  snowball.py --doi ... --direction backward|related
  Common: --out out.csv (default: print top 30) --email you@example.org
          (--email is optional but polite: it puts you in OpenAlex's faster pool)

Output columns: seed_hits (sort key) / cited_by_count / year / venue / title / doi / oa_url /
    seeds / sources. `sources` says which services returned the row (openalex, s2,
    opencitations, joined with ";"). The same paper found by several sources is merged on
    its lower-cased DOI, and one seed reaching it through two sources counts once.
OpenCitations Index v2 (keyless, data CC0, 180 requests per minute per IP): forward reads
    its citations, backward its references. It is queried independently of OpenAlex and
    S2, so either side failing does not hide the other, and a failure is reported as "not
    checked", never as zero rows. It returns DOIs but no titles: rows only OpenCitations
    knows have an empty title, and records without a DOI cannot be listed (the number
    skipped is reported). There is no OpenCitations equivalent for `related`.
Semantic Scholar calls are spaced at least 1.05 s apart (the keyed introductory limit is
    1 request per second) and retried on 429/503 with exponential backoff (2, 4, 8 s, or
    the server's Retry-After, capped at 60 s). If a keyed request is rate-limited, the
    request is resent without the key and the rest of the run uses the shared pool.
Gotchas: OpenAlex 429 = daily quota wall (resets midnight UTC). forward falls
    back to Semantic Scholar automatically (fewer fields; seed_hits still works);
    backward/related need OpenAlex itself — on 429 report "quota", never "no results".
"""
import argparse
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
S2_HOST = "api.semanticscholar.org"
S2 = f"https://{S2_HOST}/graph/v1"
OC_HOST = "api.opencitations.net"
OC = f"https://{OC_HOST}/index/v2"


def oa_headers(url):
    """Optional OpenAlex key: set OPENALEX_API_KEY to use your free account's daily budget
    ($1/day; $0.10/day without a key). Sent as a header, never in the URL, and only to api.openalex.org."""
    k = os.environ.get("OPENALEX_API_KEY", "").strip()
    return {"Authorization": "Bearer " + k} if k and urllib.parse.urlsplit(url).netloc == "api.openalex.org" else {}


# ---- Semantic Scholar: optional key, pacing, backoff ----
_S2_KEY_OFF = False     # a keyed request was rate-limited in this run: use the shared pool from now on
_S2_LAST = None         # time.monotonic() of the previous S2 request
S2_MIN_GAP = 1.05       # seconds; the keyed introductory limit is 1 request per second
S2_RETRY_CODES = (429, 503)
S2_BACKOFF = (2, 4, 8)  # seconds; three retries, doubling
S2_RETRY_AFTER_CAP = 60


def s2_auth(url):
    """`x-api-key` header for api.semanticscholar.org when S2_API_KEY is set; {} otherwise."""
    if urllib.parse.urlsplit(url).netloc != S2_HOST or _S2_KEY_OFF:
        return {}
    k = os.environ.get("S2_API_KEY", "").strip()
    return {"x-api-key": k} if k else {}


def s2_throttle(url):
    """Keep S2 requests at least S2_MIN_GAP seconds apart within one run. Other hosts: no-op."""
    global _S2_LAST
    if urllib.parse.urlsplit(url).netloc != S2_HOST:
        return
    now = time.monotonic()
    if _S2_LAST is not None:
        wait = S2_MIN_GAP - (now - _S2_LAST)
        if wait > 0:
            time.sleep(wait)
            now = time.monotonic()
    _S2_LAST = now


def s2_open(req, timeout):
    """urlopen() that paces S2 and retries it on 429/503 with backoff; other hosts get one try."""
    global _S2_KEY_OFF
    url = req.full_url
    if urllib.parse.urlsplit(url).netloc != S2_HOST:
        return urllib.request.urlopen(req, timeout=timeout)
    i = 0
    while True:
        s2_throttle(url)
        try:
            return urllib.request.urlopen(req, timeout=timeout)
        except urllib.error.HTTPError as e:
            keyed = any(k.lower() == "x-api-key" for k in req.headers)
            if e.code == 429 and keyed:
                for k in [k for k in req.headers if k.lower() == "x-api-key"]:
                    del req.headers[k]
                if not _S2_KEY_OFF:
                    print("Semantic Scholar: the key was rate-limited; using the shared pool for this run",
                          file=sys.stderr)
                _S2_KEY_OFF = True
                continue
            if e.code not in S2_RETRY_CODES or i == len(S2_BACKOFF):
                raise
            wait = S2_BACKOFF[i]
            ra = e.headers.get("Retry-After") if e.headers is not None else None
            try:
                if ra is not None:
                    wait = min(float(ra), S2_RETRY_AFTER_CAP)
            except ValueError:
                pass
            time.sleep(wait)
            i += 1


def http_json(url, email):
    if email and "openalex" in url:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}mailto={urllib.parse.quote(email)}"
    if not email or urllib.parse.urlsplit(url).netloc == OC_HOST:
        ua = "snowball.py (research-writing-kit)"   # OpenCitations never gets your address
    else:
        ua = f"snowball.py (mailto:{email})"
    req = urllib.request.Request(url, headers={"User-Agent": ua, **oa_headers(url), **s2_auth(url)})
    with s2_open(req, 30) as r:
        return json.loads(r.read())


def oa_get(url, email, retries=2):
    for i in range(retries + 1):
        try:
            return http_json(url, email), None
        except urllib.error.HTTPError as e:
            if e.code == 429:
                if i < retries:
                    time.sleep(3 * (i + 1))
                    continue
                return None, "429"
            return None, f"http {e.code}"
        except Exception as e:  # noqa: BLE001
            if i < retries:
                time.sleep(2)
                continue
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
        "seed_hits": 1, "seeds": seed_doi, "sources": ["openalex"],
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
    """Fallback when OpenAlex hits 429 (fewer fields). Pacing and retries live in s2_open."""
    rows, offset = [], 0
    while len(rows) < limit:
        n = min(100, limit - len(rows))
        try:
            data = http_json(
                f"{S2}/paper/DOI:{urllib.parse.quote(doi)}/citations"
                f"?fields=title,year,venue,externalIds,citationCount,openAccessPdf"
                f"&limit={n}&offset={offset}", email)
        except Exception as e:  # noqa: BLE001
            return rows, f"S2 not checked ({e})"
        batch = data.get("data", [])
        for it in batch:
            p = it.get("citingPaper", {}) or {}
            rows.append({
                "seed_hits": 1, "seeds": seed_doi, "sources": ["s2"],
                "cited_by_count": p.get("citationCount", 0),
                "year": p.get("year", ""), "venue": p.get("venue", "") or "",
                "title": (p.get("title") or "").strip(),
                "doi": (p.get("externalIds") or {}).get("DOI", "") or "",
                "oa_url": (p.get("openAccessPdf") or {}).get("url", "") or "",
            })
        if len(batch) < n:
            break
        offset += n
    return rows, None


def oc_doi(ids):
    """OpenCitations `citing`/`cited` hold several space-separated ids (omid:, openalex:, doi:,
    in no fixed order). Return the doi: one, lower-cased, or ""."""
    for tok in (ids or "").split():
        if tok.lower().startswith("doi:"):
            return tok[4:].strip().lower()
    return ""


def oc_fetch(doi, direction, seed_doi, limit, email, retries=2):
    """OpenCitations Index v2: forward → citations (the citing side), backward → references
    (the cited side). Returns (rows, err, no_doi_count); a non-None err means "not checked"."""
    kind, field = ("citations", "citing") if direction == "forward" else ("references", "cited")
    url = f"{OC}/{kind}/doi:{urllib.parse.quote(doi, safe='/')}"
    data = None
    for i in range(retries + 1):
        try:
            data = http_json(url, email)
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 and i < retries:
                time.sleep(3 * (i + 1))
                continue
            why = "HTTP 429, limit is 180 requests per minute per IP" if e.code == 429 else f"HTTP {e.code}"
            return [], f"OpenCitations not checked ({why})", 0
        except Exception as e:  # noqa: BLE001
            if i < retries:
                time.sleep(2)
                continue
            return [], f"OpenCitations not checked ({e})", 0
    if not isinstance(data, list):
        return [], "OpenCitations not checked (response is not a JSON array)", 0
    rows, seen, no_doi = [], set(), 0
    for it in data:
        d = oc_doi((it or {}).get(field))
        if not d:
            no_doi += 1
            continue
        if d in seen:
            continue
        seen.add(d)
        rows.append({"seed_hits": 1, "seeds": seed_doi, "sources": ["opencitations"],
                     "cited_by_count": 0, "year": "", "venue": "", "title": "", "doi": d, "oa_url": ""})
    return rows[:limit], None, no_doi


def merge_row(agg, r, seed_keys):
    """Dedupe on lower-cased DOI (title prefix when there is none). A seed that reaches the
    same paper through two sources counts once in seed_hits; empty fields are filled in."""
    key = (r["doi"] or "").lower() or r["title"].lower()[:80]
    if not key or key in seed_keys:
        return  # drop the seeds themselves
    cur = agg.get(key)
    if cur is None:
        agg[key] = r
        return
    if r["seeds"] not in cur["seeds"].split(";"):
        cur["seed_hits"] += 1
        cur["seeds"] += ";" + r["seeds"]
    for f in ("doi", "title", "venue", "year", "oa_url"):
        if not cur[f] and r[f]:
            cur[f] = r[f]
    cur["cited_by_count"] = max(cur["cited_by_count"] or 0, r["cited_by_count"] or 0)
    for src in r["sources"]:
        if src not in cur["sources"]:
            cur["sources"].append(src)


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
    src.add_argument("--doi")
    src.add_argument("--bib")
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
    seed_keys = {d.lower() for d in seeds}
    for doi in seeds:
        seed, err = resolve_seed(doi, a.email)
        rows = []
        # 429 is a DAILY QUOTA wall, and when you hit it the very FIRST OpenAlex
        #    call — seed resolution — already returns 429. This used to `continue`
        #    past the whole seed, which meant the Semantic Scholar fallback below was
        #    never reached even once (measured: 0 S2 calls). forward_s2 only needs
        #    the DOI, not OpenAlex's seed id, so skip resolution and go straight to it.
        #    OpenCitations also needs only the DOI, so it still runs below.
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
            err = None  # already recorded above
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
        if a.direction in ("forward", "backward"):
            oc_rows, oc_err, no_doi = oc_fetch(doi, a.direction, doi, a.limit, a.email)
            if oc_err:
                errors.append(f"{doi}: {oc_err}")
            if no_doi:
                print(f"  OpenCitations: skipped {no_doi} record(s) without a DOI ({doi})", file=sys.stderr)
            rows = rows + oc_rows
        for r in rows:
            merge_row(agg, r, seed_keys)

    out = sorted(agg.values(), key=lambda r: (-r["seed_hits"], -(r["cited_by_count"] or 0)))
    for r in out:
        r["sources"] = ";".join(r["sources"])
    cols = ["seed_hits", "cited_by_count", "year", "venue", "title", "doi", "oa_url", "seeds", "sources"]
    if a.out:
        with open(a.out, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(out)
        print(f"{len(out)} rows → {a.out}", file=sys.stderr)
    for r in out[: 30 if not a.out else 10]:
        title = r["title"][:70] or "(DOI only)"
        print(f"[{r['seed_hits']} seed|cited {r['cited_by_count']:>5}] {r['year']} {title}  {r['doi']}  <{r['sources']}>")
    if errors:
        print("\n⚠️ incomplete (429 = daily quota, resets midnight UTC — rerun then; NOT 'no results'):", file=sys.stderr)
        for e in errors:
            print("  " + e, file=sys.stderr)


if __name__ == "__main__":
    main()
