---
name: verify-citations
description: Check whether in-text citations are actually supported by the cited source, and in the right direction, plus authoritative DOI/ISBN checks and a retraction scan. Use when the author says "verify citations", "check the citations are right", "does this match the source", "citation check", "has anything I cite been retracted". Reads the actual source text; flags anything it can't confirm.
---

# verify-citations — check citations against the real source

> Generated from the Research Writing Kit; adapt to what's installed.
> Requires the reference PDFs (see `fetch-refs`). Never fabricate support.

## Input — feed the source file, not a converted one
Work from the draft's **source** (`.md` / `.qmd` / hand-written `.tex`). ⚠️ Never feed
a `.tex` that pandoc produced from markdown: conversion flattens `[@key]` into literal
"(Liu et al., 2023)" text and drops every `\cite{}`, so extraction finds 0 citations,
exits clean, and the whole check *looks* like there was nothing to verify while none of
it ran. If you see "0 citations" on a draft that visibly has author-year references,
that is the cause. (The same conversion also expands tables and duplicates numbers,
which inflates the uncited-claim scan.)

## Iron rules
1. **Per-clause attribution.** One sentence often carries several citations, each
   supporting a different clause ("advocates X [@a], and frames Y [@b]"). Never hand a
   whole sentence to the check for a single source — the clause that belongs to the
   neighbouring citation gets charged to the wrong paper. In practice most raw flags on
   compound sentences are this artefact, so **compound sentences get a human second
   look** after the pass: match each flag to the *position* of its citation marker
   before calling it a problem.
2. **Read the source, never recall it.** Every verdict carries a verbatim quote.
3. **Quote grounding.** Every quote offered as evidence is checked back into the PDF
   text by **plain string matching** (fuzzy, no LLM). A quote that isn't there
   (`UNGROUNDED`) means the reader may have paraphrased or invented; that verdict is
   void — rerun or check by hand. This is the one layer that breaks the "an LLM checks
   an LLM" loop; don't skip it.
4. **`supported` means "checked and it looks right", not "proven true."** The final
   word belongs to someone who knows the theory and reads the original.
5. IDs and retractions use **deterministic scripts**, not an agent.

## Method
For each "claim + citation" pair in the draft:
1. **Read the cited source** (the PDF, not the abstract) and locate the passage
   that supports — or fails to support — the claim.
2. Judge **direction**: does the source actually say this, and does it point the
   way the draft uses it? (A source that says the *opposite* is a common, serious
   error.)
3. **Authoritative ID check:** DOI via Crossref, ISBN via OpenLibrary — confirm the
   reference resolves to a real, correctly-described work. Entries with neither →
   OpenAlex title search, Semantic Scholar as fallback (preprints, forthcoming).
4. Verdict per pair: **supported / partially / unsupported / wrong-direction /
   ❓unverifiable**, each with a quoted line from the source, plus a **severity
   weighted by the citation's purpose**: a mismatch on a citation used as
   *evidence*, *contrast* or *method* = **FAIL**; on an *attribution* ("X proposed
   the term") = **WARN**; on *background/context* = **INFO — still listed, never
   dropped**. Sort by severity; read the FAILs first; then split "real problem (edit)"
   from "false alarm (citation is fine)".

## Retraction scan — every delivery
```bash
python3 tools/refs/retraction_scan.py --bib references.bib
```
Crossref update relations + OpenAlex `is_retracted`, two sources cross-checked.
`RETRACTED` hits are **confirmed by a human** (matching is fuzzy) and, if real, the
source is replaced and the skeleton node updated. **`NO_DOI` is not "scanned"** —
books and pre-DOI works have nothing to match against, so a scan with many `NO_DOI`
rows is not 100 % coverage; report them as unscanned. Rerunning `NO_DOI` rows changes
nothing; only `API_ERROR` rows are worth a retry. Retractions are ongoing: a scan
before the last submission says nothing about this one.

## Adversarial pass (recommended)
For anything flagged, run a second review with **fresh context** — the kit ships
a subagent template for exactly this: `agents/citation-skeptic.md` (a *calibrated*
skeptic that presumes the citation correct and upholds only on verbatim
contradiction in the source). If subagents aren't set up, do the same thing
manually as a separate pass under the same calibration. Two failure modes, one
guard each: the first pass rationalizes plausible-but-wrong citations (→ this
second look), and an *uncalibrated* skeptic convicts standard citations of
foundational works (→ the presumption-of-correctness rules in the template).

## Rules
- ⚠️ Couldn't get the full text (paywall/Cloudflare) → `❓unverifiable`, never
  "confirmed."
- **Scanned PDFs with no text layer, and CJK-heavy PDFs:** if MinerU is installed
  (see `setup/TOOLS.md`), prefer `mineru -p <pdf> -o <outdir> [-s start -e end]` and
  read the produced markdown — it handles scans, CJK layouts, complex tables and
  formulas well. Fallback: render pages to images (`pdftoppm`) and read them visually
  (slower). For books, extract only the intro / relevant chapters.
- Names/dates/spellings are checked even in "fact-locked" existing drafts — an old
  typo protected as "don't rewrite" otherwise propagates.
- **Co-cited pairs** (`\cite{a,b}` / `[@a; @b]`) share one clause; each source may
  carry only part of it. Mark the shared part *partially* rather than *unsupported*,
  and let the human pass settle attribution — it can't be done fully automatically.
- **Republished works:** a year mismatch between the cited version (an early web
  text) and the DOI's version (a later journal reprint) is usually deliberate. Flag
  as ⚠️ for a human, not as an error.
- **Model choice:** reading a PDF and returning a quote is mechanical — a cheaper,
  faster model is fine for the per-source readers and for the skeptic second review;
  keep the strongest model for the whole-draft synthesis and the final report. If
  subagents are used, set the model explicitly on each rather than inheriting.
- Never upload the unpublished draft to a cloud service to do this.

## Not this skill
Claims **without** a citation marker are invisible here — run
`tools/claims/uncited_claims_scan.py` (see `paper-review` Layer 5 / `co-author` 6-1a).

## Output
A table: claim / citation / purpose / severity / verdict / supporting quote (grounded
✓) / location, the retraction-scan summary (scanned / `NO_DOI` unscanned / hits), and
the `❓unverifiable` list called out for the author.
