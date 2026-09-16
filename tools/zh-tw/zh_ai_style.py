#!/usr/bin/env python3
"""Chinese AI syntax-fingerprint diagnostic (Chinese-calibrated) — local, no upload.

English AI-style tools count words by \\b\\w+\\b; Chinese has no spaces, so word
counts and per-1k rates break. This uses **Han-character count** as the denominator
and Chinese-specific metrics: em-dash / semicolon / rule-of-three (、) density,
Chinese AI convergence words, sentence length (Han chars) and burstiness, the
**total density of six "not-X-but-Y" contrast frames** (並非…而是 / 而非 / 而不是 /
不在於…而在於 / 與其…不如 / 非…而…), and a list of sentences over 120 Han chars.

🔴 **Contrast frames: judge the TOTAL, never a single frame.** A pattern seen across
several drafts, generalized here: an edit that cut 「並非…而是」 in an earlier round
looked like it fixed the register — but the count simply moved to 「而非」, which
nothing was counting at the time. The *total* never changed. This tool sums all six
frames; when the total is high, cut the non-load-bearing ones to a plain, direct
statement. **Do not respond to a high count by switching to a different one of the
six frames** — the tool would show the same total either way.

Two threshold modes:
  - **Reference mode (default, no --corpus)**: heuristic thresholds. The "high" cutoff
    for contrast-frame density (0.40 per 1000 Han characters) is the 90th-percentile
    value the kit's original author measured across 288 papers from four Taiwan
    academic journals (design/art/education, 2018–2022, pre-ChatGPT). Treat it as a
    reference point, not a rule for your field.
  - **Corpus mode (--corpus <dir>)**: real percentiles against a folder of .txt files
    you assemble yourself (≥30 needed for a stable percentile). Same corpus-hygiene
    rule as the English tool: only OTHER PEOPLE's published writing, never your own
    drafts — comparing your style against a baseline that contains your own writing
    cancels the diagnosis out. Prefer papers published before general-purpose AI
    writing tools were common, for the same reason described in the English tool.

Sparse-metric guard: a raw count below 3 is never flagged, in either mode — one
em-dash in a short passage can look like a high percentile purely because the
denominator is small, and that kind of warning teaches readers to ignore all of them.

Optional personal baseline: --authored <folder of YOUR OWN .txt writing> — a
convergence word you genuinely use at your own normal rate is not flagged as an AI
tell; only words you don't normally use are. Independent of --corpus.

Optional: if zh-metadiscourse-scale (MIT license,
https://github.com/chenweichiang/zh-metadiscourse-scale) is installed and importable
— or pointed at with the ZHMD_PATH environment variable (its `src/` directory) — its
interactional metadiscourse markers are reported alongside these metrics for extra
signal. That project says explicitly it "is not a detector"; it's used here only to
compare density against a reference, never to judge authorship. Not installed →
this section is silently skipped, no error, no hard dependency.

No required dependencies (Python 3 stdlib). PDF input needs `pdftotext` on PATH;
.docx input needs `textutil` (built into macOS) or `pandoc` — without either, convert
the file to plain text yourself first (Word/Google Docs/LibreOffice "Save As" .txt).

Usage:
    python3 zh_ai_style.py <file.md|.txt|.tex|.pdf|.docx>       # or stdin
    python3 zh_ai_style.py <file> --authored ~/my-writing       # optional personal baseline
    python3 zh_ai_style.py --authored ~/my-writing --rebuild
    python3 zh_ai_style.py <file> --corpus ~/my-zh-corpus       # optional real percentiles
    python3 zh_ai_style.py --corpus ~/my-zh-corpus --rebuild
    python3 zh_ai_style.py --selftest                            # verify the contrast-frame regexes
"""
import hashlib
import json
import os
import re
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))
from md_prose import strip_markup   # same stripping rules as the English diagnostic

