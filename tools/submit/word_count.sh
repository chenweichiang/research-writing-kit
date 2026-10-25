#!/usr/bin/env bash
# word_count.sh: count words with Microsoft Word itself (many venues define the limit by
# Word's own count). macOS + Microsoft Word ONLY: it drives Word through osascript.
# On Linux, Windows, or a Mac without Word it falls back to wordcount_approx.py, an
# APPROXIMATE count (exit 3) that must be reported as approximate.
#
# Usage: word_count.sh file.docx [--pdf output.pdf]
# How: copies the file into Word's sandbox (~/Library/Containers/com.microsoft.Word/Data/tmp/),
#   opens it with osascript and asks Word for words, characters and pages. With --pdf it
#   saves the PDF inside the sandbox and then moves it out (saving straight outside the
#   sandbox raises a permission dialog; the AppleEvent times out and Word hangs). The
#   document is closed without saving and the sandbox copy is deleted.
# Environment: PY=path/to/python3 overrides the interpreter used for the fallback.
# Exit codes: 0 = Word count succeeded; 2 = bad arguments or file; 3 = approximate count only
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="${PY:-python3}"

DOCX=""; PDF=""
while [ $# -gt 0 ]; do
  case "$1" in
    --pdf) PDF="${2:-}"; shift 2 ;;
    -h|--help) sed -n '2,14p' "$0"; exit 0 ;;
    *) DOCX="$1"; shift ;;
  esac
done
if [ -z "$DOCX" ] || [ ! -f "$DOCX" ]; then
  echo "usage: word_count.sh file.docx [--pdf output.pdf] (file not found: ${DOCX:-not given})" >&2
  exit 2
fi
DOCX="$(cd "$(dirname "$DOCX")" && pwd)/$(basename "$DOCX")"
[ -n "$PDF" ] && PDF="$(cd "$(dirname "$PDF")" 2>/dev/null && pwd)/$(basename "$PDF")"

approx() {
  echo "($1; falling back to the approximate count, which is NOT Word's number)" >&2
  "$PY" "$HERE/wordcount_approx.py" "$DOCX"
  exit 3
}

WORD_APP="/Applications/Microsoft Word.app"
SANDBOX="$HOME/Library/Containers/com.microsoft.Word/Data/tmp"
[ "$(uname -s)" = "Darwin" ] || approx "not macOS"
[ -d "$WORD_APP" ] || approx "Microsoft Word not found"
command -v osascript >/dev/null 2>&1 || approx "osascript not available"
mkdir -p "$SANDBOX" 2>/dev/null || approx "cannot create the Word sandbox temp folder"

STAMP="wc_$$_$(date +%s)"
TMP_DOCX="$SANDBOX/$STAMP.docx"
TMP_PDF="$SANDBOX/$STAMP.pdf"
cp "$DOCX" "$TMP_DOCX" || approx "cannot copy into the Word sandbox"
cleanup() { rm -f "$TMP_DOCX" "$TMP_PDF"; }
trap cleanup EXIT

MAKE_PDF="false"; [ -n "$PDF" ] && MAKE_PDF="true"

OUT="$(osascript - "$TMP_DOCX" "$TMP_PDF" "$MAKE_PDF" <<'APPLESCRIPT' 2>&1
on run argv
  set docPath to item 1 of argv
  set pdfPath to item 2 of argv
  set wantPdf to (item 3 of argv) is "true"
  tell application "Microsoft Word"
    open file name docPath
    set d to active document
    set w to compute statistics d statistic statistic words
    set c1 to compute statistics d statistic statistic characters
    set c2 to compute statistics d statistic statistic characters with spaces
    set pg to compute statistics d statistic statistic pages
    if wantPdf then
      save as d file name pdfPath file format format PDF
    end if
    set ver to version
    close d saving no
  end tell
  return (w as text) & "|" & (c1 as text) & "|" & (c2 as text) & "|" & (pg as text) & "|" & ver
end run
APPLESCRIPT
)"
RC=$?
if [ $RC -ne 0 ] || ! echo "$OUT" | grep -Eq '^[0-9]+\|[0-9]+\|[0-9]+\|[0-9]+\|'; then
  approx "Word count failed: $(echo "$OUT" | tr '\n' ' ' | cut -c1-120)"
fi

IFS='|' read -r W C1 C2 PG VER <<<"$OUT"
if [ -n "$PDF" ]; then
  if [ -f "$TMP_PDF" ]; then mv "$TMP_PDF" "$PDF" && echo "PDF saved to $PDF" >&2
  else echo "warning: Word did not produce a PDF" >&2; fi
fi
echo "Word count $W | characters (no spaces) $C1 | characters (with spaces) $C2 | pages $PG | source: Word $VER"
