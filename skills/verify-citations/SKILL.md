---
name: verify-citations
description: Check whether in-text citations are actually supported by the cited source, and in the right direction, plus authoritative DOI/ISBN checks and a retraction scan. Use when the author says "verify citations", "check the citations are right", "does this match the source", "citation check", "has anything I cite been retracted". Reads the actual source text; flags anything it can't confirm.
---

# verify-citations: check citations against the real source

> Generated from the Research Writing Kit; adapt to what's installed.
> Requires the reference PDFs (see `fetch-refs`). Never fabricate support.

## Input: feed the source file, not a converted one
Work from the draft's **source** (`.md` / `.qmd` / hand-written `.tex`). ⚠️ Never feed
a `.tex` that pandoc produced from markdown: conversion flattens `[@key]` into literal
"(Liu et al., 2023)" text and drops every `\cite{}`, so extraction finds 0 citations,
exits clean, and the whole check *looks* like there was nothing to verify while none of
it ran. If you see "0 citations" on a draft that visibly has author-year references,
that is the cause. (The same conversion also expands tables and duplicates numbers,
which inflates the uncited-claim scan.)

🔴 **Citations with a locator or prefix.** `[@feng2020, 170]`, `[@a, sec. 2.2.1]` and
`[see @b; @c, chap. 13]` are single citations of `feng2020`, `a`, `b` and `c`. Take only
the key after `@` and keep the locator ("170", "sec. 2.2.1") beside it: it tells you which
page to read. An extractor that treats "feng2020, 170" as the key finds no such entry and
skips it silently; one that splits sentences on every ". " cuts the bracket at "sec." and
loses the marker. A real draft lost 15 of 47 cited works this way while the run still
printed a clean count. **Reconcile before you trust the run:** the number of works you
checked must equal the number of distinct `@key`s in the draft, and every key the draft
cites but the `.bib` lacks is listed, never skipped.

## Iron rules
1. **Per-clause attribution.** One sentence often carries several citations, each
   supporting a different clause ("advocates X [@a], and frames Y [@b]"). Never hand a
   whole sentence to the check for a single source. The clause that belongs to the
   neighbouring citation gets charged to the wrong paper. In practice most raw flags on
   compound sentences are this artefact, so **compound sentences get a human second
   look** after the pass: match each flag to the *position* of its citation marker
   before calling it a problem.
2. **Read the source, never recall it.** Every verdict carries a verbatim quote.
3. **Quote grounding.** Every quote offered as evidence is checked back into the PDF
   text by **plain string matching** (fuzzy, no LLM). A quote that isn't there
   (`UNGROUNDED`) means the reader may have paraphrased or invented; that verdict is
   **not trustworthy**. Rerun or check by hand. This is the one layer that breaks the
   "an LLM checks an LLM" loop; don't skip it.
   🔴 *Untrustworthy is not the same as wrong.* Measured case: a 41-citation draft had
   exactly one citation that really pointed the wrong way, and it was the one both
   readers judged `unsupported` while **both of their quotes failed grounding** (they
   had paraphrased instead of quoting; their judgement was right). Treating every
   `UNGROUNDED` as "verdict void, ignore" would have let the only real error through.
   The correct move is to **open the source yourself** at that passage. Neither
   accept the verdict wholesale nor throw it away. (That batch: 104 quotes, 61
   grounded, 22 paraphrased, 19 ungrounded, 2 without a quote.)
4. **`supported` means "checked and it looks right", not "proven true."** The final
   word belongs to someone who knows the theory and reads the original.
5. IDs and retractions use **deterministic scripts**, not an agent.
   Two structural noise sources when matching **books** by title, worth recognising
   on sight: DOIs under `10.5860/choice.*` are *Choice: Current Reviews for Academic
   Libraries*: a review journal with **one same-titled review per academic book**,
   so a book resolves to its review and is reported as "year mismatch"; treat that
   prefix as a false match without further checking (same pattern: same-titled book
   reviews in other journals). And titles of three words or fewer collide with
   unrelated papers. Title matching has no discriminating power there; verify those
   by author + year, not title.

## Method
For each "claim + citation" pair in the draft:
1. **Read the cited source** (the PDF, not the abstract) and locate the passage
   that supports or fails to support the claim.
2. Judge **direction**: does the source actually say this, and does it point the
   way the draft uses it? (A source that says the *opposite* is a common, serious
   error.)
