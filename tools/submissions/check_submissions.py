#!/usr/bin/env python3
"""check_submissions.py — duplicate-submission guard + submission status overview.

Why a central ledger: simultaneous submission is a **cross-project** problem and is
therefore invisible inside any one project folder. The same manuscript under a
slightly different title, sent to a second venue, looks perfectly clean from inside
either folder. Nearly every journal and conference forbids it explicitly, and the
consequence is retraction plus a letter to your institution — this is a research
integrity line, not a scheduling preference.

Checks:
  1. one manuscript_id in more than one under-review state  -> FAIL
  2. invalid status / malformed date                        -> FAIL (a broken ledger guards nothing)
  3. project folder missing                                 -> WARN (renamed or moved; ledger drifted)
  4. under review but not confirmed for N days              -> WARN (a stale status is a false assurance)

No dependencies (Python 3 standard library only).

Usage:
  check_submissions.py [--ledger SUBMISSIONS.tsv] [--stale-days 120]
  (or set SUBMISSIONS_TSV in the environment)
Exit code 1 if anything FAILs.
"""
import argparse, os, pathlib, re, sys
from datetime import date

ACTIVE = {"submitted", "under_review", "revision"}
STATUS = ACTIVE | {"drafting", "accepted", "published", "rejected", "withdrawn", "unknown"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
COLS = ["manuscript_id", "project", "venue", "status", "submitted", "updated", "note"]


def read_ledger(p):
    p = pathlib.Path(p).expanduser()
    if not p.exists():
        sys.exit(f"FAIL no ledger at {p}\n"
                 f"     copy SUBMISSIONS.template.tsv next to your projects and start filling it in.")
    rows, header = [], None
    for ln, raw in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        cells = [c.strip() for c in raw.split("\t")]
        if header is None:
            header = cells
            missing = [c for c in COLS if c not in header]
            if missing:
                sys.exit(f"FAIL ledger missing column(s): {', '.join(missing)}")
            continue
        cells += [""] * (len(header) - len(cells))
        rows.append(dict(zip(header, cells)) | {"_line": ln})
    return rows, p.parent


def check(rows, base, stale_days):
    bad, today, by_ms = [], date.today(), {}
    for r in rows:
        st = r["status"].lower()
        if st not in STATUS:
            bad.append(("FAIL", f"line {r['_line']}: invalid status '{r['status']}'",
                        "one of " + "/".join(sorted(STATUS))))
            continue
        for col in ("submitted", "updated"):
            if r[col] and not DATE_RE.match(r[col]):
                bad.append(("FAIL", f"line {r['_line']}: bad {col} date '{r[col]}'", "use YYYY-MM-DD"))
        if st in ACTIVE:
            by_ms.setdefault(r["manuscript_id"], []).append(r)
        if r["project"]:
            proj = pathlib.Path(r["project"]).expanduser()
            if not proj.is_absolute():
                proj = base / r["project"]
            if not proj.exists():
                bad.append(("WARN", f"{r['manuscript_id']}: project folder not found",
                            f"{proj} — renamed or moved and the ledger was not updated"))
        if st in ACTIVE and r["updated"] and DATE_RE.match(r["updated"]):
            y, m, d = (int(x) for x in r["updated"].split("-"))
            age = (today - date(y, m, d)).days
            if age > stale_days:
                bad.append(("WARN", f"{r['manuscript_id']} is '{st}' but unconfirmed for {age} days",
                            f"last checked {r['updated']} — a stale status guards nothing; "
                            f"email the editor or update the row"))

    for ms, rs in by_ms.items():
        if len(rs) > 1:
            bad.append(("FAIL", f"DUPLICATE SUBMISSION RISK: {ms} is under review in {len(rs)} places",
                        " | ".join(f"{r['venue']} ({r['status']}, {r['submitted'] or 'no date'})"
                                   for r in rs)
                        + " — almost every venue forbids this; if one of them was actually "
                          "withdrawn or rejected, update the ledger now"))
    return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ledger", default=os.environ.get("SUBMISSIONS_TSV", "SUBMISSIONS.tsv"))
    ap.add_argument("--stale-days", type=int, default=120)
    a = ap.parse_args()

    rows, base = read_ledger(a.ledger)
    bad = check(rows, base, a.stale_days)
    print("=" * 70)
    print(f"  Submission ledger: {len(rows)} record(s)")
    print("=" * 70)
    active = [r for r in rows if r["status"].lower() in ACTIVE]
    if active:
        print(f"  UNDER REVIEW ({len(active)}) — before sending anything anywhere, "
              f"check it is not one of these:")
        for r in sorted(active, key=lambda x: x["submitted"]):
            print(f"    - {r['manuscript_id']:<22} {r['venue']:<34} {r['status']:<13} "
                  f"sent {r['submitted'] or '?'}")
    else:
        print("  nothing under review")
    print("-" * 70)
    for sev, title, why in bad:
        print(f"  [{sev}] {title}\n         {why}")
    if not bad:
        print("  OK - no duplicate-submission risk; ledger format and paths are sound")
    print("=" * 70)
    sys.exit(1 if any(s == "FAIL" for s, _, _ in bad) else 0)


if __name__ == "__main__":
    main()
