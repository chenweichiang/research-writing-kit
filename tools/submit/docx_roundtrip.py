#!/usr/bin/env python3
"""docx_roundtrip.py: convert a built docx back to text, compare it with the source, and
scan for leftovers a delivered manuscript must not carry.

Why it exists: a docx built from markdown (or Typst) can silently lose a paragraph, keep
an unresolved "[@key]" citation, or ship a "TODO" the author never saw. Nobody reads the
whole Word file against the source, so the machine does it.

Usage:
  docx_roundtrip.py source.md built.docx [--from markdown] [--json]
How: both sides go through pandoc to plain text (no --citeproc, so no bibliography is
needed; "[@key]" is replaced by a placeholder on both sides), are normalised and cut into
sentences, then matched fuzzily (similarity >= 0.9 counts as the same sentence). It lists
"in source, missing from docx" and "in docx, not in source", and scans the docx text for
leftovers: unresolved citations, "[[" markers, 【待確認】 / TODO / TK / XXX, "??",
Word reference errors, "[ref]", unreplaced "{{" and "$...$" math, and runs of two or more
empty paragraphs (needs python-docx; skipped with a note when missing).
Requires pandoc.
Exit codes: 0 = 0 missing, 0 extra, 0 leftovers; 1 = differences or leftovers;
2 = read error (including pandoc not installed).
"""
import argparse
import difflib
import json
import re
import subprocess
import sys
import unicodedata

THRESH = 0.9
CITE_PH = "CITEPH"

# (name, regex); the scan runs on the text converted from the docx
RESIDUE_PATTERNS = [
    ("unresolved citation ([@ or @key)", re.compile(r"\[@|(?<![\w.@])@[A-Za-z][\w:\-]{1,}")),
    ("double square bracket marker ([[)", re.compile(r"\[\[")),
    ("to-be-confirmed marker", re.compile(r"【待確認】|\bTODO\b|\bTK\b|\bXXX\b")),
    ("failed cross-reference (??)", re.compile(r"\?\?")),
    ("Word reference error", re.compile(r"Error! Reference source not found|錯誤! ?找不到參照來源")),
    ("placeholder [ref] / (ref)", re.compile(r"\[ref\]|\(ref\)", re.I)),
    ("unreplaced {{", re.compile(r"\{\{")),
    ("unreplaced $...$ math", re.compile(r"(?<![\w$])\$(?=[^\s$])[^$\n]*[\\^_{][^$\n]*\$")),
]


def pandoc_plain(path, fmt=None):
    cmd = ["pandoc", path, "-t", "plain", "--wrap=none"]
    if fmt:
        cmd += ["-f", fmt]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except FileNotFoundError:
        raise OSError("pandoc not found (install it: https://pandoc.org/installing.html)")
    if r.returncode != 0:
        raise OSError(f"pandoc failed on {path}: {r.stderr.strip()[:200]}")
    return r.stdout


def normalize(text):
    text = re.sub(r"\[[^\]\n]*@[^\]\n]*\]", CITE_PH, text)   # pandoc citation syntax
    text = text.replace("\u3000", " ").replace("\u00a0", " ")
    text = re.sub(r"[“”„「」『』]", '"', text)
    text = re.sub(r"[‘’‚]", "'", text)
    text = unicodedata.normalize("NFKC", text)               # full-width alphanumerics and punctuation to half-width
    text = re.sub(r"[ \t]+", " ", text)
    # a space between two CJK characters carries no meaning
    text = re.sub(r"(?<=[\u3400-\u9fff，。、：；？！]) (?=[\u3400-\u9fff，。、：；？！])", "", text)
    return text


def split_sentences(text):
    out = []
    for para in text.split("\n"):
        para = para.strip()
        if not para:
            continue
        for part in re.split(r"(?<=[。！？；!?;])|(?<=[.!?])\s+", para):
            part = (part or "").strip()
            if len(part) >= 2:
                out.append(part)
    return out


