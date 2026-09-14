#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Voice lint (Chinese) — mechanically catch specific "doesn't sound like me" tics,
no judgement calls. Rules are DATA, not baked in: ship your own via a rules file so
each author enforces their own voice. Local-only.

The built-in defaults are generic Chinese academic de-AI rules (a sensible starting
point). Customize by copying templates/voice_rules.template.json → voice_rules.json
and editing it; point at it with --rules. Run to "zero flags" before delivering.

Four kinds of rule: "hard" (pass/fail, counted), "soft" (density only), "report"
(listed for a human decision, never counted — e.g. AI stock phrases), and
"headings" (one regex; heading lines that match are flagged as sentence-form titles).

No dependencies (Python 3 standard library only).

Usage:
    python3 voice_lint.py <file.md|.txt|.typ>                 # built-in defaults
    python3 voice_lint.py <file> --rules voice_rules.json     # your own rules
    cat file | python3 voice_lint.py -                        # stdin
Exit code 1 if any hard-rule flags remain (usable in a pre-delivery gate).
"""
import json
import re
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent / "common"))
from md_prose import mask_nonprose
import sys
from pathlib import Path

# ── Built-in DEFAULT rules. Generic Chinese-academic de-AI tics. These are a
#    starting point — override entirely with your own via --rules. Each rule =
#    [label, regex]. "should be 0" rules are hard flags. ──
DEFAULT_HARD = [
    ["Em-dash / double-hyphen (should be 0 in formal zh prose)", r"—|――|--|−"],
    ["Semicolon (should be 0)", r"[；;]"],
    ["然而 starting a sentence", r"(^|。|，)然而"],
    ["Self-congratulatory verdict phrases",
     r"恰恰是|恰切合|之所在|價值所在|誠實所在|真正的[^，。]{0,8}(在於|重量|價值)"],
    ["Colloquial words in academic prose", r"當成|看作|看成|好像|沒辦法"],
    ["Colloquial demonstratives (那份/那個/這個東西 → 該…, or delete)",
     r"那份由|那份[表單資料紀錄]|那個[步驟東西部分問題]|這個東西"],
    ["Redundant 此一/這一類 pointing", r"此一|這一類|這一場|這一種|這一項"],
    ["Over-literary particles", r"[乃]|抑或|此即|則是"],
    # Stock closers. Every Chinese-academic style guide bans them and every AI draft
    # reaches for them; 「」-quoted mentions (the phrase being discussed) are skipped.
    ["Stock closers / summary clichés (綜上所述…)",
     r"(?<!「)(?:綜觀全案|綜上所述|總而言之|整體而言|由此觀之|一言以蔽之|總的來說|大體而言)(?!」)"],
]
# Soft rules report density only (no hard flag).
DEFAULT_SOFT = [
    ["一+measure-word density (too many reads AI-ish)", r"一[具個種套位條場道份隻]", 4.0],
]
# Report-only rules: listed for a human decision, never counted as flags. The default
# list is AI stock phrasing that was measured, not guessed: candidates were compared by
# frequency per 100k chars between Taiwan-authored design-journal papers (120) and
# machine-generated paragraphs (319), keeping only what machines use markedly more and
# human authors rarely do. Extend it with words YOU never write.
DEFAULT_REPORT = [
    ["AI stock phrases (candidates — judge each)",
     r"(?<!「)(?:關鍵作用|扮演著|多維度|標誌著|生態系統|愈發|深厚的|持久的|奠定了?基礎)(?!」)"],
]
# Headings written as full sentences or questions (「為何…？」「…是否…」). Academic
# section titles are noun phrases; this scans Markdown `#` and Typst `=` heading lines.
# Set "headings" to "" in your rules file to disable.
DEFAULT_HEADINGS = r"為何|為什麼|是否|嗎[？?]?$|？|\?$|，而|其實"


def load_rules(path):
    if not path:
        return DEFAULT_HARD, DEFAULT_SOFT, DEFAULT_REPORT, DEFAULT_HEADINGS
    cfg = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    hard = cfg.get("hard", DEFAULT_HARD)
    soft = cfg.get("soft", DEFAULT_SOFT)
    report = cfg.get("report", DEFAULT_REPORT)
    headings = cfg.get("headings", DEFAULT_HEADINGS)
    return hard, soft, report, headings


def is_prose(s):
    """Keep prose lines; drop Typst/markdown directives & figure calls."""
    s = s.strip()
    if not s or s[0] in "=#)（(|<":   # `|` table row, `<` HTML tag: not prose
        return False
    if any(k in s for k in ["cfig(", "image(", "figure(", "caption:", "numbering:",
                            "supplement:", "align(", "block(", "#set", "#show", "#let",
                            "```"]):
        return False
    return True


def main():
    if any(a in ("-h", "--help") for a in sys.argv[1:]):
        print(__doc__.strip() if __doc__ else "usage: see the header of this file")
        return
    args = sys.argv[1:]
    rules_path = None
    if "--rules" in args:
        i = args.index("--rules")
        rules_path = args[i + 1]
        del args[i:i + 2]
    src = args[0] if args else "-"
    raw = sys.stdin.read() if src == "-" else Path(src).expanduser().read_text(encoding="utf-8")
    # 🔴 Mask HTML comments and code fences before linting. The two comment markers
    #    themselves (`<!--` `-->`) contain `--`, which this tool was reporting as
    #    em-dashes — 4 false flags on a real draft. Masked, not deleted, so the
    #    line numbers reported below stay correct.
    raw = mask_nonprose(raw, layout=True)
    hard, soft, report, headings = load_rules(rules_path)

    lines_all = raw.split("\n")
    prose = [(i + 1, l) for i, l in enumerate(lines_all) if is_prose(l)]
    flags = 0
    if headings:
        hrx = re.compile(headings)
        title_hits = [(i + 1, l.strip()) for i, l in enumerate(lines_all)
                      if re.match(r"\s*(#{1,6}|={1,4})\s*\S", l) and hrx.search(l)]
        if title_hits:
            flags += len(title_hits)
            print(f"[X] Sentence-form headings (rewrite as noun phrases): {len(title_hits)}")
            for n, tline in title_hits[:6]:
                print(f"      L{n}  {tline[:50]}")
    for label, pat in hard:
        rx = re.compile(pat)
        hits = [(n, m.group()) for n, l in prose for m in rx.finditer(l)]
        if hits:
            flags += len(hits)
            print(f"[X] {label}: {len(hits)}")
            for n, g in hits[:6]:
                print(f"      L{n}  …{g}…")
    chars = sum(len(l) for _, l in prose) or 1
    for entry in soft:
        label, pat = entry[0], entry[1]
        thr = entry[2] if len(entry) > 2 else 4.0
        rx = re.compile(pat)
        s_hits = [(n, m.group()) for n, l in prose for m in rx.finditer(l)]
        dens = len(s_hits) / chars * 1000
        note = "(high — check each for removal)" if dens > thr else "(ok)"
        print(f"[.] {label}: {len(s_hits)}  ({dens:.1f}/1k chars) {note}")
    for label, pat in report:
        rx = re.compile(pat)
        r_hits = [(n, l[max(0, m.start() - 12):m.end() + 12].strip())
                  for n, l in prose for m in rx.finditer(l)]
        print(f"[?] {label}: {len(r_hits)}  (report-only, not counted)")
        for n, ctx in r_hits[:20]:
            print(f"      L{n}  …{ctx}…")
    print("[?] Overclaims (absolutes, proof verbs, unsourced 'studies show'): run "
          "tools/claims/overclaim_lint.py — same report-only rule, judged per hit.")

    print(f"\n{'=' * 40}\nHard-rule flags: {flags}  →  "
          f"{'CLEAN' if flags == 0 else 'NOT PASSED — fix each before delivering'}")
    sys.exit(1 if flags else 0)


if __name__ == "__main__":
    main()
