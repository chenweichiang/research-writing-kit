#!/usr/bin/env python3
"""English metadiscourse measurement (Hyland framework) — local, no upload. This is
not a detector.

Why this exists: the most consistent difference reported between LLM and human
academic writing shows up at the metadiscourse layer, not the sentence-punctuation
layer:
- Jiang & Hyland 2025b (Written Communication): reader-engagement markers in student
  argumentative essays, ChatGPT 5.40 vs. student 16.99 per 1000 words;
- Zhang & Zhang 2025: stance markers in research-article abstracts, ChatGPT 51.66 vs.
  human 36.69 per 1000 words, with human writing leaning more implicit.
(These figures are quoted from the original papers, not reproduced from memory —
verify against the source before citing them yourself; genres differ, so treat the
direction as the transferable part, not the exact numbers.)

The marker list follows Hyland's (2005) metadiscourse taxonomy, restricted to
common, low-false-positive forms; the reader-engagement category is this tool's own
addition on top of that taxonomy. Regex cannot distinguish USE of a form from mere
MENTION of it (e.g. quoting someone else's hedge) — use `--matches` to read the
actual sentences before trusting any single number.

Baseline: reuses `ai_style_diag.py`'s `--corpus` (<corpus>/<venue>/*.txt, ≥30 needed,
same own-draft/template exclusion rules). Cached at
`~/.cache/metadiscourse_en_kit_baseline.json`, keyed by the corpus file list.

Usage:
    python3 metadiscourse_en.py <draft> --corpus ~/my-corpus [--matches]
    python3 metadiscourse_en.py <draft> --corpus ~/my-corpus --rebuild
"""
import argparse
import hashlib
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import ai_style_diag as A  # noqa: E402  shared corpus loading, extraction, stripping

CACHE = pathlib.Path("~/.cache/metadiscourse_en_kit_baseline.json").expanduser()

# (category, name) -> regex (case-insensitive unless noted in CASE_SENSITIVE)
MARKERS = {
    ("stance", "hedges"): r"\b(may|might|could|possibly|perhaps|probably|likely|unlikely|appears? to|seems? to|"
                          r"suggests?|suggested|tends? to|relatively|somewhat|largely|generally|in general|"
                          r"to some extent|arguably)\b(?! \d)",
    ("stance", "boosters"): r"\b(clearly|undoubtedly|indeed|certainly|definitely|obviously|in fact|"
                            r"demonstrates?|demonstrated|shows? that|showed that|always|never|must be)\b",
    ("stance", "attitude markers"): r"\b(importantly|interestingly|surprisingly|remarkably|unfortunately|"
                                    r"essential|crucial|striking(ly)?|notably|significant(ly)? (for|to|in) )\b",
    ("stance", "self-mention"): r"\b(I|we|our|ours|us|my|me|the authors?|the first author|this author)\b",
    ("engagement", "reader pronouns"): r"\b(you|your|the reader|readers|one's)\b",
    ("engagement", "directives"): r"\b(note that|consider|let us|let's|imagine|recall that|it should be noted|"
                                  r"it must be noted|notice that)\b",
    ("engagement", "questions"): r"\?",
    ("engagement", "shared knowledge"): r"\b(of course|as is well known|it is well known|as we know|naturally|"
                                        r"it is widely (accepted|recognised|recognized))\b",
    ("guiding", "transitions"): r"\b(however|therefore|thus|moreover|furthermore|in addition|consequently|"
                                r"nevertheless|nonetheless|hence|whereas)\b",
    ("guiding", "frame markers"): r"\b(first(ly)?,|second(ly)?,|third(ly)?,|finally,|in sum|in summary|to conclude|"
                                  r"in conclusion|overall,|taken together|to summari[sz]e)\b",
    ("guiding", "code glosses"): r"\b(e\.g\.|i\.e\.|that is,|in other words|namely|for example|for instance|"
                                 r"such as)\b|—",
    ("guiding", "evidentials"): r"\b(according to|prior work|previous (work|studies|research)|"
                                r"(research|studies) (has|have) (shown|suggested|found)|it has been (argued|shown))\b",
}
CASE_SENSITIVE = {("stance", "self-mention")}   # capital "I" is what marks self-mention
# Direction the research above reports: LLM stance markers run high and explicit;
# reader engagement runs low.
WATCH_HIGH = {"boosters", "attitude markers"}
WATCH_LOW = {"reader pronouns", "directives", "questions"}


def count(text):
    n = len(re.findall(r"[A-Za-z][A-Za-z'-]*", text))
    out = {}
    for key, rx in MARKERS.items():
        flags = 0 if key in CASE_SENSITIVE else re.I
        out[key[1]] = len(re.findall(rx, text, flags))
    return n, out