def similar(a, b):
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return sm.real_quick_ratio() >= THRESH and sm.quick_ratio() >= THRESH and sm.ratio() >= THRESH


def unmatched(src, dst):
    """Sentences of src with no counterpart (similarity >= THRESH) in dst."""
    pool = list(dst)
    exact = {}
    for s in pool:
        exact[s] = exact.get(s, 0) + 1
    missing = []
    for s in src:
        if exact.get(s, 0) > 0:
            exact[s] -= 1
            continue
        missing.append(s)
    remaining = [s for s, n in exact.items() for _ in range(n)]
    result = []
    for s in missing:
        hit = next((i for i, d in enumerate(remaining) if similar(s, d)), None)
        if hit is None:
            result.append(s)
        else:
            remaining.pop(hit)
    return result


def scan_residue(text):
    found = []
    for name, pat in RESIDUE_PATTERNS:
        for m in pat.finditer(text):
            a, b = max(0, m.start() - 20), min(len(text), m.end() + 20)
            found.append({"type": name, "position": m.start(),
                          "context": text[a:b].replace("\n", "\u23ce")})
    return found


def empty_paragraph_runs(docx_path):
    """Runs of two or more empty paragraphs, via python-docx; returns [(start index, length)],
    or None when python-docx is not installed."""
    try:
        import docx
    except ImportError:
        return None
    d = docx.Document(docx_path)
    runs, run_start, n = [], None, 0
    for i, p in enumerate(d.paragraphs):
        empty = not p.text.strip() and not p._p.xpath(".//w:drawing | .//w:br[@w:type='page'] | .//w:pict")
        if empty:
            if run_start is None:
                run_start = i
            n += 1
        else:
            if n >= 2:
                runs.append((run_start, n))
            run_start, n = None, 0
    if n >= 2:
        runs.append((run_start, n))
    return runs


def clip(s, n=80):
    return s if len(s) <= n else s[:n] + "..."


def main():
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    ap.add_argument("source")
    ap.add_argument("docx")
    ap.add_argument("--from", dest="fmt", default="markdown", help="source format (default: markdown)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    try:
        src_txt = pandoc_plain(a.source, a.fmt)
        doc_txt = pandoc_plain(a.docx)
        empties = empty_paragraph_runs(a.docx)
    except Exception as e:
        print(f"read error: {e}", file=sys.stderr)
        return 2

    src_s = split_sentences(normalize(src_txt))
    doc_s = split_sentences(normalize(doc_txt))
    missing = unmatched(src_s, doc_s)
    extra = unmatched(doc_s, src_s)
    residue = scan_residue(doc_txt)
    for start, n in (empties or []):
        residue.append({"type": "consecutive empty paragraphs", "position": start,
                        "context": f"{n} empty paragraphs in a row from paragraph {start + 1}"})

    summary = f"missing {len(missing)}, extra {len(extra)}, leftovers {len(residue)}"
    if a.json:
        print(json.dumps({"missing": missing, "extra": extra, "residue": residue, "summary": summary},
                         ensure_ascii=False, indent=2))
    else:
        print(f"source {len(src_s)} sentences, docx {len(doc_s)} sentences")
        print(f"\n== in source, missing from docx ({len(missing)}) ==")
        for s in missing:
            print(f"  - {clip(s)}")
        print(f"\n== in docx, not in source ({len(extra)}) ==")
        for s in extra:
            print(f"  - {clip(s)}")
        print(f"\n== leftovers ({len(residue)}) ==")
        for r in residue:
            print(f"  - [{r['type']}] @{r['position']}: ...{r['context']}...")
        if empties is None:
            print("  (python-docx not installed: empty-paragraph check skipped)")
        print(f"\n{summary}")
    return 0 if not (missing or extra or residue) else 1


if __name__ == "__main__":
    sys.exit(main())
