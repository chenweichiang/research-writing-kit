---
name: co-author
description: Collaborative long-form academic writing for papers and grant/funding proposals. Use to turn a topic or sources into a paper or proposal ("help me write this paper", "build the skeleton"); decide a research method (Phase 3.0 compares 8+ comparable studies, writes `method-decision.md`); add the submission declarations (AI use, ethics, data availability, contributions, competing interests, pre-registration) or check a venue's AI rules and AI-generated figures (`method/AI_DISCLOSURE.md`); rewrite, expand or resubmit an existing draft (rejected and retargeting, conference to journal, talk to paper → Phase 0.5, with text-recycling disclosure); document the literature search (`search-log.md`); native polish ("reads like a translation" → Phase 5.5, change lists adjudicated item by item); a one-line "full polish" before delivery; version numbers, changelog and delivery folders (`method/VERSIONING.md`); cutting to a page or word limit (`method/COMPRESSION.md`); merging a co-author's manuscript or a multi-team proposal with every sentence traced to its source (`method/COLLABORATION.md`); checking figures in the typeset PDF; whether a topic is worth a full paper at all (Phase 1.5 contribution gate). The author decides what to say and signs off; Claude verifies literature, researches the venue, designs method, drafts and self-checks. Default is a verified complete draft; skeleton-first only on request. Check-only → paper-review; slides → a deck skill.
---

# co-author: collaborative paper / proposal writing

> **This skill was generated from the Research Writing Kit and should be adapted to
> the author.** Placeholders in `<ANGLE BRACKETS>` are filled in at setup.
> Full method: `method/WORKFLOW.md` + `method/PHILOSOPHY.md` + `method/IRON-RULES.md`.

> Author profile (filled at setup):
> - Field: `<FIELD>`
> - Writing language(s): `<LANGUAGE>` (native) / `<SECOND_LANG>` (if any, back-translated)
> - Usual venues: `<VENUES>`
> - Register corpus (same-field published papers, the yardstick for papers, proposals and
>   applications): `<ZH_CORPUS_DIR and/or CORPUS_DIR, plus the venue folder per target venue,
>   or "none: lite comparison against 2-3 sample papers">`
> - Voice profile (letters and personal statements only): `<VOICE_PROFILE_PATH or "none">`
> - Mode: `<lite | full>` (which tools exist, see the project CLAUDE.md)

## Two modes (decide at intake)

- **Default: "write it to good."** Author names the topic → you go all the way to a
  *verified complete first draft*, then they iterate. Skeleton is built but internal.
- **Skeleton mode** (only if they say "just build the skeleton / develop the
  argument, don't write yet"): hand the skeleton over for sign-off before prose.

## 🔴 Iron rules (from `method/IRON-RULES.md`, do not drop)

1. **Never fabricate a citation.** Every reference is really fetched and its support
   direction verified. Unverifiable → `❓unverified`, never faked.
2. **Build the skeleton; don't gate by default.** Always write `skeleton.md` first;
   send a one-page direction summary as non-blocking and keep going.
3. **Author signs off in a language they can check.** Skeleton in their strongest
   language; second-language output ships with an **independent back-translation**.
4. **No third-party uploads; effect sizes + CIs.** Follow venue method rules; profile data
   first; Likert as ordinal; seeds fixed; nothing unpublished goes to third-party cloud services.
5. **Papers sound like the field; letters sound like the author.** Papers, grant
   proposals and applications follow the register of same-field published papers, in
   either language (measured with `tools/register/register_profile.py`, or compared by
   reading sample papers in lite mode). The voice profile is only for letters, cover
   letters, bios and personal statements, or when the author explicitly asks for their
   own voice. Author-written passages are preserved either way.
6. **Delivery comes with a verification report.** Citations + format + toolchain +
   `❓unverified` list. Don't hand over anything you haven't cleaned yourself.
7. **Deliver in the venue's format from version one.** Not raw markdown. Version
   number, file names, delivery folders and changelog follow `method/VERSIONING.md`
   (X = times sent out, Y = content, Z = wording; the `VERSION` file is the only
   source; run `tools/versioning/version_check.py` before every delivery).
8. **Files are the only authority; the conversation is not.** Long sessions drift:
   after a context compaction the model still carries a half-decayed version of the
   story and argues with the files without noticing. That is the structural cause of
   "it gets worse every round", not a memory lapse. So: **every Phase ends by writing
   back a `## Progress` block to `skeleton.md`** (done / next / open questions / known
   risks / files touched this round). A rule that says "read" without "write" lets the
   file fall behind reality. **After a compaction or in a new session, the first action
   is to re-read `skeleton.md` + `venue-notes.md` (+ the numbers ledger if one exists)
   and say so explicitly: "the conversation is not authoritative; the files are."**
   What the files don't record didn't happen; on conflict the file wins and the
   conflict is reported (it usually means a write-back was missed).

## Full polish (one-line trigger)

When the author says "full polish", "run everything before I send it" or similar, take
the existing draft through the stages below in this order, **without asking at each
stage**, and report once at the end. The order has reasons; do not swap stages.

| # | Stage | Chinese draft | English draft | Why here |
|---|---|---|---|---|
| 1 | Citations | `verify-citations` on the whole draft + `tools/refs/retraction_scan.py` + `tools/claims/uncited_claims_scan.py` (Phase 6-1-0, 6-1a) | same | content errors first, or the polish has to be redone |
| 2 | Proofreading | `paper-review` layers 1-2 (typos and punctuation, internal-wording grep, `tools/zh-tw/zh_gloss_scan.py --en` for English inside Chinese prose, semantic proofreading) | layers 1-2 (grammar checker, `tools/en/lt_check.sh`) | typos disturb the later judgments |
| 3 | Native polish | Phase 5.5, `zh-tw-native-editor` | Phase 5.5, `en-native-editor` | get the language right first |
| 4 | De-AI | `voice_lint.py --paper` + `zh_ai_style.py` (contrast total) | `ai_style_diag.py --gate` + `de-cadencing-scholar` | polish before rhythm; the other way round, the polish undoes the de-cadencing |
| 5 | Overclaims | `tools/claims/overclaim_lint.py`, each hit adjudicated | same, `--lang en` | polishing and de-AI can both strengthen the wording |
| 6 | Localization (zh-TW addon) | `tools/zh-tw/zh_localize.py` | the Chinese back-translation only | every earlier rewrite can bring in non-local terms, so scan last |
| 7 | Regression | `doc-regress` (incl. R6 internal wording) + `register_profile.py` before and after; a co-author's manuscript adds `tools/collab/source_trace.py --gate` | same | confirm stages 1-6 broke no load-bearing string, number or citation |
| 8 | New versioned PDF | `method/VERSIONING.md`: decide the number (wording only: patch; stage 1 changed content: minor) → CHANGELOG → build → `version_check.py` → `tools/figures/figure_check.py` | same; rebuild the back-translation PDF | the delivered file and the record must agree |

- **Carry the author's standing preferences without being told** (the ones recorded in
  their CLAUDE.md and voice rules), and the field register for papers and proposals
  (Iron rule 5). Someone else's manuscript follows `method/COLLABORATION.md`: only the
  clearest deviations, every sentence traceable to the original.
