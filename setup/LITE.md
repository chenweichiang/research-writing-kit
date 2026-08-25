# Lite mode — zero installs, just Claude + the web

> The default path for most people, especially non-technical authors. Everything in
> the method works here; the optional local tools (`TOOLS.md`) only make it faster or
> more rigorous. A generated skill in lite mode must never reference a tool that
> isn't installed as if it exists.

## What lite mode uses
- **Literature:** WebSearch + Semantic Scholar / OpenAlex / Crossref (all free, no
  install). Citation graphs tell you what to cite; the web fetches open-access PDFs.
- **Verification:** Claude reads the actual source (open-access PDF or the publisher
  page you can view) and checks the claim's direction. Paywalled + no OA → `❓unverified`.
- **Method / analysis:** Claude describes the design honestly and states what analysis
  is appropriate; simple summaries done carefully. (Heavy stats want full mode.)
- **Language / de-AI:** Claude does the convergence-word and AI-syntax passes by hand,
  compares before/after, and — for a second language — produces an independent
  back-translation. (Local linters/corpora are a full-mode upgrade.)
- **Formatting:** Claude produces the cleanest export it can and, if there's no
  typesetting toolchain, is explicit that a final layout pass is still needed. For a
  proper PDF, a minimal Typst/Quarto install is the first upgrade worth making.
- **Pre-delivery scans still run in lite mode:** the bundled retraction scan
  (`tools/refs/retraction_scan.py`), uncited-claims scan
  (`tools/claims/uncited_claims_scan.py`), and document-regression checks
  (`tools/regress/`, via the `doc-regress` skill) need only Python 3 and, for the
  retraction scan, the network — no install. Lite mode is not an excuse to skip them.

## The one honesty caveat in lite mode
Lite mode can't run local statistical tests or a corpus-anchored style baseline. That's
fine for most writing, but if the paper's contribution *is* a quantitative result, tell
the author plainly that the stats deserve the full-mode tools (or a statistician), and
don't overstate what a by-hand check proves.

## When to suggest upgrading
Only when the author hits a real wall: many papers to fetch behind a paywall, a genuine
quantitative analysis, or a high-stakes de-AI pass before a top-venue submission. Then
point them at `TOOLS.md` — one tool at a time, never a big-bang install.
