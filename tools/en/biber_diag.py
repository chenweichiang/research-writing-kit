#!/usr/bin/env python3
"""English syntactic-feature comparison (Biber tagger) — local, no upload. Runs in a
**separate, optional** environment (`pybiber` + `spaCy` — see install notes below);
none of the rest of this kit needs it.

Why this exists: `ai_style_diag.py` measures punctuation, contrast sentences and
vocabulary; it has no grammar-level measure. Reinhart et al. 2025 (PNAS,
arXiv:2410.16107) compared 66 Biber (1988) syntactic features between human and
instruction-tuned LLM writing and found GPT-4o producing present-participial
clauses at 5.3x the human rate (d=1.38), that-clauses as subject at 2.6x (d=0.77),
nominalizations at 2.1x (d=1.23), and phrasal coordination at 1.9x (d=0.81) — one
"dense, noun-heavy" style.
⚠️ Those ratios are specific to GPT-4o/Llama 3 in that study, not a guarantee about
   any other model — so beyond those four named features, this tool also compares
   the full 66-feature set against your own baseline and lists everything that falls
   outside the 5th/95th percentile, whichever direction it goes.
⚠️ Cross-genre generalization of this kind of measure is weak (a classifier trained
   on one paper's prose can drop close to chance on a different genre in the same
   field), so the baseline has to be same-genre papers — this tool reuses
   `ai_style_diag.py`'s `--corpus` loading and its own-draft/template exclusion rules,
   so the two tools always compare against the same population.

Install (a separate virtual environment is recommended — pybiber/spaCy pull in a
fair amount of dependency weight, and most people using this kit will never need
this optional tool):
    python3 -m venv ~/.venvs/biber
    ~/.venvs/biber/bin/pip install pybiber spacy polars
    ~/.venvs/biber/bin/python -m spacy download en_core_web_sm

Reading by direction: Reinhart et al.'s four features are fixed in the LLM direction
(turn nominalizations back into verbs, split sentence-final -ing clauses) only when they
sit ABOVE the baseline p90. Inside the band they stay as they are, and below p10 the fix
runs the other way: a draft that was already "de-nominalized" past the field's range
reads looser and more conversational than the papers it will sit next to. `--groups`
compares against the target venue only; `--json` feeds `tools/register/register_profile.py`.

Usage:
    ~/.venvs/biber/bin/python biber_diag.py <draft.pdf|.tex|.md|.docx> --corpus ~/my-corpus
    ~/.venvs/biber/bin/python biber_diag.py <draft> --corpus ~/my-corpus --groups <venue> [--json]
    ~/.venvs/biber/bin/python biber_diag.py --corpus ~/my-corpus --rebuild-baseline
    ~/.venvs/biber/bin/python biber_diag.py --corpus ~/my-corpus --venues chi,dis

`--venues` limits which venue folders are loaded at all (the baseline is built from them
only). `--groups` keeps the whole corpus as the baseline and compares against the named
folders when they hold at least 30 papers, falling back to the whole corpus otherwise.

Baseline cache: `~/.cache/biber_kit_baseline.csv` (recomputed automatically whenever
the corpus file list changes; the first run takes a few minutes).
"""
import argparse
import hashlib
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import ai_style_diag as A  # noqa: E402  shared corpus loading, extraction, stripping

CACHE = pathlib.Path.home() / ".cache" / "biber_kit_baseline.csv"

# Reinhart et al. 2025's four features where instruction-tuned models ran high
# (direction = above human). Feature IDs are pybiber's own f_NN_name convention.
REINHART = {
    "f_25_present_participle": ("present-participial clauses", 5.3),
    "f_29_that_subj": ("that-clauses as subject", 2.6),
    "f_14_nominalizations": ("nominalizations", 2.1),
    "f_64_phrasal_coordination": ("phrasal coordination", 1.9),
}


def _nlp():
    try:
        import spacy
    except ImportError:
        sys.exit("Needs `spacy` in this environment: pip install spacy && "
                 "python -m spacy download en_core_web_sm\n"
                 "(Recommended: a separate venv — see the file header. This tool is "
                 "optional; the rest of the kit works without it.)")
    try:
        return spacy.load("en_core_web_sm", disable=["ner"])
    except OSError:
        sys.exit("spaCy model missing: python -m spacy download en_core_web_sm")


