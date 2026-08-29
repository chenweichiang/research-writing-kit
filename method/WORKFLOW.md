# The Method — The Full Pipeline

> The 8-phase pipeline, generalized and language-neutral. This is what the
> `co-author` skill orchestrates. Each phase notes what it needs in **lite mode**
> (Claude + web only) versus **full mode** (optional local tools from
> `setup/TOOLS.md`). Nothing here requires the full tools; they only make it faster
> or more rigorous.

## Phase 0 — Intake (the author decides what to write)

Get: (1) the topic, sources, or which existing draft to work on — messy is fine;
(2) the **target venue and output language**; (3) whether there's existing data to
analyze; (4) the mode (default "write it to good", or explicit skeleton-first);
(5) whether there's an **existing draft** to work from → if so, Phase 0.5 first.

## Phase 0.5 — Onboard an existing draft (only if one exists)

Before writing a single new word:
1. **Provenance triage.** Which passages did the author write themselves vs
   AI/mixed? Author-written = voice asset → preserve, minimal edits only, no
   wholesale rewrite. Only AI/mixed/authorized passages get heavy edits. When
   unsure, ask.
2. **Reverse-extract the skeleton** from the existing draft (claim / evidence /
   so-what per section) so the old draft enters the same source-of-truth system.
3. **Treat all existing citations as unverified** — re-run verification; re-check
   format against the *new* target venue. "Fact-locked" ≠ "check-exempt": names,
   dates, spellings still get checked against authoritative sources (an old typo
   protected as "don't rewrite" will otherwise propagate).
4. **Produce a disposition table**: mark each section keep / light-edit / rewrite /
   new-write, one reason each, plus a content-gap list.
5. **Read a real sample of the material before judging feasibility** — never judge
   research value from filenames, file counts, or folder structure. Sample-read
   3–5 items across the quality spectrum first.

> **Before a journal/conference submission, check the ledger.** Simultaneous
> submission is forbidden almost everywhere and is a *cross-project* problem: the same
> manuscript, retitled and sent to a second venue, looks clean from inside either
> project folder. Keep one `SUBMISSIONS.tsv` above all projects
> (`tools/submissions/check_submissions.py`), never change a `manuscript_id` when you
> retarget, and update the row the day a status changes — a stale "under review" from
> eight months ago guards nothing.

> **Inventory text recycling when onboarding an existing draft.** Every onboarding case
> *is* reuse: a short paper being extended, a talk becoming an article, last year's
> proposal, a student report. Reuse is legitimate — **not disclosing it is not**, and
> similarity software matches you against your own earlier work. Method and background
> can be reused within reason; **results and discussion cannot**. Rewrite what you can,
> cite yourself for what you can't, and state the extension in the cover letter.
> Conference-to-journal extension is the normal case and usually welcome, but venues
> state how much new material they expect. If the source is student work, the authorship
> and consent questions are separate from the recycling one — settle both.

## Phase 1 — Two-track scouting

### Track A — Literature & prior work (classics + recent hot)
- **Lite:** WebSearch + Semantic Scholar / OpenAlex citation graphs to find what
  the field considers canonical and what's newly hot around your seed papers.
- **Full:** also query a local literature RAG for full-text you already hold.
- 🔴 Whatever you hold locally is a *convenience sample*, not "what the field's
  classics are." "Not in my library" ≠ "doesn't exist." Let the citation graph,
  not your shelf, decide what should be cited. Never invent a citation to fill a gap.
- **Phase 1A — leave a search trail.** Record *how* the literature was found, in
  `venue-notes.md` or a `search-log.md`: which databases (OpenAlex / Semantic
  Scholar / web / your own library), the query strings, the date, inclusion and
  exclusion criteria, hit counts per step. Why: a reviewer asking "why is X
  missing?" gets an answer about the strategy's boundary rather than a shrug;
  retargeting the paper six months later doesn't start from zero; and any paper
  with a review component may be asked for this table outright (PRISMA-style).

