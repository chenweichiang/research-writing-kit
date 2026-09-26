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
`~/.cache/metadiscourse_en_kit_baseline.json`, keyed by the corpus file list; values are
stored per paper so `--groups` can pick a subset without recomputing.

Reading by direction: a deviation can go either way, and the fixes are opposite. A marker
above the baseline p90 is reduced, one below p10 is restored toward the field's usual
amount, and one inside the band is left alone. Point the baseline at the target venue
with `--groups` (venue folder names): the same draft can sit below p10 against a mixed
corpus and well inside the band against its own field. Stance markers (hedges, boosters,
attitude) carry claim strength, so the author decides those; guiding markers
(transitions, code glosses) are what a native-polish pass may add or trim
(`tools/register/register_profile.py` applies that policy).

Usage:
    python3 metadiscourse_en.py <draft> --corpus ~/my-corpus [--matches]
    python3 metadiscourse_en.py <draft> --corpus ~/my-corpus --groups <venue>[,<venue>] [--json]
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


class BaselineError(Exception):
    """The corpus cannot give a baseline (missing, or fewer than 30 usable papers)."""


def _venue_texts(corpus_dir: pathlib.Path, venues=None):
    """[("venue/file", raw)] so every paper keeps its venue for --groups."""
    names = venues or sorted(d.name for d in corpus_dir.iterdir() if d.is_dir())
    out = []
    for v in names:
        kept, _ = A.load_corpus(corpus_dir, [v])
        out += [(f"{v}/{n}", raw) for n, raw in kept]
    return out


def baseline(corpus_dir: pathlib.Path, venues=None, rebuild=False):
    """{_key, docs: [{name: "venue/file", v: {marker: per 1000 words}}]}."""
    kept = _venue_texts(corpus_dir, venues)
    if len(kept) < 30:
        raise BaselineError(f"Baseline only {len(kept)} papers, need ≥30 for percentiles.")
    key = hashlib.md5(("\n".join(sorted(n for n, _ in kept))
                       + json.dumps(list(MARKERS.values()))).encode()).hexdigest()
    if not rebuild and CACHE.exists():
        try:
            c = json.loads(CACHE.read_text())
            if c.get("_key") == key and "docs" in c:
                return c
        except Exception:
            pass
    docs = []
    for name, raw in kept:
        n, c = count(A.clean(raw))
        if n < 800:
            continue
        docs.append({"name": name, "v": {k: round(v / n * 1000, 3) for k, v in c.items()}})
    if len(docs) < 30:
        raise BaselineError(f"Only {len(docs)} baseline papers had ≥800 words after cleaning, need ≥30.")
    out = {"_key": key, "docs": docs}
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(out))
    return out


def quantile(vals, q):
    """Nearest-rank quantile (vals already sorted)."""
    return vals[min(len(vals) - 1, max(0, round(q * (len(vals) - 1))))]


def profile(text, corpus_dir: pathlib.Path, groups=None, venues=None, min_docs=30):
    """{n_words, n_docs, groups, feats: {marker: {cat, count, value, p10, p50, p90, pct, status}}}.
    `text` should already be A.clean()ed. A `groups` subset with fewer than min_docs papers
    falls back to the whole baseline, and `groups` says so. None when the draft is under 800 words."""
    b = baseline(corpus_dir, venues)
    n, c = count(text)
    if n < 800:
        return None
    docs, used = b["docs"], "all"
    if groups:
        sub = [d for d in docs if d["name"].split("/")[0] in groups]
        if len(sub) >= min_docs:
            docs, used = sub, ",".join(groups)
        else:
            used = f"all ({','.join(groups)} has only {len(sub)} papers, fewer than {min_docs})"
    feats = {}
    for (cat, name) in MARKERS:
        vals = sorted(d["v"][name] for d in docs)
        v = c[name] / n * 1000
        p10, p50, p90 = quantile(vals, .1), quantile(vals, .5), quantile(vals, .9)
        feats[name] = dict(cat=cat, count=c[name], value=round(v, 3), p10=p10, p50=p50, p90=p90,
                           pct=round(pct(vals, v), 1),
                           status="high" if v > p90 else ("low" if v < p10 else "ok"))
    return dict(n_words=n, n_docs=len(docs), groups=used, feats=feats)


