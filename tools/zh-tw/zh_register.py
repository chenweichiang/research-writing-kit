#!/usr/bin/env python3
"""zh_register.py: the register profile of a Chinese academic draft, i.e. where each of
52 features falls among published journal papers from the same field. Local, no upload.
This is not a detector.

Why this exists: native polish needs a yardstick. "Reads like a Taiwan scholar wrote it"
is defined here as "falls inside the distribution of real papers in the target field"
(register alignment, Demir & Egbert 2026, Applied Corpus Linguistics), not as a set of
prescriptive rules. A rule-based polish pass can fix hundreds of surface items and still
leave every register deviation where it was, and some popular rules push the draft the
wrong way: turning every 進行 into a bare verb, splitting long sentences, banning the
semicolon. Taiwan journal papers use all three as a matter of course, so a draft that has
none of them sits outside the field's range.

zh_ai_style.py measures AI syntax fingerprints (dashes, rule-of-three, contrast frames,
convergence words). This tool measures register: translationese, self-mention, linking,
metadiscourse, stance, punctuation and sentence length. Both share md_prose.strip_markup.
Which features may move in which direction (the policy) lives in
tools/register/register_profile.py, not here.

Baseline corpus (you assemble it; nothing ships with the kit):
  <corpus>/<venue>/*.txt   one plain-text file per published paper, grouped by journal
  <corpus>/*.txt           also read; their venue is "all" unless manifest.tsv says otherwise
  <corpus>/manifest.tsv    optional, tab-separated, header with `file` and `venue` (or
                           `journal`) columns; overrides the folder name
  Needs at least 30 usable papers (1000+ Han characters each after quotations are
  removed). A --venue subset is used only when it holds 30 or more papers; otherwise the
  whole corpus is used and the report says so.
  Corpus hygiene: only other people's published papers, never your own drafts. Prefer
  papers published before general-purpose AI writing tools were common, so the baseline
  is not already drifting toward machine prose. Files whose names look like drafts
  (草稿, draft, name_v0.1.txt) are skipped.
Text inside 「」『』《》〈〉 is removed before counting, in the corpus and in the draft
alike: quotations and example sentences are not the author's register.
Cache: <corpus>/.zh_register_baseline.json, rebuilt when the file list or features change.

Usage:
    python3 zh_register.py <draft.md|.txt|.tex|.docx|.pdf> --corpus <dir> [--venue JOURNAL] [--json]
    ZH_CORPUS_DIR=<dir> python3 zh_register.py <draft>
    python3 zh_register.py --corpus <dir> --rebuild      # after adding or removing papers
    python3 zh_register.py --selftest                     # builds a synthetic corpus in a temp dir
Standard library only.
"""
import argparse
import hashlib
import json
import os
import re
import statistics
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))
from md_prose import strip_markup  # noqa: E402

HAN = r"[一-鿿]"
QUOTES = r"「[^」]*」|『[^』]*』|《[^》]*》|〈[^〉]*〉"
CACHE_NAME = ".zh_register_baseline.json"
MIN_DOCS = 30
MIN_HAN = 1000
DRAFT_NAME = re.compile(r"草稿|draft|_v\d+\.\d+", re.I)

