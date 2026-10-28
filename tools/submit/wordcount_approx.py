#!/usr/bin/env python3
"""wordcount_approx.py: approximate word count (CJK characters + Latin words + digit runs).

This is an APPROXIMATION and can differ from Word's own count by ten percent or more.
Before submitting, count the way the venue counts (word_count.sh asks Word itself, on
macOS only). Anything reported from this tool must be called "approximate".

Usage:
  wordcount_approx.py file.docx|file.md|file.txt
Output: one line starting with "Approximate word count". Exit code 0 (2 on a read error).
.docx input is read through pandoc; word_count.sh falls back to this tool when Word is
not available.
"""
import re
import subprocess
import sys

CJK = re.compile(r"[㐀-䶿一-鿿豈-﫿぀-ヿ가-힯]")
WORD = re.compile(r"[A-Za-z]+(?:['’\-][A-Za-z]+)*|\d+(?:[.,]\d+)*")


def approx_count(text):
    """Return a dict: words (CJK characters + Latin words + digit runs), cjk, latin,
    chars_nospace, chars_space."""
    cjk = len(CJK.findall(text))
    rest = CJK.sub(" ", text)
    latin = len(WORD.findall(rest))
    return {
        "words": cjk + latin,
        "cjk": cjk,
        "latin": latin,
        "chars_nospace": len(re.sub(r"\s", "", text)),
        "chars_space": len(text.replace("\n", "")),
    }


def read_text(path):
    if path.lower().endswith(".docx"):
        try:
            r = subprocess.run(["pandoc", path, "-t", "plain", "--wrap=none"],
                               capture_output=True, text=True)
        except FileNotFoundError:
            raise OSError("pandoc not found (needed to read .docx here; install pandoc "
                          "or pass a .md/.txt export)")
        if r.returncode != 0:
            raise OSError(r.stderr.strip() or "pandoc failed")
        return r.stdout
    return open(path, encoding="utf-8").read()


def format_line(c):
    return (f"Approximate word count {c['words']} (CJK characters {c['cjk']} + Latin words and "
            f"digit runs {c['latin']}) | characters (no spaces) {c['chars_nospace']} | "
            f"characters (with spaces) {c['chars_space']} | pages unknown | "
            "APPROXIMATE: can differ from Word by 10% or more; count the venue's way before submitting")


def main(argv):
    if any(a in ("-h", "--help") for a in argv[1:]):
        print(__doc__)
        return 0
    if len(argv) != 2:
        print(__doc__)
        return 2
    try:
        text = read_text(argv[1])
    except (OSError, UnicodeDecodeError) as e:
        print(f"read error: {e}", file=sys.stderr)
        return 2
    print(format_line(approx_count(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
