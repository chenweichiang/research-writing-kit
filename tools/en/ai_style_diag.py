#!/usr/bin/env python3
"""English AI style-fingerprint diagnostic — local, no upload (unpublished-draft rule).

Measures the AI syntax fingerprints reviewers actually notice — em-dash / semicolon
density, contrast sentences (`rather than`, `instead of`, `not..but`, "X, not Y",
`not only`, measured as **five shapes plus a de-duplicated TOTAL** — see below),
rule-of-three, sentence length, burstiness, LLM convergence-word density (word list
`en_slop_terms.tsv` beside this file), and stock generative-AI openers at the start of
the paper/Introduction — as PERCENTILES against a baseline corpus of published papers
in your field. Cloud detectors (GPTZero-style) upload your draft and false-positive on
academic prose; this is the local alternative.

⚠️ REQUIRES A BASELINE CORPUS you assemble yourself: a folder of .txt full texts of
   PUBLISHED papers in your target venues (needs ≥30 to compute percentiles).
   🔴 Corpus hygiene: put ONLY other people's published papers in it — never your own
   drafts/posters/co-authored work (comparing your style against a baseline that
   contains your own writing makes the diagnosis cancel itself out). Exclude any of
   your own files with --exclude.
   🔴 Corpus vintage: prefer papers published **before 2023** if you can find enough of
   them — anything published after generative AI became common may itself have been
   AI-polished, which would quietly raise your "normal" and hide the very drift you're
   trying to catch. If you don't have 30 pre-2023 papers in your venues, a mixed-vintage
   corpus is better than none, but treat the percentiles as a looser signal.

Point at the corpus with --corpus <dir> or the CORPUS_DIR env var. Expected layout:
   <corpus>/<venue>/*.txt   (e.g. corpus/chi/*.txt, corpus/dis/*.txt)

Requires: Python 3 stdlib (+ `pdftotext` on PATH for PDF input; `textutil` (macOS,
built in) or `pandoc` for `.docx` input — many venues only keep a .docx submission
version). Lite fallback with none of those installed: convert the file to plain text
yourself (Word/Google Docs/LibreOffice "Save As" / "Download" → .txt) and point this
script at the .txt instead.

Usage:
    python3 ai_style_diag.py <draft.pdf|.tex|.md|.txt|.docx> --corpus ~/my-corpus
    python3 ai_style_diag.py draft.md --corpus ~/my-corpus --venues chi,dis
    python3 ai_style_diag.py draft.md --corpus ~/my-corpus --exclude myname,myproject
    python3 ai_style_diag.py draft.md --corpus ~/my-corpus --gate   # exit 2 if contrast total > baseline p90
    python3 ai_style_diag.py --selftest                              # verify the measurement rules; no corpus needed

Reading: percentile >90 = well above field norm = a source of "looks like AI". The
"x median" column is how many times your draft's rate is the field's typical rate —
useful for a tic that's rare in the field (median near 0), where a percentile alone
can undersell how far out your draft sits.

🔴 **Contrast sentences: judge the TOTAL, never a single shape.** A pattern seen across
several drafts, generalized here: an editing pass swapped `rather than` for a mix of
"X, not Y" and `instead of` — but nothing was counting "X, not Y" at the time, so the
edit looked clean. The **total** contrast-sentence density never moved, and reviewers
still flagged the sentence type. Cut the non-load-bearing ones to a plain, direct
statement (say the side that matters; if the contrast is genuinely load-bearing, give
it its own sentence). **Do not swap one contrast shape for another** — a reviewer
notices the total, not which of the five forms carries it.

Editing: keep em-dashes/semicolons doing conceptual work (antithesis / closing /
embedded questions); move pure asides to commas/parens; stock openers ("In the era
of…", "…faces a paradigm shift") are close to absent at the start of published human
papers in most fields — start from the problem instead. Don't flatten sentence-length
variance — flattening rhythm reads MORE like AI.
"""
import argparse
import os
import pathlib
import re
import statistics
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "common"))
from md_prose import strip_markup   # same stripping rules for every diagnostic

# Only sentence-length burstiness is bad when LOW (low variance = monotone = AI-ish).
# Every other metric is a tic density where low is simply good.
LOW_IS_BAD = {"burst"}