# Chinese AI convergence words (perception layer; not errors — only "AI-ish" in excess).
AI_WORDS = [
    "構成", "正是", "值得注意的是", "進一步", "彰顯", "凸顯", "賦予", "誠然",
    "某種程度上", "換言之", "從而", "旨在", "致力於", "蘊含", "折射", "交織",
    "不可或缺", "至關重要", "深刻地", "全方位", "多元", "豐富", "揭示", "體現",
    "不僅", "更是", "層層", "層面", "維度", "脈絡下", "視角下",
]

# ── Contrast frames (six shapes, summed to one TOTAL) ───────────────────────────
# "非…而…" excludes a preceding 並/而/除/無/莫/是 so it doesn't double-count a
# 並非…而是 / 而非 hit that already matched one of the other five patterns.
CONTRAST_FORMS = [
    ("並非／不是…而是", r"(?:並非|不是)[^。；！？]{0,60}?而是"),
    ("而非", r"而非"),
    ("而不是", r"而不是"),
    ("不在於…而在於", r"不在於[^。；！？]{0,60}?而在於"),
    ("與其…不如", r"與其[^。；！？]{0,60}?不如"),
    ("非…而…", r"(?<![並而除無莫是])非[一-鿿]{1,8}[，,]\s*而(?!非|不是)"),
]

# Heuristic thresholds (per 1000 Han chars), used when --corpus is not given.
# contrast: 0.40 = the reference p90 described in the module docstring above.
TH = {"emdash": (5, 10), "semi": (8, 15), "triplet": (8, 16), "contrast": (0.25, 0.40)}
LONG_SENT = 120   # Han chars; sentences above this are listed (enumerations with ≥3 「、」 exempt)
MIN_RAW = 3        # a metric's raw count below this is never flagged (see docstring)

HAN = r"[一-鿿]"


def _arg_value(flag):
    for i, a in enumerate(sys.argv):
        if a == flag and i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return None


