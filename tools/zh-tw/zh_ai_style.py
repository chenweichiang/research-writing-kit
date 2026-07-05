#!/usr/bin/env python3
"""Chinese AI syntax-fingerprint diagnostic (Chinese-calibrated) — local, no upload.

English AI-style tools count words by \\b\\w+\\b; Chinese has no spaces, so word
counts and per-1k rates break. This uses **Han-character count** as the denominator
and Chinese-specific metrics: em-dash / semicolon / rule-of-three (、) density,
Chinese AI convergence words, sentence length (Han chars) and burstiness.

⚠️ With no field corpus baseline, thresholds are HEURISTIC (marked below), not
   percentiles. They over-flag dense long-sentence academic prose — read them
   *relatively*: comparing the same draft before/after editing is the most reliable use.

Optional personal baseline: if you point --authored at a folder of YOUR OWN writing
(.txt), convergence words you genuinely use at normal rates won't be flagged as AI
tells — only words you don't use will. Without it, falls back to pure heuristic.

No dependencies (Python 3 stdlib; PDF input needs `pdftotext` on PATH).

Usage:
    python3 zh_ai_style.py <file.md|.txt|.tex>            # or stdin
    python3 zh_ai_style.py <file> --authored ~/my-writing # optional personal baseline
    python3 zh_ai_style.py --authored ~/my-writing --rebuild
"""
import json
import re
import statistics
import sys
from pathlib import Path

# Chinese AI convergence words (perception layer; not errors — only "AI-ish" in excess).
AI_WORDS = [
    "構成", "正是", "值得注意的是", "進一步", "彰顯", "凸顯", "賦予", "誠然",
    "某種程度上", "換言之", "從而", "旨在", "致力於", "蘊含", "折射", "交織",
    "不可或缺", "至關重要", "深刻地", "全方位", "多元", "豐富", "揭示", "體現",
    "不僅", "更是", "層層", "層面", "維度", "脈絡下", "視角下",
]

# Heuristic thresholds (per 1000 Han chars); no corpus baseline, relative use only.
TH = {"emdash": (5, 10), "semi": (8, 15), "triplet": (8, 16)}  # (notice, high)

HAN = r"[一-鿿]"


def _authored_dir():
    for i, a in enumerate(sys.argv):
        if a == "--authored" and i + 1 < len(sys.argv):
            return Path(sys.argv[i + 1]).expanduser()
    return None


def extract(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        import subprocess
        return subprocess.run(["pdftotext", str(path), "-"],
                              capture_output=True, text=True).stdout
    txt = path.read_text(encoding="utf-8", errors="ignore")
    if path.suffix.lower() == ".tex":
        txt = re.sub(r"(?m)%.*$", "", txt)
        txt = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^}]*\})?", " ", txt)
    txt = re.sub(r"```.*?```", " ", txt, flags=re.S)
    txt = re.sub(r"!?\[[^\]]*\]\([^)]*\)", " ", txt)
    txt = re.sub(r"【[^】]*】", " ", txt)  # drop to-do markers
    return txt


def profile(text: str):
    han = re.findall(HAN, text)
    n = len(han)
    if n < 120:  # section drafts are often short; below this, rates are too noisy
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
    return dict(n=n, emdash=k(emdash), semi=k(semi), triplet=k(triplet),
                slen=round(mean, 1), burst=round(burst, 2),
                emdash_raw=emdash, words=words)


def flag(key, val):
    lo, hi = TH.get(key, (1e9, 1e9))
    return " [HIGH]" if val >= hi else (" [notice]" if val >= lo else "")


def personal_baseline(authored: Path, rebuild=False):
    """Per-1k-Han rates of AI_WORDS in YOUR OWN writing, cached beside the folder.
    Resolves the tension 'a convergence word is both your real word and an AI tell':
    your words at normal rates don't count as AI-ish. Returns {} if no folder given."""
    if not authored or not authored.is_dir():
        return {"_n": 0, "_files": 0}
    cache = authored / ".voice_wordbase.json"
    if cache.exists() and not rebuild:
        try:
            return json.loads(cache.read_text(encoding="utf-8"))
        except Exception:
            pass
    # 🔴 Hygiene: the baseline is YOUR OWN writing only. Skip anything that looks like
    # an AI/co-authored draft (草稿/draft/ai) — including those would let the tool treat
    # AI tics as "your real words" and cancel the diagnosis out.
    _DRAFTY = ("草稿", "draft", "ai", "gpt", "claude", "generated")
    files = sorted(p for p in authored.glob("*.txt")
                   if not any(d in p.name.lower() for d in _DRAFTY))
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


def report(text: str, authored: Path) -> str:
    p = profile(text)
    if not p:
        return ("Fewer than 120 Han chars — too short for stable rates. For a short "
                "section draft, use voice_lint.py / zh_localize.py instead; run this on "
                "a fuller draft.")
    L = [f"Draft: {p['n']} Han chars | metrics = per 1000 Han (heuristic, not percentile)",
         f"{'em-dash':<22}{p['emdash']:>7}/k{flag('emdash', p['emdash'])}  (raw {p['emdash_raw']})",
         f"{'semicolon':<22}{p['semi']:>7}/k{flag('semi', p['semi'])}",
         f"{'rule-of-three A、B、C':<22}{p['triplet']:>7}/k{flag('triplet', p['triplet'])}",
         f"{'mean sentence len':<22}{p['slen']:>7} Han   burstiness SD/mean={p['burst']}"]
    base = personal_baseline(authored)
    bn = base.get("_n", 0)
    real = {w for w in AI_WORDS if base.get(w, 0) > 0}
    L.append("\nChinese AI convergence words:")
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
        if ai_sig:
            L.append("  [AI signal] (words you don't use — replace first): "
                     + "、".join(f"{w}×{c}" for w, c, _ in ai_sig))
        if over:
            L.append("  [over-used real word] (>2× your norm, trim a little): "
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
        L.append("  (no personal baseline — pure heuristic. Point --authored at a folder "
                 "of your own .txt writing to reduce false positives on your real words.)")
    L.append("\nEditing principle: em-dash → move pure asides to commas/parens (keep "
             "antithesis / closing / embedded questions); excess rule-of-three → some "
             "to running sentences; convergence words → more concrete verbs. Re-run to compare.")
    return "\n".join(L)


def main():
    args = [a for a in sys.argv[1:]]
    authored = _authored_dir()
    if authored:
        i = args.index("--authored")
        del args[i:i + 2]
    if "--rebuild" in args:
        b = personal_baseline(authored, rebuild=True)
        print("Personal baseline rebuilt: %s Han / %s files." % (
            b.get("_n", 0), b.get("_files", 0)))
        args = [a for a in args if a != "--rebuild"]
        if not args:
            return
    arg = args[0] if args else "-"
    text = sys.stdin.read() if arg == "-" else extract(Path(arg).expanduser())
    print(report(text, authored))


if __name__ == "__main__":
    main()
