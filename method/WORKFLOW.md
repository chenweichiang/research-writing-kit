# The Method: The Full Pipeline

> The 8-phase pipeline, generalized and language-neutral. This is what the
> `co-author` skill orchestrates. Each phase notes what it needs in **lite mode**
> (Claude + web only) versus **full mode** (optional local tools from
> `setup/TOOLS.md`). Nothing here requires the full tools; they only make it faster
> or more rigorous.
>
> For the method-decision step (Phase 3.0) see `method/METHOD_DECISION.md` (the
> decision procedure) and `method/METHOD_CARDS.md` (per-method analysis cards).
> For the full rigor checklist behind the literature → argument → method pipeline
> (thirteen stages, each with its methodological rationale), see
> `method/RIGOR_PROCESS.md`: this file does not repeat that content, only points
> to it at the relevant phase.

## Phase 0: Intake (the author decides what to write)

Get: (1) the topic, sources, or which existing draft to work on (messy is fine);
(2) the **target venue and output language**; (3) whether there's existing data to
analyze; (4) the mode (default "write it to good", or explicit skeleton-first);
(5) whether there's an **existing draft** to work from → if so, Phase 0.5 first.

## Phase 0.5: Onboard an existing draft (only if one exists)

Before writing a single new word:
1. **Provenance triage.** Which passages did the author write themselves vs
   AI/mixed? Author-written = voice asset → preserve, minimal edits only, no
   wholesale rewrite. Only AI/mixed/authorized passages get heavy edits. When
   unsure, ask.
2. **Reverse-extract the skeleton** from the existing draft (claim / evidence /
   so-what per section) so the old draft enters the same source-of-truth system.
3. **Treat all existing citations as unverified**: re-run verification; re-check
   format against the *new* target venue. "Fact-locked" ≠ "check-exempt": names,
   dates, spellings still get checked against authoritative sources (an old typo
   protected as "don't rewrite" will otherwise propagate).
4. **Produce a disposition table**: mark each section keep / light-edit / rewrite /
   new-write, one reason each, plus a content-gap list.
5. **Read a real sample of the material before judging feasibility**: never judge
   research value from filenames, file counts, or folder structure. Sample-read
   3–5 items across the quality spectrum first.

> **Before a journal/conference submission, check the ledger.** Simultaneous
> submission is forbidden almost everywhere and is a *cross-project* problem: the same
> manuscript, retitled and sent to a second venue, looks clean from inside either
> project folder. Keep one `SUBMISSIONS.tsv` above all projects
> (`tools/submissions/check_submissions.py`), never change a `manuscript_id` when you
> retarget, and update the row the day a status changes. A stale "under review" from
> eight months ago guards nothing.

> **Inventory text recycling when onboarding an existing draft.** Every onboarding case
> *is* reuse: a short paper being extended, a talk becoming an article, last year's
> proposal, a student report. Reuse is legitimate. **Not disclosing it is not**, and
> similarity software matches you against your own earlier work. Method and background
> can be reused within reason; **results and discussion cannot**. Rewrite what you can,
> cite yourself for what you can't, and state the extension in the cover letter.
> Conference-to-journal extension is the normal case and usually welcome, but venues
> state how much new material they expect. If the source is student work, the authorship
> and consent questions are separate from the recycling one. Settle both.

## Phase 1: Two-track scouting

### Track A: Literature & prior work (classics + recent hot)
- **Lite:** WebSearch + Semantic Scholar / OpenAlex citation graphs to find what
  the field considers canonical and what's newly hot around your seed papers.
- **Full:** also query a local literature RAG for full-text you already hold.
- 🔴 Whatever you hold locally is a *convenience sample*, not "what the field's
  classics are." "Not in my library" ≠ "doesn't exist." Let the citation graph,
  not your shelf, decide what should be cited. Never invent a citation to fill a gap.
- **Phase 1A: leave a search trail.** Record *how* the literature was found, in
  `venue-notes.md` or a `search-log.md`: which databases (OpenAlex / Semantic
  Scholar / web / your own library), the query strings, the date, inclusion and
  exclusion criteria, hit counts per step. Why: a reviewer asking "why is X
  missing?" gets an answer about the strategy's boundary rather than a shrug;
  retargeting the paper six months later doesn't start from zero; and any paper
  with a review component may be asked for this table outright (PRISMA-style).

