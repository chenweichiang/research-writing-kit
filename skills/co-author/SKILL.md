---
name: co-author
description: Collaborative long-form academic writing — papers AND grant/funding proposals. Use when the author says "help me write this paper", "turn these sources into a paper", "develop this", "build the skeleton", "co-author", or wants to write a grant/funding/fellowship proposal, or has an existing draft to rewrite/upgrade/resubmit ("rewrite this", "it got rejected, submit elsewhere", "turn this talk/old proposal into a journal paper" → Phase 0.5), or needs the submission declarations (AI-use disclosure / ethics / data availability / author contributions / competing interests / pre-registration) or asks "what am I missing that should be there". Division of labor = the author decides what to say and gives final sign-off; Claude verifies literature, researches the venue's current format and review norms, designs method / runs analysis when needed, writes the draft, and self-checks every step. Default = "write it all the way to a verified complete draft"; only build-skeleton-first when the author explicitly asks. For check-only (don't rewrite) → paper-review; for slides → a deck skill.
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
- **Phase 1 — Two-track scouting:** (A) literature via citation graphs + web, holdings
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
- **Phase 3 — Method/analysis:** design or analyze; data local, effect sizes + CIs,
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
    the voice gate). English (or other second-language) delivery: statistical style
    tools staying green is necessary but not sufficient — run a **de-cadencing pass
    with clean context** (subagent template: `agents/de-cadencing-scholar.md`; give it
    the file path only) to catch the rhythm tics a human eye reads as "AI-polished".
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
