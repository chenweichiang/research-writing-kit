#!/usr/bin/env bash
# lt_check.sh — LanguageTool grammar + US/UK spelling-consistency check (fully offline)
#
# Role: paper-review Layer 1 "deep pass" after a fast grammar check — catches real
#   grammar a fast checker misses (subject-verb agreement / articles / tense /
#   easily-confused pairs) + mixed US/UK spelling.
# Design: variant isn't hardcoded; default en-US. For a British venue, --variant en-GB
#   flips it in one shot. Whichever variant you lock, mixed spelling gets flagged
#   (the other variant's spellings are marked) — symmetric.
# Privacy: LanguageTool (brew build) is pure local Java — the draft never leaves the
#   machine (satisfies "unpublished drafts stay local").
#
# Requires: languagetool + pandoc  (macOS: brew install languagetool pandoc)
#   Override the binary with:  LT=/path/to/languagetool  lt_check.sh ...
# Optional n-gram data: if $LT_NGRAMS (default ~/Corpora/lt-ngrams) contains an
#   `en/` folder, it is auto-mounted via --languagemodel — statistical detection of
#   confusable pairs (affect/effect, their/there) that rule-based checking misses.
#   Download "ngram data" from languagetool.org (~15 GB unpacked; the Lucene index
#   is lazily loaded, so it does not eat RAM). Entirely optional — without it the
#   script runs exactly as before.
#
# Usage:
#   lt_check.sh <file> [--variant en-US|en-GB|en-CA|en-AU] [--json] [--keep]
#   Accepts .tex/.latex/.qmd/.rmd/.md/.markdown/.txt; markup is converted to plain
#   prose by pandoc first (code/math/citation keys stripped by lt_strip_noprose.lua).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FILTER="$HERE/lt_strip_noprose.lua"
# LanguageTool binary: env override, else whatever's on PATH.
LT="${LT:-$(command -v languagetool || true)}"
# Optional n-gram data dir: mounted only if it exists; absent = run as before.
NGRAMS="${LT_NGRAMS:-$HOME/Corpora/lt-ngrams}"

VARIANT="en-US"; JSON=0; KEEP=0; FILE=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --variant) VARIANT="$2"; shift 2 ;;
    --json)    JSON=1; shift ;;
    --keep)    KEEP=1; shift ;;
    -h|--help) grep '^#' "$0" | grep -v '^#!' | sed 's/^# \{0,1\}//' | head -28; exit 0 ;;
    -*) echo "unknown option: $1" >&2; exit 2 ;;
    *)  FILE="$1"; shift ;;
  esac
done

[[ -z "$FILE" ]] && { echo "usage: lt_check.sh <file> [--variant en-US|en-GB] [--json]" >&2; exit 2; }
[[ -f "$FILE" ]] || { echo "file not found: $FILE" >&2; exit 2; }
[[ -n "$LT" && -x "$LT" ]] || { echo "languagetool not found (brew install languagetool), or set LT=/path/to/languagetool" >&2; exit 3; }

ext="${FILE##*.}"; ext="$(echo "$ext" | tr '[:upper:]' '[:lower:]')"
case "$ext" in
  tex|latex)            FROM="latex" ;;
  qmd|rmd|md|markdown)  FROM="markdown" ;;
  txt|"")               FROM="" ;;
  *)                    FROM="markdown" ;;
esac

TMP="$(mktemp -t ltcheck).txt"
cleanup() { [[ "$KEEP" -eq 1 ]] || rm -f "$TMP"; }
trap cleanup EXIT

if [[ -z "$FROM" ]]; then
  cp "$FILE" "$TMP"
else
  command -v pandoc >/dev/null || { echo "pandoc needed to convert $ext (brew install pandoc)" >&2; exit 3; }
  pandoc -f "$FROM" -t plain --wrap=none --lua-filter="$FILTER" "$FILE" \
    | sed -E 's/[[:space:]]+([.,;:!?)])/\1/g' > "$TMP"
fi
[[ "$KEEP" -eq 1 ]] && echo "[intermediate plain text: $TMP]" >&2

# macOS ships bash 3.2, where expanding an empty array under `set -u` errors out —
# hence the ${arr[@]+...} guard.
NGRAM_OPT=()
[[ -d "$NGRAMS/en" ]] && NGRAM_OPT=(--languagemodel "$NGRAMS")

if [[ "$JSON" -eq 1 ]]; then
  "$LT" -l "$VARIANT" ${NGRAM_OPT[@]+"${NGRAM_OPT[@]}"} --json "$TMP"
else
  echo "== LanguageTool ($VARIANT) == $FILE"
  "$LT" -l "$VARIANT" ${NGRAM_OPT[@]+"${NGRAM_OPT[@]}"} "$TMP"
fi