# (key, group, regex), counted per 1000 Han characters. Editing this list invalidates
# the cache automatically (the cache key hashes FEATURES).
FEATURES = [
    ("本研究", "self-mention", r"本研究"),
    ("本文", "self-mention", r"本文"),
    ("筆者", "self-mention", r"筆者"),
    ("我們", "self-mention", r"我們"),
    ("被", "translationese", r"被"),
    ("進行", "translationese", r"進行"),
    ("加以/予以", "translationese", r"加以|予以"),
    ("對於", "translationese", r"對於"),
    ("關於", "translationese", r"關於"),
    ("作為", "translationese", r"作為"),
    ("一個", "translationese", r"一個"),
    ("一種", "translationese", r"一種"),
    ("一項", "translationese", r"一項"),
    ("其 (pronoun)", "translationese", r"(?<![尤極與])其(?![他中實餘次])"),
    ("它/它們", "translationese", r"它"),
    ("的", "translationese", r"的"),
    ("之", "translationese", r"之"),
    ("具有", "translationese", r"具有"),
    ("針對", "translationese", r"針對"),
    ("而言", "translationese", r"而言"),
    ("透過/經由", "linking", r"透過|經由"),
    ("藉由/藉以", "linking", r"藉由|藉以"),
    ("因此", "linking", r"因此"),
    ("此外", "linking", r"此外"),
    ("然而", "linking", r"然而"),
    ("但 (not 不但)", "linking", r"(?<!不)但(?!願)"),
    ("而且", "linking", r"而且"),
    ("同時", "linking", r"同時"),
    ("以及", "linking", r"以及"),
    ("並 (not 並非)", "linking", r"並(?!非)(?=" + HAN + ")"),
    ("則", "linking", r"則"),
    ("例如", "metadiscourse", r"例如"),
    ("換言之/亦即/也就是說", "metadiscourse", r"換言之|亦即|也就是說"),
    ("首先", "metadiscourse", r"首先"),
    ("其次", "metadiscourse", r"其次"),
    ("綜上所述/總而言之", "metadiscourse", r"綜上所述|總而言之"),
    ("值得注意/由此可見", "metadiscourse", r"值得注意|由此可見"),
    ("研究顯示/研究指出", "metadiscourse", r"研究(?:顯示|指出)"),
    ("不僅", "metadiscourse", r"不僅"),
    ("脈絡下", "metadiscourse", r"脈絡下"),
    ("可能/或許", "stance", r"可能|或許"),
    ("顯示", "stance", r"顯示"),
    ("發現", "stance", r"發現"),
    ("認為", "stance", r"認為"),
    ("相當", "stance", r"相當"),
    ("semicolon", "punctuation", r"；"),
    ("colon", "punctuation", r"："),
    ("dash", "punctuation", "\u2014\u2014|\u2014"),
    ("contrast (並非/而非/而不是)", "punctuation", r"並非|而非|而不是"),
]
SENT_KEYS = [("mean sentence length", "sentence length"),
             ("median sentence length", "sentence length"),
             ("mean clause length", "sentence length")]
ALL_KEYS = [k for k, _, _ in FEATURES] + [k for k, _ in SENT_KEYS]
GROUP = {k: g for k, g, _ in FEATURES} | dict(SENT_KEYS)
RX = {k: re.compile(r) for k, _, r in FEATURES}
SKIP_LINE = ("|", "#", "!", "<!--", ":::")


def corpus_from_env(value=None):
    v = value or os.environ.get("ZH_CORPUS_DIR")
    return Path(v).expanduser() if v else None


def extract(path: Path) -> str:
    """.pdf / .docx go through zh_ai_style's converter; everything else through strip_markup."""
    suf = path.suffix.lower()
    if suf in (".pdf", ".docx"):
        import zh_ai_style
        return zh_ai_style.extract(path)
    return strip_markup(path.read_text(encoding="utf-8", errors="ignore"), tex=suf == ".tex")


def prose(text: str) -> str:
    return re.sub(QUOTES, "", text)


def measure(text: str):
    """{key: value}; None when there are fewer than 1000 Han characters (per-1000 rates
    are unstable on short text). `text` should already be stripped of layout syntax."""
    t = prose(text)
    n = len(re.findall(HAN, t))
    if n < MIN_HAN:
        return None
    k = n / 1000
    out = {key: round(len(rx.findall(t)) / k, 3) for key, rx in RX.items()}
    big = [len(re.findall(HAN, s)) for s in re.split(r"[。！？]", t)]
    big = [x for x in big if x >= 5]
    small = [len(re.findall(HAN, s)) for s in re.split(r"[，；：。！？]", t)]
    small = [x for x in small if x >= 2]
    out["mean sentence length"] = round(statistics.mean(big), 1) if big else 0.0
    out["median sentence length"] = float(statistics.median(big)) if big else 0.0
    out["mean clause length"] = round(statistics.mean(small), 1) if small else 0.0
    out["_han"] = n
    return out


def _manifest(corpus: Path):
    f = corpus / "manifest.tsv"
    if not f.exists():
        return {}
    rows = [l.rstrip("\n").split("\t") for l in f.read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.startswith("#")]
    if not rows:
        return {}
    head = rows[0]
    col = "venue" if "venue" in head else "journal"
    out = {}
    for r in rows[1:]:
        d = dict(zip(head, r))
        if d.get("file"):
            out[d["file"]] = d.get(col, "all")
    return out


