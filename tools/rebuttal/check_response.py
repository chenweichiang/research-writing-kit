#!/usr/bin/env python3
"""check_response.py — completeness check for a response-to-reviewers letter.

Three ways an R&R goes wrong, all of them checklist problems rather than skill
problems, and all of them invisible to a human reading their own letter at 2am:

  · a reviewer point never gets answered (the editor reads them side by side)
  · the letter says "we have revised this" but the manuscript never changed
  · point numbers get renumbered and the letter now cites ones that don't exist

⚠️ This checks COMPLETENESS, not quality. Every point being answered does not mean
   it is answered well. Judgement is a human's job (or a clean-context review pass).

No dependencies (Python 3 standard library only).

Usage:
  check_response.py --points points.tsv --revisions revisions.tsv --letter letter.md
Exit code 1 if anything must be fixed before sending.
"""
import argparse, pathlib, re, sys

ACCEPTISH = {"ACCEPT", "PARTIAL"}
VALID_VERDICT = ACCEPTISH | {"DECLINE"}
PID_RE = re.compile(r"\b([ER]\d*\.\d+)\b")   # R1.3 / E.1 / R2.10


def read_tsv(path, required):
    """Read a TSV (blank lines and # comments allowed). Missing columns stop the run —
    silently skipping them would turn this checker into another source of false green."""
    rows, header = [], None
    for ln, raw in enumerate(pathlib.Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        cells = [c.strip() for c in raw.split("\t")]
        if header is None:
            header = cells
            missing = [c for c in required if c not in header]
            if missing:
                sys.exit(f"FAIL {path}: missing column(s) {', '.join(missing)} "
                         f"(found: {', '.join(header)})")
            continue
        cells += [""] * (len(header) - len(cells))
        rows.append(dict(zip(header, cells)) | {"_line": ln})
    if header is None:
        sys.exit(f"FAIL {path}: no header row")
    return rows


def check(points_p, revs_p, letter_p):
    points = read_tsv(points_p, ["id", "verdict"])
    revs = read_tsv(revs_p, ["point_id", "location"])
    letter = pathlib.Path(letter_p).read_text(encoding="utf-8")
    bad = []

    ids = [p["id"] for p in points]
    for i in sorted({i for i in ids if ids.count(i) > 1}):
        bad.append(("FAIL", f"duplicate point id {i} in points.tsv",
                    "two rows share an id — nothing can tell which one the letter answers"))

    by_pid = {}
    for r in revs:
        by_pid.setdefault(r["point_id"], []).append(r)
    in_letter = set(PID_RE.findall(letter))

    for p in points:
        pid, verdict = p["id"], p["verdict"].strip().upper()
        if verdict not in VALID_VERDICT:
            bad.append(("FAIL", f"{pid}: invalid verdict '{p['verdict']}'",
                        f"must be one of {'/'.join(sorted(VALID_VERDICT))} (line {p['_line']})"))
            continue
        if pid not in in_letter:
            bad.append(("FAIL", f"{pid} does not appear in the letter",
                        "every point a reviewer raised needs an answer — editors check one by one"))
        rows = by_pid.get(pid, [])
        if verdict in ACCEPTISH:
            if not rows:
                bad.append(("FAIL", f"{pid} is {verdict} but has no row in revisions.tsv",
                            "promising a change you never made is the second most common way R&R fails"))
            elif not any(r["location"].strip() and r["location"].strip() != "-" for r in rows):
                bad.append(("FAIL", f"{pid} has a revision row but location is empty",
                            "be specific: 'S4.2, 2nd paragraph'. 'the Method section' is not findable"))
        else:
            ev = " ".join(r.get("evidence", "") for r in rows).strip()
            if not ev:
                bad.append(("FAIL", f"{pid} is DECLINE with no evidence",
                            "declining is legitimate, but every DECLINE gets read by the editor — "
                            "point at where the manuscript already answers this, or give the "
                            "methodological reason"))

    for orphan in sorted(in_letter - set(ids)):
        bad.append(("WARN", f"letter cites {orphan}, which is not in points.tsv",
                    "renumbered without syncing, or a reviewer point never got logged"))
    return points, revs, bad


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--points", required=True)
    ap.add_argument("--revisions", required=True)
    ap.add_argument("--letter", required=True)
    a = ap.parse_args()

    points, revs, bad = check(a.points, a.revisions, a.letter)
    n_fail = sum(1 for s, _, _ in bad if s == "FAIL")
    print("=" * 68)
    print(f"  Response completeness: {len(points)} points / {len(revs)} revision rows")
    print("=" * 68)
    if not bad:
        print("  OK - all four checks pass (completeness only; quality is a separate pass)")
    for sev, title, why in bad:
        print(f"  [{sev}] {title}\n         {why}")
    print("=" * 68)
    tally = {}
    for p in points:
        tally[p["verdict"].upper()] = tally.get(p["verdict"].upper(), 0) + 1
    print("  verdicts: " + "  ".join(f"{k}={v}" for k, v in sorted(tally.items())))
    if tally.get("DECLINE", 0) > len(points) / 2:
        print("  ! more than half are DECLINE - make sure you are not arguing with the reviewers")
    if tally.get("ACCEPT", 0) == len(points) and len(points) > 3:
        print("  ! everything accepted - make sure you did not change something that was right")
    print("=" * 68)
    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()