### Track B: Venue format & review norms (do this every time, for the current cycle)
Standards and formats change yearly. Memory and last-cycle impressions are traps.
Research the **current** official call: length limits, format rules, required
attachments/templates, blind-review rules, and what reviewers actually weigh.
Grab the official template (or, absent one, measure the format of the author's
past submitted PDFs). Save findings to `venue-notes.md` in the project folder.
You'll write to it and tick against it at final check.

**Record the preprint policy while you are there.** Venues differ sharply: most accept
preprints, a few treat them as prior publication and will desk-reject, and some require
the preprint link and version to be declared at submission. Note whether you may post,
when, any embargo after acceptance, and whether the accepted manuscript and the version
of record are treated differently. ⚠️ A preprint server is **not** a submission.
Submitting to two journals at once is a submission problem, so keep the two questions apart.

## Phase 1.5: Direction summary (non-blocking by default)

Compress "gap / angle + contribution claim + main argument line + recommended
venue (with alternatives and why)" to **one page** and show the author.
🔴 **The target venue is the author's call, not an internal decision**: surface
"where to submit" as explicit options (it affects their tenure points, timeline,
cost). In default mode you may proceed on the recommended venue while the question
is out; in skeleton mode, wait for the nod.

## Phase 2: Verify & fetch (kill hallucinated citations)

- **Lite:** open each source, read enough to confirm it says what you cite it for
  and in the right direction; check DOIs/ISBNs against Crossref / OpenLibrary.
- **Full:** `fetch-refs` + `tools/refs/pdf_fetch.py` (open-access sources → TLS
  impersonation → a real browser on a persistent profile, plus your institutional
  access) to pull full texts, then `verify-citations` (an agent per paper actually
  reads the PDF).
- ⚠️ Cloudflare-fronted publishers do **not** need to be hand-downloaded. The
  browser layer clears them (measured on ACM/Wiley/SAGE/AIP). What matters is that
  every remaining miss is tagged `PAYWALL` (no entitlement) / `CAPTCHA` (clear it
  once by hand) / `NO-LINK` (tooling gap), so you know which are worth more time.
- ⚠️ Whatever you could not read in full stays `❓unverified`: never treat an
  abstract, or a paper you only saw the landing page of, as confirmed.

## Phase 3.0: Method decision (compare comparable studies first, then choose)

Do this whenever new data will be collected, existing data needs to become a paper,
or a proposal is being written. Full procedure: `method/METHOD_DECISION.md`;
per-method cards: `method/METHOD_CARDS.md`.

🔴 **Check the literature before deciding, regardless of whether you already think
you know the answer.** What's common or appropriate for a field (a research
design, a statistical test, a qualitative approach) is settled by checking
comparable papers, not by memory or a generic playbook. Write the pre-check guess
and the post-check answer side by side, and note anything considered and then
dropped after checking, with the reason.

1. State the claims you want to make and their type (causal / correlational /
   prevalence / interpretive / mechanistic / design knowledge / feasibility).
   The claim type decides the method.
2. Read the methods sections of **at least 8 comparable studies**, filling a
   comparison table (`templates/literature-matrix.template.md`); from **at
   least 5** of them, extract the actual analysis practice into a second table
   (test/model, effect size + CI, correction for quantitative; coding
   approach, inter-rater/reflexivity for qualitative).
3. Shortlist **at least two candidate methods**; for each, write what it can
   and cannot support, how the core construct is actually measured and its
   most plausible alternative explanation, and (the item independent review
   most often finds missing) **a check outside the author's own judgment**
   (a second coder, a blind rater, an external reviewer, or someone else
   collecting the data). Narrowing the claim is not a substitute when the
   researcher is the sole judge.
4. Decide; write a claim-alignment table (downgrade any claim the chosen
   method can't carry) and a premortem (three most likely reasons this fails
   or gets rejected).
5. Produce `method-decision.md` (template: `templates/method-decision.template.md`)
   and run `python3 tools/method/method_decision_check.py method-decision.md`
   before the author signs off. The check proves the required sections
   exist, not that the method is right. Re-run steps 2–4 when the target
   venue changes.