def corpus_files(corpus: Path):
    """[(relative name, venue, path)] for <corpus>/*.txt and <corpus>/<venue>/*.txt."""
    if not corpus or not corpus.is_dir():
        return []
    man = _manifest(corpus)
    out = []
    for f in sorted(corpus.glob("*.txt")) + sorted(corpus.glob("*/*.txt")):
        if DRAFT_NAME.search(f.name):
            continue
        rel = f.relative_to(corpus).as_posix()
        venue = man.get(rel) or man.get(f.name) or (f.parent.name if f.parent != corpus else "all")
        out.append((rel, venue, f))
    return out


def baseline(corpus: Path, rebuild=False):
    """{_key, docs: [{file, venue, v: {key: value}}]}, or None when fewer than 30 usable papers."""
    files = corpus_files(corpus)
    if len(files) < MIN_DOCS:
        return None
    sig = json.dumps(FEATURES, ensure_ascii=False) + "|".join(k for k, _ in SENT_KEYS) + QUOTES
    key = hashlib.md5(("\n".join(f"{r}\t{v}" for r, v, _ in files) + sig).encode()).hexdigest()
    cache = corpus / CACHE_NAME
    if not rebuild and cache.exists():
        try:
            c = json.loads(cache.read_text(encoding="utf-8"))
            if c.get("_key") == key:
                return c
        except (OSError, ValueError):
            pass
    docs = []
    for rel, venue, f in files:
        v = measure(strip_markup(f.read_text(encoding="utf-8", errors="ignore")))
        if v:
            docs.append({"file": rel, "venue": venue, "v": v})
    if len(docs) < MIN_DOCS:
        return None
    out = {"_key": key, "docs": docs}
    try:
        cache.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass
    return out


def quantile(vals, q):
    """Nearest-rank quantile (vals already sorted)."""
    return vals[min(len(vals) - 1, max(0, round(q * (len(vals) - 1))))]


def pct(vals, x):
    """Mid-rank percentile (ties count half), so a feature that is 0 in many papers is
    not reported as the 0th percentile just because the draft is also 0."""
    below = sum(1 for v in vals if v < x)
    ties = sum(1 for v in vals if v == x)
    return (below + 0.5 * ties) / len(vals) * 100


def venues(corpus: Path):
    b = baseline(corpus)
    return sorted({d["venue"] for d in b["docs"]}) if b else []


def profile(text: str, corpus: Path, venue: str = None, min_docs: int = MIN_DOCS):
    """{n_docs, venue, han, feats: {key: {group, value, p10, p50, p90, pct, status}}};
    status = high (> p90) / low (< p10) / ok. None when the corpus or the draft is too small."""
    b = baseline(corpus)
    if not b:
        return None
    v = measure(text)
    if not v:
        return None
    docs, used = b["docs"], "all"
    if venue:
        sub = [d for d in docs if d["venue"] == venue]
        if len(sub) >= min_docs:
            docs, used = sub, venue
        else:
            used = f"all ({venue} has only {len(sub)} papers, fewer than {min_docs})"
    feats = {}
    for key in ALL_KEYS:
        vals = sorted(d["v"][key] for d in docs)
        p10, p50, p90 = quantile(vals, .1), quantile(vals, .5), quantile(vals, .9)
        x = v[key]
        status = "high" if x > p90 else ("low" if x < p10 else "ok")
        feats[key] = dict(group=GROUP[key], value=x, p10=p10, p50=p50, p90=p90,
                          pct=round(pct(vals, x), 1), status=status)
    return dict(n_docs=len(docs), venue=used, han=v["_han"], feats=feats)


def _plain(line: str) -> str:
    """For locating instances line by line: drop HTML comments, Markdown emphasis and link syntax."""
    line = re.sub(r"<!--.*?(-->|$)", "", line)
    line = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line)
    return re.sub(r"[*_`]", "", line)


def _in(i, lines):
    return not lines or any(a <= i <= b for a, b in lines)