- **The report always gives**: the numbers per stage (citations passed and flagged,
  typos fixed, polish items proposed and accepted, contrast total before and after,
  overclaim dispositions, localization hits, regression FAIL / WARN), the new version
  and PDF path, and any stage that did not pass, with the reason. A stage that does not
  apply (no numbers ledger, say) is reported as "not applicable", never skipped silently.

## The pipeline (see `method/WORKFLOW.md` for the full version)

- **Phase 0 (Intake):** topic/sources, target venue + output language, existing data?,
  mode, existing draft? (→ 0.5). **For journals/conferences, check the submission
  ledger first** (`tools/submissions/check_submissions.py`): simultaneous submission is
  a *cross-project* problem. The same manuscript under a new title, sent elsewhere,
  looks clean from inside either folder. Keep one ledger above all projects, never
  change a `manuscript_id` when retargeting, and update it the day a status changes.
- **Phase 0.5 (Onboard existing draft):** provenance triage (preserve author-written
  passages), reverse-extract skeleton, treat old citations as unverified, disposition
  table, read a real sample before judging. **Also inventory text recycling**: every
  onboarding case *is* reuse (short paper → full paper, talk → article, last year's
  proposal, a student report). Reuse is legitimate; **not disclosing it is not**, and
  similarity software will match you against your own earlier work. Method and
  background may be reused within reason; **results and discussion may not**. Disclose
  in the cover letter and cite the earlier work. Conference-to-journal extension is the
  common case and usually welcome, but venues state how much new material they expect.
  **Someone else is the lead writer** (you rewrite or polish a co-author's manuscript;
  a proposal with sub-projects by different people) → `method/COLLABORATION.md`: never
  edit the original, write changes as an edit layer; every sentence traces back to a
  source, checked with `python3 tools/collab/source_trace.py --orig <original and their
  replies...> --draft <new draft> --gate` before handing back (fix every 🔴); never
  write in their site details or design assumptions; open questions are opened,
  tracked, closed and cleared before submission; keep an ownership table for sections,
  figures and tables.
- **Phase 1 (Two-track scouting):** full rigor checklist for the literature →
  argument → method pipeline is `method/RIGOR_PROCESS.md` (thirteen stages, each
  with its methodological rationale): declare the review type and a stopping
  rule before reading; a classic is not just "highly cited": check whether it
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
  **current** format & review norms → `venue-notes.md`. **Include the preprint policy**: venues differ sharply.
  Most accept preprints, a few treat them as prior publication, some require the link
  at submission. Record whether/when you may post and any embargo. (A preprint server
  is *not* a submission; two journals at once is.) **Include the generative-AI rules**
  for journals and funders alike: may AI draft, where the statement goes and which
  fields it needs, what is allowed for AI-generated figures; link and date read. They
  differ sharply (Taylor & Francis does not allow an AI first draft of a manuscript or
  sections; Springer Nature does not allow figures generated from a text prompt alone;
  ACM no longer requires disclosure of writing assistance). Signpost table as of
  2026-10 and what it means for this workflow: `method/AI_DISCLOSURE.md`; re-read the
  current page for every manuscript.