def _features(docs: dict):
    """docs: {doc_id: text} -> a polars DataFrame, one row per doc, normalized per
    1000 tokens (pybiber's own convention)."""
    try:
        import polars as pl
        import pybiber as pb
    except ImportError:
        sys.exit("Needs `pybiber` and `polars` in this environment: "
                 "pip install pybiber polars\n"
                 "(Recommended: a separate venv — see the file header.)")
    corp = pl.DataFrame({"doc_id": list(docs), "text": list(docs.values())})
    proc = pb.CorpusProcessor()
    tokens = proc.process_corpus(corp, nlp_model=_nlp(), n_process=4, batch_size=8)
    return pb.biber(tokens, force_ttr=False)


def _corpus(corpus_dir: pathlib.Path, venues=None):
    """Same baseline source, same own-draft/template exclusion, as ai_style_diag.py's
    --corpus — so the two tools are always comparing against the same population."""
    names = venues or sorted(d.name for d in corpus_dir.iterdir() if d.is_dir())
    out = {}
    for v in names:
        kept, _ = A.load_corpus(corpus_dir, [v])
        for name, raw in kept:
            body = A.clean(raw)
            if len(body.split()) >= 800:
                out[f"{v}/{name}"] = body   # doc_id keeps the venue for --groups
    return out


def baseline(corpus_dir: pathlib.Path, venues=None, rebuild=False):
    try:
        import polars as pl
    except ImportError:
        sys.exit("Needs `polars` in this environment: pip install polars pybiber spacy\n"
                 "(Recommended: a separate venv — see the file header. This tool is "
                 "optional; the rest of the kit works without it.)")
    corp = _corpus(corpus_dir, venues)
    if len(corp) < 30:
        sys.exit(f"Baseline only {len(corp)} papers — need ≥30 for percentiles. "
                 "Add more published full texts to the corpus.")
    key = hashlib.md5("\n".join(sorted(corp)).encode()).hexdigest()
    stamp = CACHE.with_suffix(".key")
    if not rebuild and CACHE.exists() and stamp.exists() and stamp.read_text().strip() == key:
        return pl.read_csv(CACHE)
    print(f"Computing Biber baseline for {len(corp)} papers (a few minutes)…", file=sys.stderr)
    df = _features(corp)
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    df.write_csv(CACHE)
    stamp.write_text(key)
    return df


def quantile(vals, q):
    """Nearest-rank quantile (vals already sorted)."""
    return vals[min(len(vals) - 1, max(0, round(q * (len(vals) - 1))))]


def profile(text, base, groups=None, min_docs=30, name="draft"):
    """{n_docs, groups, feats: {feature: {value, p10, p50, p90, pct, status}}}. `text` should
    already be A.clean()ed. `groups` filters the baseline by the venue prefix of doc_id; a
    subset with fewer than min_docs papers falls back to the whole baseline, and says so."""
    import polars as pl
    used = "all"
    if groups:
        mask = [str(d).split("/")[0] in groups for d in base["doc_id"].to_list()]
        sub = base.filter(pl.Series(mask))
        if sub.height >= min_docs:
            base, used = sub, ",".join(groups)
        else:
            used = f"all ({','.join(groups)} has only {sub.height} papers, fewer than {min_docs})"
    tgt = _features({name: text}).row(0, named=True)
    feats = {}
    for c in (c for c in base.columns if c.startswith("f_")):
        vals = sorted(v for v in base[c].to_list() if v is not None)
        x = tgt[c]
        # Ties count as half a rank: short drafts and 0-heavy features would otherwise
        # get reported as the 0th percentile just because the comparator is "<", not "<=".
        below = sum(1 for v in vals if v < x)
        ties = sum(1 for v in vals if v == x)
        p10, p50, p90 = quantile(vals, .1), quantile(vals, .5), quantile(vals, .9)
        feats[c] = dict(value=round(x, 3), p10=round(p10, 3), p50=round(p50, 3), p90=round(p90, 3),
                        pct=round((below + 0.5 * ties) / len(vals) * 100, 1),
                        status="high" if x > p90 else ("low" if x < p10 else "ok"))
    return dict(n_docs=base.height, groups=used, feats=feats)