def locate(raw: str, key: str, lines=None, limit=8):
    """[(line number, context)] for one feature in the unstripped draft. Not for sentence
    length. `lines` = [(start, end)] restricts the search. Table, heading and comment lines
    are skipped."""
    if key not in RX:
        return []
    out = []
    for i, line in enumerate(raw.split("\n"), 1):
        if not _in(i, lines):
            continue
        s = line.lstrip()
        if not s or s.startswith(SKIP_LINE):
            continue
        line = _plain(line)
        body = re.sub(QUOTES, lambda m: "\u3000" * len(m.group(0)), line)
        for m in RX[key].finditer(body):
            out.append((i, line[max(0, m.start() - 14): m.end() + 14].strip()))
            if len(out) >= limit:
                return out
    return out


def long_sentences(raw: str, lines=None, top=5):
    """The longest sentences, for "sentence length high": [(line, Han chars, opening)]."""
    out = []
    for i, line in enumerate(raw.split("\n"), 1):
        if not _in(i, lines) or line.lstrip().startswith(SKIP_LINE):
            continue
        for s in re.split(r"(?<=[。！？])", prose(_plain(line))):
            n = len(re.findall(HAN, s))
            if n >= 5:
                out.append((i, n, s.strip()[:30]))
    return sorted(out, key=lambda x: -x[1])[:top]


def short_runs(raw: str, lines=None, top=5, max_len=35):
    """Adjacent pairs of short sentences, for "sentence length low" (merge candidates):
    [(line, combined Han chars, the two openings)]."""
    out = []
    for i, line in enumerate(raw.split("\n"), 1):
        if not _in(i, lines) or line.lstrip().startswith(SKIP_LINE):
            continue
        ss = [s for s in re.split(r"(?<=[。！？])", prose(_plain(line)))
              if len(re.findall(HAN, s)) >= 5]
        for a, b in zip(ss, ss[1:]):
            na, nb = len(re.findall(HAN, a)), len(re.findall(HAN, b))
            if na <= max_len and nb <= max_len:
                out.append((i, na + nb, a.strip()[:16] + " / " + b.strip()[:16]))
    return sorted(out, key=lambda x: x[1])[:top]


def report(p) -> str:
    L = [f"Draft {p['han']} Han chars | baseline = {p['venue']}, {p['n_docs']} papers | "
         "per 1000 Han chars | a descriptive comparison, not a detector",
         f"{'group':<16}{'feature':<26}{'draft':>8}{'p10':>8}{'median':>8}{'p90':>8}{'pctile':>8}"]
    prev = None
    for k, f in p["feats"].items():
        flag = {"high": "  \u25b2 high", "low": "  \u25bc low"}.get(f["status"], "")
        L.append(f"{f['group'] if f['group'] != prev else '':<16}{k:<26}{f['value']:>8.2f}"
                 f"{f['p10']:>8.2f}{f['p50']:>8.2f}{f['p90']:>8.2f}{f['pct']:>7.0f}%{flag}")
        prev = f["group"]
    n_out = sum(f["status"] != "ok" for f in p["feats"].values())
    L.append(f"\n{n_out} feature(s) outside the p10-p90 band. Any single paper sits outside on a "
             "few; what matters is whether the deviations point the same way (sentences short "
             "across the board, 本文 high while 本研究 is low). Which ones to fix, and in which "
             "direction, is decided by tools/register/register_profile.py.")
    return "\n".join(L)


# ---------- self-test ----------
_ZH_SENTS = [
    "本研究以半結構訪談蒐集十二位教師的課程經驗，並透過主題分析進行資料整理，以理解教師在設計課程時的考量",
    "研究結果顯示，教師在規劃課程時同時考量學生的先備知識、學校的設備條件以及課程時數的限制",
    "此外，受訪教師認為跨領域合作具有相當的價值，但也指出行政支援不足時合作難以持續",
    "針對上述發現，本研究進一步比較不同年資教師的回應，發現資深教師較重視課程的整體連貫",
    "因此，研究者建議學校在推動課程改革時，應同時提供教師共同備課的時間與空間",
    "教師的回饋也可能受到學校文化與同儕關係的影響，因此詮釋時需保留脈絡差異",
]