- **Phase 1.5 (Direction summary):** one page (gap/angle + contribution + main line +
  recommended venue as explicit options). Non-blocking in default mode.
  - **Is the venue compatible with this workflow?** If it does not allow AI drafting,
    say so in the summary and let the author choose: another venue, another process
    (they write the first draft, AI only translates and polishes), or a question to
    the editor. Phases 2-4 go ahead; Phase 5 drafting waits for the choice.
  - **Contribution gate (once per manuscript, after the summary is written).** Whoever
    writes a paper rates its topic too kindly. Give the summary, `venue-notes.md` and
    the list of evidence in hand to `clean-reviewer` and have it answer as that venue's
    editor: (1) the contribution in one sentence, and whether this venue's readers care;
    (2) what level the evidence can carry (full paper, short paper, poster or exhibition
    paper, only a teaching record); (3) the most likely reason for rejection, desk
    rejection included; (4) one verdict of five: **write the full paper / shrink to a
    short paper or poster / change venue / collect more data first / not worth writing**.
    The last four are real verdicts, not failures: pass them to the author with reasons
    and alternative venues, and stop for their choice even in default mode (the scope
    changed, and writing on costs a whole paper). Typical cases this catches early:
    sessions held but the data never collected and no ethics approval; a desk rejection
    with no comments; a proposal whose fallback was agreed in advance as a poster. Give
    it `ADJUDICATED.md` too, so it re-raises settled directions only with new evidence.