def extract(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        import subprocess
        return subprocess.run(["pdftotext", str(path), "-"],
                              capture_output=True, text=True).stdout
    if path.suffix.lower() == ".docx":
        import subprocess
        for cmd in (["textutil", "-convert", "txt", "-stdout", str(path)],
                    ["pandoc", "-t", "plain", "--wrap=none", str(path)]):
            try:
                out = subprocess.run(cmd, capture_output=True, text=True)
            except FileNotFoundError:
                continue
            if out.returncode == 0 and out.stdout.strip():
                return out.stdout
        sys.exit(f"Can't read .docx — needs `textutil` (macOS) or `pandoc` on PATH: "
                 f"{path}\nLite fallback: 'Save As' / 'Download' plain text (.txt) "
                 "from Word / Google Docs / LibreOffice and point this script at that file.")
    txt = path.read_text(encoding="utf-8", errors="ignore")
    # 🔴 Use the shared stripping rules (`../common/md_prose.py`). Stripping only code
    #    fences / image links / brackets and missing HTML comments, frontmatter, tables,
    #    headings and emphasis markers is the mistake this shares with the English tool —
    #    see that module's docstring for the measured damage on real drafts.
    return strip_markup(txt, tex=path.suffix.lower() == ".tex")


def profile(text: str):
    han = re.findall(HAN, text)
    n = len(han)
    if n < 200:  # section drafts are often short; below this, rates are too noisy
        return None
    k = lambda c: round(c / n * 1000, 1)
    emdash = text.count("——") + len(re.findall(r"(?<!—)—(?!—)", text))
    semi = text.count("；") + text.count(";")
    triplet = len(re.findall(HAN + r"{1,6}、" + HAN + r"{1,6}、", text))  # A、B、C
    sents = [s for s in re.split(r"[。！？；]", text) if len(re.findall(HAN, s)) >= 4]
    slens = [len(re.findall(HAN, s)) for s in sents]
    mean = statistics.mean(slens) if slens else 0
    burst = statistics.stdev(slens) / mean if len(slens) > 1 and mean else 0
    words = {w: len(re.findall(re.escape(w), text)) for w in AI_WORDS}
    words = {w: c for w, c in words.items() if c}
    forms = {name: len(re.findall(rx, text)) for name, rx in CONTRAST_FORMS}
    contrast = sum(forms.values())
    # Long sentences: split on 。！？ only (a semicolon chain is still one sentence);
    # an enumeration with ≥3 「、」 is exempt — a list is long by nature.
    full = [x for x in re.split(r"[。！？]", text) if len(re.findall(HAN, x)) > LONG_SENT]
    long_sents = [x.strip() for x in full if x.count("、") < 3]
    return dict(n=n, emdash=k(emdash), semi=k(semi), triplet=k(triplet),
                slen=round(mean, 1), burst=round(burst, 2),
                emdash_raw=emdash, words=words,
                contrast=k(contrast), contrast_raw=contrast, contrast_forms=forms,
                long_sents=long_sents)


def flag(key, val, raw=None):
    if raw is not None and raw < MIN_RAW:
        return ""
    lo, hi = TH.get(key, (1e9, 1e9))
    return " [HIGH]" if val >= hi else (" [notice]" if val >= lo else "")


AUTHORED_DIR_DEFAULT = None   # no private default — pass --authored explicitly


def personal_baseline(authored: Path, rebuild=False):
    """Per-1k-Han rates of AI_WORDS in YOUR OWN writing, cached beside the folder.
    Resolves the tension "a convergence word is both your real word and an AI tell":
    your words at your own normal rate don't count as AI-ish. Returns {} if no
    folder is given."""
    if not authored or not authored.is_dir():
        return {"_n": 0, "_files": 0}
    cache = authored / ".voice_wordbase.json"
    if cache.exists() and not rebuild:
        try:
            return json.loads(cache.read_text(encoding="utf-8"))
        except Exception:
            pass
    # 🔴 Hygiene: the baseline is YOUR OWN writing only. Skip anything that looks like
    # an AI/co-authored draft (草稿/draft/ai/claude/gpt/generated) — including those
    # would let the tool treat AI tics as "your real words" and cancel the diagnosis out.
    # "ai" is matched only as a whole delimiter-bounded token (`_ai`, `ai-`, `ai.txt`, or
    # the whole stem) — plain substring matching would throw away `train.txt`, `detail.txt`,
    # `explain.txt` and every other filename that merely contains "ai".
    _DRAFTY = ("草稿", "draft", "gpt", "claude", "generated")
    _AI_TOKEN = re.compile(r"(?:^|[_\-. ])ai(?=$|[_\-. ])")

    def _drafty(name: str) -> bool:
        low = name.lower()
        return any(d in low for d in _DRAFTY) or bool(_AI_TOKEN.search(low))
    files = sorted(p for p in authored.glob("*.txt") if not _drafty(p.name))
    if not files:
        return {"_n": 0, "_files": 0}
    total = "\n".join(f.read_text(encoding="utf-8", errors="ignore") for f in files)
    n = len(re.findall(HAN, total))
    if n == 0:
        return {"_n": 0, "_files": len(files)}
    base = {"_n": n, "_files": len(files)}
    for w in AI_WORDS:
        c = len(re.findall(re.escape(w), total))
        if c:
            base[w] = round(c / n * 1000, 3)
    try:
        cache.write_text(json.dumps(base, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass
    return base


BASE_KEYS = ("emdash", "semi", "triplet", "contrast", "slen", "burst")

# Optional: zh-metadiscourse-scale. Purely additive — never a hard dependency.
# The six interactional markers below are the subset that project's own reference
# data (reference.csv in that repo) reports as most robust between machine and human
# writing; see its README for the full framework and the "not a detector" caveat.
_ZHMD_PATH = os.environ.get("ZHMD_PATH")
zhmd_profile = None
try:
    if _ZHMD_PATH and Path(_ZHMD_PATH).expanduser().is_dir():
        sys.path.insert(0, str(Path(_ZHMD_PATH).expanduser()))
    from zhmd import profile as zhmd_profile  # type: ignore
except Exception:
    zhmd_profile = None
MD_INTERACTIVE = ["累加轉折", "視角框架", "引據標記", "語碼註解", "對比重述", "框架標記"]
MD_ROBUST = {"累加轉折", "視角框架", "引據標記"}


def corpus_baseline(corpus_dir: Path, rebuild=False):
    """Percentile distributions for BASE_KEYS (+ each AI_WORD, + zhmd markers if
    available) from a corpus dir you point --corpus at. Cached beside the corpus
    dir, keyed by the file list. Returns None if fewer than 30 usable files."""
    files = sorted(corpus_dir.glob("*.txt")) if corpus_dir.is_dir() else []
    files = [f for f in files if f.exists()]
    if len(files) < 30:
        return None
    cache = corpus_dir / ".zh_style_baseline.json"
    key = hashlib.md5(("\n".join(f.name for f in files) + f"|zhmd={bool(zhmd_profile)}").encode()).hexdigest()
    if not rebuild and cache.exists():
        try:
            c = json.loads(cache.read_text(encoding="utf-8"))
            if c.get("_key") == key:
                return c
        except Exception:
            pass
    dist = {k: [] for k in BASE_KEYS}
    words = {w: [] for w in AI_WORDS}
    md = {m: [] for m in MD_INTERACTIVE}
    n_used = 0
    for f in files:
        t = strip_markup(f.read_text(encoding="utf-8", errors="ignore"))
        pr = profile(t)
        if not pr:
            continue
        n_used += 1
        for k in BASE_KEYS:
            dist[k].append(pr[k])
        for w in AI_WORDS:
            words[w].append(round(len(re.findall(re.escape(w), t)) / pr["n"] * 1000, 3))
        if zhmd_profile:
            r = zhmd_profile(t)
            for m in MD_INTERACTIVE:
                md[m].append(round(r["per15k"][m], 3))
    if n_used < 30:
        return None
    out = {"_key": key, "_n": n_used, "dist": {k: sorted(v) for k, v in dist.items()},
           "words": {w: sorted(v) for w, v in words.items()},
           "md": {m: sorted(v) for m, v in md.items() if v}}
    try:
        cache.write_text(json.dumps(out, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass
    return out


def _pct(vals, x):
    below = sum(1 for v in vals if v < x)
    ties = sum(1 for v in vals if v == x)
    return (below + 0.5 * ties) / len(vals) * 100


def report(text: str, authored: Path, corpus_dir: Path = None) -> str:
    p = profile(text)
    if not p:
        return ("Fewer than 200 Han chars — too short for stable rates. For a short "
                "section draft, edit by eye instead; run this on a fuller draft.")
    cb = corpus_baseline(corpus_dir) if corpus_dir else None

    raw = {"emdash": p["emdash_raw"], "contrast": p["contrast_raw"]}

    def row(label, key, unit="/k", extra=""):
        v = p[key]
        r = raw.get(key)
        if cb:
            vals = cb["dist"][key]
            med = vals[len(vals) // 2]
            pc = _pct(vals, v)
            if r is not None and r < MIN_RAW:
                fl = ""
            elif key == "burst":
                fl = " [notice]" if pc < 10 else ""
            elif key == "slen":
                # Chinese sentence length is watched on BOTH ends: a machine-rewritten
                # pass often produces suspiciously SHORT sentences, and the kit
                # author's own long-sentence habit reads as normal for them (not AI) —
                # only flag "too long" if your own field/reviewer expects short ones.
                fl = (" [notice] unusually short (a common sign of mechanical rewriting)"
                      if pc < 10 else
                      " [notice] unusually long (check against your venue's norm)" if pc > 97 else "")
            else:
                fl = " [HIGH]" if pc > 97 else (" [notice]" if pc > 90 else "")
            return f"{label:<10}{v:>7}{unit}  corpus median {med:>6}  p{pc:>3.0f}{fl}{extra}"
        return f"{label:<10}{v:>7}{unit}{flag(key, v, r) if key in TH else ''}{extra}"

    head = (f"Draft {p['n']} Han chars | baseline = {cb['_n']} papers ({corpus_dir})"
            if cb else
            f"Draft {p['n']} Han chars | metrics = per 1000 Han "
            f"(no --corpus given — reference thresholds, see header)")
    L = [head,
         row("em-dash", "emdash", extra=f"  (raw {p['emdash_raw']})"),
         row("semicolon", "semi"),
         row("rule-of-three (A、B、C)", "triplet"),
         row("mean sentence len", "slen", unit=" Han"),
         row("burstiness", "burst", unit=""),
         row("contrast total", "contrast", extra=f"  (raw {p['contrast_raw']}: "
             + "、".join(f"{n} {c}" for n, c in p["contrast_forms"].items() if c) + ")"),
         "    Keep load-bearing contrasts; state the rest plainly (say the side that "
         "matters). 🔴 Do NOT switch to a different one of the six frames — that "
         "changes which form carries it, not the total. Reference p90 (see header) "
         "≈ 0.40/1k; the kit author's own writing runs about 0.1/1k."]
    if zhmd_profile:
        r = zhmd_profile(text)
        L.append("\nInteractional metadiscourse markers (zh-metadiscourse-scale, per "
                 "15,000 Han chars; installed — see module docstring for how to add this):")
        for m in MD_INTERACTIVE:
            v = r["per15k"][m]
            ref = r["reference"].get(m, {})
            irr = ref.get("irr_machine_vs_human", "")
            line = f"  {m:<6}{v:>7.1f}"
            if cb and cb.get("md", {}).get(m):
                vals = cb["md"][m]
                pc = _pct(vals, v)
                fl = ((" [HIGH]" if m in MD_ROBUST else " [notice]")
                      if pc > 90 and r["counts"][m] >= MIN_RAW else "")
                line += f"  corpus median {vals[len(vals)//2]:>5.1f}  p{pc:>3.0f}{fl}"
            line += f"  (machine/human {irr}{', robust' if m in MD_ROBUST else ''})"
            L.append(line)
        if r["han"] < 3000:
            L.append("  [notice] Draft is under 3,000 Han chars — read these as "
                     "'present or absent', not as reliable densities (see that "
                     "project's README).")
    elif not zhmd_profile:
        L.append("\n(Optional: install zh-metadiscourse-scale — MIT, "
                 "https://github.com/chenweichiang/zh-metadiscourse-scale — for "
                 "interactional-metadiscourse markers alongside these metrics. Not "
                 "required.)")
    if p["long_sents"]:
        L.append(f"\nSentences over {LONG_SENT} Han chars (enumerations exempt): "
                 f"{len(p['long_sents'])} — split each, or re-punctuate into a running sentence")
        for x in p["long_sents"][:8]:
            L.append(f"    …{x[:36]}…({len(re.findall(HAN, x))} chars)")
        if len(p["long_sents"]) > 8:
            L.append(f"    …and {len(p['long_sents']) - 8} more")
    base = personal_baseline(authored)
    bn = base.get("_n", 0)
    real = {w for w in AI_WORDS if base.get(w, 0) > 0}
    L.append("\nChinese AI convergence words (two-tier if --authored is given: your "
             "real words at your own normal rate are kept; only abnormal words are flagged):")
    if p["words"]:
        ai_sig, over, normal = [], [], []
        for w, c in sorted(p["words"].items(), key=lambda x: -x[1]):
            dens = round(c / p["n"] * 1000, 2)
            if w in real:
                norm = base[w]
                over_q = dens > max(norm * 2.0, 1.0) and c >= 3
                (over if over_q else normal).append((w, c, dens, norm))
            elif dens >= 0.5 or c >= 2:
                ai_sig.append((w, c, dens))
        if cb:
            def over_corpus(w, dens):
                vals = cb["words"].get(w)
                return (not vals) or dens > vals[int(len(vals) * 0.9)]
            ai_sig = [x for x in ai_sig if over_corpus(x[0], x[2])]
            over = [x for x in over if over_corpus(x[0], x[2])]
        if ai_sig:
            L.append(("  [AI signal] (words you don't use, above corpus p90 — replace first): "
                     if cb else "  [AI signal] (words you don't use — replace first): ")
                     + "、".join(f"{w}×{c}" for w, c, _ in ai_sig))
        if over:
            L.append("  [over-used real word] (>2x your norm, trim a little): "
                     + "、".join(f"{w}×{c}({d}>{nm}/k)" for w, c, d, nm in over))
        if normal:
            L.append("  [your real word, normal rate — keep]: "
                     + "、".join(f"{w}×{c}" for w, c, *_ in normal))
        if not (ai_sig or over):
            L.append("  OK — no abnormal AI signal.")
    else:
        L.append("  OK — no notable convergence words.")
    if bn:
        L.append(f"  (personal baseline = {bn} Han / {base.get('_files','?')} files; "
                 "small sample, conservative. After adding writing, run --rebuild.)")
    else:
        L.append("  (no personal baseline — pure heuristic. Point --authored at a "
                 "folder of your own .txt writing to reduce false positives on your real words.)")
    L.append("\nEditing principle: em-dash → move pure asides to commas/parens (keep "
             "antithesis / closing / embedded questions); excess rule-of-three → some "
             "to running sentences; convergence words → more concrete verbs. Re-run to compare.")
    return "\n".join(L)


def selftest() -> int:
    """Positive/negative fixtures for the six contrast-frame regexes. Touches no
    corpus — run this after editing CONTRAST_FORMS."""
    cases = [
        ("這些遺物並非骨骸，而是被棄置的模型。", 1, "並非…而是"),
        ("它是可檢視的物件，而非外部神諭。", 1, "而非"),
        ("學生直接寫程式，而不是下提示詞。", 1, "而不是"),
        ("重點不在於工具，而在於提問。", 1, "不在於…而在於"),
        ("與其修補，不如重寫。", 1, "與其…不如"),
        ("物性空間非給定，而是界定。", 1, "非…而是 counted once"),
        ("這不是問題。", 0, "plain negation"),
        ("非營利組織而言尚屬少見。", 0, "「非營利」 is not a contrast frame"),
        ("並非所有學生都參與。", 0, "「並非」 alone is not a contrast frame"),
        ("除非另有說明，而且資料齊全。", 0, "「除非」 is not a contrast frame"),
        ("這並非易事，而是需要時間。", 1, "並非…而是 not double-counted by 非…而…"),
    ]
    bad = 0
    for text, want, why in cases:
        got = sum(len(re.findall(rx, text)) for _, rx in CONTRAST_FORMS)
        ok = got == want
        bad += not ok
        print(f"{'PASS' if ok else 'FAIL'} {why:<44} want {want} got {got}")
    print("all passed" if not bad else f"{bad} failure(s)")
    return 1 if bad else 0


def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        sys.exit(selftest())
    authored_val = _arg_value("--authored")
    corpus_val = _arg_value("--corpus")
    authored = Path(authored_val).expanduser() if authored_val else None
    corpus_dir = Path(corpus_val).expanduser() if corpus_val else None
    for flag_name, val in (("--authored", authored_val), ("--corpus", corpus_val)):
        if val is not None:
            i = args.index(flag_name)
            del args[i:i + 2]
    if "--rebuild" in args:
        if corpus_dir:
            cb = corpus_baseline(corpus_dir, rebuild=True)
            print(f"Corpus baseline rebuilt: {cb['_n'] if cb else 0} papers.")
        if authored:
            b = personal_baseline(authored, rebuild=True)
            print("Personal baseline rebuilt: %s Han / %s files. Real words (per 1k Han): %s" % (
                b.get("_n", 0), b.get("_files", 0),
                "、".join(f"{w}={b[w]}" for w in AI_WORDS if w in b) or "(none)"))
        args = [a for a in args if a != "--rebuild"]
        if not args:
            return
    arg = args[0] if args else "-"
    text = sys.stdin.read() if arg == "-" else extract(Path(arg).expanduser())
    print(report(text, authored, corpus_dir))


if __name__ == "__main__":
    main()
