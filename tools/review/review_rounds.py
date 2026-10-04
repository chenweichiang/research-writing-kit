#!/usr/bin/env python3
"""review_rounds.py: a convergence ledger for review rounds, and when to stop reviewing.

Why it exists: a manuscript went through ten review rounds and every round still
produced a "new" fatal finding, yet nothing recorded the answer to two questions:
are these genuinely new problems, or the same already-settled issue raised in
different words? Is the review converging at all? Without that record a review has
no end: a simulated reviewer can always find something to pick at, and the author
is asked the same thing over and over.

The ledger is a tab-separated file kept with the manuscript (for example
`docs/review-rounds.tsv`); after each round one row is appended per fatal or major
finding. A template is in review-rounds.template.tsv.
  round  date  version  id  severity  repeat_of  disposition  note  summary
  - severity: fatal or major (minor findings are not recorded; they do not affect the stop rule)
  - repeat_of: empty = newly raised; an id from an earlier round, or an A-number from
    ADJUDICATED.md = raised again
  - disposition: fixed / declined / pending / withdrawn (withdrawn = the reviewer was wrong).
    The Chinese values 已改 / 裁定不改 / 待裁定 / 撤回 are accepted as aliases.
  - note: required when a repeat re-raises an adjudicated item (an A-number, or an item
    whose earlier disposition was "declined"): it must state the new evidence, otherwise
    the ledger is reported as an error

ADJUDICATED.md is the project's list of items the author has already ruled on, one
per table row starting with an A-number, e.g. `| A15 | 2026-09-05 | topic | ruling | basis |`.
Re-raising one without new evidence is skipped by the review procedure.

Stop rule: two consecutive rounds with no new fatal and no new major finding means
review has converged; recommend stopping and leave the rest to submission and external
review. A repeat is not new: raising the same thing in other words means the review
is going in circles.

Usage:
  review_rounds.py docs/review-rounds.tsv [--adjudicated ADJUDICATED.md] [--json]
  review_rounds.py docs/review-rounds.tsv --suggest    # findings logged as new whose summary resembles an earlier one
Exit code: 0 = ledger is sound; 1 = ledger has errors (a repeat that points nowhere, an adjudicated
item re-raised without new evidence, an invalid field)
"""
import argparse
import csv
import json
import os
import re
import sys
from collections import OrderedDict
from difflib import SequenceMatcher

FIELDS = ["round", "date", "version", "id", "severity", "repeat_of", "disposition", "note", "summary"]
SEV = {"fatal", "major"}
DISP = {"fixed", "declined", "pending", "withdrawn"}
DISP_ALIAS = {"已改": "fixed", "裁定不改": "declined", "待裁定": "pending", "撤回": "withdrawn"}


def norm_disp(v):
    v = v.strip()
    return DISP_ALIAS.get(v, v.lower())