def pct(vals, x):
    below = sum(1 for v in vals if v < x)
    ties = sum(1 for v in vals if v == x)
    return (below + 0.5 * ties) / len(vals) * 100


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target")
    ap.add_argument("--corpus", required=True,
                    help="baseline corpus dir, same layout as ai_style_diag.py's --corpus")
    ap.add_argument("--venues", default="",
                    help="comma-separated venue subdirs to load at all (default: all); the "
                         "baseline is built from these only and needs ≥30 papers")
    ap.add_argument("--groups", default="",
                    help="comma-separated venue subdirs to compare against; the baseline stays "
                         "the whole corpus and falls back to it when the subset has <30 papers")
    ap.add_argument("--matches", action="store_true",
                    help="list the first 8 actual matches (with context) per marker")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--rebuild", action="store_true")
    args = ap.parse_args()
    corpus_dir = pathlib.Path(args.corpus).expanduser()
    if not corpus_dir.is_dir():
        sys.exit(f"Corpus dir not found: {corpus_dir}")
    venues = [v.strip() for v in args.venues.split(",") if v.strip()] or None
    groups = [g.strip() for g in args.groups.split(",") if g.strip()] or None
    p = pathlib.Path(args.target).expanduser()
    if not p.exists():
        sys.exit(f"Not found: {p}")
    try:
        if args.rebuild:
            baseline(corpus_dir, venues, True)
        text = A.clean(A.extract_text(p))
        prof = profile(text, corpus_dir, groups, venues)
    except BaselineError as e:
        sys.exit(str(e))
    if prof is None:
        sys.exit("Draft under 800 words, statistics unstable.")
    if args.json:
        print(json.dumps(prof, ensure_ascii=False, indent=1))
        return
    print(f"Draft {prof['n_words']} words | baseline {prof['n_docs']} field papers "
          f"({prof['groups']}) | per 1000 words | this is a descriptive comparison, not a detector")
    print(f"{'cat':<11}{'marker':<26}{'count':>5}{'draft':>8}{'p10':>7}{'median':>8}{'p90':>7}{'pctile':>8}")
    cat_prev = None
    for name, f in prof["feats"].items():
        flag = ""
        if f["count"] >= 3 or name in WATCH_LOW:
            if f["status"] == "high":
                flag = " \u25b2 high" + (" (LLM-typical direction)" if name in WATCH_HIGH else "")
            elif f["status"] == "low":
                flag = " \u25bc low" + (" (LLM-typical direction)" if name in WATCH_LOW else "")
        cat = f["cat"]
        print(f"{cat if cat != cat_prev else '':<11}{name:<26}{f['count']:>5}{f['value']:>8.2f}"
              f"{f['p10']:>7.2f}{f['p50']:>8.2f}{f['p90']:>7.2f}{f['pct']:>7.0f}%{flag}")
        cat_prev = cat
    if args.matches:
        for (cat, name), rx in MARKERS.items():
            flags = 0 if (cat, name) in CASE_SENSITIVE else re.I
            ms = list(re.finditer(rx, text, flags))[:8]
            if ms:
                print(f"\n[{name}]")
                for m in ms:
                    print("   …" + re.sub(r"\s+", " ", text[max(0, m.start() - 50):m.end() + 50]) + "…")
    print("\nReading (by direction): reduce a marker flagged high, restore one flagged low toward "
          "the field's usual amount, and leave in-band markers alone. The research above reports "
          "LLM writing running high on explicit stance (boosters, attitude markers) and low on "
          "reader engagement; another common pattern is too few hedges, code glosses and "
          "evidentials, which makes claims read more certain than the evidence and leaves the "
          "reader to supply the links between sentences. Compare against the target venue "
          "(--groups): against a mixed corpus a draft can look far off on markers that are "
          "normal for its own field. Stance markers (hedges, boosters, attitude) set claim "
          "strength, so the author decides them; guiding markers (transitions, code glosses) "
          "can be adjusted in a polish pass. Read the sentences with --matches before editing. "
          "Self-mention runs low in an anonymized submission; that is expected, not a signal.")


if __name__ == "__main__":
    main()
