---
name: co-author
description: Collaborative long-form academic writing — papers AND grant/funding proposals. Use when the author says "help me write this paper", "turn these sources into a paper", "develop this", "build the skeleton", "co-author", or wants to write a grant/funding/fellowship proposal, or needs the submission declarations (AI-use disclosure / ethics / data availability / author contributions / competing interests / pre-registration) or asks "what am I missing that should be there", or wants to **decide on a research method** ("should this be quantitative or qualitative", "how do people in my field usually design a study like this", "help me pick a method" — routes to Phase 3.0: compare at least 8 comparable studies' methods before deciding, producing a `method-decision.md`), or has an existing draft to rewrite/upgrade/resubmit ("rewrite this", "it got rejected, submit elsewhere", "turn this talk/old proposal into a journal paper" → Phase 0.5). Division of labor = the author decides what to say and gives final sign-off; Claude verifies literature, researches the venue's current format and review norms, designs method / runs analysis when needed, writes the draft, and self-checks every step. Default = "write it all the way to a verified complete draft"; only build-skeleton-first when the author explicitly asks. For check-only (don't rewrite) → paper-review; for slides → a deck skill.
---

# co-author — collaborative paper / proposal writing

> **This skill was generated from the Research Writing Kit and should be adapted to
> the author.** Placeholders in `<ANGLE BRACKETS>` are filled in at setup.
> Full method: `method/WORKFLOW.md` + `method/PHILOSOPHY.md` + `method/IRON-RULES.md`.

> Author profile (filled at setup):
> - Field: `<FIELD>`
> - Writing language(s): `<LANGUAGE>` (native, voice-matched) / `<SECOND_LANG>` (if any, back-translated)
> - Usual venues: `<VENUES>`
> - Voice profile: `<VOICE_PROFILE_PATH or "none — aim for venue register">`
> - Mode: `<lite | full>` (which tools exist — see the project CLAUDE.md)

## Two modes (decide at intake)

- **Default: "write it to good."** Author names the topic → you go all the way to a
  *verified complete first draft*, then they iterate. Skeleton is built but internal.
- **Skeleton mode** (only if they say "just build the skeleton / develop the
  argument, don't write yet"): hand the skeleton over for sign-off before prose.

## 🔴 Iron rules (from `method/IRON-RULES.md` — do not drop)

1. **Never fabricate a citation.** Every reference is really fetched and its support
   direction verified. Unverifiable → `❓unverified`, never faked.
2. **Build the skeleton; don't gate by default.** Always write `skeleton.md` first;
   send a one-page direction summary as non-blocking and keep going.
3. **Author signs off in a language they can check.** Skeleton in their strongest
   language; second-language output ships with an **independent back-translation**.
4. **Data stays local; effect sizes + CIs.** Follow venue method rules; profile data
   first; Likert as ordinal; seeds fixed; nothing unpublished goes to the cloud.
5. **"Sounds like the author" only where sure.** Match voice in their own language
   with real samples; otherwise aim for faithful strong academic prose.
6. **Delivery comes with a verification report.** Citations + format + toolchain +
   `❓unverified` list. Don't hand over anything you haven't cleaned yourself.
7. **Deliver in the venue's format from version one.** Not raw markdown.
8. **Files are the only authority; the conversation is not.** Long sessions drift:
   after a context compaction the model still carries a half-decayed version of the
   story and argues with the files without noticing — that is the structural cause of
   "it gets worse every round", not a memory lapse. So: **every Phase ends by writing
   back a `## Progress` block to `skeleton.md`** (done / next / open questions / known
   risks / files touched this round) — a rule that says "read" without "write" lets the
   file fall behind reality. **After a compaction or in a new session, the first action
   is to re-read `skeleton.md` + `venue-notes.md` (+ the numbers ledger if one exists)
   and say so explicitly: "the conversation is not authoritative; the files are."**
   What the files don't record didn't happen; on conflict the file wins and the
   conflict is reported (it usually means a write-back was missed).

## The pipeline (see `method/WORKFLOW.md` for the full version)

- **Phase 0 — Intake:** topic/sources, target venue + output language, existing data?,
  mode, existing draft? (→ 0.5). **For journals/conferences, check the submission
  ledger first** (`tools/submissions/check_submissions.py`): simultaneous submission is
  a *cross-project* problem — the same manuscript under a new title, sent elsewhere,
  looks clean from inside either folder. Keep one ledger above all projects, never
  change a `manuscript_id` when retargeting, and update it the day a status changes.
- **Phase 0.5 — Onboard existing draft:** provenance triage (preserve author-written
  passages), reverse-extract skeleton, treat old citations as unverified, disposition
  table, read a real sample before judging. **Also inventory text recycling** — every
  onboarding case *is* reuse (short paper → full paper, talk → article, last year's
  proposal, a student report). Reuse is legitimate; **not disclosing it is not**, and
  similarity software will match you against your own earlier work. Method and
  background may be reused within reason; **results and discussion may not**. Disclose
  in the cover letter and cite the earlier work. Conference-to-journal extension is the
  common case and usually welcome — but venues state how much new material they expect.
- **Phase 1 — Two-track scouting:** full rigor checklist for the literature →
  argument → method pipeline is `method/RIGOR_PROCESS.md` (thirteen stages, each
  with its methodological rationale): declare the review type and a stopping
  rule before reading; a classic is not just "highly cited" — check whether it
  is cited across different camps and whether it has been replicated or
  overturned; synthesize **by concept, not by author or chronology**
  (`templates/literature-matrix.template.md`; for candidate classics a topic's
  literature converges on, run `tools/refs/lit_map.py` first); a "nobody has
  done this" claim needs a search trail and a stated boundary, not an
  impression. (A) literature via citation graphs + web, holdings
  are a convenience sample not the canon. **Keep a `search-log.md`** in the project:
  which databases (OpenAlex / Semantic Scholar / web / own library), the query strings,
  the date run, inclusion/exclusion criteria, hits per step. Three reasons: a reviewer
  asking "why did you miss X" gets an answer (a strategy boundary vs. an oversight);
  retargeting the paper six months later doesn't start from zero; and any draft with a
  review-like component will be asked for exactly this table. (B) the venue's
  **current** format & review norms → `venue-notes.md`. **Include the preprint policy**: venues differ sharply —
  most accept preprints, a few treat them as prior publication, some require the link
  at submission. Record whether/when you may post and any embargo. (A preprint server
  is *not* a submission; two journals at once is.)
- **Phase 1.5 — Direction summary:** one page (gap/angle + contribution + main line +
  recommended venue as explicit options). Non-blocking in default mode.
- **Phase 2 — Verify & fetch:** read each source enough to confirm direction; check
  DOIs/ISBNs; `❓unverified` for anything you couldn't confirm.
- **Phase 3.0 — Method decision: compare comparable studies first, then choose a
  method.** Do this whenever new data will be collected, existing data needs to
  become a paper, or a proposal is being written. Full guidance:
  `method/METHOD_DECISION.md` (the decision procedure) and `method/METHOD_CARDS.md`
  (per-method analysis cards — quantitative, qualitative, mixed/design research,
  arts/practice research).
  🔴 **Check the literature before deciding, regardless of whether you already
  think you know the answer** — what's common or appropriate in a field (a
  research design, a statistical test, a qualitative approach) is settled by
  checking comparable papers, not by memory or a generic playbook; write the
  pre-check guess and the post-check answer side by side so it's visible
  whether checking changed the judgment, and note anything considered and then
  dropped after checking, with the reason.
  Procedure: (1) state the claims you want to make and their type (causal /
  correlational / prevalence / interpretive / mechanistic / design knowledge /
  feasibility) before picking a method — the claim type decides the method;
  (2) read the methods sections of **at least 8 comparable studies** (your own
  literature search first, then citation databases), filling a comparison table
  (`templates/literature-matrix.template.md`), and from **at least 5** of them
  extract the actual analysis practice into a second table — for quantitative
  work: test/model, effect size + CI, multiple-comparison correction; for
  qualitative work: analytic approach, coding process, how inter-rater
  agreement or reflexivity was handled; (3) shortlist **at least two candidate
  methods**, each with what it can and cannot support, how the core construct
  is actually measured and its most plausible alternative explanation, and —
  the item independent review most often finds missing — **a check outside the
  author's own judgment** (a second coder, a blind rater, an external reviewer,
  or someone else collecting the data; narrowing the claim is not a substitute
  when the researcher is the only judge); (4) decide, write a claim-alignment
  table (downgrade any claim the chosen method can't carry), and a premortem
  (the three most likely reasons this gets rejected or fails); (5) produce
  `method-decision.md` (template: `templates/method-decision.template.md`) and
  run `python3 tools/method/method_decision_check.py method-decision.md` before
  the author signs off in their own language — the check proves the required
  sections exist, not that the method is right. Re-run steps 2–4 when the
  target venue changes.
- 🔴 **Pre-data-collection plan (hard gate).** If `method-decision.md` calls for
  new data or an effect claim, write `analysis-plan.md` (template:
  `templates/analysis-plan.template.md` — ethics approval, stopping rule,
  primary analysis or qualitative approach, what result would change your
  mind, the independent check, data-in-hand checkpoints, who reviewed the
  plan) and commit it **before** collecting anything; run
  `python3 tools/method/analysis_plan_check.py analysis-plan.md` (it checks
  that the plan's commit date precedes the start of data collection). Any
  deviation afterward is written into the plan's deviations section, never
  edited into the earlier sections. This is the only step in the whole
  pipeline that cannot be repaired after the fact — pre-registration only has
  value ahead of the data, and ethics approval must precede collection.
  Everything else (synthesis quality, problematization) stays a judgment call
  guided by the templates, not a script gate.
- **Phase 3 — Method/analysis:** **for existing data, first check how comparable
  papers in the target field usually analyze this kind of data** — reuse
  `method-decision.md`'s analysis-method table if one exists, extend it if the
  data type differs, rather than defaulting to a generic recipe. Then: design or
  analyze; data local, effect sizes + CIs,
  Likert ordinal, seeds fixed; fold results back into skeleton nodes. Start the
  **numbers ledger** here (`tools/regress/numbers-ledger.template.md`; method in the
  `doc-regress` skill) — every number that will appear in the draft gets a row with its
  producing script. **Numbers that are too tidy are a red flag**: an effect size of
  exactly 0.5, exactly 2×, identical variance across conditions, identical CIs per
  group — usually a constant leaking from a broken pipeline, not a result. Go back to
  the log and exit code before writing it down.
- **Phase 3.5 — Design diagnosis** (full mode, optional; only when *new data* will be
  collected *and* an effect will be claimed; skip for descriptive / RtD work). Phase 3
  picks the test; this step asks whether **the design itself can answer the question**
  — a correct test on a biased design still returns a confident wrong answer. If R and
  a design-simulation package (e.g. DeclareDesign) are installed, declare the design
  (world / estimand / sampling & assignment / estimator) and simulate; otherwise reason
  it through in prose and say so. Judge **coverage and bias, not power**: high power
  with low coverage means the design guarantees a significant result whether or not
  the intervention works, and **adding participants to a biased design makes it worse**
  (bias doesn't shrink with N, the CI does). A single-group pre/post design cannot
  structurally separate the intervention from the testing effect — add a control, or
  downgrade the claim to non-causal. Fix the design before sizing the sample. Write the
  result into the skeleton node's load-bearing-assumptions field and, in Phase 5, into
  the limitations as numbers rather than "could not be cleanly separated". **This is
  also the moment to pre-register** if the venue values it: the declaration *is* the
  hypothesis + analysis plan; registering later has no value. Record the decision for
  the Phase 6 declarations.
- **Phase 4 — Skeleton:** each node = claim / move / evidence(+source card) / so-what,
  with flags; core causal nodes get load-bearing-assumptions. Save `skeleton.md` in the
  project folder. (Optional Phase 4.5 formal check for a single core causal claim.)
- **Phase 5 — Write the full first draft:** bound to the skeleton, into the format.
  Own language → voice-match + language toolchain. Second language → strong prose,
  de-AI, independent back-translation for sign-off.
  **The de-AI pass has two halves, and the second is the one people skip:** the style
  tools remove convergence words and cadence; `python3 tools/claims/overclaim_lint.py
  <draft>` removes *saying more than the data supports*. Run it in both language
  branches — own language after the voice gate, second language after the fingerprint
  and grammar tools and **before** the de-cadencing pass. It reports, you judge: a real
  0/72 or 100% result is data and stays; an unsupported absolute converges (all→most,
  prove→show, the only→one of the few). Quoted source text is out of scope.
  🔴 **Contrast sentences are a revision-time default, and need measuring every
  round, not just before delivery.** Answering one review comment at a time
  nudges toward adding another "it's X, not Y" boundary line, so the total
  climbs with each revision round rather than staying flat. Rule: ① state
  things plainly while drafting and revising, and keep a contrast only where
  it is doing real argumentative work; ② **measure after every revision
  round**, not only before delivery — English:
  `python3 tools/en/ai_style_diag.py <draft> --gate` (exits non-zero when the
  total contrast-sentence count is over the baseline's 90th percentile);
  Chinese: `tools/zh-tw/zh_ai_style.py` reports the same total against a
  Chinese baseline; ③ **do not fix an overage by swapping to a different
  contrast shape** — "rather than" → "X, not Y", 並非…而是 → 而非, are the same
  tic in different clothes, and the total does not move. After any rule
  change to how contrast (or any style measure) is counted, re-run
  `python3 tools/submissions/style_reaudit.py` against every manuscript still
  drafting or under review (tracked in
  `tools/submissions/style_targets.template.tsv`).
  **Baseline and measuring stack.** Build (or point `--corpus` at) a folder of
  **same-genre, pre-2022** published papers by other people — never your own
  drafts, never a mix of the author's writing and others'. Run, every
  revision round: English `ai_style_diag.py --gate` (contrast, punctuation,
  sentence length, opening stock phrases) + `tools/en/biber_diag.py`
  (grammatical register — dozens of Biber-style features against the
  baseline) + `tools/en/bundle_diag.py` (lexical bundles the draft over-uses
  relative to the baseline) + `tools/en/metadiscourse_en.py` (Hyland stance /
  engagement / boosting-hedging markers against the baseline). **Directions
  the literature actually supports, not just tool thresholds:** ① keep
  argument structure author-led (skeleton-first, already this skill's
  practice); ② keep genuine reader-engagement and implicit-stance markers in
  English prose — LLM output tends to under-use both relative to expert
  writing, which reads as more certain than the evidence supports; ③ don't
  let stock connectives ("it is worth noting that…", "furthermore…") carry
  the paragraph's framing — state the framing plainly, in your own words,
  instead; ④ where the fingerprint tool flags heavy nominalization or a
  sentence-final gerund clause, convert the nominalization back to a verb and
  split the trailing "-ing" clause into its own sentence; ⑤ for Chinese
  drafts, check sentence length **at both ends** — a mechanical revision pass
  over-shortens into choppy fragments about as often as it runs long, so a
  percentile near the bottom of the distribution deserves a look too, not
  just the top. A method with no controlled comparison yet (e.g., matching
  register to an exemplar paragraph from the baseline) stays a trial: measure
  before/after with the tools above, and drop it if the numbers don't
  improve.
  **Register, not just tics.** A senior co-author's verdict on a proposal that had
  passed every tool was "wording and syntax not academic enough, too much text and too
  few figures". Four rules came out of it, checked before delivery in any language:
  ① section headings are noun phrases, never full sentences or questions, and a
  subsection does not restate its chapter title; ② the "not X but Y" frame is kept only
  where the contrast carries weight, everything else is stated plainly; ③ sentences
  over ~120 characters (Chinese) / ~45 words (English) are split unless they are
  enumerations; ④ a term is handled once at first mention — an in-place one-sentence
  definition, a parenthetical original-language gloss, or a pointer to the full
  explanation — and **not** collected into a glossary (harder to read). Explanatory
  asides in parentheses become defining sentences. Traditional-Chinese drafts get all
  four measured by the bundled tools (`setup/addons/zh-tw/README.md` §4).
  **Figures before prose** (same verdict): a table that repeats an overview figure
  folds into the figure; before splitting or dropping a figure or table, list the
  regression rules pinned to it and decide each string's destination (load-bearing
  sentences move into the prose when a figure goes).
- **Phase 6 — Whole-draft verification (you do all of it, before the author sees it):**
  - **6-1 Citations:** re-verify every in-text citation against the PDF (`verify-citations`;
    prose drifts past what the source says). Mismatch → fix now or downgrade to `❓`.
  - **6-1-0 Retraction scan — every delivery, not once:**
    `python3 tools/refs/retraction_scan.py --bib references.bib` (Crossref update
    relations + OpenAlex `is_retracted`).
    Citing a retracted work is the hardest error to repair after submission, and
    retractions keep happening — clean last time ≠ clean this time. `RETRACTED` hits
    need a human look (fuzzy matching); if real, swap the source and update the
    skeleton node. **`NO_DOI` is not "scanned"**: books and pre-DOI works can't be
    matched at all, so report them as unscanned rather than clean.
  - **6-1a Uncited-claim scan:** `python3 tools/claims/uncited_claims_scan.py --src <draft>`.
    Citation verification only sees sentences that carry a citation marker; the
    quantitative / causal / superlative claims *without* one ("41 students showed…",
    "improved by 23%", "the first to…") are invisible to it — and in practice-based
    work they are the main evidence. Pure regex, no LLM. Each hit gets one of three
    dispositions: add a citation · point to your own data (a ledger row) · soften the
    wording. Adjudicated hits get an inline waiver note with a reason so they stop
    reporting. **No delivery while hits are unadjudicated.**
  - **6-1b Numbers ledger reconciliation:** run the project's regression rules
    (`doc-regress` skill: R-STALE / R-LEDGER), then read both ways — every number in
    the draft has a ledger row, every ledger row is findable in the draft. A mismatch
    is either a number without provenance or an orphan from an unsynced edit. This is
    the only guard once APA-style recomputation tools can't parse the model tables
    (mixed models, ordinal models, Bayesian output).
  - **6-1c Figure and table provenance:** every figure/table points to the script and
    data file that produced it (logged in the ledger); every claim in a caption can be
    pointed to on the figure; truncated axes are marked. Figures are evidence, not
    decoration, and they are the usual blind spot.
  - **6-1d Analysis-plan reconciliation (if `analysis-plan.md` exists):** run
    `python3 tools/method/analysis_plan_check.py analysis-plan.md --phase6`
    (write every deviation, or explicitly "no deviations" — never leave it
    blank); the draft's method section reports any deviation honestly, and
    anything analyzed outside the plan is labeled exploratory, not confirmatory.
  - **6-1e Literature update:** the field may have moved between when the
    argument was scoped and now. Re-run the Phase 1 keyword search and a
    forward citation snowball (`tools/refs/snowball.py`) for anything
    published since the `search-log.md` start date; fold anything relevant
    into the comparison table or skeleton, and record the check in
    `search-log.md` regardless of the outcome.
  - **6-2 Format:** tick `venue-notes.md` item by item (length, structure, section order,
    attachments, font/margins — every hard rule).
  - **6-2a Submission declarations — six items.** These are conditions for the
    submission being accepted and for later accountability, not formatting trivia;
    missing ones get desk-rejected or retracted. For each, record *required? / present?
    / accurate?* in the verification report — "written" or "not applicable (reason)",
    never blank:
    1. 🔴 **Generative-AI use disclosure.** A draft produced through this pipeline is
       AI-assisted; this declaration is not optional. Per ACM and most journals: list
       the tools and the tasks they did (literature search / drafting / rewriting /
       translation / code / analysis) and state that the authors take responsibility
       for the whole text. Put it where the venue says (disclosure section or
       acknowledgements). **The disclosure must match what actually happened** — do
       not shrink a co-written draft to "language polishing".
    2. **Research ethics.** Human participants → IRB/ethics approval or exemption,
       with number and institution, in the Method; consent and handling of
       identifiable data stated.
    3. **Data and code availability.** Repository / OSF link if shareable; if not, why
       and how to request. Cross-check the ledger: rows marked "raw file not in repo"
       are exactly where a reviewer will push.
    4. **Author contributions (CRediT).** Required with multiple authors; be specific
       about student co-authors.
    5. **Competing interests and funding.** Grant numbers and funder; otherwise state
       "The authors declare no competing interests."
    6. **Pre-registration.** If Phase 3.5 ran and an effect is claimed: give the link,
       or say nothing — never imply one that doesn't exist.
    > Rule: **"the venue didn't ask" ≠ "don't write it."** AI disclosure and ethics go in
    > even when the call is silent; the rest follow `venue-notes.md`.
  - **6-3 Language toolchain green** (per language branch; own-language drafts also pass
    the voice gate) **and the overclaim pass adjudicated** — every
    `overclaim_lint.py` candidate either kept with the evidence that carries it, or
    converged. Iterating grows overclaims back: each new paragraph brings new absolutes,
    so this reruns on every delivery, not once. English (or other second-language)
    delivery: statistical style tools staying green is necessary but not sufficient —
    run a **de-cadencing pass with clean context** (subagent template:
    `agents/de-cadencing-scholar.md`; give it the file path only) to catch the rhythm
    tics a human eye reads as "AI-polished" (its tic #6 is this same overclaim list).
  - **6-4 Clean final review:** hand the draft to a fresh reviewer context (a subagent
    without the drafting history, or a separate pass) **together with the project's
    `ADJUDICATED.md`** — the list of "looks wrong, was checked, is right" decisions.
    Clean context is the point of this review and also its cost: without the list it
    re-raises settled questions and the author gets asked the same thing twice.
    Instruct it: re-opening an adjudicated item requires stating new evidence.
  - **6-5 Verification report** (citations · format tick-list · toolchain results ·
    declarations table · `❓unverified` list) and **6-6 delivery as the formatted PDF**
    (own-language and back-translation as a pair for second-language papers).
- **Phase 7 — Iterate:** author reacts; substantive changes written back to
  `skeleton.md`; swap evidence per node without rebuilding the argument.
  **A number changes → update the ledger first, then the draft, then rerun the
  regression rules** (the order matters: editing the draft first means R-STALE never
  sees the old value). **A new paragraph → rerun `uncited_claims_scan.py`** — new prose
  almost always carries new uncited claims, and waivers only cover old sentences. Each
  round ends with a `## Progress` write-back (Iron rule 8: Phase 7 has the most rounds
  and the most session breaks, so this is where drift accumulates). Finish with
  `paper-review`.
- **Phase 8 — After acceptance (submission is not the end):** reviews arriving → the
  `rebuttal` skill. **Proofs** usually allow 48–72 hours and are for *errors only* —
  substantive changes there get refused or trigger re-review; check author names and
  order, funder ids, that figure numbers still match their in-text references, that no
  table row got dropped in typesetting, and that non-Latin names/institutions survived
  the layout. **Rights**: CC-BY vs transfer — check whether a funder mandates open
  access *before* signing, and make sure every co-author (students included) knows the
  terms. **Dissemination**: post the preprint/repository copy per the embargo you
  recorded in Phase 1, then update the submission ledger to `published` — an unupdated
  ledger means your next duplicate-submission check runs on stale data.

## What this skill orchestrates (adapt to what's installed)

- Literature: web + citation graphs (lite) / `fetch-refs` + `verify-citations` + local
  RAG (full).
- Venue norms: web search of the official call → `venue-notes.md`.
- Method decision: comparable-studies comparison + `method/METHOD_DECISION.md` +
  `method/METHOD_CARDS.md` (`tools/method/method_decision_check.py`,
  `tools/method/analysis_plan_check.py`); full rigor checklist in
  `method/RIGOR_PROCESS.md`.
- Method/analysis: describe honestly (lite) / R · Python · Jupyter (full).
- Language: voice profile + careful AI-tic pass (lite) / local linters + corpora (full,
  see `setup/TOOLS.md`; Traditional-Chinese-Taiwan authors: `setup/addons/zh-tw/`).
- Reviews came back: `rebuttal` (point-by-point + revision table + completeness check).
- Submission status: `tools/submissions/check_submissions.py` + one central ledger.
- Pre-delivery scans (bundled, zero-install): `tools/refs/retraction_scan.py`,
  `tools/claims/uncited_claims_scan.py`; numbers ledger + regression rules via the
  `doc-regress` skill (`tools/regress/`).
- Finish: `paper-review` + a PDF build (`build-pdf`).

## Not this skill
- **Check/proofread only, don't rewrite** → `paper-review`.
- **Just fetch reference PDFs** → `fetch-refs`. **Just check citation direction** →
  `verify-citations`. **Slides** → a deck skill.
- One line: *"help me look at this" = paper-review; "help me write/rewrite/resubmit" =
  co-author.*