# ── Baseline-contamination guard (two tracks: filename + content) ──────────────
# Measured case: a 164-file baseline turned out to hold 92 of the author's own
# drafts (89 of them versions of ONE paper). Contamination 56% → the author's own
# syntax became "the norm" and three metrics that should have read >90th
# percentile came back at 40/64/68. Why the old guard missed it: `--exclude`
# matches the FILENAME only, and the drafts were named `20260104_v0.0.48.txt`;
# they were also anonymised submission versions, so the author's name never
# appeared in the text either. Hence two tracks, and err on the side of dropping
# a file — a baseline short by a few papers is harmless, a contaminated one is not.
DRAFT_FILENAME_RE = re.compile(r"_v\d+\.\d+")     # versioned draft: name_v0.0.48.txt
DRAFT_CONTENT_MARKERS = (                            # checked in the first 3000 chars
    "ANONYMOUS AUTHOR",                 # double-blind submission version
    "Affiliations withheld",
    "Your Art Paper Title Here",        # venue template placeholder
    "LATEX Class for the Association",  # acmart class documentation, not a paper
    "The Name of the Title Is Hope",    # acmart sample-* demo files
    "Instructions for Using Springer",  # Springer llncs usage instructions
)


def is_draft_or_template(f: pathlib.Path, text: str, excl):
    """Return (drop?, reason) for a baseline file. `excl` = user --exclude substrings."""
    if any(p in f.name.lower() for p in excl):
        return True, "--exclude"
    if DRAFT_FILENAME_RE.search(f.stem):
        return True, "versioned draft filename"
    head = text[:3000].lower()
    for mk in DRAFT_CONTENT_MARKERS:
        if mk.lower() in head:
            return True, f"content marker '{mk}'"
    return False, ""

METRICS = [
    ("emdash", "em-dash /1k"),
    ("notbut", "not..but /1k"),
    ("commanot", "X, not Y /1k"),
    ("rather", "rather than /1k"),
    ("instead", "instead of /1k"),
    ("notonly", "not only (no but) /1k"),
    ("contrast", "TOTAL contrast /1k"),
    ("neither", "neither..nor /1k"),
    ("triplet", "rule-of-three /1k"),
    ("semi", "semicolon /1k"),
    ("colon", "mid-sentence colon /1k"),
    ("slen", "mean sentence len (words)"),
    ("burst", "burstiness SD/mean"),
    ("slop", "LLM convergence words /1k"),
]

# ── LLM convergence words ("slop") ────────────────────────────────────────────
# The list is `en_slop_terms.tsv` next to this file: terms LLM essays use far more
# than published HCI papers do (derived from sam-paech/slop-forensics, MIT; see the
# TSV header). Words HCI papers use anyway — notably, landscape — were dropped, so a
# hit is a word your field would not naturally write. As with every other metric, the
# number is a percentile against YOUR corpus; the top hits are printed so you can see
# which words carry it. If your field's vocabulary overlaps the list, rebuild it.
SLOP_TSV = pathlib.Path(__file__).resolve().parent / "en_slop_terms.tsv"


def _load_slop():
    words, phrases = set(), []
    if SLOP_TSV.exists():
        for line in SLOP_TSV.read_text(encoding="utf-8").splitlines():
            if not line or line.startswith("#") or line.startswith("term\t"):
                continue
            term, kind = line.split("\t")[:2]
            (words.add(term) if kind == "word" else phrases.append(term))
    return words, phrases


SLOP_WORDS, SLOP_PHRASES = _load_slop()


def slop_hits(text: str) -> Counter:
    toks = re.findall(r"[a-z][a-z'-]*", text.lower())
    c = Counter(t for t in toks if t in SLOP_WORDS)
    joined = " " + " ".join(toks) + " "
    for ph in SLOP_PHRASES:
        n = joined.count(" " + ph + " ")
        if n:
            c[ph] = n
    return c


# ── Contrast sentences (five shapes, de-duplicated total) ──────────────────────
# Each shape is counted separately, then the total is de-duplicated by the position
# of the "not" token — "Code, not a tool, but a medium." would otherwise trip both
# the not..but and the X-not-Y regex on the same word. "not only/merely/just/simply"
# followed later by "but" is a single not-only-but frame, not two hits; "not"
# followed by only/merely/yet/all/surprisingly/etc. is ordinary negation, excluded.
RE_NOTBUT = re.compile(r"\bnot\b[^.;:?]{1,60}\bbut\b", re.I)
RE_COMMANOT = re.compile(
    r",\s+(not)\s+(?!only\b|merely\b|just\b|simply\b|necessarily\b|least\b|yet\b|"
    r"all\b|always\b|surprisingly\b|significantly\b|to mention\b)\w", re.I)
RE_NOTONLY = re.compile(r"\bnot (?:only|merely|just|simply)\b(?![^.;:?]{0,60}\bbut\b)", re.I)
RE_RATHER = re.compile(r"\brather than\b", re.I)
RE_INSTEAD = re.compile(r"\binstead of\b", re.I)