- **Phase 2 (Verify & fetch):** read each source enough to confirm direction; check
  DOIs/ISBNs; `❓unverified` for anything you couldn't confirm. **For the PDFs still
  missing, subtract the author's own library first**: `python3 tools/refs/missing_refs.py
  --bib <refs.bib> --pdfdir <project PDF folder> [--library <their PDF folder>]` writes
  the list of what is really missing, with DOI/URL links. Once they have downloaded
  those by hand, `tools/refs/inbox_ingest.py` matches the downloads folder against the
  list and files each PDF (details in the `fetch-refs` skill).
- **Phase 3.0 (Method decision): compare comparable studies first, then choose a
  method.** Do this whenever new data will be collected, existing data needs to
  become a paper, or a proposal is being written. Full guidance:
  `method/METHOD_DECISION.md` (the decision procedure) and `method/METHOD_CARDS.md`
  (per-method analysis cards: quantitative, qualitative, mixed/design research,
  arts/practice research).
  🔴 **Check the literature before deciding, regardless of whether you already
  think you know the answer**: what's common or appropriate in a field (a
  research design, a statistical test, a qualitative approach) is settled by
  checking comparable papers, not by memory or a generic playbook; write the
  pre-check guess and the post-check answer side by side so it's visible
  whether checking changed the judgment, and note anything considered and then
  dropped after checking, with the reason.
  Procedure: (1) state the claims you want to make and their type (causal /
  correlational / prevalence / interpretive / mechanistic / design knowledge /
  feasibility) before picking a method, since the claim type decides the method;
  (2) read the methods sections of **at least 8 comparable studies** (your own
  literature search first, then citation databases), filling a comparison table
  (`templates/literature-matrix.template.md`), and from **at least 5** of them
  extract the actual analysis practice into a second table, for quantitative
  work: test/model, effect size + CI, multiple-comparison correction; for
  qualitative work: analytic approach, coding process, how inter-rater
  agreement or reflexivity was handled; (3) shortlist **at least two candidate
  methods**, each with what it can and cannot support, how the core construct
  is actually measured and its most plausible alternative explanation, and
  (the item independent review most often finds missing) **a check outside the
  author's own judgment** (a second coder, a blind rater, an external reviewer,
  or someone else collecting the data; narrowing the claim is not a substitute
  when the researcher is the only judge); (4) decide, write a claim-alignment
  table (downgrade any claim the chosen method can't carry), and a premortem
  (the three most likely reasons this gets rejected or fails); (5) produce
  `method-decision.md` (template: `templates/method-decision.template.md`) and
  run `python3 tools/method/method_decision_check.py method-decision.md` before
  the author signs off in their own language. The check proves the required
  sections exist, not that the method is right. Re-run steps 2–4 when the
  target venue changes.
- 🔴 **Pre-data-collection plan (hard gate).** If `method-decision.md` calls for
  new data or an effect claim, write `analysis-plan.md` (template:
  `templates/analysis-plan.template.md`: ethics approval, stopping rule,
  primary analysis or qualitative approach, what result would change your
  mind, the independent check, data-in-hand checkpoints, who reviewed the
  plan) and commit it **before** collecting anything; run
  `python3 tools/method/analysis_plan_check.py analysis-plan.md` (it checks
  that the plan's commit date precedes the start of data collection). Any
  deviation afterward is written into the plan's deviations section, never
  edited into the earlier sections. This is the only step in the whole
  pipeline that cannot be repaired after the fact. Pre-registration only has
  value ahead of the data, and ethics approval must precede collection.
  Everything else (synthesis quality, problematization) stays a judgment call
  guided by the templates, not a script gate.
- **Phase 3 (Method/analysis):** **for existing data, first check how comparable
  papers in the target field usually analyze this kind of data**: reuse
  `method-decision.md`'s analysis-method table if one exists, extend it if the
  data type differs, rather than defaulting to a generic recipe. Then: design or
  analyze; data local, effect sizes + CIs,
  Likert ordinal, seeds fixed; fold results back into skeleton nodes. Start the
  **numbers ledger** here (`tools/regress/numbers-ledger.template.md`; method in the
  `doc-regress` skill). Every number that will appear in the draft gets a row with its
  producing script. **Numbers that are too tidy are a red flag**: an effect size of
  exactly 0.5, exactly 2×, identical variance across conditions, identical CIs per
  group, usually a constant leaking from a broken pipeline, not a result. Go back to
  the log and exit code before writing it down.
- **Phase 3.5 (Design diagnosis)** (full mode, optional; only when *new data* will be
  collected *and* an effect will be claimed; skip for descriptive / RtD work). Phase 3
  picks the test; this step asks whether **the design itself can answer the question**.
  A correct test on a biased design still returns a confident wrong answer. If R and
  a design-simulation package (e.g. DeclareDesign) are installed, declare the design
  (world / estimand / sampling & assignment / estimator) and simulate; otherwise reason
  it through in prose and say so. Judge **coverage and bias, not power**: high power
  with low coverage means the design guarantees a significant result whether or not
  the intervention works, and **adding participants to a biased design makes it worse**
  (bias doesn't shrink with N, the CI does). A single-group pre/post design cannot
  structurally separate the intervention from the testing effect, so add a control, or
  downgrade the claim to non-causal. Fix the design before sizing the sample. Write the
  result into the skeleton node's load-bearing-assumptions field and, in Phase 5, into
  the limitations as numbers rather than "could not be cleanly separated". **This is
  also the moment to pre-register** if the venue values it: the declaration *is* the
  hypothesis + analysis plan; registering later has no value. Record the decision for
  the Phase 6 declarations.
- **Phase 4 (Skeleton):** each node = claim / move / evidence(+source card) / so-what,
  with flags; core causal nodes get load-bearing-assumptions. Save `skeleton.md` in the
  project folder. (Optional Phase 4.5 formal check for a single core causal claim.)
- **Phase 5 (Write the full first draft):** bound to the skeleton, into the format.
  Papers, proposals and applications aim at the target field's register in either
  language (Iron rule 5): before drafting, read a few same-venue paragraphs
  (`tools/register/register_profile.py <draft> --lang zh|en --corpus <corpus> --venue
  <folder> --exemplars 4`, or 2-3 sample papers in lite mode) for sentence length, how
  clauses join and how often the field uses its usual self-reference; never copy from
  them. The voice profile applies only to letters and personal statements. Own language →
  language toolchain (Chinese voice_lint with `--paper` for papers, proposals and
  applications). Second language → strong prose, de-AI, independent back-translation for
  sign-off. Both then go through Phase 5.5.
  **The de-AI pass has two halves, and the second is the one people skip:** the style
  tools remove convergence words and cadence; `python3 tools/claims/overclaim_lint.py
  <draft>` removes *saying more than the data supports*. Run it in both language
  branches: own language after the voice gate, second language after the fingerprint
  and grammar tools and **before** the de-cadencing pass. It reports, you judge: a real
  0/72 or 100% result is data and stays; an unsupported absolute converges (all→most,
  prove→show, the only→one of the few). Quoted source text is out of scope.
  🔴 **Contrast sentences are a revision-time default, and need measuring every
  round, not just before delivery.** Answering one review comment at a time
  nudges toward adding another "it's X, not Y" boundary line, so the total
  climbs with each revision round rather than staying flat. Rule: ① state
  things plainly while drafting and revising, and keep a contrast only where
  it is doing real argumentative work; ② **measure after every revision
  round**, not only before delivery. English:
  `python3 tools/en/ai_style_diag.py <draft> --gate` (exits non-zero when the
  total contrast-sentence count is over the baseline's 90th percentile);
  Chinese: `tools/zh-tw/zh_ai_style.py` reports the same total against a
  Chinese baseline; ③ **do not fix an overage by swapping to a different
  contrast shape**: "rather than" → "X, not Y", 並非…而是 → 而是, are the same
  tic in different clothes, and the total does not move. After any rule
  change to how contrast (or any style measure) is counted, re-run
  `python3 tools/submissions/style_reaudit.py` against every manuscript still
  drafting or under review (tracked in
  `tools/submissions/style_targets.template.tsv`).
  **Baseline and measuring stack.** Build (or point `--corpus` at) a folder of
  **same-genre, pre-2022** published papers by other people, never your own
  drafts, never a mix of the author's writing and others'. Run, every
  revision round: English `ai_style_diag.py --gate` (contrast, punctuation,
  sentence length, opening stock phrases) + `tools/en/biber_diag.py`
  (grammatical register: dozens of Biber-style features against the
  baseline) + `tools/en/bundle_diag.py` (lexical bundles the draft over-uses
  relative to the baseline) + `tools/en/metadiscourse_en.py` (Hyland stance /
  engagement / boosting-hedging markers against the baseline). **Directions
  the literature actually supports, not just tool thresholds:** ① keep
  argument structure author-led (skeleton-first, already this skill's
  practice); ② keep genuine reader-engagement and implicit-stance markers in
  English prose: LLM output tends to under-use both relative to expert
  writing, which reads as more certain than the evidence supports; ③ don't
  let stock connectives ("it is worth noting that…", "furthermore…") carry
  the paragraph's framing, state the framing plainly, in your own words,
  instead; ④ only when `biber_diag.py` reports nominalizations or sentence-final
  gerund clauses **above** the baseline's p90, convert the nominalization back to a
  verb and split the trailing "-ing" clause into its own sentence; inside the band,
  leave them, and below p10 the fix runs the other way (applying the rule to a draft
  that is already low pushes it further out of the field); ⑤ for Chinese
  drafts, check sentence length **at both ends**: a mechanical revision pass
  over-shortens into choppy fragments about as often as it runs long, and Taiwan
  journal papers write long sentences as a matter of course, so a percentile near the
  bottom of the distribution deserves a look too, not just the top. Same-venue exemplar
  paragraphs (Phase 5) are a reference, not a quality guarantee: no controlled
  comparison exists for academic argumentative prose, and a small A/B inside a polishing
  pass (deviation list alone vs. the list plus four exemplar paragraphs, one run per
  cell) came out slightly better with exemplars in Chinese and slightly worse in
  English. Attach them if you like; to judge whether they helped, measure before/after
  with the tools above.
  **Register, not just tics.** A senior co-author's verdict on a proposal that had
  passed every tool was "wording and syntax not academic enough, too much text and too
  few figures". Four rules came out of it, checked before delivery in any language:
  ① section headings are noun phrases, never full sentences or questions, and a
  subsection does not restate its chapter title; ② the "not X but Y" frame is kept only
  where the contrast carries weight, everything else is stated plainly; ③ sentences
  over ~120 characters (Chinese) / ~45 words (English) are split unless they are
  enumerations; ④ a term is handled once at first mention (an in-place one-sentence
  definition, a parenthetical original-language gloss, or a pointer to the full
  explanation) and **not** collected into a glossary (harder to read). Explanatory
  asides in parentheses become defining sentences. Traditional-Chinese drafts get all
  four measured by the bundled tools (`setup/addons/zh-tw/README.md` §4).
  **Figures before prose** (same verdict): a table that repeats an overview figure
  folds into the figure; before splitting or dropping a figure or table, list the
  regression rules pinned to it and decide each string's destination (load-bearing
  sentences move into the prose when a figure goes).
- **Phase 5.5 (Native polish, both languages; after the toolchain passes, before
  Phase 6).** After many rounds of local patching, translationese and unidiomatic
  phrasing accumulate, and the style tools cannot see it: they measure AI fingerprints,
  not whether the text reads like the field. "Reads like a native scholar of this field"
  is defined as **register features inside the p10-p90 band of same-field published
  papers** (register alignment), not a rulebook. So: measure the deviations first, fix
  only what sits outside the band, leave in-band features alone, and send stance to the
  author. Why this definition, and what it replaced: `method/WORKFLOW.md` Phase 5.5.
  - **Measure:** `python3 tools/register/register_profile.py <draft> --lang zh|en
    --corpus <corpus> --venue <folder> --lines <range> --out <tmp>/dev_<range>.md
    [--exemplars 4 --exemplar-out <tmp>/ex.md]` (English adds `--biber-python
    <BIBER_PYTHON>` if the Biber environment is installed). The list has four sections:
    to fix / locked / for the author / inside the band. Each item gives the whole-draft
    count, the amount that brings it back into the band, bounds for the editor's own
    range, and instances. The per-feature policies (band / cap / locked / report) are at
    the top of the script; override them with `--policy-file`.
  - **Dispatch:** Chinese → `zh-tw-native-editor` (zh-TW addon), English →
    `en-native-editor`. English runs **en-native-editor → de-cadencing-scholar**: fix
    the language first, then the rhythm; the other order lets the polish undo the
    de-cadencing. If you edit an agent definition, dispatch it from a new session (a
    running session may keep the version it loaded at start).
  - **Split and run in parallel:** 3-4 ranges by section, one editor each, each with
    its own deviation list (`--lines`). **Editors return change lists only**
    (`edits_<range>.py`, one category and reason per item) and never edit the draft;
    parallel editors would overwrite each other.
  - **The dispatch prompt gives** (clean context, no drafting history): the draft path,
    the line range, the deviation list and feel-reference paths, where to write the
    change list, the venue folder, the locked terms, the `ADJUDICATED.md` path, the
    **word budget** `--grow-budget` (merging sentences usually saves characters;
    restoring 進行/透過 or to-infinitives adds some, to be offset elsewhere), and who
    the author is (someone else's draft: only the clearest deviations). Papers never
    get the voice profile (Iron rule 5).
  - **Feel-reference paragraphs** are optional. In the method author's small trial
    they did not help consistently. The same trial showed the two failure modes to
    watch during adjudication: overshooting (every 本文 in a section switched to
    本研究, which pushes 本研究 over its own band) and joining two sentences with
    different subjects by a comma.
  - **Self-check gate:** `tools/register/polish_check.py --corpus <corpus> --venue
    <folder> --grow-budget <N>`. Each editor runs it until it passes; the main session
    then merges every list and runs it once more (`--edits` takes a comma-separated
    list). It blocks: changed numbers, citations, comments, quoted text, math, LaTeX
    commands, Latin words (Chinese) or locked terms; growth over budget; more contrast
    frames, stock metadiscourse, dashes, sentence-initial 然而 or mainland terms; more
    over-long sentences; and **register direction** (the whole draft measured before
    and after: a high feature may not rise, a low one may not fall, an in-band one may
    not be pushed out). Stance counts that change are reported, not blocked. The
    prose semicolon is not blocked. `--selftest` proves it still blocks.
  - 🔴 **The main session adjudicates every item; never accept a batch wholesale.**
    Read each proposal in context: accept / accept rewritten / reject. Editor errors
    seen in practice: deleting a 一項 that states a real count, reordering so that 其中
    loses its referent, turning someone else's position into the paper's conclusion,
    removing 被 so the subject becomes unclear, merging two different claims into one
    sentence. **Look twice at edits that add words** (a restored 進行 or 透過, a
    connective added while merging): does the sentence really read better, or is it
    chasing a number? Keep only the accepted items and write them back with
    `polish_check.py ... --apply` (it writes only if everything passes).
  - **After write-back:** rerun `register_profile.py` (how far the deviations
    converged), the project's regression rules (`doc-regress`), Chinese `voice_lint
    --paper` + `zh_ai_style.py` / English `ai_style_diag.py --gate`, and rebuild the PDF
    to check the page count. English then goes to de-cadencing and back-translation
    (from the polished English). **After de-cadencing, run `register_profile.py`
    again** and compare it with the post-5.5 list: splitting "both A and B", cutting
    triads and deleting "however"-type links can push phrasal coordination or
    transitions back out of the band; revert those edits.
  - **Record** one entry in `ADJUDICATED.md` (baseline, out-of-band items before and
    after, proposed and accepted counts, reasons for rewrites and rejections, the
    "needs the author" list), so the next round knows where the draft stands.
  - **When to rerun:** after a Phase 7 rewrite (a section or more rewritten, or many
    review rounds), on the changed passages only; in `rebuttal`, on the revised
    passages before the response letter is written. A few changed words do not need it.
  - **Lite (no corpus, or no Python):** read the target journal's author guidelines
    plus 2-3 papers from that journal that the author provides or names, and compare the
    draft with them by reading: self-reference (本研究/本文, *we*/*this study*), sentence
    length and how clauses join, linking words, translationese, punctuation, and for
    English articles, transitions, nominalizations and to-infinitives. Write the
    deviation list by hand and label it a reading, not a measurement; the editor still
    returns a change list and the main session still adjudicates. Claim no percentiles.
  - **Human editors still have a place:** language professionals mostly revise at
    sentence level, while claims and argument are shaped by disciplinary peers (Lillis
    & Curry 2006). A professional editor for an English submission, or a same-field
    colleague reading a Chinese draft for its argument, is still worth it.
- **Phase 6 (Whole-draft verification) (you do all of it, before the author sees it):**
  - **6-1 Citations:** re-verify every in-text citation against the PDF (`verify-citations`;
    prose drifts past what the source says). Mismatch → fix now or downgrade to `❓`.
  - **6-1-0 Retraction scan, every delivery, not once:**
    `python3 tools/refs/retraction_scan.py --bib references.bib` (Crossref update
    relations + OpenAlex `is_retracted`).
    Citing a retracted work is the hardest error to repair after submission, and
    retractions keep happening. Clean last time ≠ clean this time. `RETRACTED` hits
    need a human look (fuzzy matching); if real, swap the source and update the
    skeleton node. **`NO_DOI` is not "scanned"**: books and pre-DOI works can't be
    matched at all, so report them as unscanned rather than clean.
  - **6-1a Uncited-claim scan:** `python3 tools/claims/uncited_claims_scan.py --src <draft>`.
    Citation verification only sees sentences that carry a citation marker; the
    quantitative / causal / superlative claims *without* one ("41 students showed…",
    "improved by 23%", "the first to…") are invisible to it, and in practice-based
    work they are the main evidence. Pure regex, no LLM. Each hit gets one of three
    dispositions: add a citation · point to your own data (a ledger row) · soften the
    wording. Adjudicated hits get an inline waiver note with a reason so they stop
    reporting. **No delivery while hits are unadjudicated.**
  - **6-1b Numbers ledger reconciliation:** run the project's regression rules
    (`doc-regress` skill: R-STALE / R-LEDGER), then read both ways: every number in
    the draft has a ledger row, every ledger row is findable in the draft. A mismatch
    is either a number without provenance or an orphan from an unsynced edit. This is
    the only guard once APA-style recomputation tools can't parse the model tables
    (mixed models, ordinal models, Bayesian output).
  - **6-1c Figure and table provenance:** every figure/table points to the script and
    data file that produced it (logged in the ledger); every claim in a caption can be
    pointed to on the figure; truncated axes are marked. Figures are evidence, not
    decoration, and they are the usual blind spot. On the typeset PDF run
    `python3 tools/figures/figure_check.py <draft.pdf> --out <tmp>/figcheck` (needs
    PyMuPDF): numbering gaps and duplicates, captions and in-text references that do not
    match, figures running past the text column or the page, text in vector figures under
    6 pt, rasters shrunk until their text is unreadable. Look at the cropped PNGs it writes
    (a vision-capable subagent can take a few each). In a review copy, comment markers
    create reference noise; judge on the submission build.
  - **6-1d Analysis-plan reconciliation (if `analysis-plan.md` exists):** run
    `python3 tools/method/analysis_plan_check.py analysis-plan.md --phase6`
    (write every deviation, or explicitly "no deviations", never leave it
    blank); the draft's method section reports any deviation honestly, and
    anything analyzed outside the plan is labeled exploratory, not confirmatory.
  - **6-1e Literature update:** the field may have moved between when the
    argument was scoped and now. Re-run the Phase 1 keyword search and a
    forward citation snowball (`tools/refs/snowball.py`) for anything
    published since the `search-log.md` start date; fold anything relevant
    into the comparison table or skeleton, and record the check in
    `search-log.md` regardless of the outcome.
  - **6-2 Format:** tick `venue-notes.md` item by item (length, structure, section order,
    attachments, font/margins, every hard rule). Over a page or word limit →
    `method/COMPRESSION.md`: read how the limit is counted, find the pinned boundaries,
    budget per section, cut from light to heavy and report what each cut saved; 🔴 never
    shrink figures, never cut the core claim or load-bearing evidence.
  - **6-2a Submission declarations, six items.** These are conditions for the
    submission being accepted and for later accountability, not formatting trivia;
    missing ones get desk-rejected or retracted. For each, record *required? / present?
    / accurate?* in the verification report, "written" or "not applicable (reason)",
    never blank:
    1. 🔴 **Generative-AI use disclosure.** A draft produced through this pipeline is
       AI-assisted; this declaration is not optional. Per ACM and most journals: list
       the tools and the tasks they did (literature search / drafting / rewriting /
       translation / code / analysis) and state that the authors take responsibility
       for the whole text. Place and fields follow `venue-notes.md` and
       `method/AI_DISCLOSURE.md` (a statement in the manuscript with tool versions,
       an AI Declaration, a separate closing section, the acknowledgements, the methods
       section; it varies). If the venue does not allow AI drafting, that should have
       surfaced in Phase 1.5, not here. **The disclosure must match what actually
       happened.** Do not shrink a co-written draft to "language polishing"; when the
       writing process or the model changed, re-check every verb in the statement. If
       human coding was done with AI pre-labels visible, the methods disclose the
       procedure (`method/RIGOR_PROCESS.md` Stage 11).
       **AI-generated or AI-processed figures:** never for research results or
       photographs of the actual work; conceptual figures follow the venue (tool and
       version in the caption, Intellect also the full prompt; no text-prompt-only
       figures for Springer Nature); masking or blurring goes in the statement too.
       Keep engine, version, seed and prompt in `figures/ai-generation-log.md`.
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
       or say nothing, never imply one that doesn't exist.
    > Rule: **"the venue didn't ask" ≠ "don't write it."** AI disclosure and ethics go in
    > even when the call is silent; the rest follow `venue-notes.md`.
  - **6-3 Language toolchain green** (per language branch; Chinese drafts also pass
    voice_lint, with `--paper` for papers, proposals and applications) **and the
    overclaim pass adjudicated**: every
    `overclaim_lint.py` candidate either kept with the evidence that carries it, or
    converged. Iterating grows overclaims back: each new paragraph brings new absolutes,
    so this reruns on every delivery, not once. English (or other second-language)
    delivery: statistical style tools staying green is necessary but not sufficient.
    After the Phase 5.5 native polish, run a **de-cadencing pass with clean context**
    (subagent template: `agents/de-cadencing-scholar.md`; give it the file path only) to
    catch the rhythm tics a human eye reads as "AI-polished" (its tic #6 is this same
    overclaim list), then re-measure register as Phase 5.5 describes.
  - **6-4 Clean final review:** dispatch the named agent `clean-reviewer` (template:
    `agents/clean-reviewer.md`) with the draft **and the project's `ADJUDICATED.md`**:
    the list of "looks wrong, was checked, is right" decisions. Clean context is the
    point of this review and also its cost: without the list it re-raises settled
    questions and the author gets asked the same thing twice. Its definition already
    carries the common discipline (quote and locate every criticism, reopen an
    adjudicated item only with new evidence), so the prompt gives the file paths and
    what to focus on this round. It is a named agent because the review needs the
    strongest model at the highest effort, and effort can only be pinned in an agent
    definition's frontmatter, never in the Agent call. Without subagents, do a separate
    pass that reads only the files.
  - **6-5 Verification report** (citations · format tick-list · toolchain results ·
    declarations table · `❓unverified` list) and **6-6 delivery as the formatted PDF**
    (own-language and back-translation as a pair for second-language papers). Before
    handing it over run `python3 tools/versioning/version_check.py <project>
    [--submission <submitted.pdf>]` (`VERSION` and CHANGELOG agree, the delivery folder
    holds one version only, no version string in the submitted text, no delivered
    number reused after its tag).
- **Phase 7 (Iterate):** author reacts; substantive changes written back to
  `skeleton.md`; swap evidence per node without rebuilding the argument.
  **A number changes → update the ledger first, then the draft, then rerun the
  regression rules** (the order matters: editing the draft first means R-STALE never
  sees the old value). **A new paragraph → rerun `uncited_claims_scan.py`**: new prose
  almost always carries new uncited claims, and waivers only cover old sentences. Each
  round ends with a `## Progress` write-back (Iron rule 8: Phase 7 has the most rounds
  and the most session breaks, so this is where drift accumulates). **After a large
  rewrite, rerun Phase 5.5 on the changed passages**: text patched into an old draft is
  where translationese grows back. Finish with `paper-review`.