def baseline(corpus_dir: pathlib.Path, venues=None, rebuild=False):
    kept, _ = A.load_corpus(corpus_dir, venues)
    if len(kept) < 30:
        sys.exit(f"Baseline only {len(kept)} papers — need ≥30 for percentiles.")
    key = hashlib.md5("\n".join(sorted(n for n, _ in kept)).encode()).hexdigest()
    if not rebuild and CACHE.exists():
        try:
            c = json.loads(CACHE.read_text())
            if c.get("_key") == key:
                return c
        except Exception:
            pass
    dist = {k[1]: [] for k in MARKERS}
    used = 0
    for _, raw in kept:
        body = A.clean(raw)
        n, c = count(body)
        if n < 800:
            continue
        used += 1
        for k, v in c.items():
            dist[k].append(round(v / n * 1000, 3))
    if used < 30:
        sys.exit(f"Only {used} baseline papers had ≥800 words after cleaning — need ≥30.")
    out = {"_key": key, "_n": used, "dist": {k: sorted(v) for k, v in dist.items()}}
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(out))
    return out


def pct(vals, x):
    below = sum(1 for v in vals if v < x)
    ties = sum(1 for v in vals if v == x)
    return (below + 0.5 * ties) / len(vals) * 100


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target")
    ap.add_argument("--corpus", required=True,
                    help="baseline corpus dir — same layout as ai_style_diag.py's --corpus")
    ap.add_argument("--venues", default="",
                    help="comma-separated venue subdirs to use (default: all)")
    ap.add_argument("--matches", action="store_true",
                    help="list the first 8 actual matches (with context) per marker")
    ap.add_argument("--rebuild", action="store_true")
    args = ap.parse_args()
    corpus_dir = pathlib.Path(args.corpus).expanduser()
    if not corpus_dir.is_dir():
        sys.exit(f"Corpus dir not found: {corpus_dir}")
    venues = [v.strip() for v in args.venues.split(",") if v.strip()] or None
    b = baseline(corpus_dir, venues, args.rebuild)
    p = pathlib.Path(args.target).expanduser()
    if not p.exists():
        sys.exit(f"Not found: {p}")
    text = A.clean(A.extract_text(p))
    n, c = count(text)
    if n < 800:
        sys.exit("Draft under 800 words — statistics unstable.")
    print(f"Draft {n} words | baseline {b['_n']} field papers | per 1000 words | "
          "this is a descriptive comparison, not a detector")
    print(f"{'cat':<11}{'marker':<26}{'count':>5}{'draft':>8}{'baseline med':>13}{'pctile':>7}")
    cat_prev = None
    for (cat, name), _ in MARKERS.items():
        v = c[name] / n * 1000
        vals = b["dist"][name]
        pc = pct(vals, v)
        flag = ""
        if c[name] >= 3 or name in WATCH_LOW:
            if name in WATCH_HIGH and pc > 90:
                flag = " << high (LLM-typical direction)"
            elif name in WATCH_LOW and pc < 5:   # ~16% of human papers have zero directives;
                flag = " << low (LLM-typical direction)"    # 0 landing at the 8th pctile isn't itself worth flagging
            elif pc > 97 or pc < 3:
                flag = " · outlier"
        print(f"{cat if cat != cat_prev else '':<11}{name:<26}{c[name]:>5}{v:>8.2f}"
              f"{vals[len(vals)//2]:>13.2f}{pc:>6.0f}%{flag}")
        cat_prev = cat
    if args.matches:
        for (cat, name), rx in MARKERS.items():
            flags = 0 if (cat, name) in CASE_SENSITIVE else re.I
            ms = list(re.finditer(rx, text, flags))[:8]
            if ms:
                print(f"\n[{name}]")
                for m in ms:
                    print("   …" + re.sub(r"\s+", " ", text[max(0, m.start() - 50):m.end() + 50]) + "…")
    print("\nReading: the research above reports LLM writing running high on stance "
          "markers (especially explicit ones — boosters, attitude markers) and low on "
          "reader engagement. When hedges and transitions are noticeably below the "
          "baseline, claims tend to read more categorically than the evidence "
          "supports, and the logic between sentences is left for the reader to "
          "reconstruct. On an outlier, read the sentences with --matches before "
          "editing; fix by letting claims track the evidence and addressing the "
          "reader directly where it's natural, not by mechanically inserting or "
          "deleting markers. Self-mention runs low in an anonymized submission — "
          "that's expected, not a signal.")


if __name__ == "__main__":
    main()