### 🔴 Pre-data-collection plan (hard gate)

If Phase 3.0 calls for new data or an effect claim, write `analysis-plan.md`
(template: `templates/analysis-plan.template.md`, covering ethics approval, stopping
rule, primary analysis or qualitative approach, what result would change your
mind, the independent check, data-in-hand checkpoints, who reviewed the plan)
and commit it **before** collecting anything. Run
`python3 tools/method/analysis_plan_check.py analysis-plan.md` (it checks that
the commit date precedes the start of data collection). Any deviation
afterward goes into the plan's own deviations section. It is never edited into the
earlier sections. This is the only step in the whole pipeline that cannot be
repaired after the fact: pre-registration only has value ahead of the data,
and ethics approval must precede collection. Everything else (literature
synthesis quality, problematization) stays a judgment call guided by the
templates, not a script gate.

## Phase 3: Method / analysis (in parallel with the skeleton)

Decide whether this paper needs to *design a method* (collecting new data) or
*analyze existing data*. **For existing data, first check how comparable papers
in the target field usually analyze this kind of data**: reuse
`method-decision.md`'s analysis-method table if one exists, extend it if the
data type differs, rather than defaulting to a generic recipe.
- **Design:** follow the venue's methodological playbook. **First diagnose whether
  the design can answer the question** (bias and coverage, not only power, as detailed in
  Phase 3.5); *then* estimate sample size. High power with low coverage is a biased
  design, and adding participants makes it worse. A single-group pre/post cannot
  separate the intervention from testing / maturation effects: add a control
  (waitlist, stepped) or downgrade the claim to non-causal in the text. Pre-register
  here if you will. This is the moment the hypotheses and analysis plan exist and
  the data doesn't.
- **Analyze (lite):** describe the design honestly and state what analysis is
  appropriate; do simple summaries carefully. **Full:** run it in R/Python/Jupyter.
- Iron rules: **no third-party uploads; effect sizes + CIs; Likert → ordinal models,
  not means; seeds fixed.** Fold results (numbers + effect sizes) back into the
  skeleton nodes that need them, and into the **numbers ledger** (Iron Rule 8;
  format from `skills/doc-regress`, template `tools/regress/numbers-ledger.template.md`).
  Every number that will appear in prose gets a row: value, where it came from, the
  script/command, seed. This is the only defense once the draft starts iterating.

### Phase 3.5: Design diagnosis (only when new data will be collected *and* an effect claimed)

Phase 3 answers "given this design, which test?" This step asks the prior
question: **can this design answer the question at all?** A correctly chosen test
on a biased design still returns a confident wrong answer.
- **Full:** declare the design (model / inquiry / data strategy / answer strategy)
  and run a Monte-Carlo diagnosis (R `DeclareDesign`). Read **coverage** (the share
  of CIs that contain the true value; should be ≈.95), not just power. Power ≈1
  with coverage ≈0 means the design guarantees a significant result whether or not
  the intervention works. Compare "add participants" against "add a control":
  the control usually wins.
- **Lite:** reason it through in words: what besides the intervention could move
  the outcome, and does the design let you tell them apart? State the claim's
  ceiling honestly.
- Output goes back into the skeleton's `load-bearing-assumptions / open-rebuttals`
  field and into the limitations section, as numbers where you have them.
- Skip for purely descriptive, qualitative, or research-through-design papers;
  forcing it there manufactures false precision.
- Same honesty ceiling as Phase 4.5: the diagnosis is only as good as the
  data-generating process you declared. Wrong declaration → confident wrong
  diagnosis. The declaration itself is human-reviewed; it is an internal
  diagnostic, not a deliverable.

## Phase 4: Build the argument skeleton