def synthetic_corpus(root: Path, n=MIN_DOCS, venue="JX", seed=7):
    """A throwaway corpus for tests: n papers of about 1500 Han characters in <root>/<venue>/."""
    import random
    d = root / venue
    d.mkdir(parents=True, exist_ok=True)
    for i in range(n):
        rnd = random.Random(seed + i)
        body = "。".join(rnd.choice(_ZH_SENTS) for _ in range(40)) + "。"
        (d / f"paper{i:02d}.txt").write_text(body, encoding="utf-8")
    return root


def selftest() -> int:
    good = True

    def t(name, cond):
        nonlocal good
        good &= bool(cond)
        print(("PASS " if cond else "FAIL ") + name)

    v = measure("本研究透過訪談進行分析，並非抽樣。" * 80)
    t("並非 is not counted as 並", v["並 (not 並非)"] == 0 and v["contrast (並非/而非/而不是)"] > 0)
    t("text inside 「」 is not counted", measure("本研究「本文進行被」分析資料並整理。" * 100)["本文"] == 0)
    t("fewer than 1000 Han chars returns None", measure("本研究很短。") is None)
    t("其他 / 尤其 are not the pronoun 其",
      measure("其他資料與尤其重要的部分，其結果一致。" * 80)["其 (pronoun)"] > 0
      and measure("其他資料與尤其重要的部分。" * 100)["其 (pronoun)"] == 0)
    t("不但 is not counted as 但", measure("不但如此，資料也完整。" * 120)["但 (not 不但)"] == 0)
    t("ties count half in the percentile", pct([0, 0, 0, 1], 0) == 37.5)
    raw = "# 標題本文\n\n本文分析資料。\n| 本文 | 表 |\n"
    t("locate skips headings and tables", [n for n, _ in locate(raw, "本文")] == [3])
    with tempfile.TemporaryDirectory() as tmp:
        c = synthetic_corpus(Path(tmp))
        b = baseline(c)
        t("synthetic 30-paper corpus builds a baseline", b and len(b["docs"]) == MIN_DOCS)
        draft = ("本文以問卷蒐集資料。本文分析結果。本文討論意義。" * 60)
        p = profile(draft, c, venue="JX")
        t("venue subset used when it has 30 papers", p and p["venue"] == "JX")
        t("本文 flagged high against a corpus that never uses it", p and p["feats"]["本文"]["status"] == "high")
        t("unknown venue falls back to the whole corpus", "fewer than" in profile(draft, c, "NOPE")["venue"])
        small = Path(tmp) / "small"
        synthetic_corpus(small, n=5)
        t("a 5-paper corpus gives no baseline", baseline(small) is None)
    print("\nselftest: all passed" if good else "\nselftest: FAILED")
    return 0 if good else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", nargs="?", help="draft (.md/.txt/.tex/.docx/.pdf)")
    ap.add_argument("--corpus", help="baseline corpus dir (default: $ZH_CORPUS_DIR)")
    ap.add_argument("--venue", help="compare against this venue's papers only (a folder name "
                                    "or manifest value; falls back to the whole corpus under 30 papers)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--rebuild", action="store_true", help="recompute the baseline cache")
    ap.add_argument("--selftest", action="store_true", help="run the built-in checks (no corpus needed)")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    corpus = corpus_from_env(a.corpus)
    if not corpus:
        ap.error("needs a baseline corpus: --corpus <dir> or ZH_CORPUS_DIR (see the header)")
    if not corpus.is_dir():
        sys.exit(f"Corpus dir not found: {corpus}")
    if a.rebuild:
        b = baseline(corpus, rebuild=True)
        print(f"Baseline rebuilt: {len(b['docs'])} papers, venues {venues(corpus)}" if b
              else f"Fewer than {MIN_DOCS} usable papers in {corpus}")
        if not a.target:
            return 0
    if not a.target:
        ap.error("needs a draft path (or --selftest / --rebuild)")
    path = Path(a.target).expanduser()
    if not path.exists():
        sys.exit(f"Not found: {path}")
    p = profile(extract(path), corpus, a.venue)
    if p is None:
        sys.exit(f"Cannot measure: fewer than {MIN_DOCS} usable papers in the corpus, "
                 f"or the draft has under {MIN_HAN} Han characters")
    print(json.dumps(p, ensure_ascii=False, indent=1) if a.json else report(p))
    return 0


if __name__ == "__main__":
    sys.exit(main())
