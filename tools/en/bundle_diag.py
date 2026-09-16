#!/usr/bin/env python3
"""Lexical-bundle overuse diagnostic (English + Traditional Chinese) — local, no upload.

Why this exists: research on LLM vs. human academic writing finds systematic
differences at the level of multi-word **bundles** (Jiang & Hyland's stance bundles,
Kobak-style excess vocabulary), and the fixed-word-list tools in this kit only look
at single words or fixed phrases. This tool derives its comparison from your own
baseline corpus instead: it lists bundles your draft repeats that are ALSO common in
real published papers (so they're not exotic jargon) but that your draft uses far
more than the baseline does. The fix is rewording or cutting the repeat — not
swapping in a different fixed sentence pattern.

Baseline: a folder of .txt files you assemble yourself.
  English — reuses `ai_style_diag.py`'s `--corpus` (<corpus>/<venue>/*.txt layout,
    same own-draft/template exclusion rules).
  Chinese — a flat folder of .txt files (same `--corpus`, no venue subfolders):
    published papers in your genre, ideally pre-dating common AI writing assistance
    for the same reason described in `zh_ai_style.py`.
Method: English bundles are 3–4 lowercase word n-grams; Chinese bundles are 3–4
consecutive Han characters (no word segmentation — Chinese academic writing doesn't
reliably segment into words the way English does).
Reports only bundles that appear ≥3 times in your draft, appear in a high enough
share of baseline documents to count as ordinary field vocabulary rather than your
paper's own topic terms (English ≥5% of documents, Chinese ≥20% — Chinese 3–4
character strings are noisier at low document frequency and skew toward topic terms),
and occur in your draft at ≥3x the baseline's per-10,000 rate.

No dependencies beyond this kit's `common/md_prose.py` (Python 3 stdlib).

Usage:
    python3 bundle_diag.py <draft> --lang en --corpus ~/my-corpus
    python3 bundle_diag.py <draft> --lang zh --corpus ~/my-zh-corpus
    python3 bundle_diag.py <draft> --lang en --corpus ~/my-corpus --top 30
"""
import argparse
import pathlib
import re
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "common"))
import ai_style_diag as A  # noqa: E402  English corpus loading/cleaning, shared with ai_style_diag/biber_diag

HAN = re.compile(r"[一-鿿]+")
MIN_DF = {"en": 0.05, "zh": 0.20}


def en_grams(text):
    toks = re.findall(r"[a-z][a-z'-]*", text.lower())
    c = Counter()
    for n in (3, 4):
        for i in range(len(toks) - n + 1):
            c[" ".join(toks[i:i + n])] += 1
    return c, len(toks)


def zh_grams(text):
    c, total = Counter(), 0
    for run in HAN.findall(text):
        total += len(run)
        for n in (3, 4):
            for i in range(len(run) - n + 1):
                c[run[i:i + n]] += 1
    return c, total


def corpus_texts(lang, corpus_dir: pathlib.Path, venues=None):
    if lang == "en":
        kept, _ = A.load_corpus(corpus_dir, venues)
        return [A.clean(raw) for _, raw in kept]
    from md_prose import strip_markup
    return [strip_markup(f.read_text(encoding="utf-8", errors="ignore"))
            for f in sorted(corpus_dir.glob("*.txt")) if f.exists()]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target")
    ap.add_argument("--lang", choices=["en", "zh"], help="default: auto-detect from Han-character density")
    ap.add_argument("--corpus", required=True,
                    help="baseline corpus dir — English: <corpus>/<venue>/*.txt "
                         "(same as ai_style_diag.py); Chinese: a flat folder of .txt")
    ap.add_argument("--venues", default="",
                    help="English only: comma-separated venue subdirs (default: all)")
    ap.add_argument("--top", type=int, default=20)
    args = ap.parse_args()
    p = pathlib.Path(args.target).expanduser()
    if not p.exists():
        sys.exit(f"Not found: {p}")
    corpus_dir = pathlib.Path(args.corpus).expanduser()
    if not corpus_dir.is_dir():
        sys.exit(f"Corpus dir not found: {corpus_dir}")

    raw = A.extract_text(p)
    lang = args.lang or ("zh" if len(HAN.findall(raw)) > len(raw) * 0.02 else "en")
    if lang == "zh":
        from md_prose import strip_markup
        text = strip_markup(raw, tex=p.suffix.lower() == ".tex")
    else:
        text = A.clean(raw)
    gram = en_grams if lang == "en" else zh_grams
    tc, tn = gram(text)
    venues = [v.strip() for v in args.venues.split(",") if v.strip()] or None
    docs = corpus_texts(lang, corpus_dir, venues if lang == "en" else None)
    if len(docs) < 30:
        sys.exit(f"Baseline only {len(docs)} papers — need ≥30. "
                 "Add more published full texts to the corpus.")
    hc, hdf, hn = Counter(), Counter(), 0
    for d in docs:
        c, n = gram(d)
        hc.update(c)
        hdf.update(c.keys())
        hn += n
    unit = 10000
    rows = []
    for g, k in tc.items():
        if k < 3 or hdf[g] < MIN_DF[lang] * len(docs):
            continue
        tr = k / tn * unit
        hr = (hc[g] + 0.5) / hn * unit
        ratio = tr / hr
        if ratio >= 3:
            rows.append((ratio, g, k, tr, hr, hdf[g] / len(docs)))
    rows.sort(reverse=True)
    # Drop a shorter bundle that's wholly contained in a longer one with the same
    # count (Chinese 3-character strings are frequently a substring of a 4-character one).
    keep = []
    for r in rows:
        if any(r[1] in o[1] and r[2] == o[2] and r[1] != o[1] for o in rows):
            continue
        keep.append(r)
    unit_name = "10k words" if lang == "en" else "10k chars"
    print(f"Draft {tn} {'words' if lang == 'en' else 'Han chars'} | baseline {len(docs)} field "
          f"papers | thresholds: draft >=3x, baseline doc-frequency >={MIN_DF[lang]:.0%}, ratio >=3")
    if not keep:
        print("No noticeably overused general-academic bundles found.")
        return
    print(f"{'bundle':<28}{'count':>6}{'draft/' + unit_name:>17}{'baseline/' + unit_name:>19}"
          f"{'ratio':>7}{'baseline doc%':>14}")
    for ratio, g, k, tr, hr, df in keep[:args.top]:
        print(f"{g:<28}{k:>6}{tr:>17.2f}{hr:>19.2f}{ratio:>7.1f}{df * 100:>13.0f}%")
    print("\nReading: these are bundles real published papers also use, but your draft "
          "uses noticeably more of. Reword the repeats or cut some outright; do NOT "
          "swap in a different fixed sentence pattern — that just relocates the tic."
          + ("" if len(keep) <= args.top else f" ({len(keep) - args.top} more not shown)"))
    if lang == "zh":
        print("⚠️ Chinese 3–4 character bundles often reflect your TOPIC (a paper about "
              "users will legitimately repeat 使用者) — use this to find repeated PHRASING, "
              "not as an AI-style signal by itself. For the metadiscourse layer, see "
              "zh_ai_style.py's optional zh-metadiscourse-scale integration.")


if __name__ == "__main__":
    main()