def load(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        lines = [l for l in f if l.strip() and not l.startswith("#")]
    for r in csv.DictReader(lines, delimiter="\t"):
        row = {k: (r.get(k) or "").strip() for k in FIELDS}
        row["disposition"] = norm_disp(row["disposition"])
        rows.append(row)
    return rows


def adjudicated_ids(path):
    if not path or not os.path.exists(path):
        return set()
    with open(path, encoding="utf-8") as f:
        return set(re.findall(r"^\|\s*(A\d+)\s*\|", f.read(), re.M))


def check(rows, adj):
    errs = []
    seen = {}                               # id -> row
    for r in rows:
        where = f"round {r['round']} {r['id']}"
        if not r["round"].isdigit():
            errs.append(f"{where}: round is not an integer")
        if r["severity"] not in SEV:
            errs.append(f"{where}: severity must be fatal or major (minor is not recorded), got \"{r['severity']}\"")
        if r["disposition"] and r["disposition"] not in DISP:
            errs.append(f"{where}: disposition must be one of {' / '.join(sorted(DISP))}, got \"{r['disposition']}\"")
        rep = r["repeat_of"]
        if rep:
            prior = seen.get(rep)
            is_adj = rep in adj or re.fullmatch(r"A\d+", rep) is not None
            if not prior and not is_adj:
                errs.append(f"{where}: repeat_of \"{rep}\" is in no earlier round and not in ADJUDICATED")
            settled = is_adj or (prior and prior["disposition"] == "declined")
            if settled and not r["note"]:
                errs.append(f"🔴 {where}: re-raises the settled item \"{rep}\" without stating new evidence "
                            "(no new evidence means skip it)")
        if r["id"] in seen and seen[r["id"]]["round"] != r["round"]:
            errs.append(f"{where}: id repeats round {seen[r['id']]['round']}; use fresh ids in each round")
        seen.setdefault(r["id"], r)
    return errs


def table(rows):
    rounds = OrderedDict()
    for r in sorted(rows, key=lambda x: int(x["round"]) if x["round"].isdigit() else 0):
        t = rounds.setdefault(r["round"], {"version": r["version"], "date": r["date"],
                                           "fatal_new": 0, "fatal_rep": 0, "major_new": 0, "major_rep": 0,
                                           "withdrawn": 0})
        if r["disposition"] == "withdrawn":
            t["withdrawn"] += 1
            continue
        k = ("fatal" if r["severity"] == "fatal" else "major") + ("_rep" if r["repeat_of"] else "_new")
        if k in t:
            t[k] += 1
    return rounds


def converged(rounds):
    keys = list(rounds)
    if len(keys) < 2:
        return False, "fewer than two rounds, too early to judge convergence"
    last2 = [rounds[k] for k in keys[-2:]]
    if all(t["fatal_new"] == 0 and t["major_new"] == 0 for t in last2):
        return True, (f"rounds {keys[-2]} and {keys[-1]} raised no new fatal or major finding: "
                      "recommend stopping; leave the rest to submission and external review")
    for k in reversed(keys):
        t = rounds[k]
        if t["fatal_new"] or t["major_new"]:
            return False, f"round {k} still raised new findings: fatal {t['fatal_new']}, major {t['major_new']}"
    return False, "no new findings in the latest rounds"   # unreachable once two rounds are clean


def bigrams(s):
    s = re.sub(r"\s+", "", s.lower())
    return {s[i:i + 2] for i in range(len(s) - 1)}


def suggest(rows, th=0.45):
    out = []
    for i, r in enumerate(rows):
        if r["repeat_of"]:
            continue
        a = bigrams(r["summary"])
        for p in rows[:i]:
            if p["round"] == r["round"] or not a:
                continue
            b = bigrams(p["summary"])
            j = len(a & b) / max(1, len(a | b))
            seq = SequenceMatcher(None, r["summary"], p["summary"]).ratio()
            if max(j, seq) >= th:
                out.append((r, p, max(j, seq)))
    return out


def main():
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    ap.add_argument("ledger", help="the review-rounds TSV (see review-rounds.template.tsv)")
    ap.add_argument("--adjudicated", default="",
                    help="path to ADJUDICATED.md (default: look beside the ledger, then one level up)")
    ap.add_argument("--suggest", action="store_true",
                    help="list findings logged as new whose summary resembles an earlier round's")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    adj_path = a.adjudicated
    if not adj_path:
        base = os.path.dirname(os.path.abspath(a.ledger))
        for c in (os.path.join(base, "ADJUDICATED.md"), os.path.join(base, "..", "ADJUDICATED.md")):
            if os.path.exists(c):
                adj_path = c
                break
    rows = load(a.ledger)
    errs = check(rows, adjudicated_ids(adj_path))
    rounds = table(rows)
    ok, why = converged(rounds)
    if a.json:
        print(json.dumps({"rounds": rounds, "converged": ok, "reason": why, "errors": errs},
                         ensure_ascii=False, indent=1))
        return 1 if errs else 0
    print("round  version   fatal (new/repeat)  major (new/repeat)  withdrawn")
    for k, t in rounds.items():
        print(f"{k:>5}  {t['version']:<8}  {t['fatal_new']:>3} / {t['fatal_rep']:<12}  "
              f"{t['major_new']:>3} / {t['major_rep']:<11}  {t['withdrawn']}")
    print(("\n✅ " if ok else "\n⏳ ") + why)
    if a.suggest:
        sug = suggest(rows)
        print(f"\n== Logged as new but the summary resembles an earlier round's ({len(sug)}): check whether it is a repeat ==")
        for r, p, s in sug:
            print(f"  round {r['round']} {r['id']} ~ round {p['round']} {p['id']} ({s:.2f}): {r['summary'][:40]}")
    if errs:
        print("\n== Ledger errors ==")
        for e in errs:
            print("  " + e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