def contrast_counts(text: str) -> dict:
    """Count each contrast shape, and a de-duplicated TOTAL. See module docstring:
    the total, not any single shape, is what a reviewer notices."""
    nb = [m.start() for m in RE_NOTBUT.finditer(text)]
    cn = [m.start(1) for m in RE_COMMANOT.finditer(text)]
    no = [m.start() for m in RE_NOTONLY.finditer(text)]
    ra = len(RE_RATHER.findall(text))
    ins = len(RE_INSTEAD.findall(text))
    total = len(set(nb) | set(cn) | set(no)) + ra + ins
    return dict(notbut=len(nb), commanot=len(cn), notonly=len(no),
                rather=ra, instead=ins, contrast=total)


# ── Stock generative-AI openers ─────────────────────────────────────────────────
# Only checked in the first ~400 words of the paper and the first ~150 words after an
# "Introduction" heading — these phrases are near-absent at the *start* of published
# human papers in most fields, but some (e.g. "increasingly", "landscape of") are
# common enough mid-paper that flagging them everywhere would be noise, not signal.
STOCK_OPENERS = (
    "in the era of", "in an era of", "in the age of", "in today's", "paradigm shift",
    "rapidly evolving", "ever-evolving", "has emerged as", "have emerged as",
    "the advent of", "with the rise of", "plays a crucial role", "plays a pivotal role",
    "as ai continues", "in an increasingly", "revolutioniz",
)


def opener_hits(text: str) -> list:
    low = re.sub(r"\s+", " ", text.lower())
    words = low.split(" ")
    zones = [("start of paper", " ".join(words[:400]))]
    m = re.search(r"\bintroduction\b", low)
    if m:
        zones.append(("start of Introduction", " ".join(low[m.end():].split(" ")[:150])))
    hits = []
    for zone, seg in zones:
        for p in STOCK_OPENERS:
            i = seg.find(p)
            if i >= 0:
                hits.append((zone, p, seg[max(0, i - 40):i + len(p) + 40]))
    return hits


def extract_text(path: pathlib.Path) -> str:
    if path.suffix.lower() == ".pdf":
        import subprocess
        return subprocess.run(["pdftotext", str(path), "-"],
                              capture_output=True, text=True).stdout
    if path.suffix.lower() == ".docx":
        # Many venues only keep a .docx submission version. macOS ships `textutil`;
        # elsewhere, install `pandoc`. Neither on PATH → tell the person the manual
        # fallback rather than failing silently.
        import subprocess
        for cmd in (["textutil", "-convert", "txt", "-stdout", str(path)],
                    ["pandoc", "-t", "plain", "--wrap=none", str(path)]):
            try:
                out = subprocess.run(cmd, capture_output=True, text=True)
            except FileNotFoundError:
                continue
            if out.returncode == 0 and out.stdout.strip():
                return out.stdout
        sys.exit(f"Can't read .docx — needs `textutil` (built into macOS) or `pandoc` "
                 f"on PATH: {path}\n"
                 "Lite fallback: open the file in Word / Google Docs / LibreOffice, "
                 "'Save As' or 'Download' as plain text (.txt), and point this script "
                 "at that .txt file instead.")
    txt = path.read_text(errors="ignore")
    if path.suffix.lower() == ".tex":
        txt = re.sub(r"(?m)%.*$", "", txt)
        txt = re.sub(r"\\(cite[a-z]*|ref|label|includegraphics|input)\{[^}]*\}", "", txt)
        txt = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", txt)
        txt = txt.replace("{", " ").replace("}", " ")
    return txt


def clean(txt: str) -> str:
    """Strip everything that is not prose, then drop review line numbers and
    anything after References.

    🔴 The stripping rules live in `../common/md_prose.py` — layout syntax
    (frontmatter, table separators, HTML comments, citation keys) otherwise gets
    counted as punctuation and inflates every number. See that module for the
    measured damage."""
    txt = strip_markup(txt)
    lines = [l for l in txt.split("\n") if not re.fullmatch(r"\s*\d+\s*", l)]
    body = "\n".join(lines)
    m = re.search(r"\bREFERENCES\b|\bReferences\s*\n", body)
    if m and m.start() > len(body) * 0.5:
        body = body[:m.start()]
    return body


