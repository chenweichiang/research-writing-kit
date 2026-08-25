#!/usr/bin/env python3
"""retraction_scan.py — has anything I cite been retracted? (Crossref + OpenAlex, stdlib)

Retraction Watch data is served through Crossref: a retracted article carries an
`update-to` / `updated-by` relation of type retraction / withdrawal / removal.
OpenAlex exposes the same signal as a boolean `is_retracted`. This script asks both
for every DOI and flags an entry if EITHER says retracted (they lag each other).

Input: a `.bib` file (DOIs taken from `doi = {...}` fields) or a plain text file with
one DOI per line (`#` comments allowed), or DOIs on the command line.

Status per entry:
  OK           both sources answered, no retraction relation
  RETRACTED    a retraction/withdrawal notice exists (REQUIRES human review)
  NOT_FOUND    DOI unknown to both Crossref and OpenAlex (typo? check the DOI)
  API_ERROR    a query failed (network / 429 quota) — NOT a pass; rerun later
  NO_DOI       entry has no DOI — cannot be scanned at all (books, early papers)

🔴 NO_DOI is not "scanned clean". Retraction matching runs on DOI records; an
   entry without a DOI simply falls outside what this tool can check. They are
   listed separately so a complete scan does not look incomplete, and so nobody
   mistakes "no DOI" for "verified".
🔴 API_ERROR is not "scanned clean" either. The exit code says so.

Zero-install: Python 3 standard library only. Free keyless APIs.

Usage:
  retraction_scan.py --bib references.bib [--email you@example.org] [--out report.json]
  retraction_scan.py --dois dois.txt
  retraction_scan.py 10.1016/S0140-6736(97)11096-0 10.1145/3313831.3376215

Exit codes: 0 = every DOI entry scanned, none retracted
            1 = at least one RETRACTED
            2 = no retraction found, but some queries failed (scan incomplete)
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

CROSSREF = "https://api.crossref.org/works/"
OPENALEX = "https://api.openalex.org/works/doi:"
OA_DEAD = False   # set on the first OpenAlex 429: daily quota gone, skip further OA calls


# ── input ─────────────────────────────────────────────────────────────────────
def parse_bib(path):
    """Return [{key, title, doi}] from a .bib file (brace-balanced field reader)."""
    t = open(path, encoding="utf-8", errors="replace").read()
    out = []
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,]+),", t):
        if m.group(1).lower() in ("comment", "preamble", "string"):
            continue
        key, st = m.group(2).strip(), m.end()
        nx = re.search(r"\n@\w+\s*\{", t[st:])
        body = t[st:st + (nx.start() if nx else len(t) - st)]

        def field(name):
            # word boundary: a disabled `_doi = {...}` must not count as doi
            mm = re.search(r"(?<![_a-zA-Z])" + name + r"\s*=\s*[{\"]", body, re.I)
            if not mm:
                return ""
            i, depth, buf = mm.end(), 1, []
            closer = "}" if body[mm.end() - 1] == "{" else '"'
            while i < len(body) and depth > 0:
                c = body[i]
                if closer == "}":
                    depth += c == "{"
                    depth -= c == "}"
                elif c == '"':
                    depth = 0
                if depth > 0:
                    buf.append(c)
                i += 1
            return re.sub(r"\s+", " ", "".join(buf)).strip()

        doi = field("doi")
        dm = re.search(r"10\.\d{4,9}/[^\s,}\"]+", doi)
        out.append({"key": key, "title": field("title"),
                    "doi": dm.group(0).rstrip(".") if dm else ""})
    return out


def parse_doi_list(path):
    out = []
    for i, line in enumerate(open(path, encoding="utf-8", errors="replace"), 1):
        s = line.split("#", 1)[0].strip()
        if not s:
            continue
        s = re.sub(r"^(?:https?://)?(?:dx\.)?doi\.org/", "", s, flags=re.I)
        out.append({"key": f"line{i}", "title": "", "doi": s})
    return out


# ── network ───────────────────────────────────────────────────────────────────
def get_json(url, ua, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def crossref_work(doi, ua, email):
    """Return (message | None, error). None + '' means a clean 404 (DOI not in Crossref)."""
    url = CROSSREF + urllib.parse.quote(doi, safe="")
    if email:
        url += "?mailto=" + urllib.parse.quote(email)
    try:
        return get_json(url, ua)["message"], ""
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, ""
        return None, f"crossref http {e.code}"
    except Exception as e:  # noqa: BLE001 — any failure is an API_ERROR, never a pass
        return None, f"crossref {type(e).__name__}: {e}"


def crossref_retraction(msg):
    """List of (type, notice_doi) retraction-like relations in a Crossref record.

    `updated-by`: this article was updated by a notice (the usual retraction shape).
    `update-to`:  this record IS the notice pointing at the article.
    `relation`:   defensive — some members file retractions as generic relations."""
    out = []
    for fld in ("updated-by", "update-to"):
        for u in msg.get(fld) or []:
            ty = (u.get("type") or "").lower()
            if any(k in ty for k in ("retract", "withdraw", "removal")):
                out.append((u.get("type") or "?", u.get("DOI", "")))
    for rel, items in (msg.get("relation") or {}).items():
        if any(k in rel.lower() for k in ("retract", "withdraw", "removal")):
            for it in items if isinstance(items, list) else []:
                out.append((rel, it.get("id", "")))
    return out


def openalex_retracted(doi, ua, email):
    """Return (is_retracted | None, error). None + '' = not in OpenAlex or quota skipped."""
    global OA_DEAD
    if OA_DEAD:
        return None, "openalex skipped (daily quota exhausted earlier in this run)"
    url = OPENALEX + urllib.parse.quote(doi, safe="")
    if email:
        url += "?mailto=" + urllib.parse.quote(email)
    try:
        w = get_json(url, ua)
        return bool(w.get("is_retracted")), ""
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, ""
        if e.code == 429:
            OA_DEAD = True
            print("[WARN] OpenAlex 429 (daily quota exhausted, resets midnight UTC) — "
                  "OpenAlex skipped for the rest of this run", file=sys.stderr)
        return None, f"openalex http {e.code}"
    except Exception as e:  # noqa: BLE001
        return None, f"openalex {type(e).__name__}: {e}"


# ── scan ──────────────────────────────────────────────────────────────────────
def scan_entry(e, ua, email):
    row = {"key": e["key"], "doi": e["doi"], "title": e.get("title", "")[:120]}
    if not e["doi"]:
        row.update(status="NO_DOI", note="no DOI — retraction matching not applicable")
        return row
    msg, cr_err = crossref_work(e["doi"], ua, email)
    notices = crossref_retraction(msg) if msg else []
    oa, oa_err = openalex_retracted(e["doi"], ua, email)
    row.update(crossref_title=" ".join(msg.get("title") or [])[:160] if msg else "",
               crossref_notices=notices, openalex_is_retracted=oa)
    if notices or oa:
        row["status"] = "RETRACTED"
    elif cr_err or oa_err:
        # 🔴 One source failing is enough to make the verdict unreliable: a retraction
        #    known only to the source that failed would be missed. Report, don't pass.
        row.update(status="API_ERROR", error="; ".join(x for x in (cr_err, oa_err) if x))
    elif msg is None and oa is None:
        row["status"] = "NOT_FOUND"
    else:
        row["status"] = "OK"
    return row


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dois", nargs="*", help="DOIs given directly")
    ap.add_argument("--bib", help="BibTeX file; DOIs read from doi fields")
    ap.add_argument("--dois", dest="doi_file", help="text file, one DOI per line")
    ap.add_argument("--email", default="", help="contact e-mail for the polite API pools (optional)")
    ap.add_argument("--out", default="", help="write full JSON report here")
    ap.add_argument("--sleep", type=float, default=0.5, help="seconds between entries (be polite)")
    a = ap.parse_args()

    entries = []
    if a.bib:
        entries += parse_bib(a.bib)
    if a.doi_file:
        entries += parse_doi_list(a.doi_file)
    entries += [{"key": d, "title": "", "doi": re.sub(r"^(?:https?://)?(?:dx\.)?doi\.org/", "", d)}
                for d in a.dois]
    if not entries:
        ap.error("nothing to scan: give --bib, --dois, or DOIs on the command line")

    ua = "retraction_scan.py (research-writing-kit%s)" % (f"; mailto:{a.email}" if a.email else "")
    rows = []
    for i, e in enumerate(entries, 1):
        row = scan_entry(e, ua, a.email)
        rows.append(row)
        tag = {"OK": "[OK]  ", "RETRACTED": "[FAIL]", "API_ERROR": "[WARN]",
               "NOT_FOUND": "[WARN]", "NO_DOI": "[--]  "}[row["status"]]
        extra = ""
        if row["status"] == "RETRACTED":
            extra = "  Crossref=%s OpenAlex=%s" % (row["crossref_notices"] or "-", row["openalex_is_retracted"])
        elif row["status"] == "API_ERROR":
            extra = "  " + row["error"]
        print(f"{tag} [{i}/{len(entries)}] {row['status']:<9} {row['key'][:28]:<28} {row['doi']}{extra}",
              flush=True)
        if row["status"] != "NO_DOI" and i < len(entries):
            time.sleep(a.sleep)

    counts = {s: sum(1 for r in rows if r["status"] == s)
              for s in ("OK", "RETRACTED", "NOT_FOUND", "API_ERROR", "NO_DOI")}
    scanned = len(rows) - counts["NO_DOI"]
    print(f"\n=== retraction scan: {len(rows)} entries | scanned {scanned} | OK {counts['OK']} | "
          f"RETRACTED {counts['RETRACTED']} | NOT_FOUND {counts['NOT_FOUND']} | "
          f"API_ERROR {counts['API_ERROR']} ===")
    if counts["NO_DOI"]:
        print(f"[--]   {counts['NO_DOI']} entries have NO DOI: not scanned, not a pass — "
              "retraction matching needs a DOI record (books / early literature). "
              "Rerunning will not change them.")
        for r in rows:
            if r["status"] == "NO_DOI":
                print(f"       {r['key'][:28]:<28} {r['title'][:70]}")
    for r in rows:
        if r["status"] == "RETRACTED":
            print(f"[FAIL] RETRACTED {r['key']} doi:{r['doi']}\n"
                  f"       {r['crossref_title']}\n"
                  f"       Crossref notices={r['crossref_notices'] or '-'}  "
                  f"OpenAlex is_retracted={r['openalex_is_retracted']}\n"
                  f"       -> read the notice before deciding; a retraction may be for reasons "
                  f"unrelated to the claim you cite, but it must be acknowledged.")
    if counts["API_ERROR"]:
        print(f"[WARN] {counts['API_ERROR']} queries failed — the scan is INCOMPLETE. "
              "Rerun later (OpenAlex quota resets midnight UTC).")
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            json.dump({"scanned": scanned, "counts": counts, "rows": rows},
                      fh, ensure_ascii=False, indent=1)
        print("report:", a.out)
    if counts["RETRACTED"]:
        return 1
    if counts["API_ERROR"]:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
