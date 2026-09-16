#!/usr/bin/env python3
"""Re-run the style-fingerprint tools on every tracked manuscript after a
measurement-rule change.

Why this exists: a fix to `ai_style_diag.py` / `zh_ai_style.py` (a corrected regex,
a swapped baseline corpus, a bug in how sentences are split) only protects
manuscripts that get re-measured with the fixed tool. Without a step like this, a
paper checked under the *old*, buggy rule can sit "clean" in your records while it's
actually above your field's norm — and stay that way straight through submission.
Run this any time you change the measurement logic in `ai_style_diag.py`,
`zh_ai_style.py`, or `common/md_prose.py` (both style tools depend on it).

Reads two files you maintain yourself:
  --ledger   your submission ledger, e.g. `SUBMISSIONS.tsv`
             (see tools/submissions/SUBMISSIONS.template.tsv / check_submissions.py)
  --targets  which file to measure for each manuscript, e.g. `style_targets.tsv`
             (see tools/submissions/style_targets.template.tsv)
Every ledger row whose status is drafting/submitted/under_review/revision must have
a matching row in the targets file — checked and reported, not silently skipped,
because a manuscript with no measured target has no protection at all.

Paths in the targets file are resolved relative to --root (default: the ledger
file's own directory — same convention `check_submissions.py` uses for its
`project` column) unless they start with `~` or are already absolute. This script
never hardcodes a path to your projects; point it at your own files with the flags.

Usage:
    python3 style_reaudit.py --ledger SUBMISSIONS.tsv --targets style_targets.tsv \\
        --en-corpus ~/my-corpus [--zh-corpus ~/my-zh-corpus] [--root ~/my-projects]

    # registry check only — no style tools run, no corpus needed:
    python3 style_reaudit.py --ledger SUBMISSIONS.tsv --targets style_targets.tsv --check
"""
import argparse
import csv
import glob
import pathlib
import statistics
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "en"))
sys.path.insert(0, str(HERE.parent / "zh-tw"))

NEEDS_TARGET = {"drafting", "submitted", "under_review", "revision"}


def read_tsv(path: pathlib.Path):
    rows = []
    with open(path, encoding="utf-8") as f:
        lines = [l for l in f if l.strip() and not l.startswith("#")]
    for r in csv.DictReader(lines, delimiter="\t"):
        rows.append(r)
    return rows


def resolve(path_field: str, root: pathlib.Path):
    """Return (path, state). state: 'skip' (deliberately un-measured, path == '-'),
    'missing' (nothing found), or 'ok'. A glob picks the most recently modified match."""
    p = path_field.strip()
    if p == "-":
        return None, "skip"
    base = (pathlib.Path(p).expanduser()
            if (p.startswith("~") or pathlib.Path(p).is_absolute()) else root / p)
    if "*" in p:
        hits = [pathlib.Path(x) for x in glob.glob(str(base))]
        if not hits:
            return None, "missing"
        return max(hits, key=lambda x: x.stat().st_mtime), "ok"
    return (base, "ok") if base.exists() else (None, "missing")