def load_corpus(corpus: pathlib.Path, venues=None, exclude=()):
    """Load raw texts from a --corpus dir, applying the own-draft/template guard
    above. `venues=None` means every immediate subdirectory. Returns
    (kept, excluded): kept = [(filename, raw_text), …], excluded = [(filename, reason), …].

    Shared with `biber_diag.py`, `bundle_diag.py` and `metadiscourse_en.py` — same
    corpus, same exclusion rules, one place to fix them."""
    excl = [e.strip().lower() for e in exclude] if exclude else []
    vdirs = ([corpus / v for v in venues] if venues
             else [d for d in corpus.iterdir() if d.is_dir()])
    kept, excluded = [], []
    for vdir in vdirs:
        if not vdir.is_dir():
            print(f"(skipping missing {vdir.name})", file=sys.stderr)
            continue
        for f in vdir.glob("*.txt"):
            raw = f.read_text(errors="ignore")
            drop, why = is_draft_or_template(f, raw, excl)
            if drop:
                excluded.append((f.name, why))
            else:
                kept.append((f.name, raw))
    return kept, excluded


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
        # `---` counts only as a WORD-INTERNAL dash (word---word), which is how an
        # ASCII em-dash is written. Decorative `---` is already stripped in clean();
        # this is the second line of defence.
        emdash=per1k(text.count("—") + len(re.findall(r"(?<=\w)---(?=\w)", text))),
        **{k: per1k(v) for k, v in contrast_counts(text).items()},
        neither=per1k(len(re.findall(r"\bneither\b[^.;:?]{1,60}\bnor\b", text, re.I))),
        triplet=per1k(len(re.findall(r"\b\w+, \w+, and \w+\b", text))),
        semi=per1k(text.count(";")),
        colon=per1k(len(re.findall(r"[a-z]: [a-z]", text))),
        slen=mean, burst=statistics.stdev(slens) / mean if len(slens) > 1 else 0,
        slop=per1k(sum(slop_hits(text).values())),
    )


