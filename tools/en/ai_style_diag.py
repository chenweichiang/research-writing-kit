#!/usr/bin/env python3
"""English AI style-fingerprint diagnostic — local, no upload (unpublished-draft rule).

Measures the AI syntax fingerprints reviewers actually notice — em-dash / semicolon
density, `rather than`, `not..but` antithesis, rule-of-three, sentence length and
burstiness — as PERCENTILES against a baseline corpus of published papers in your
field. Cloud detectors (GPTZero-style) upload your draft and false-positive on
academic prose; this is the local alternative.

⚠️ REQUIRES A BASELINE CORPUS you assemble yourself: a folder of .txt full texts of
   PUBLISHED papers in your target venues (needs ≥30 to compute percentiles).
   🔴 Corpus hygiene: put ONLY other people's published papers in it — never your own
   drafts/posters/co-authored work (comparing your style against a baseline that
   contains your own writing makes the diagnosis cancel itself out). Exclude any of
   your own files with --exclude.

Point at the corpus with --corpus <dir> or the CORPUS_DIR env var. Expected layout:
   <corpus>/<venue>/*.txt   (e.g. corpus/chi/*.txt, corpus/dis/*.txt)

Requires: Python 3 stdlib (+ `pdftotext` on PATH only if the target is a PDF).

Usage:
    python3 ai_style_diag.py <draft.pdf|.tex|.md|.txt> --corpus ~/my-corpus
    python3 ai_style_diag.py draft.md --corpus ~/my-corpus --venues chi,dis
    python3 ai_style_diag.py draft.md --corpus ~/my-corpus --exclude myname,myproject

Reading: percentile >90 = well above field norm = a source of "looks like AI".
Editing: keep em-dashes/semicolons doing conceptual work (antithesis / closing /
embedded questions); move pure asides to commas/parens; don't flatten sentence-length
variance — flattening rhythm reads MORE like AI.
"""
import argparse
import os
import pathlib
import re
import statistics
import sys

METRICS = [
    ("emdash", "em-dash /1k"), ("notbut", "not..but /1k"),
    ("neither", "neither..nor /1k"), ("rather", "rather than /1k"),
    ("triplet", "rule-of-three /1k"), ("semi", "semicolon /1k"),
    ("colon", "mid-sentence colon /1k"), ("slen", "mean sentence len (words)"),
    ("burst", "burstiness SD/mean"),
]


def extract_text(path: pathlib.Path) -> str:
    if path.suffix.lower() == ".pdf":
        import subprocess
        return subprocess.run(["pdftotext", str(path), "-"],
                              capture_output=True, text=True).stdout
    txt = path.read_text(errors="ignore")
    if path.suffix.lower() == ".tex":
        txt = re.sub(r"(?m)%.*$", "", txt)
        txt = re.sub(r"\\(cite[a-z]*|ref|label|includegraphics|input)\{[^}]*\}", "", txt)
        txt = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", txt)
        txt = txt.replace("{", " ").replace("}", " ")
    return txt


def clean(txt: str) -> str:
    lines = [l for l in txt.split("\n") if not re.fullmatch(r"\s*\d+\s*", l)]
    body = "\n".join(lines)
    m = re.search(r"\bREFERENCES\b|\bReferences\s*\n", body)
    if m and m.start() > len(body) * 0.5:
        body = body[:m.start()]
    return body


def profile(text: str, name: str, min_words: int = 800):
    words = re.findall(r"[A-Za-z][A-Za-z'-]*", text)
    n = len(words)
    if n < min_words:
        return None
    per1k = lambda c: c / n * 1000
    sents = [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z])", re.sub(r"\s+", " ", text))
             if len(s.split()) >= 3]
    slens = [len(s.split()) for s in sents]
    mean = statistics.mean(slens)
    return dict(
        name=name, words=n,
        emdash=per1k(text.count("—") + text.count("---")),
        notbut=per1k(len(re.findall(r"\bnot\b[^.;:?]{1,60}\bbut\b", text, re.I))),
        neither=per1k(len(re.findall(r"\bneither\b[^.;:?]{1,60}\bnor\b", text, re.I))),
        rather=per1k(len(re.findall(r"\brather than\b", text, re.I))),
        triplet=per1k(len(re.findall(r"\b\w+, \w+, and \w+\b", text))),
        semi=per1k(text.count(";")),
        colon=per1k(len(re.findall(r"[a-z]: [a-z]", text))),
        slen=mean, burst=statistics.stdev(slens) / mean if len(slens) > 1 else 0,
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", help="draft (.pdf/.tex/.md/.txt)")
    ap.add_argument("--corpus", default=os.environ.get("CORPUS_DIR"),
                    help="baseline corpus dir (or CORPUS_DIR env). Layout: <corpus>/<venue>/*.txt")
    ap.add_argument("--venues", default="",
                    help="comma-separated venue subdirs to use (default: all subdirs)")
    ap.add_argument("--exclude", default="",
                    help="comma-separated substrings; corpus files matching are skipped "
                         "(use to keep YOUR OWN writing out of the baseline)")
    args = ap.parse_args()

    if not args.corpus:
        sys.exit("No baseline corpus. Assemble a folder of published papers in your "
                 "field (see the header) and pass --corpus <dir> or set CORPUS_DIR.")
    corpus = pathlib.Path(args.corpus).expanduser()
    if not corpus.is_dir():
        sys.exit(f"Corpus dir not found: {corpus}")

    tpath = pathlib.Path(args.target).expanduser()
    if not tpath.exists():
        sys.exit(f"Not found: {tpath}")
    target = profile(clean(extract_text(tpath)), tpath.name)
    if not target:
        sys.exit("Draft under 800 words — statistics unstable.")

    excl = [e.strip().lower() for e in args.exclude.split(",") if e.strip()]
    venues = [v.strip() for v in args.venues.split(",") if v.strip()]
    vdirs = ([corpus / v for v in venues] if venues
             else [d for d in corpus.iterdir() if d.is_dir()])
    base = []
    for vdir in vdirs:
        if not vdir.is_dir():
            print(f"(skipping missing {vdir.name})", file=sys.stderr)
            continue
        for f in vdir.glob("*.txt"):
            if any(p in f.name.lower() for p in excl):
                continue
            s = profile(clean(f.read_text(errors="ignore")), f.name)
            if s:
                base.append(s)
    if len(base) < 30:
        sys.exit(f"Baseline only {len(base)} papers — need ≥30 for percentiles. "
                 "Add more published full texts to the corpus.")

    print(f"Draft {target['words']} words | baseline {len(base)} field papers")
    print(f"{'metric':<28}{'draft':>9}{'median':>10}{'pctile':>8}")
    for key, label in METRICS:
        vals = sorted(b[key] for b in base)
        rank = sum(1 for v in vals if v < target[key]) / len(vals) * 100
        med = vals[len(vals) // 2]
        flag = " <<" if rank > 90 or rank < 10 else ""
        print(f"{label:<28}{target[key]:>9.2f}{med:>10.2f}{rank:>7.0f}%{flag}")


if __name__ == "__main__":
    main()
