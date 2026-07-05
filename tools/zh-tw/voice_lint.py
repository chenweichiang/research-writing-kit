#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Voice lint (Chinese) — mechanically catch specific "doesn't sound like me" tics,
no judgement calls. Rules are DATA, not baked in: ship your own via a rules file so
each author enforces their own voice. Local-only.

The built-in defaults are generic Chinese academic de-AI rules (a sensible starting
point). Customize by copying templates/voice_rules.template.json → voice_rules.json
and editing it; point at it with --rules. Run to "zero flags" before delivering.

No dependencies (Python 3 standard library only).

Usage:
    python3 voice_lint.py <file.md|.txt|.typ>                 # built-in defaults
    python3 voice_lint.py <file> --rules voice_rules.json     # your own rules
    cat file | python3 voice_lint.py -                        # stdin
Exit code 1 if any hard-rule flags remain (usable in a pre-delivery gate).
"""
import json
import re
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
    ["Over-literary particles", r"[乃]|抑或|此即|則是"],
]
# Soft rules report density only (no hard flag).
DEFAULT_SOFT = [
    ["一+measure-word density (too many reads AI-ish)", r"一[具個種套位條場道份隻]", 4.0],
]


def load_rules(path):
    if not path:
        return DEFAULT_HARD, DEFAULT_SOFT
    cfg = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    hard = cfg.get("hard", DEFAULT_HARD)
    soft = cfg.get("soft", DEFAULT_SOFT)
    return hard, soft


def is_prose(s):
    """Keep prose lines; drop Typst/markdown directives & figure calls."""
    s = s.strip()
    if not s or s[0] in "=#)（(":
        return False
    if any(k in s for k in ["cfig(", "image(", "figure(", "caption:", "numbering:",
                            "supplement:", "align(", "block(", "#set", "#show", "#let",
                            "```"]):
        return False
    return True


def main():
    args = sys.argv[1:]
    rules_path = None
    if "--rules" in args:
        i = args.index("--rules")
        rules_path = args[i + 1]
        del args[i:i + 2]
    src = args[0] if args else "-"
    raw = sys.stdin.read() if src == "-" else Path(src).expanduser().read_text(encoding="utf-8")
    hard, soft = load_rules(rules_path)

    prose = [(i + 1, l) for i, l in enumerate(raw.split("\n")) if is_prose(l)]
    flags = 0
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

    print(f"\n{'=' * 40}\nHard-rule flags: {flags}  →  "
          f"{'CLEAN' if flags == 0 else 'NOT PASSED — fix each before delivering'}")
    sys.exit(1 if flags else 0)


if __name__ == "__main__":
    main()