Output a structured skeleton; each argument node has four fields:
**claim / move / evidence (a *verified* source, with a source card for anything the
author hasn't read) / so-what**, plus flags: `⚠needs-method`, `⚠needs-analysis`,
`❓citation-unverified`. Core causal/eliminative nodes also get a
`load-bearing-assumptions / open-rebuttals` field.
🔴 The skeleton lives as `skeleton.md` **in the project folder**, not in the chat.
Any new session (or any session after a context compaction) reads `skeleton.md` +
`venue-notes.md` + the numbers ledger before doing anything, and every phase ends
by writing its progress back into `skeleton.md` (Iron Rule 8: files are the only
authority; the conversation is not).

### Phase 4.5: Formalize the core claim (optional; only if there's one core causal claim)
For a paper with a single core causal or eliminative claim, you can stress-test it
with a formal checker to surface hidden premises and un-answered rebuttals, then
fold those into the skeleton's limitations. This is an **internal diagnostic**, not
a deliverable, and it checks *validity, not truth* (see the honesty-ceiling note in
`IRON-RULES.md`). Purely descriptive / review papers skip this.

## Phase 5: Write the complete first draft (bound to the skeleton, into the format)

Write section by section, strictly bound to the skeleton, with no filler (this is the
anti-homogenization point). Follow `venue-notes.md` for structure and format.
- **Default mode:** write the whole first draft (the author needs something
  substantial to react to). **Skeleton mode:** deliver section by section.
- 🔴 **Into the format from version one; the output is a formatted document**, not
  raw markdown (Iron Rule 7).
- **Register, not voice, for papers, grant proposals and applications** (Iron Rule 5):
  aim at the register of same-field published papers in either language. Before
  drafting, read a few paragraphs from papers in the target venue (full:
  `tools/register/register_profile.py --exemplars` picks paragraphs near the venue
  median; lite: 2-3 papers the author names) for sentence length, how clauses join
  and the field's usual self-reference; never copy from them. The `VOICE_PROFILE`
  is for letters, cover letters, bios and personal statements, or when the author
  asks for their own voice.
- **In the author's own language:** run the language toolchain (lite: careful
  self-review against the sample papers + an AI-tic pass; full: the local
  linters/corpora in `setup/TOOLS.md`, with the Chinese voice gate in `--paper`
  mode for papers, proposals and applications).
- **In a second language the author doesn't write:** write strong academic prose,
  de-AI it, and produce an **independent back-translation** for the author to
  sign off on.
- **Both branches end on the overclaim pass** (`tools/claims/overclaim_lint.py`):
  de-AI has two halves: convergence words and cadence on one side, *saying more than
  the data supports* on the other. Removing only the first still reads as machine-
  written, and an unsupported absolute is a substantive fault, not a stylistic one.
  Report-only: keep what the evidence carries (real 0/72 or 100% results are data),
  converge the rest.

## Phase 5.5: Native polish (both languages; after the toolchain passes, before Phase 6)

After many rounds of local patching, translationese and unidiomatic phrasing build
up, and the style tools cannot see it: they measure AI fingerprints, not whether the
text reads like the field. This phase closes that gap.

**Why the yardstick is a distribution, not a rulebook.**
- *Define "native" as "inside the field's range".* Register alignment (Demir &
  Egbert 2026, *Applied Corpus Linguistics*) asks whether a text's linguistic
  features occur at the rates usual for its register. Here that becomes: each
  feature of the draft should fall inside the p10-p90 band of same-field published
  papers. The target is the band, not the median.
- *LLM text is narrower than human text.* Demir & Egbert report that the standard
  deviations for the ChatGPT corpus are generally lower than for the human corpus.
  Prescriptive "purification" rules push every sentence the same way (turn every
  nominalization or 進行 + verb into a bare verb, split every long sentence, ban the
  semicolon) and so move a draft toward that narrow profile, even where the field's
  papers write otherwise. Those rules are right only for features the draft has
  **too much** of.
- *A polish pass that does not know where the draft deviates fixes the surface only.*
  It corrects articles, prepositions and collocations and leaves every register
  deviation where it was. So the editor gets a measured deviation list, and a
  mechanical check verifies that no edit moved a feature the wrong way.
- *"Sound more like a native speaker" is mostly a change of vocabulary.* The rewrite
  prompted that way diversified the essays' word choice and raised their perplexity
  (Liang et al. 2023, *Patterns*), and LLM-processed abstracts carry a surplus of style
  words (Kobak et al. 2025, *Science Advances*). Register is not vocabulary, so lexical
  elevation (swapping plain words for fancier ones) is banned.