3. **Authoritative ID check:** DOI via Crossref, ISBN via OpenLibrary, to confirm the
   reference resolves to a real, correctly-described work. Entries with neither →
   OpenAlex title search, Semantic Scholar as fallback (preprints, forthcoming).
   🔴 **Crossref: only a 404 means "DOI not found".** A timeout, an SSL error, a 429 or a
   5xx says nothing about the DOI. Retry those (three tries with a short wait), and if
   they still fail, report the entry as "Crossref query failed, not checked" instead of
   as a bibliography problem. A checker that treated every exception as "not found"
   reported 2, then 5, then 1 missing DOIs on three runs of the same `.bib`, while every
   one of them resolved when queried directly.
   🔴 **OpenLibrary endpoints (checked 2026-09-19).** `…/api/books?bibkeys=ISBN:…`
   now returns 404 for everything while the site itself is up, so code written
   against it reports "not in OpenLibrary" for every book — a verification that
   silently never happens. Use `https://openlibrary.org/isbn/<isbn>.json`: it is
   exact and 404s only when the book really is absent.
   ⚠️ `search.json?q=isbn:<isbn>` is a **fuzzy** search, not a lookup: a
   nonexistent-but-valid ISBN came back with three hits, the first an unrelated
   book. If you use it to add author/year, keep only a doc whose `isbn` field
   actually contains your ISBN **and** whose title matches the exact record —
   OpenLibrary search docs are work-level and aggregate many editions' ISBNs, so
   ISBN membership alone let one book's author and year attach to another book's
   title.
   ⚠️ Separate "the API failed" from "the book is not there". Only the second is a
   finding about the bibliography; the first is a finding about your run, and
   folding them together is how a broken checker looks like a clean report.
   ⚠️ **Author fields arrive at different granularities.** Crossref's `family` is a
   surname; OpenLibrary's `author_name` is a full name ("Alain Depocas"). Compare the
   folded whole string *and* its last token on both sides, or a bib entry written as
   "Depocas" fails to match "Alain Depocas" and a correct reference gets reported as
   wrong. Two entries were misreported this way before both forms were kept. Keep
   particles attached too ("van Dijk", "de Souza"), since a bib may write either form.
4. Verdict per pair: **supported / partially / unsupported / wrong-direction /
   ❓unverifiable**, each with a quoted line from the source, plus a **severity
   weighted by the citation's purpose**: a mismatch on a citation used as
   *evidence*, *contrast* or *method* = **FAIL**; on an *attribution* ("X proposed
   the term") = **WARN**; on *background/context* = **INFO, still listed, never
   dropped**. Sort by severity; read the FAILs first; then split "real problem (edit)"
   from "false alarm (citation is fine)".

## Retraction scan, every delivery
```bash
python3 tools/refs/retraction_scan.py --bib references.bib
```
Crossref update relations + OpenAlex `is_retracted`, two sources cross-checked.
`RETRACTED` hits are **confirmed by a human** (matching is fuzzy) and, if real, the
source is replaced and the skeleton node updated. **`NO_DOI` is not "scanned"**:
books and pre-DOI works have nothing to match against, so a scan with many `NO_DOI`
rows is not 100 % coverage; report them as unscanned. Rerunning `NO_DOI` rows changes
nothing; only `API_ERROR` rows are worth a retry. Retractions are ongoing: a scan
before the last submission says nothing about this one.

## Adversarial pass (recommended)
For anything flagged, run a second review with **fresh context**, the kit ships
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
  read the produced markdown. It handles scans, CJK layouts, complex tables and
  formulas well. Fallback: render pages to images (`pdftoppm`) and read them visually
  (slower). For books, extract only the intro / relevant chapters.
- Names/dates/spellings are checked even in "fact-locked" existing drafts. An old
  typo protected as "don't rewrite" otherwise propagates.
- **Co-cited pairs** (`\cite{a,b}` / `[@a; @b]`) share one clause; each source may
  carry only part of it. Mark the shared part *partially* rather than *unsupported*,
  and let the human pass settle attribution. It can't be done fully automatically.
- **Republished works:** a year mismatch between the cited version (an early web
  text) and the DOI's version (a later journal reprint) is usually deliberate. Flag
  as ⚠️ for a human, not as an error.
- **Model choice:** the two halves of this skill want different models. Reading a PDF
  and returning a quote is mechanical, so the per-source readers run fine on a cheaper,
  faster model. The skeptic second review is not mechanical: it decides whether a
  source contradicts a claim, and on the author's own citation set the strongest tier
  was right 0.95 of the time against 0.75 for the mid tier. Run the second review, the
  whole-draft synthesis and the final report on the strongest model available. If
  subagents are used, set the model explicitly on each rather than inheriting, so the
  split survives whatever the main session happens to be running.
- Never upload the unpublished draft to a third-party cloud service to do this.

## Not this skill
Claims **without** a citation marker are invisible here. Run
`tools/claims/uncited_claims_scan.py` (see `paper-review` Layer 5 / `co-author` 6-1a).

## Output
A table: claim / citation / purpose / severity / verdict / supporting quote (grounded
✓) / location, the retraction-scan summary (scanned / `NO_DOI` unscanned / hits), and
the `❓unverifiable` list called out for the author.