def main():
    import json
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", nargs="?", help="draft (.pdf/.tex/.md/.docx)")
    ap.add_argument("--corpus", default=None,
                    help="baseline corpus dir, same layout as ai_style_diag.py's --corpus")
    ap.add_argument("--venues", default="",
                    help="comma-separated venue subdirs to load at all (default: all subdirs)")
    ap.add_argument("--groups", default="",
                    help="comma-separated venue subdirs to compare against (whole corpus stays "
                         "the baseline; falls back to it when the subset has <30 papers)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--rebuild-baseline", action="store_true",
                    help="recompute the Biber baseline even if the cache looks current")
    args = ap.parse_args()
    if not args.corpus:
        sys.exit("Needs a baseline corpus: pass --corpus <dir> (same layout as "
                 "ai_style_diag.py's --corpus: <corpus>/<venue>/*.txt).")
    corpus_dir = pathlib.Path(args.corpus).expanduser()
    if not corpus_dir.is_dir():
        sys.exit(f"Corpus dir not found: {corpus_dir}")
    venues = [v.strip() for v in args.venues.split(",") if v.strip()] or None
    groups = [g.strip() for g in args.groups.split(",") if g.strip()] or None
    base = baseline(corpus_dir, venues, rebuild=args.rebuild_baseline)
    if not args.target:
        print(f"Baseline ready: {base.height} papers -> {CACHE}")
        return

    p = pathlib.Path(args.target).expanduser()
    if not p.exists():
        sys.exit(f"Not found: {p}")
    text = A.clean(A.extract_text(p))
    if len(text.split()) < 800:
        sys.exit("Draft under 800 words, statistics unstable.")
    prof = profile(text, base, groups, name=p.name)
    if args.json:
        print(json.dumps(prof, ensure_ascii=False, indent=1))
        return
    F = prof["feats"]
    print(f"Draft {p.name} | baseline {prof['n_docs']} field papers ({prof['groups']}) | per 1000 tokens")
    print("\n[Reinhart et al. 2025's four features, GPT-4o : human ratio in that study]")
    print(f"{'feature':<28}{'draft':>8}{'baseline med':>13}{'x median':>10}{'pctile':>8}  GPT-4o")
    hot = 0
    for c, (label, gpt) in REINHART.items():
        f = F[c]
        ratio = f"{f['value'] / f['p50']:>9.1f}x" if f["p50"] else f"{'-':>10}"
        flag = {"high": " \u25b2 high", "low": " \u25bc low"}.get(f["status"], "")
        hot += f["status"] == "high"
        print(f"{label:<28}{f['value']:>8.2f}{f['p50']:>13.2f}{ratio}{f['pct']:>7.0f}%  {gpt}x{flag}")
    print(f"-> {hot} of 4 features above the baseline p90.")

    outl = [(c, f) for c, f in F.items() if c not in REINHART
            and c not in ("f_43_type_token", "f_44_mean_word_length")
            and (f["pct"] >= 95 or f["pct"] <= 5)]
    print(f"\n[Remaining {len(F) - len(REINHART)} features outside the baseline 5%/95%]")
    for c, f in sorted(outl, key=lambda x: -abs(x[1]["pct"] - 50)):
        side = "high" if f["pct"] >= 95 else "low"
        print(f"  {c:<32}{f['value']:>8.2f}  baseline median {f['p50']:>7.2f}  {f['pct']:>4.0f}%  {side}")
    if not outl:
        print("  none")
    print("\nReading (by direction): these are perceptual-layer clues, not a verdict; any "
          "single paper's grammar drifts from the field average anyway. Reinhart et al. "
          "describe a dense, noun-heavy direction. Only when those four features are flagged "
          "high do you fix them that way (turn nominalizations back into verbs, split a "
          "trailing -ing participial clause into its own sentence). Leave them alone inside the "
          "band, and when they are flagged low the fix runs the other way: an over-corrected "
          "draft reads looser and more conversational than the field's papers.")


if __name__ == "__main__":
    main()