- *Language editing is sentence-level work.* Language professionals mostly revise at
  sentence level, while claims and argument are shaped by disciplinary peers (Lillis
  & Curry 2006, *Written Communication*). The editor subagent does the first kind of
  work; anything touching claim strength or argument goes to the author.
- *Eyes alone are not a reliable judge.* Reviewers in applied linguistics could not
  reliably tell AI-written from human-written abstracts (Casal & Kessler 2023,
  *Research Methods in Applied Linguistics*). Acceptance rests on measurement against
  the corpus first, reading second.

**Full mode** (a corpus of same-field published papers; see `setup/TOOLS.md`):
1. Measure: `tools/register/register_profile.py` gives the deviation list per line
   range (to fix / locked / for the author / inside the band), with bounds for each
   range so an editor does not overshoot into the other end of the band.
2. Dispatch one editor per range, in parallel: `agents/zh-tw-native-editor.md`
   (zh-TW addon) or `agents/en-native-editor.md`. Editors return change lists and
   never edit the draft. Stance and claim strength are listed for the author.
3. Self-check: `tools/register/polish_check.py` blocks changed numbers, citations,
   quotations and locked terms, growth past the word budget, new forbidden forms,
   and any feature that moves away from the band (a high feature rising, a low one
   falling, an in-band one pushed out).
4. The main session adjudicates every item (accept / accept rewritten / reject);
   accepted items are written back with `polish_check.py --apply`.
5. Re-measure. For English, `de-cadencing-scholar` runs after the native editor,
   then register is measured once more, because de-cadencing can push phrasal
   coordination or transitions back out of the band.
Feel-reference paragraphs from the corpus are optional: in the method author's small
trial they did not help consistently.

**Lite mode** (no corpus or no Python): read the target journal's author
guidelines and 2-3 of its papers that the author provides or names. Compare the draft
with them by reading, on the same dimensions the tools measure (self-reference,
sentence length and how clauses join, linking words, translationese, punctuation;
for English also articles, transitions, nominalizations and to-infinitives). Write
the deviation list by hand, labelled as a reading, not a measurement. The editor
still returns a change list, and the main session still adjudicates every item.

A professional language editor for an English submission, or a same-field colleague
reading a draft for its argument, still has a place after this phase.

## Phase 6: Whole-draft verification (before handing back, you do all of it)

1. Re-verify **every** in-text citation against the source (`verify-citations`:
   clause-level verdicts, quotes grounded in the source text, severity-weighted).
   1a. **Retraction scan**: the whole bibliography against Crossref update
       relations + OpenAlex (`tools/refs/retraction_scan.py`). Retractions keep
       happening; a clean scan last submission proves nothing today. Hits are
       hand-checked, then the reference is replaced and the skeleton node updated.
   1b. **Uncited-claims scan**: citation checking only sees sentences that carry a
       citation; quantitative / causal / superlative claims *without* one are its
       blind spot, and in design and practice-based papers those are the main
       evidence (`tools/claims/uncited_claims_scan.py`). Each hit is dispositioned
       one of three ways: cite it, point to your own data (ledger row), or soften
       the wording. Nothing undispositioned ships.
   1c. **Numbers-ledger reconciliation**: run the `doc-regress` checks, then walk
       it by hand: every number in the draft has a ledger row, every ledger row has
       a place in the draft. A mismatch is a number with no provenance or an orphan
       from an earlier edit.
   1d. **Figure and table provenance**: each figure/table → the script and data file
       that made it (logged in the ledger); each caption claim → visible in the
       figure; no truncated axes that mislead. Figures are evidence, not decoration.
   1e. **Analysis-plan reconciliation** (if `analysis-plan.md` exists): run
       `python3 tools/method/analysis_plan_check.py analysis-plan.md --phase6`;
       write every deviation, or explicitly "no deviations" (never blank). The
       method section reports any deviation honestly, and anything analyzed
       outside the plan is labeled exploratory, not confirmatory.
   1f. **Literature update**: the field may have moved between when the
       argument was scoped and now. Re-run the Phase 1 keyword search and a
       forward citation snowball (`tools/refs/snowball.py`) for anything
       published since the `search-log.md` start date; fold anything relevant
       into the comparison table or skeleton, and record the check regardless
       of outcome.