def selftest() -> int:
    """Positive/negative fixtures for the contrast-shape regexes and the opener
    detector. Touches no corpus — run this after editing any regex above."""
    cases = [
        ("It positions code not as a tool but as a medium.", 1, "not X but Y"),
        ("The model becomes an object, not an oracle.", 1, "X, not Y"),
        ("Code, not a tool, but a medium.", 1, "comma not..but counts once"),
        ("We use classes rather than prompts.", 1, "rather than"),
        ("We program it instead of prompting it.", 1, "instead of"),
        ("This is not only a tool.", 1, "not only (no but)"),
        ("This is not only a tool but also a medium.", 1, "not only...but counts once"),
        ("The effect was, not surprisingly, small.", 0, "'not surprisingly' isn't contrast"),
        ("Results were not significant.", 0, "plain negation"),
        ("Some items, not yet coded, were dropped.", 0, "'not yet' isn't contrast"),
        ("Neither A nor B held.", 0, "neither..nor is counted separately"),
    ]
    bad = 0
    for text, want, why in cases:
        got = contrast_counts(text)["contrast"]
        ok = got == want
        bad += not ok
        print(f"{'PASS' if ok else 'FAIL'} {why:<36} want {want} got {got}")
    hits = opener_hits("In the era of generative AI, the field faces a paradigm shift. "
                       + "word " * 50)
    ok = {h[1] for h in hits} == {"in the era of", "paradigm shift"}
    bad += not ok
    print(f"{'PASS' if ok else 'FAIL'} opener detection, got {sorted({h[1] for h in hits})}")
    late = opener_hits("word " * 600 + "in the era of generative AI")
    ok = not late
    bad += not ok
    print(f"{'PASS' if ok else 'FAIL'} openers past the opening zone are not flagged, got {len(late)}")
    print("all passed" if not bad else f"{bad} failure(s)")
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", nargs="?", help="draft (.pdf/.tex/.md/.txt/.docx)")
    ap.add_argument("--corpus", default=os.environ.get("CORPUS_DIR"),
                    help="baseline corpus dir (or CORPUS_DIR env). Layout: <corpus>/<venue>/*.txt")
    ap.add_argument("--venues", default="",
                    help="comma-separated venue subdirs to use (default: all subdirs)")
    ap.add_argument("--exclude", default="",
                    help="comma-separated substrings; corpus files matching are skipped "
                         "(use to keep YOUR OWN writing out of the baseline)")
    ap.add_argument("--gate", action="store_true",
                    help="exit 2 if total contrast-sentence density is above the "
                         "baseline p90 (for a pre-delivery check in a script or hook)")
    ap.add_argument("--show-contrast", action="store_true",
                    help="list every contrast sentence (default: first 8)")
    ap.add_argument("--selftest", action="store_true",
                    help="verify the measurement rules themselves; needs no corpus")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest())
    if not args.target:
        ap.error("draft path required (or use --selftest)")

    if not args.corpus:
        sys.exit("No baseline corpus. Assemble a folder of published papers in your "
                 "field (see the header) and pass --corpus <dir> or set CORPUS_DIR.")
    corpus = pathlib.Path(args.corpus).expanduser()
    if not corpus.is_dir():
        sys.exit(f"Corpus dir not found: {corpus}")

    tpath = pathlib.Path(args.target).expanduser()
    if not tpath.exists():
        sys.exit(f"Not found: {tpath}")
    body = clean(extract_text(tpath))
    target = profile(body, tpath.name)
    if not target:
        sys.exit("Draft under 800 words — statistics unstable.")

    excl = [e.strip() for e in args.exclude.split(",") if e.strip()]
    venues = [v.strip() for v in args.venues.split(",") if v.strip()] or None
    kept, excluded = load_corpus(corpus, venues, excl)
    base = [s for s in (profile(clean(raw), name) for name, raw in kept) if s]
    if len(base) < 30:
        sys.exit(f"Baseline only {len(base)} papers — need ≥30 for percentiles. "
                 "Add more published full texts to the corpus.")

    print(f"Draft {target['words']} words | baseline {len(base)} field papers")
    if excluded:
        reasons = ", ".join(f"{w} x{c}" for w, c in
                            Counter(w for _, w in excluded).most_common())
        print(f"  excluded {len(excluded)} ({reasons})")
    print(f"{'metric':<24}{'draft':>9}{'median':>10}{'x median':>10}{'pctile':>8}")
    p90 = {}
    for key, label in METRICS:
        if key == "slop" and not SLOP_WORDS:
            continue          # word list missing beside the script: metric silently off
        vals = sorted(b[key] for b in base)
        rank = sum(1 for v in vals if v < target[key]) / len(vals) * 100
        med = vals[len(vals) // 2]
        p90[key] = vals[int(len(vals) * 0.9)]
        ratio = f"{target[key] / med:>9.1f}x" if med > 0 else f"{'—':>10}"
        # 🔴 A low percentile only means something for burstiness. Flagging
        # "neither..nor appears 0 times, corpus median is also 0" is pure noise —
        # it teaches the reader to ignore the warnings.
        flag = " <<" if rank > 90 or (key in LOW_IS_BAD and rank < 10) else ""
        print(f"{label:<24}{target[key]:>9.2f}{med:>10.2f}{ratio}{rank:>7.0f}%{flag}")
    if SLOP_WORDS:
        top = slop_hits(body).most_common(15)
        print("convergence-word hits: "
              + (", ".join(f"{w}×{n}" for w, n in top) if top else "none"))

    # 🔴 Contrast: judge the TOTAL, and show the actual sentences — you can't edit
    # what you can't see, and the number alone invites swapping shapes instead of cutting.
    raw_c = contrast_counts(body)
    over = target["contrast"] > p90["contrast"]
    print(f"\nTotal contrast sentences: {raw_c['contrast']} = {target['contrast']:.2f}/1k words "
          f"(field p90 = {p90['contrast']:.2f}) -> "
          f"{'OVER FIELD NORM <<' if over else 'within field norm'}"
          f"  [not..but {raw_c['notbut']}, X-not-Y {raw_c['commanot']}, "
          f"rather than {raw_c['rather']}, instead of {raw_c['instead']}, "
          f"not only {raw_c['notonly']}]")
    if over:
        print("  Fix: cut the non-load-bearing ones to a plain statement. Do NOT swap to "
              "another contrast shape — the total is unchanged either way, and reviewers "
              "notice the total, not the label.")
    flat = re.sub(r"\s+", " ", body)
    sents = re.split(r"(?<=[.!?])\s+(?=[A-Z])", flat)
    csents = [x for x in sents if contrast_counts(x)["contrast"]]
    show = csents if args.show_contrast else csents[:8]
    for x in show:
        print(f"    · {x[:150]}{'…' if len(x) > 150 else ''}")
    if len(csents) > len(show):
        print(f"    …and {len(csents) - len(show)} more (--show-contrast to list all)")

    hits = opener_hits(body)
    if hits:
        print("\nStock generative-AI openers (near-absent at the start of published human "
              "papers in most fields; start from the problem instead):")
        for zone, phrase, ctx in hits:
            print(f"    · [{zone}] \"{phrase}\" …{ctx}…")
    else:
        print("\nStock openers: none")

    if args.gate and over:
        sys.exit(2)


if __name__ == "__main__":
    main()
