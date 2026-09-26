# Lite mode: zero installs, just Claude + the web

> The default path for most people, especially non-technical authors. Everything in
> the method works here; the optional local tools (`TOOLS.md`) only make it faster or
> more rigorous. A generated skill in lite mode must never reference a tool that
> isn't installed as if it exists.

## What lite mode uses
- **Literature:** WebSearch + Semantic Scholar / OpenAlex / Crossref (all free, no
  install). Citation graphs tell you what to cite; the web fetches open-access PDFs.
  **Literature map** (candidate classics for a topic, Phase 1 / `method/RIGOR_PROCESS.md`
  stage 3): without `tools/refs/lit_map.py`, pull the reference lists of 5–8 seed
  papers by hand and count which sources recur across them. Recurring across
  *different authors/venues* is the signal, not any single paper's citation count.
- **Verification:** Claude reads the actual source (open-access PDF or the publisher
  page you can view) and checks the claim's direction. Paywalled + no OA → `❓unverified`.
- **Method decision** (Phase 3.0): without `tools/method/method_decision_check.py`,
  still do the procedure by hand: read 8 comparable studies' methods sections, fill
  the comparison table in `templates/method-decision.template.md` in prose, and check
  off each required section yourself before the author signs off. The check script
  only verifies the sections exist; doing it in prose is not a lesser version of the
  judgment, just of the format nagging.
- **Pre-data-collection plan** (if new data / an effect claim is coming): still write
  `analysis-plan.md` from the template and get eyes on it *before* collecting anything.
  This step's value comes from timing, not tooling, so lite mode has no excuse to
  skip it. Note the commit or send date by hand instead of relying on
  `analysis_plan_check.py` to verify it.
- **Method / analysis:** Claude describes the design honestly and states what analysis
  is appropriate; simple summaries done carefully. (Heavy stats want full mode.)
- **Language / de-AI:** Claude does the convergence-word and AI-syntax passes by hand,
  compares before/after, and (for a second language) produces an independent
  back-translation. (Local linters/corpora are a full-mode upgrade.) **Contrast
  sentences** (*not X but Y*, *X, not Y*, *rather than*, *instead of*, *not only*):
  without `ai_style_diag.py --gate`, count them by hand every revision round: list
  each hit with its shape, get a total, and track whether the total is going down
  round over round, not just whether any single occurrence looks fine in isolation.
  The same rule applies without the tool: fixing an overage by rewriting one shape
  into another doesn't move the total, so don't count it as progress.
- **Register / native polish** (`method/WORKFLOW.md` Phase 5.5): without a corpus or
  Python, the yardstick is still the field, not a rulebook. Read the target journal's
  author guidelines and 2–3 of its papers that the author provides or names, then
  compare the draft with them by reading: self-reference (本研究/本文; *we* / *this
  study*), sentence length and how clauses join, linking words, translationese,
  punctuation, and for English also articles, transitions, nominalizations and
  to-infinitives. Write the deviations down as a short list labelled "a reading, not a
  measurement", fix only what clearly departs from the sample papers, leave stance and
  claim strength to the author, and adjudicate every edit as the full path does. The
  editor agents (`agents/en-native-editor.md`, `agents/zh-tw-native-editor.md`) work
  from that hand-written list when no measured one exists.
- **Formatting:** Claude produces the cleanest export it can and, if there's no
  typesetting toolchain, is explicit that a final layout pass is still needed. For a
  proper PDF, a minimal Typst/Quarto install is the first upgrade worth making.
- **Pre-delivery scans still run in lite mode:** the bundled retraction scan
  (`tools/refs/retraction_scan.py`), uncited-claims scan
  (`tools/claims/uncited_claims_scan.py`), and document-regression checks
  (`tools/regress/`, via the `doc-regress` skill) need only Python 3 and, for the
  retraction scan, the network. No install. Lite mode is not an excuse to skip them.

## The one honesty caveat in lite mode
Lite mode can't run local statistical tests or a corpus-anchored style baseline, and a
register comparison against 2–3 sample papers is a reading, not a percentile. Say which
one the author got. That's fine for most writing, but if the paper's contribution *is* a quantitative result, tell
the author plainly that the stats deserve the full-mode tools (or a statistician), and
don't overstate what a by-hand check proves.

## When to suggest upgrading
Only when the author hits a real wall: many papers to fetch behind a paywall, a genuine
quantitative analysis, or a high-stakes de-AI pass before a top-venue submission. Then
point them at `TOOLS.md`: one tool at a time, never a big-bang install.