### Track B — Venue format & review norms (do this every time, for the current cycle)
Standards and formats change yearly — memory and last-cycle impressions are traps.
Research the **current** official call: length limits, format rules, required
attachments/templates, blind-review rules, and what reviewers actually weigh.
Grab the official template (or, absent one, measure the format of the author's
past submitted PDFs). Save findings to `venue-notes.md` in the project folder —
you'll write to it and tick against it at final check.

**Record the preprint policy while you are there.** Venues differ sharply: most accept
preprints, a few treat them as prior publication and will desk-reject, and some require
the preprint link and version to be declared at submission. Note whether you may post,
when, any embargo after acceptance, and whether the accepted manuscript and the version
of record are treated differently. ⚠️ A preprint server is **not** a submission — but
two journals at once is; keep the two questions apart.

## Phase 1.5 — Direction summary (non-blocking by default)

Compress "gap / angle + contribution claim + main argument line + recommended
venue (with alternatives and why)" to **one page** and show the author.
🔴 **The target venue is the author's call, not an internal decision** — surface
"where to submit" as explicit options (it affects their tenure points, timeline,
cost). In default mode you may proceed on the recommended venue while the question
is out; in skeleton mode, wait for the nod.

## Phase 2 — Verify & fetch (kill hallucinated citations)

- **Lite:** open each source, read enough to confirm it says what you cite it for
  and in the right direction; check DOIs/ISBNs against Crossref / OpenLibrary.
- **Full:** `fetch-refs` (multi-source + institutional access) to pull full texts,
  then `verify-citations` (an agent per paper actually reads the PDF).
- ⚠️ Some publishers block automated fetch; if you can only view in a browser,
  mark `❓unverified` rather than treating it as confirmed.

## Phase 3 — Method / analysis (in parallel with the skeleton)

Decide whether this paper needs to *design a method* (collecting new data) or
*analyze existing data*.
- **Design:** follow the venue's methodological playbook. **First diagnose whether
  the design can answer the question** (bias and coverage, not only power — see
  Phase 3.5); *then* estimate sample size. High power with low coverage is a biased
  design, and adding participants makes it worse. A single-group pre/post cannot
  separate the intervention from testing / maturation effects: add a control
  (waitlist, stepped) or downgrade the claim to non-causal in the text. Pre-register
  here if you will — this is the moment the hypotheses and analysis plan exist and
  the data doesn't.
- **Analyze — lite:** describe the design honestly and state what analysis is
  appropriate; do simple summaries carefully. **Full:** run it in R/Python/Jupyter.
- Iron rules: **data stays local; effect sizes + CIs; Likert → ordinal models,
  not means; seeds fixed.** Fold results (numbers + effect sizes) back into the
  skeleton nodes that need them — and into the **numbers ledger** (Iron Rule 8;
  format from `skills/doc-regress`, template `tools/regress/numbers-ledger.template.md`).
  Every number that will appear in prose gets a row: value, where it came from, the
  script/command, seed. This is the only defense once the draft starts iterating.

### Phase 3.5 — Design diagnosis (only when new data will be collected *and* an effect claimed)

Phase 3 answers "given this design, which test?" This step asks the prior
question: **can this design answer the question at all?** A correctly chosen test
on a biased design still returns a confident wrong answer.
- **Full:** declare the design (model / inquiry / data strategy / answer strategy)
  and run a Monte-Carlo diagnosis (R `DeclareDesign`). Read **coverage** (the share
  of CIs that contain the true value; should be ≈.95), not just power. Power ≈1
  with coverage ≈0 means the design guarantees a significant result whether or not
  the intervention works. Compare "add participants" against "add a control" —
  the control usually wins.
- **Lite:** reason it through in words — what besides the intervention could move
  the outcome, and does the design let you tell them apart? State the claim's
  ceiling honestly.
- Output goes back into the skeleton's `load-bearing-assumptions / open-rebuttals`
  field and into the limitations section — as numbers where you have them.
- Skip for purely descriptive, qualitative, or research-through-design papers;
  forcing it there manufactures false precision.
- Same honesty ceiling as Phase 4.5: the diagnosis is only as good as the
  data-generating process you declared. Wrong declaration → confident wrong
  diagnosis. The declaration itself is human-reviewed; it is an internal
  diagnostic, not a deliverable.