2. Final format check against `venue-notes.md`, every official hard rule.
   2a. **The six submission declarations**, each marked "written" or "not
       applicable + why", never blank: generative-AI use disclosure (**always**, because
       this pipeline drafts with an AI. Say which tools did which tasks, and that
       the authors take responsibility); research ethics (IRB approval or exemption
       id, consent, identifiable-data handling); data & code availability (and it
       must agree with the ledger. Rows marked "raw file not in repo" are exactly
       what a reviewer will ask about); author contributions (CRediT); competing
       interests & funding; pre-registration (link it if it exists; never imply one
       that doesn't). The first two are written even when the venue doesn't ask.
   2b. If the venue names a **reporting guideline** (COREQ / SRQR / TREND / CONSORT /
       STROBE / PRISMA / GRAMMS), the completed checklist is an attachment.
3. Language toolchain clean (per language) **and every overclaim candidate
   adjudicated**: kept with its evidence, or converged; this reruns every delivery,
   because each round of new prose brings new absolutes. For English, the de-cadencing
   pass (`agents/de-cadencing-scholar.md`) after the fingerprint tools are green and
   after the Phase 5.5 native polish, followed by a register re-measure.
4. **A clean second-pass review** with no drafting context, reviewer's eyes, and
   hand it the project's `ADJUDICATED.md` (decisions already made, with reasons), or
   it will re-raise settled questions as discoveries. Re-opening an adjudicated item
   requires new evidence. This is a judgement task that needs the strongest model at
   the highest effort. An Agent call can set the model but not the effort, so the
   review runs as a named agent whose definition pins both (`agents/clean-reviewer.md`).
5. Produce the **verification report** (citations / retraction & uncited scans /
   ledger reconciliation / format tick-sheet incl. declarations / toolchain /
   `❓unverified` list).
6. Deliver = the formatted document + the report (+ back-translation if second-lang).

## Phase 7: Iterate with the author (repeat until good)

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
- **Close every round by writing back** to `skeleton.md`'s `## Progress` block:
  what changed, why, what's left. Phase 7 has the most rounds and the most session
  boundaries; this is where drift accumulates (Iron Rule 8).
- After big changes, re-run the affected checks (citations / format / and if the
  core claim's structure changed, Phase 4.5), and Phase 5.5 on the rewritten
  passages: text patched into an old draft is where translationese grows back.
  Finish with a full `paper-review`.

## Phase 8: After acceptance (submission is not the end)

The most error-prone stage, because by now everyone has relaxed, and a proof, once
signed off, is printed.

### 8.1 Reviews came back
→ the `rebuttal` skill: split the reviews into smallest units, decide every verdict
*before* editing, map each accepted point to a real location in the manuscript, then
verify completeness mechanically. **Declining is legitimate**; declining without
evidence is not, and neither is accepting something that makes the paper worse. The
revised passages get the Phase 5.5 native polish before the response letter quotes them.

### 8.2 Proofs
Typically a 48–72 hour window, and **for errors only**: substantive changes at this
stage get refused or trigger re-review.

Check: author names and order · funder/grant ids · figure numbers still matching their
in-text references · no table row dropped in typesetting · references not mangled by
the production system · DOIs resolving · and, for non-Latin names and institutions,
that the typesetter did not substitute characters or break the encoding. If any number
changed, reconcile it against the numbers ledger (`skills/doc-regress`;
`tools/regress/numbers-ledger.template.md`) before signing off.

### 8.3 Rights and licence: read before signing
CC-BY vs a traditional transfer is a real choice. ⚠️ **A funder may mandate open
access**; discovering that after signing a transfer is an expensive mistake. Decide
what you need to keep: repository deposit, classroom use, reuse in a future book. Every
co-author, students included, must know and agree to the terms.

### 8.4 Dissemination and closing the loop
Post the preprint or repository copy according to the embargo you recorded in Phase 1
(the accepted manuscript and the version of record usually have different rules). Then
**update the submission ledger to `published`**: a ledger that is not updated means
the next duplicate-submission check runs on stale data. Record the DOI in the project
README: you will need it when you cite yourself, and it is the evidence behind any
future text-recycling disclosure.