- **Phase 8 (After acceptance) (submission is not the end):** reviews arriving → the
  `rebuttal` skill. **Proofs** usually allow 48–72 hours and are for *errors only*.
  Substantive changes there get refused or trigger re-review; check author names and
  order, funder ids, that figure numbers still match their in-text references, that no
  table row got dropped in typesetting, and that non-Latin names/institutions survived
  the layout. **Rights**: CC-BY vs transfer, check whether a funder mandates open
  access *before* signing, and make sure every co-author (students included) knows the
  terms. **Dissemination**: post the preprint/repository copy per the embargo you
  recorded in Phase 1, then update the submission ledger to `published`. An unupdated
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
- Language: careful AI-tic pass, register compared against sample papers (lite) / local
  linters + corpora (full, see `setup/TOOLS.md`; Traditional-Chinese-Taiwan authors:
  `setup/addons/zh-tw/`). The voice profile serves letters and personal statements.
- Native polish (Phase 5.5): agents `zh-tw-native-editor` (zh-TW addon) and
  `en-native-editor` (change lists only) + `tools/register/register_profile.py`
  (deviation list and feel reference; it reads `tools/zh-tw/zh_register.py`,
  `tools/en/metadiscourse_en.py` and, if installed, `tools/en/biber_diag.py`) +
  `tools/register/polish_check.py` (change-list self-check, register direction,
  `--apply`).
- Clean final review: agent `clean-reviewer`.
- Reviews came back: `rebuttal` (point-by-point + revision table + completeness check).
- Submission status: `tools/submissions/check_submissions.py` + one central ledger.
- Pre-delivery scans (bundled, zero-install): `tools/refs/retraction_scan.py`,
  `tools/claims/uncited_claims_scan.py`; numbers ledger + regression rules via the
  `doc-regress` skill (`tools/regress/`).
- Delivery: `method/VERSIONING.md` + `tools/versioning/version_check.py`;
  `tools/figures/figure_check.py` on the typeset PDF (needs PyMuPDF); page and word
  limits: `method/COMPRESSION.md`.
- Co-authored manuscripts: `method/COLLABORATION.md` + `tools/collab/source_trace.py`.
- Venue AI rules and AI figures: `method/AI_DISCLOSURE.md`.
- Finish: `paper-review` + a PDF build (`build-pdf`).

## Not this skill
- **Check/proofread only, don't rewrite** → `paper-review`.
- **Just fetch reference PDFs** → `fetch-refs`. **Just check citation direction** →
  `verify-citations`. **Slides** → a deck skill.
- One line: *"help me look at this" = paper-review; "help me write/rewrite/resubmit" =
  co-author.*
