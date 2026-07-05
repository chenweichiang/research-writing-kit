---
name: verify-citations
description: Check whether in-text citations are actually supported by the cited source, and in the right direction, plus authoritative DOI/ISBN checks. Use when the author says "verify citations", "check the citations are right", "does this match the source", "citation check". Reads the actual source text; flags anything it can't confirm.
---

# verify-citations — check citations against the real source

> Generated from the Research Writing Kit; adapt to what's installed.
> Requires the reference PDFs (see `fetch-refs`). Never fabricate support.

## Method
For each "claim + citation" pair in the draft:
1. **Read the cited source** (the PDF, not the abstract) and locate the passage
   that supports — or fails to support — the claim.
2. Judge **direction**: does the source actually say this, and does it point the
   way the draft uses it? (A source that says the *opposite* is a common, serious
   error.)
3. **Authoritative ID check:** DOI via Crossref, ISBN via OpenLibrary — confirm the
   reference resolves to a real, correctly-described work.
4. Verdict per pair: **supported / partially / unsupported / wrong-direction /
   ❓unverifiable**, each with a quoted line from the source.

## Adversarial pass (recommended)
For anything flagged, run a second, skeptical check (a fresh pass told to default
to "unsupported" unless the source clearly backs the claim). This catches
plausible-but-wrong citations that a single pass rationalizes.

## Rules
- ⚠️ Couldn't get the full text (paywall/Cloudflare) → `❓unverifiable`, never
  "confirmed."
- Names/dates/spellings are checked even in "fact-locked" existing drafts — an old
  typo protected as "don't rewrite" otherwise propagates.
- Never upload the unpublished draft to a cloud service to do this.

## Output
A table: claim / citation / verdict / supporting quote / location, with the
`❓unverifiable` list called out for the author.