def check_registry(ledger_rows, targets, root: pathlib.Path):
    """Every active ledger row needs a target; every target's path must exist and
    declare a real language. Returns a list of human-readable problem strings."""
    problems = []
    tids = {t["target_id"] for t in targets}
    for r in ledger_rows:
        if r["status"].strip().lower() in NEEDS_TARGET and r["manuscript_id"] not in tids:
            problems.append(f"[FAIL] ledger entry '{r['manuscript_id']}' ({r['status']}) "
                            "has no row in the style-targets file")
    for t in targets:
        _, state = resolve(t["path"], root)
        if state == "missing":
            problems.append(f"[FAIL] {t['target_id']}: path not found: {t['path']} "
                            "(renamed, moved, or --root is wrong?)")
        if t["lang"] not in ("en", "zh"):
            problems.append(f"[FAIL] {t['target_id']}: lang must be en/zh, got '{t['lang']}'")
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ledger", required=True,
                    help="your submission ledger (see SUBMISSIONS.template.tsv)")
    ap.add_argument("--targets", required=True,
                    help="which file to measure per manuscript (see style_targets.template.tsv)")
    ap.add_argument("--root", default=None,
                    help="base dir for relative paths in --targets (default: --ledger's own directory)")
    ap.add_argument("--en-corpus", default=None,
                    help="baseline corpus for English targets (same as ai_style_diag.py --corpus)")
    ap.add_argument("--zh-corpus", default=None,
                    help="baseline corpus for Chinese targets (same as zh_ai_style.py --corpus); "
                         "omit to fall back on zh_ai_style.py's built-in reference threshold")
    ap.add_argument("--check", action="store_true",
                    help="only validate the registry (every active row has a target, every "
                         "path resolves); don't run the style tools, no corpus needed")
    args = ap.parse_args()

    ledger_path = pathlib.Path(args.ledger).expanduser()
    targets_path = pathlib.Path(args.targets).expanduser()
    if not ledger_path.exists():
        sys.exit(f"Ledger not found: {ledger_path}")
    if not targets_path.exists():
        sys.exit(f"Targets file not found: {targets_path}")
    root = pathlib.Path(args.root).expanduser() if args.root else ledger_path.parent

    ledger_rows = read_tsv(ledger_path)
    targets = read_tsv(targets_path)
    problems = check_registry(ledger_rows, targets, root)
    for p in problems:
        print(p)
    if args.check:
        print("registry OK" if not problems else f"{len(problems)} problem(s)")
        sys.exit(1 if problems else 0)

    import ai_style_diag as A  # noqa: E402
    import zh_ai_style as Z  # noqa: E402

    en_targets = [t for t in targets if t["lang"] == "en"]
    zh_targets = [t for t in targets if t["lang"] == "zh"]

    cvals = evals = p90c = None
    if en_targets:
        if not args.en_corpus:
            print("[WARN] English targets present but no --en-corpus given — skipping English rows.")
        else:
            corpus_dir = pathlib.Path(args.en_corpus).expanduser()
            kept, _ = A.load_corpus(corpus_dir)
            base = [s for s in (A.profile(A.clean(raw), name) for name, raw in kept) if s]
            if len(base) < 30:
                print(f"[WARN] English baseline only {len(base)} papers — need ≥30. Skipping English rows.")
            else:
                cvals = sorted(b["contrast"] for b in base)
                evals = sorted(b["emdash"] for b in base)
                p90c = cvals[int(len(cvals) * 0.9)]
                print(f"\nEnglish contrast-sentence total: field median {statistics.median(cvals):.2f}, "
                      f"p90 {p90c:.2f} (per 1000 words, baseline {len(base)} papers)")

    zth = None
    if zh_targets:
        if not args.zh_corpus:
            zth = Z.TH["contrast"][1]
            print(f"[WARN] Chinese targets present but no --zh-corpus given — using the "
                  f"heuristic reference threshold ({zth}/1k Han chars, see zh_ai_style.py header).")
        else:
            zcb = Z.corpus_baseline(pathlib.Path(args.zh_corpus).expanduser())
            if zcb:
                zv = zcb["dist"]["contrast"]
                zth = zv[int(len(zv) * 0.9)]
                print(f"Chinese contrast-frame total: corpus median {zv[len(zv)//2]:.2f}, "
                      f"p90 {zth:.2f} (per 1000 Han chars, baseline {zcb['_n']} papers)")
            else:
                zth = Z.TH["contrast"][1]
                print(f"[WARN] Chinese corpus had fewer than 30 usable files — using the "
                      f"heuristic reference threshold ({zth}/1k Han chars).")

    print(f"\n{'manuscript':<28}{'lang':<5}{'contrast':>9}{'pctile':>8}{'emdash pctile':>15}  "
          f"verdict  file")
    bad = 0
    for t in targets:
        path, state = resolve(t["path"], root)
        if state == "skip":
            print(f"{t['target_id']:<28}{t['lang']:<5}{'—':>9}{'':>8}{'':>15}  skip     {t['note']}")
            continue
        if state == "missing" or path is None:
            continue
        if t["lang"] == "en":
            if cvals is None:
                continue
            prof = A.profile(A.clean(A.extract_text(path)), path.name)
            if not prof:
                print(f"{t['target_id']:<28}en   {'too short':>9}{'':>8}{'':>15}  —        {path.name}")
                continue
            pct = sum(1 for v in cvals if v < prof["contrast"]) / len(cvals) * 100
            epct = sum(1 for v in evals if v < prof["emdash"]) / len(evals) * 100
            over = prof["contrast"] > p90c
            print(f"{t['target_id']:<28}en   {prof['contrast']:>9.2f}{pct:>7.0f}%{epct:>14.0f}%  "
                  f"{'OVER' if over else 'ok  '}     {path.name}")
        else:
            if zth is None:
                continue
            prof = Z.profile(Z.extract(path))
            if not prof:
                print(f"{t['target_id']:<28}zh   {'too short':>9}")
                continue
            over = prof["contrast"] > zth
            print(f"{t['target_id']:<28}zh   {prof['contrast']:>9.2f}{'':>8}{'':>15}  "
                  f"{'OVER' if over else 'ok  '}     {path.name}")
        bad += over

    print(f"\n{bad} manuscript(s) over the contrast-sentence threshold. Leave a "
          "submitted/under-review manuscript as it is until its next revision round; "
          "fix a drafting manuscript on your normal editing pass — don't touch a "
          "version that's already with a venue.")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