## Phase 4 — Build the argument skeleton

Output a structured skeleton; each argument node has four fields:
**claim / move / evidence (a *verified* source, with a source card for anything the
author hasn't read) / so-what**, plus flags: `⚠needs-method`, `⚠needs-analysis`,
`❓citation-unverified`. Core causal/eliminative nodes also get a
`load-bearing-assumptions / open-rebuttals` field.
🔴 The skeleton lives as `skeleton.md` **in the project folder**, not in the chat —
any new session (or any session after a context compaction) reads `skeleton.md` +
`venue-notes.md` + the numbers ledger before doing anything, and every phase ends
by writing its progress back into `skeleton.md` (Iron Rule 8: files are the only
authority; the conversation is not).

### Phase 4.5 — Formalize the core claim (optional; only if there's one core causal claim)
For a paper with a single core causal or eliminative claim, you can stress-test it
with a formal checker to surface hidden premises and un-answered rebuttals, then
fold those into the skeleton's limitations. This is an **internal diagnostic**, not
a deliverable, and it checks *validity, not truth* (see the honesty-ceiling note in
`IRON-RULES.md`). Purely descriptive / review papers skip this.

## Phase 5 — Write the complete first draft (bound to the skeleton, into the format)

Write section by section, strictly bound to the skeleton — no filler (this is the
anti-homogenization point). Follow `venue-notes.md` for structure and format.
- **Default mode:** write the whole first draft (the author needs something
  substantial to react to). **Skeleton mode:** deliver section by section.
- 🔴 **Into the format from version one; the output is a formatted document**, not
  raw markdown (Iron Rule 7).
- **In the author's own language:** match the `VOICE_PROFILE`, then run the
  language toolchain (lite: careful self-review against the voice profile + an
  AI-tic pass; full: the local linters/corpora in `setup/TOOLS.md`).
- **In a second language the author doesn't write:** write strong academic prose,
  de-AI it, and produce an **independent back-translation** for the author to
  sign off on.
- **Both branches end on the overclaim pass** (`tools/claims/overclaim_lint.py`):
  de-AI has two halves — convergence words and cadence on one side, *saying more than
  the data supports* on the other. Removing only the first still reads as machine-
  written, and an unsupported absolute is a substantive fault, not a stylistic one.
  Report-only: keep what the evidence carries (real 0/72 or 100% results are data),
  converge the rest.

## Phase 6 — Whole-draft verification (before handing back — you do all of it)

1. Re-verify **every** in-text citation against the source (`verify-citations`:
   clause-level verdicts, quotes grounded in the source text, severity-weighted).
   1a. **Retraction scan** — the whole bibliography against Crossref update
       relations + OpenAlex (`tools/refs/retraction_scan.py`). Retractions keep
       happening; a clean scan last submission proves nothing today. Hits are
       hand-checked, then the reference is replaced and the skeleton node updated.
   1b. **Uncited-claims scan** — citation checking only sees sentences that carry a
       citation; quantitative / causal / superlative claims *without* one are its
       blind spot, and in design and practice-based papers those are the main
       evidence (`tools/claims/uncited_claims_scan.py`). Each hit is dispositioned
       one of three ways: cite it, point to your own data (ledger row), or soften
       the wording. Nothing undispositioned ships.
   1c. **Numbers-ledger reconciliation** — run the `doc-regress` checks, then walk
       it by hand: every number in the draft has a ledger row, every ledger row has
       a place in the draft. A mismatch is a number with no provenance or an orphan
       from an earlier edit.
   1d. **Figure and table provenance** — each figure/table → the script and data file
       that made it (logged in the ledger); each caption claim → visible in the
       figure; no truncated axes that mislead. Figures are evidence, not decoration.
2. Final format check against `venue-notes.md`, every official hard rule.
   2a. **The six submission declarations**, each marked "written" or "not
       applicable + why" — never blank: generative-AI use disclosure (**always** —
       this pipeline drafts with an AI, so say which tools did which tasks, and that
       the authors take responsibility); research ethics (IRB approval or exemption
       id, consent, identifiable-data handling); data & code availability (and it
       must agree with the ledger — rows marked "raw file not in repo" are exactly
       what a reviewer will ask about); author contributions (CRediT); competing
       interests & funding; pre-registration (link it if it exists; never imply one
       that doesn't). The first two are written even when the venue doesn't ask.
   2b. If the venue names a **reporting guideline** (COREQ / SRQR / TREND / CONSORT /
       STROBE / PRISMA / GRAMMS), the completed checklist is an attachment.
3. Language toolchain clean (per language) **and every overclaim candidate
   adjudicated** — kept with its evidence, or converged; this reruns every delivery,
   because each round of new prose brings new absolutes. For English, the de-cadencing
   pass (`agents/de-cadencing-scholar.md`) after the fingerprint tools are green.
4. **A clean second-pass review** with no drafting context, reviewer's eyes — and
   hand it the project's `ADJUDICATED.md` (decisions already made, with reasons), or
   it will re-raise settled questions as discoveries. Re-opening an adjudicated item
   requires new evidence. This is a judgement task: use the main model, don't
   downgrade.
5. Produce the **verification report** (citations / retraction & uncited scans /
   ledger reconciliation / format tick-sheet incl. declarations / toolchain /
   `❓unverified` list).
6. Deliver = the formatted document + the report (+ back-translation if second-lang).

## Phase 7 — Iterate with the author (repeat until good)

The author reads the complete draft and says what to change.
- 🔴 **Skeleton = source of truth.** Substantive changes (argument, evidence,
  structure) get written back into `skeleton.md`. Pure wording polish doesn't.
- If the author says "this citation feels off" → go back to Phase 1–2, swap the
  evidence in that node only; don't rebuild the argument.
- Every iteration is re-formatted and re-delivered, not a markdown diff.
- 🔴 **Numbers: ledger first, prose second.** Re-run the analysis → update the
  ledger → *then* edit the draft → run `doc-regress`. The order is not optional:
  editing the prose first hides the stale value from the recurrence check.
- **Any newly written paragraph → re-run the uncited-claims scan.** New prose almost
  always brings new uncited claims; the waivers you added last round only cover the
  old sentences.
- **Close every round by writing back** to `skeleton.md`'s `## Progress` block —
  what changed, why, what's left. Phase 7 has the most rounds and the most session
  boundaries; this is where drift accumulates (Iron Rule 8).
- After big changes, re-run the affected checks (citations / format / and if the
  core claim's structure changed, Phase 4.5). Finish with a full `paper-review`.

## Phase 8 — After acceptance (submission is not the end)

The most error-prone stage, because by now everyone has relaxed — and a proof, once
signed off, is printed.

### 8.1 Reviews came back
→ the `rebuttal` skill: split the reviews into smallest units, decide every verdict
*before* editing, map each accepted point to a real location in the manuscript, then
verify completeness mechanically. **Declining is legitimate**; declining without
evidence is not, and neither is accepting something that makes the paper worse.

### 8.2 Proofs
Typically a 48–72 hour window, and **for errors only** — substantive changes at this
stage get refused or trigger re-review.

Check: author names and order · funder/grant ids · figure numbers still matching their
in-text references · no table row dropped in typesetting · references not mangled by
the production system · DOIs resolving · and, for non-Latin names and institutions,
that the typesetter did not substitute characters or break the encoding. If any number
changed, reconcile it against the numbers ledger (`skills/doc-regress`;
`tools/regress/numbers-ledger.template.md`) before signing off.

### 8.3 Rights and licence — read before signing
CC-BY vs a traditional transfer is a real choice. ⚠️ **A funder may mandate open
access**; discovering that after signing a transfer is an expensive mistake. Decide
what you need to keep: repository deposit, classroom use, reuse in a future book. Every
co-author, students included, must know and agree to the terms.

### 8.4 Dissemination and closing the loop
Post the preprint or repository copy according to the embargo you recorded in Phase 1
(the accepted manuscript and the version of record usually have different rules). Then
**update the submission ledger to `published`** — a ledger that is not updated means
the next duplicate-submission check runs on stale data. Record the DOI in the project
README: you will need it when you cite yourself, and it is the evidence behind any
future text-recycling disclosure.
