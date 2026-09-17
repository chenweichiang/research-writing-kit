# Rigor Process: From Literature to Argument to Method to Report

> Division of labor with the rest of this kit: this file is the whole pipeline and
> the rigor test at each step; `method/METHOD_DECISION.md` is method choice
> specifically (Section 8 below just points there); `method/METHOD_CARDS.md` is the
> per-method analysis cards; the bundled tools in `tools/README.md` and
> `setup/TOOLS.md` are the writing and checking toolchain; the `co-author` skill is
> what actually runs these steps. This file doesn't repeat that content, only
> points to it.
>
> Evidence tags: **[full text]** = the original text, or a real passage of it, was
> actually read; **[abstract only]** = only the abstract was read; **[secondhand]**
> = the original wasn't read, and the claim rests on secondhand sources that agree
> with each other. Anything tagged **[secondhand]** gets the original read before it
> goes into a manuscript. The running list is in Section 6.

---

## 1. A common way to do this, and where a rigorous researcher would push back

A common way researchers approach a new topic: establish the classic literature →
see how the surrounding conversation has framed it → see what recent work has done
→ work out where you stand and what your position is → introduce your own topic →
decide on a method.

The direction is right. Methodologically it roughly maps to a "narrative review plus
gap-spotting." The problem is that every step here still describes *what to do*.
It never says *how to avoid fooling yourself doing it*, and the whole sequence
only covers the first half of a research project. Laid out step by step:

| The common step | What it's actually called | Where it goes wrong | Basis |
|---|---|---|---|
| Establish the classics | Database search + citation snowballing | Assuming "heavily cited" means "classic." Citations themselves can be stacked into an authority that has no real basis; it's also common to read only secondhand summaries and never the original | Greenberg 2009: a citation network behind one medical belief contained 242 papers, 675 citations, and 220,553 supporting paths. The appearance of authority came from selective citation, amplification, and citation itself turning an assumption into a stated fact [full text]; Jergas & Baethge 2015: the total citation-error rate across medical journals was 25.4% [full text] |
| See how the conversation has framed it | Critical synthesis | Writing a paper-by-paper summary; never declaring what kind of review this is while writing as if it covers "the whole field" | Boote & Beile 2005: a literature review is not an "exhaustive summary" [full text]; Snyder 2019: traditional reviews are often ad hoc and lack method [abstract only] |
| See what recent work has done | Forward snowballing, a search trail | One round of database search only; no stopping rule; no record, so you can't later answer "why wasn't X included?" | Greenhalgh & Peacock 2005: of 495 sources found, only 30% came from a planned search and 51% came from snowballing [full text]; Wohlin 2014's stopping rule [full text] |
| Work out your position | Argument structure | A claim with no "why this evidence is enough to carry it"; no counterarguments written in; wording stronger than the evidence | Toulmin; Booth et al. [secondhand]; Hu & Cao 2011 on hedging vs. boosting [full text] |
| Introduce your topic | Gap-spotting vs. problematization | Only doing "nobody's done this yet," which tends to produce a small contribution; a "gap" is itself a rhetorical construction. Cherry-picking convenient literature manufactures a false one | Sandberg & Alvesson 2011, Alvesson & Sandberg 2011 [abstract only]; Locke & Golden-Biddle 1997 [abstract, partial] |
| Decide on a method | Method decision (`method/METHOD_DECISION.md`) | Method not aligned with the research question, the conceptual framework, or the quality criteria | Maxwell 2013's interactive design model [full text: Maxwell 2023 interview]; Crotty 1998 [secondhand] |

**Stages a rigorous researcher would ask about that are missing from the common
version above:**

1. **Purpose and type of contribution**: who this is for, why it matters, and what
   kind of knowledge it's meant to add.
2. **Locking the analysis plan before data collection**: both quantitative and
   qualitative work can be pre-registered; deciding the analysis after seeing the
   data lets the results mislead you.
3. **The researcher's own bias**: before seeing the data, have someone who disagrees
   review the plan, and write down in advance what result would change your mind.
4. **Data-collection checkpoints and a deviation log.**
5. **Reporting confirmatory and exploratory results separately**: not writing an
   idea you had after seeing the data as if it were a hypothesis you had before
   (HARKing).
6. **Qualitative and practice-based research have their own rigor criteria**: the
   language of quantitative reliability and validity doesn't transfer directly.
7. **The extra risks of AI-assisted research**: fabricated citations, distorted
   summaries, the validity problem of an LLM acting as a coder.
8. **A literature update before delivery**: the field may have moved between when
   the project started and when it's submitted.

---

## 2. The full process (thirteen stages)

Each stage lists: what to do, the output, the check, common failure modes, the
basis, and the corresponding tool. The stages are not strictly linear. A change in
any one of them means going back and re-checking alignment (Section 3).

### Stage 1: Purpose and type of contribution

- **Do**: write down whose question this answers and why it matters (one sentence
  academic, one sentence practical), and what kind of knowledge it's meant to
  contribute.
- **Criteria**:
  - Corley & Gioia 2011 split theoretical contribution into two axes: originality
    (incremental vs. revelatory) and utility (scientific vs. practical) [abstract
    only]. Name your own square honestly first. Claiming "revelatory" while
    delivering an incremental, confirmatory study reads as overclaiming.
  - Whetten 1989's checklist: What's new? So what? Why so? Well done? Done well?
    [abstract, partial + secondhand]. "Nobody's done this" only answers *What's
    new*. It leaves *So what* unanswered.
  - Design and arts research contributions are often **intermediate-level
    knowledge**: more abstract than a single artifact, without aiming for a general
    theory (Höök & Löwgren 2012 [full text]); the vehicle is an annotated
    portfolio (Gaver & Bowers 2012 [full text]). The artifact itself is not the
    contribution. There has to be an argument layer explaining what transferable
    thing it teaches.
- **Output**: the "purpose and contribution type" section at the top of `skeleton.md`.
- **Common failure**: treating "new" as "a contribution"; starting the literature
  search before deciding the contribution type, so the literature ends up
  rationalizing what you already wanted to do.

### Stage 2: Plan the literature review (set the rules before reading)

- **Do**:
  1. Declare the review type. Grant & Booth 2009 use SALSA (search, appraisal,
     synthesis, analysis) to compare 14 review types [abstract only]. Criteria:
     - Needs to be exhaustive and reproducible → systematic review;
     - The concept boundary isn't settled yet, vocabulary is inconsistent → scoping
       review;
     - Producing a new perspective from existing research → integrative review
       (Torraco 2005, 2016 [abstract only]);
     - Evaluating positions and methods without aiming for exhaustiveness →
       critical review;
     - Just background → narrative review (the highest-risk option).
  2. **Before reading anything**, write down: databases and sources, the query
     strings, the year and language range, inclusion/exclusion criteria, and a
     stopping rule.
- **Output**: `search-log.md` (already required by the `co-author` skill's Phase 1).
- **Common failures**:
  - Setting exclusion criteria after already reading the literature, which quietly
    excludes whatever disagrees with you;
  - Searching only in English without saying so. For medical interventions, an
    English-only limit doesn't change much (Dobrescu et al. 2021 [abstract only]),
    but in design, art, and the humanities, important arguments are often only
    published in another language, so that conclusion doesn't transfer;
  - Non-English literature needs its own search pass (national repositories,
    regional databases, theses in the working language).

### Stage 3: Establish the classics and find the newest work

- **Do**: database search plus citation snowballing together. Wohlin 2014's
  procedure [full text]:
  1. **Start with a diverse seed set** (different communities, publishers, years,
     authors) so you don't just land in one small clique that cites itself;
  2. **Backward snowballing**: read the references;
  3. **Forward snowballing**: see who cites it;
  4. **Stopping rule**: stop once both directions stop turning up anything new.
- **How to judge "classic"**: raw citation count isn't enough. Cross-check three
  things: how broadly it's cited (citations from researchers who hold different
  positions count for more than citations clustered inside one clique that cites
  itself); whether later work has replicated, supported, or overturned it; whether
  it sits at the intersection of multiple citation chains.
- **Read the original**: any time a manuscript says "source X claims Y," go back to
  the original and find the actual passage. A secondhand summary has roughly a
  one-in-four chance of being wrong (Jergas & Baethge 2015's 25.4% total error rate
  [full text]).
- **Output**: the snowballing record in `search-log.md`; a candidate list, each
  entry tagged classic/new, in-hand/to-fetch, original read or not.
- **Tools**: your own local literature library if you keep one, the `fetch-refs`
  skill's `snowball.py`, OpenAlex, and Crossref (see Section 4).
- **Common failures**:
  - One round of keyword search only. Wohlin cites a Kitchenham example: a manual
    search found 20 papers; an automated search on top of it found 33 more [full
    text];
  - Treating "found everything" as the goal. A literature review is a sample: no
    review captures the whole population of relevant work, and what matters
    instead is that the process is inspectable (Wohlin [full text]).

### Stage 4: Critical synthesis and contextualizing

- **Do**:
  1. **Organize by concept**: build a matrix with concepts as rows and sources as
     columns; a matrix organized by author or by year hides the same comparison.
     This comes from Webster & Watson 2002, though
     only the abstract has been read so far. The full argument for it is still
     unread [abstract only].
  2. **Identify positions, schools, and disputes**: what are the competing answers
     to the same question, and where do they actually diverge?
  3. **Evaluate prior work's methods**: what methods were used, and what were their
     strengths and weaknesses. This feeds directly into Stage 8's method decision.
  4. **Self-assess with Boote & Beile 2005's 12 criteria** [full text]:
     - Coverage: inclusion/exclusion criteria stated;
     - Synthesis: distinguishes done from not-yet-done, situates the work in a
       broader scholarly and historical context, uses the field's vocabulary
       correctly, explains the key variables and phenomena, produces a new
       perspective;
     - Methodology: identifies the field's main methods and their trade-offs, links
       theory to method;
     - Significance: states practical and scholarly importance;
     - Rhetoric: the structure is clear.
- **Output**: `literature-matrix.md` (template: `templates/literature-matrix.template.md`,
  covering concept matrix, classic-status judgment, position map, prior-methods
  evaluation, problematization, self-assessment).
- **A worked example from design research**: Cárdenas Cordova et al. 2025 (*Design
  Science*) organized 52 references with reflexive thematic analysis, moving past
  a paper-by-paper listing [full text].
- **Common failure**: writing an annotated bibliography instead; leaving out the
  "methods" column entirely, which means the method decision has to be redone from
  scratch later.

### Stage 5: Problematization and the space for a contribution

- **Do**:
  1. **Classify your own gap** (Sandberg & Alvesson 2011 [abstract, partial]):
     - the literature contradicts itself (confusion);
     - the literature ignores or lacks evidence on something (neglect);
     - applying an existing theory to a new context (application): this one
       usually has the lowest bar and the smallest contribution.
  2. **Ask again**: even filled, is this contribution actually small?
  3. **Problematize** (Alvesson & Sandberg 2011 [abstract only]): find the unstated
     assumption behind this literature, and judge whether it's worth challenging and
     whether there's evidence to challenge it with.
  4. **Guard against a false gap**: a "gap" is something an author constructs
     rhetorically out of the surrounding literature (Locke & Golden-Biddle 1997
     [abstract, partial]). Writing "no study has addressed X" needs the search
     records from Stages 2–3 to back it up, and needs to state the search's own
     boundary (e.g., "in English- and Chinese-language design journals from
     2015–2026").
- **Output**: the "gap and contribution" section of `skeleton.md`, including the gap
  type and the search records that support it.
- **Common failures**:
  - Doing only gap-spotting and landing on "doable, publishable, but nobody
    cares";
  - Over-problematizing: challenging an assumption nobody holds, or one that's
    already been overturned.

### Stage 6: Reverse verification (actively look for what contradicts you)

- **Do**: once the skeleton has taken shape, before drafting prose, actively search
  for literature that would contradict or limit your own claim, and record it in
  the skeleton's load-bearing-assumptions field. It later becomes a concession, a
  response, or a stated limitation.
- **Basis**:
  - "Acknowledge and respond" is a required part of an argument (Booth et al.
    [secondhand]); it is not optional;
  - Duyx et al. 2017: papers with a statistically significant result were cited 1.6
    times as often as non-significant ones, and 2.7 times as often when the authors
    explicitly said the finding supported their hypothesis [full text]. Picking
    citations by memory systematically favors whatever already supports your own
    result.
- **Tool**: this kit does not currently bundle a dedicated reverse-citation search
  tool. Run it the same way as Stage 3's search (your own local library first, if
  you keep one, then the databases in Section 4), aimed specifically at the
  opposing case; Stage 3's search already turned up the supporting one.
- **Common failure**: writing one sentence like "of course, some disagree" and
  stopping there, without stating under what conditions the claim actually breaks
  down.

### Stage 7: Conceptual framework and paradigm alignment

- **Do**:
  1. **Separate theoretical and conceptual frameworks** (Grant & Osanloo 2014 [full
     text]):
     - theoretical framework = an existing, already-validated theory being borrowed;
     - conceptual framework = the researcher's own account of how these concepts
       relate and how the problem should be investigated.
  2. **Maxwell's five components move together** [full text: Maxwell 2023
     interview]: goals, conceptual framework, research questions, methods, validity.
     The research question sits at the center. Changing any one component means
     re-checking all the others.
  3. **Crotty 1998's four-layer alignment** [secondhand]: epistemology → theoretical
     perspective → methodology → methods, connecting down to analytic technique and
     quality criteria.
  4. **Mixed methods need a stated stance**: Howe 1988 argues quantitative and
     qualitative work are not necessarily incompatible at either the practical or
     epistemological level, but the researcher has to say whether they're taking a
     pragmatist stance or keeping each paradigm strictly separate by phase
     [abstract only].
  5. **Arts research aligns in the opposite direction**: work back from the method
     to the question. Borgdorff 2012: evaluation has to check whether the chosen
     method (experimental, participatory, interpretive, analytic) actually answers
     the question posed [full text].
- **Output**: an alignment table (research question → claim type → method →
  analysis → quality criteria), one row per question. This can sit next to the
  claim-alignment table in `method/METHOD_DECISION.md`'s Step 6.
- **Common failures**:
  - Claiming interpretive phenomenology while quantifying word frequencies in
    transcripts;
  - Defending qualitative work with quantitative "reproducibility" language, or the
    reverse;
  - Checking alignment once and never again after the method changed.

### Stage 8: Method decision

Follow `method/METHOD_DECISION.md`:
- Check comparable papers first, regardless of whether the answer already feels
  obvious;
- At least 8 comparable studies with their methods sections read, at least 5 with
  their analysis methods specifically extracted;
- The pre-check default judgment, the post-check difference, and any approach
  dropped after checking (with a reason) all written side by side;
- At least two candidates, each specifying: the core construct's measurement and
  most plausible alternative explanation; an independent check beyond the
  researcher;
- A claim-alignment table and a pre-mortem;
- `method-decision.md` produced and passed through
  `tools/method/method_decision_check.py` before it goes to the author.

**How accurate this step actually is**: an internal blind test on seven real past
cases found that following this procedure anticipated the real method-related
problem 78% of the time, versus 36% for the same judgment made before checking the
literature. The item most often missed was an independent check beyond the
researcher (see `method/METHOD_DECISION.md` Sections 5 and 7 for the full account
and its limits: one reviewer, few cases, and the reviewer already knew the
cases).

### Stage 9: Lock the plan before data collection

- **Do**:
  1. **Design diagnosis**: only when the project will claim an effect from new data
     (`method/WORKFLOW.md` Phase 3.5).
  2. **Ethics review**: approval obtained *before* any data is collected. Having
     the application ready is not the same as having it approved.
  3. **Analysis plan and pre-registration**:
     - Quantitative: the stopping rule for data collection, exclusion rules,
       primary outcome variables, model, and scoring method are all fixed in
       advance. Simmons et al. 2011's six author requirements [full text] and
       Wicherts et al. 2016's 34-item researcher-degrees-of-freedom checklist [full
       text] can be used directly.
     - Pre-registration needs to be specific, precise, and exhaustive, ideally
       specifying "only hypothesis A will be tested" (Wicherts [full text]).
     - Qualitative research can also pre-register the interview guide, an initial
       coding framework, and the range within which it may be revised after data
       collection begins (Haven & Van Grootel 2019 [abstract only]).
  4. **Write down, before seeing the data, what result would change your mind.**
     This is the core of adversarial collaboration working at all (Ceci et al. 2024
     [full text]).
  5. **Have someone who disagrees review the plan**, before data collection. A
     review that happens after the results are in comes too late to matter.
  6. **Pre-mortem**: assume failure a year from now and work backward to the
     reasons. From Klein 2007, unread in the original [secondhand].
- **Output**: `analysis-plan.md` (template: `templates/analysis-plan.template.md`;
  finalized by a commit or an OSF pre-registration; mandatory, see Section 5),
  checked with `tools/method/analysis_plan_check.py` before data collection starts.
- **Common failures**:
  - Pre-registering too vaguely: "the main outcome is this scale" still leaves
    many scoring choices open;
  - Treating pre-registration as a formality. Nosek et al. 2019 point out it's a
    skill that has to be practiced [full text].

### Stage 10: Data collection

- **Do**: at the end of each collection session, confirm the data actually arrived
  and the count matches. Attendance is not data. Log any deviation from the plan
  (sample, procedure, instrument) at the time it happens, with the reason.
- **Output**: a data-collection record; the deviation log, written into
  `analysis-plan.md` Section 6, checked before delivery with
  `tools/method/analysis_plan_check.py --phase6`.
- **Common failure**: letting participants self-submit data after a session and
  losing a whole batch; a deviation that never gets logged and is later written up
  as if it were the original design.

### Stage 11: Analysis

- **Quantitative**:
  - Confirmatory analysis follows the plan; anything outside the plan is labeled
    exploratory. Writing a post-hoc idea as if it were a pre-registered hypothesis
    is HARKing, and it turns a chance result into a hard-to-dislodge theory (Kerr
    1998 [full text]);
  - When an analysis choice has multiple defensible options, run a multiverse or
    sensitivity analysis to see whether the conclusion survives (Steegen et al.
    2016 [full text]; Dragicevic et al. 2019 built an interactive version for CHI
    [full text]). 29 teams analyzing the same dataset produced effect sizes ranging
    from 0.89 to 2.93 (Silberzahn et al. 2018 [full text]);
  - Scale selection and scoring have to be transparent: a ten-item scale summed in
    different ways has 1,023 possible combinations (Flake & Fried 2020 [full
    text]).
- **Qualitative**:
  - Self-assess with Levitt et al. 2018's method-integrity criteria [full text],
    across two dimensions:
    - fidelity to the phenomenon: sufficient data, managing your own influence on
      it, findings grounded in the data;
    - utility for the research goal: contextualized, generates insight, a
      meaningful contribution, gaps between findings explained;
  - Counterexamples and contradictory data get written in and explained; dropping
    them is not acceptable;
  - Reflexivity needs a structure (memos, an analytic log) built up over the
    course of the analysis; one paragraph of confession at the end does not meet
    this bar;
  - Sample-size justification depends on the analytic approach (see
    `method/METHOD_CARDS.md`'s qualitative group).
- **AI-assisted coding**: assistive only, with mandatory human review. A comparison
  across 164 interviews found AI coding substantially over-coded, and the authors
  do not recommend it as a replacement for human coding (Boettinger et al. 2026
  [abstract only]).
- **Output**: analysis scripts and records, a numbers ledger (already required,
  see `templates`'s numbers-ledger convention and `method/WORKFLOW.md` Phase 3),
  and a list of exploratory analyses.

### Stage 12: Writing and reporting

- **Argument order in the introduction**: establish the field's importance first,
  then the gap, and only then how this study fills it. This is Swales' CARS
  model's three moves [secondhand]; the most common mistake is skipping the middle
  step.
- **Ask Toulmin's six questions of every substantive claim** [secondhand]: what's
  the evidence, what connects it to the claim, what backs up that connection
  itself, is the qualifier strong enough, and under what conditions does it not
  hold.
- **Calibrate claim strength**: verbs and adverbs need to match the evidence
  ("suggest," "indicate," "demonstrate," and "prove" are not interchangeable).
  Over-hedging is also a problem. A reader can no longer tell what you're actually
  claiming (Hu & Cao 2011 [full text]). Tools: `tools/claims/overclaim_lint.py`,
  `tools/en/metadiscourse_en.py`.
- **Reporting guidelines and transparency**:
  - Check which reporting guideline applies to the design (COREQ / SRQR / TREND /
    CONSORT / STROBE / PRISMA / GRAMMS: see the relevant card in
    `method/METHOD_CARDS.md`);
  - Confirmatory and exploratory results reported separately;
  - Deviations from the plan reported as they actually happened;
  - Material- and data-sharing rates in HCI research run low (Wacharamanotham et
    al. 2020 [abstract only]): share what can be shared.
- **AI-use disclosure**: per venue rules, and written even when the venue doesn't
  ask (`method/WORKFLOW.md` Phase 6, the six submission declarations).

### Stage 13: Pre-delivery checks

- **Citations**: every "source X says Y" is checked against the original
  (`skills/verify-citations`); any AI-suggested reference is checked by DOI. GPT-3.5
  fabricated 55% of the citations it generated, GPT-4 fabricated 18%, and even the
  real ones carried substantive errors 43% and 24% of the time, respectively
  (Walters & Wilder 2023 [full text]).
- **Retractions**: re-run the retraction scan (`tools/refs/retraction_scan.py`).
  Among 136 retracted dental-research papers, 84 were still cited afterward, and
  only 5.4% of those citations noted the retraction: 69.3% were still positive
  citations (Theis-Mahon & Bakker 2020 [abstract only]).
- **Literature update**: before delivery, re-run one round of forward snowballing
  and keyword search to see whether anything new has appeared since the project
  started. Section 1's common version of this process has no equivalent step:
  this one was added here.
- **Summary distortion**: an AI-written summary can read fluently and still be
  wrong, in ways automatic metrics don't catch (Maynez et al. 2020 [full text]).
  Anything sourced from an AI-generated summary gets checked against the original.
- **Clean second-pass review simulating a reviewer**: `co-author` Phase 6,
  `paper-review`'s fourth layer.

### Practice-based research (research-through-design, art-as-research): the same stages, a different criterion

When the work itself is part of the research, Stages 9–12's criteria are replaced
by the criteria below, the underlying rigor requirement still applies:

- **Candy 2006** [full text]: a practice output needs to be accompanied by
  documentation of the process and some form of written analysis that supports its
  position and shows critical reflection. Ordinary practice explores toward the
  maker's own goal; practice-based research has to produce understanding that's new
  to people other than the maker.
- **Zimmerman et al. 2007's four evaluation lenses** [full text]:
  - Process: the method choice's rationale and enough detail to be redone;
  - Invention: a full literature review showing what was actually advanced;
  - Relevance: replaces validity;
  - Extensibility: whether someone else could use it in a different context.
- **Gaver 2012** [full text]: an annotated portfolio respects the specificity of
  individual works while still offering the extensibility and inspectability the
  research community expects. There's no community-wide consensus on whether
  RtD should aim for generalizable theory at all. State your own stance in the
  paper.
- **Common failure**: showing only the artifact with no process record; defending
  practice-based research with "reproducibility," which is simply the wrong
  criterion to apply.

---

## 3. Cross-stage principles

1. **Iterative**: when a real-world constraint forces a method change, go back
   and re-check the research question, conceptual framework, and validity
   criteria (Maxwell). Expect to revisit earlier stages; a single straight pass
   through is uncommon.
2. **Decisions leave a paper trail**: every decision gets written down with a
   reason and a date; the file is the sole authority (Iron Rule 8 in
   `method/IRON-RULES.md`). An undocumented decision can't later be told apart from
   a post-hoc rationalization.
3. **A literature review is a sample**: quality comes from an inspectable
   procedure (Wohlin); claiming exhaustiveness does not establish it.
4. **The researcher is the hardest bias to catch in yourself**: get the plan
   challenged before the data exists, with the criteria for changing your mind
   stated in advance (Munafò et al. 2017 name three specific biases: seeing
   patterns in randomness, confirmation bias, and hindsight bias [full text]).
5. **AI output is only a signpost**: a well-formatted answer is not the same as a
   true one. Checking it line by line is a required step; treating it as optional
   is not acceptable.

---

## 4. Existing tools, mapped, and where the gaps are

### 4.1 By stage: what exists, what's missing, and what's out there

| Stage | Already have | Gap | Off-the-shelf options | Recommendation |
|---|---|---|---|---|
| 2 Plan the review | `search-log.md` requirement | Declaring the review type; a PRISMA flow diagram | The PRISMA 2020 flow diagram (Page et al. 2021) | The R package `PRISMA2020` produces this |
| 3 Classics & recent | Your own local literature library (if you keep one), `snowball.py`, Crossref, OpenAlex | Citation-network visualization | ResearchRabbit, Connected Papers (cloud services that only use public bibliographic metadata; they never see your own draft, and no independent accuracy evaluation was found); `bibliometrix` (R, local, has a GUI); VOSviewer (local) | This kit bundles `tools/refs/lit_map.py`, which finds which papers are most co-cited across a batch of references you already have. Treat the output as a starting list of candidate classics; it is not a verdict. `bibliometrix` and `openalexR` are free to install locally if you want the visualization layer |
| 3 Screening at scale | None | No screening tool for hundreds of candidate papers | ASReview (open source, local; simulation studies show it can save 50–85% of screening effort at 95% recall) | Install locally (`pip install asreview`) for a systematic or scoping review with a large candidate set |
| 4 Synthesis | None | A template for a concept matrix and a position map | QualCoder, Taguette (local; can treat literature passages as qualitative data to code); Argdown (turns an argument into a navigable map from plain text) | This kit ships `templates/literature-matrix.template.md`; install Argdown or a qualitative coding tool if the synthesis is large enough to need one |
| 6 Reverse verification | None bundled: see Stage 6 above | Literature outside your own local library | scite (cloud; classifies citations as supporting or disputing; an independent evaluation found the "supporting" category's recall was only 0.05, per Bakker et al. 2023) | Treat it as one lead among several, never as a conclusion |
| 8 Method decision | `method/METHOD_DECISION.md`, `method/METHOD_CARDS.md`, `tools/method/method_decision_check.py`, DeclareDesign | No good option found for method-selection guidance in languages other than English | SAGE Research Methods' Methods Map (subscription-based, so check whether your own institution's library carries it before assuming access); Tea (University of Washington) picks a statistical test from your hypothesis and data. It is still maintained but covers only classic tests, and it does not cover mixed models or ordinal regression | This kit bundles Tea as `tools/method/tea_second_opinion.py` |
| 9 Lock the plan | Design diagnosis (`method/WORKFLOW.md` Phase 3.5) | Analysis-plan template, pre-registration | OSF pre-registration templates (including a qualitative version), AsPredicted; Wicherts et al. 2016's 34-item checklist; a Transparency Checklist (a web form, unreachable when checked) | This kit ships `templates/analysis-plan.template.md` (mandatory before data collection) and `tools/method/analysis_plan_check.py` |
| 11 Analysis | Standard R/Python statistical tooling | Multiverse analysis, Bayesian result visualization | `ggdist`, `tidybayes` (Kay; `ggdist` is still actively updated); Boba (UW's multiverse-analysis tool, unmaintained since 2021) | Install `ggdist`/`tidybayes` if you need them; write a multiverse analysis yourself in R: the existing multiverse tool (Boba) is unmaintained |
| 11 Qualitative + LLM | This kit's qualitative playbook (`method/METHOD_CARDS.md`) | A tool that checks LLM coding against human coding | CollabCoder (CHI 2024, CC0, still updated). **Requires an OpenAI API key and sends data to the cloud** | Don't use it unless your data-privacy rules allow sending material to a third-party API, or you can point it at a self-hosted model instead |
| 12 Writing | `tools/claims/overclaim_lint.py`, `tools/en/metadiscourse_en.py`, `tools/en/ai_style_diag.py` | An index of reporting guidelines | The EQUATOR Network (a free database of reporting guidelines) | Check it once the target venue is chosen |
| 13 Pre-delivery | `skills/verify-citations`, `tools/refs/retraction_scan.py` (already queries Crossref's Retraction Watch data) | A literature-update step | No new tool needed: just re-run the forward snowball | Written into `co-author` Phase 6 |

### 4.2 Research-group systems worth knowing about

- **Maintained and usable**: Tea (UW); `ggdist`, `tidybayes` (Kay); OpenScholar and
  Ai2 ScholarQA (Ai2 + UW, published in *Nature* in 2026, code still active);
  CoQuest (UIUC, research-question ideation, MIT licensed).
- **Unmaintained**: Tisane (2022), Boba (2021), ScholarPhi (2023, folded into
  Semantic Scholar's online reader).
- **No public code found**: CiteSee, Threddy, Synergi, Relatedly, Scim,
  PaperWeaver, DiscipLink, Scideator, PaTAT. These were all published at CHI or
  UIST with real user studies, but no released code repository could be found under
  the paper's name or the common naming conventions for that group's tools. They are most
  likely research prototypes that were never open-sourced (not proof they don't
  exist somewhere). What's worth borrowing is the design idea; the code itself
  isn't available:
  - marking which citations you've read and which you haven't while reading;
  - cross-organizing related-work sections from multiple papers by theme;
  - recombining aspects of different papers into a new idea.
- **Design and arts research method frameworks** (already covered in Section 2
  above): Goldsmiths' annotated portfolios; KTH's strong concepts and first-person
  design methods; CMU's research-through-design evaluation lenses; Candy's
  practice-research framework. The Society for Artistic Research's Research
  Catalogue is still active as of 2026 as another publication channel for
  practice-as-research. TU Delft's Delft Design Guide and a UK PRAG report page
  both failed to load when checked and were not verified.

### 4.3 Evaluation data: how to know whether an AI research tool is actually accurate

- **CiteME** (Press et al., NeurIPS 2024; arXiv 2407.12861): given a passage of
  text, find which paper it cites.
  - Frontier language models at the time scored 4.2–18.5% correct; humans scored
    69.7%;
  - CiteAgent, which adds search and paper-reading ability, scored 35.3% [abstract
    only];
  - This tested 2024-era models and current ones may do better, but the underlying
    point, "an AI-found citation is not itself evidence," has external data
    behind it.
- **Walters & Wilder 2023**: the fabricated-citation rates cited in Stage 13.
- **LitSearch, ScholarQABench, SciFact**: benchmarks for literature search and
  scholarly question-answering tools; not individually re-checked here.

### 4.4 Not recommended

- **SciScore, Penelope.ai**: upload the full manuscript to a third party.
- **The web versions of statcheck and rSPRITE**: send data to an external server.
  Use the R packages directly instead, since they cover the same need locally.
- **Consensus, SciSpace**: uploaded documents are processed in the cloud; this
  class of commercial research assistant (also Elicit, Undermind) has almost no
  independent accuracy evaluation available.
- **PaperQA2**: by default it calls a cloud-hosted model, and it builds its own
  separate index. It does not work from a literature library you already
  maintain. Running both means they will drift apart from each other over time.
- **CollabCoder**: see the table above. It sends data to OpenAI.

---

## 5. Which steps this kit treats as mandatory (defaults, open to revision)

The judgment call is "can this be fixed after the fact" and "can a program check
whether it was done well."

| Step | Default | Reason |
|---|---|---|
| Pre-data analysis plan `analysis-plan.md` (Stage 9) | **Mandatory**, gated by `tools/method/analysis_plan_check.py`; the finalized commit has to predate the start of data collection | The one genuinely irretrievable step in the whole process: pre-registration only means anything if it exists before the data does (Nosek et al. 2019); analytic flexibility inflates false positives (Simmons et al. 2011); ethics approval has to come before collection. Only required when new data will be collected or an effect will be claimed from data already in hand; skipped for a pure literature study; practice-based research substitutes a documented plan instead |
| Deviation log (Stage 10) | **Mandatory**, checked at delivery with `--phase6` | An unrecorded deviation gets quietly written up as the original design during drafting; recording it costs little |
| Method decision `method-decision.md` (Stage 8) | **Mandatory** | Comparable-study comparison is checkable, and the blind test shows a real gain (36% → 78%) |
| Pre-delivery literature update (Stage 13) | **Mandatory step**, written into the delivery checklist, no script | Can be done retroactively but is easy to forget; naming it as a step is enough |
| Literature synthesis matrix `literature-matrix.md` (Stage 4) | **Tracked as done or not**, quality not machine-checked | Whether the synthesis is actually good can't be judged by a program, and a hard gate here would just produce a filled-in form. The reporting-guideline literature makes the same point about itself: a completed checklist doesn't mean the work behind it was done well |
| Problematization, contribution type, Boote & Beile self-assessment (Stages 1, 4, 5) | **No gate**, guided by the template | Judgment calls, caught by skeleton review and the clean-context reviewer simulation instead |
| Adversarial pre-plan review (Stage 9) | **Folded into a field on the analysis plan** ("who reviewed this plan"), no justification required if nobody was available | Blocking the whole project because no reviewer was available would cost more than the step is worth, but it still gets written down either way |

**The risk in this table**: too many mandatory steps and every project ends up
filling out forms. So only two kinds are mandatory: steps that can't be fixed
after the fact, and steps with evidence behind them that they actually improve
quality. Adjust the list later if evidence shows a non-mandatory step was skipped
and something went wrong because of it.

---

## 6. Known limitations (read the originals before these go into a manuscript)

- **Secondhand only**: Swales 1990 (CARS), Crotty 1998 (the four-layer framework),
  Toulmin 1958, Booth, Colomb & Williams's *The Craft of Research*, Ravitch &
  Riggan, Lincoln & Guba 1985 (the four trustworthiness criteria), Tracy 2010
  (eight criteria, the secondhand source cites the 2020 edition), Klein 2007
  (pre-mortem), Chambers 2013 (registered reports), Hart 1999.
- **Abstract only**: Webster & Watson 2002 (the concept-organization argument's
  full text), Grant & Booth 2009, Snyder 2019, Torraco 2005/2016, Sandberg &
  Alvesson 2011, Alvesson & Sandberg 2011, Locke & Golden-Biddle 1997, Whetten
  1989, Corley & Gioia 2011, Haven & Van Grootel 2019, Wacharamanotham et al. 2020,
  Boettinger et al. 2026, Dobrescu et al. 2021.
- **Could not be found at all**: Paré et al. 2015 (a review-type typology), Egger
  et al. 1997 (language bias), Zimmerman, Stolterman & Forlizzi 2010 (an RtD
  critique).
- **Cross-domain analogy**: the literature behind problematization, CARS, and
  claim-strength calibration mostly comes from management, applied linguistics, and
  psychology. Applying it to design, art, and HCI is an inference. No study
  directly validating it in those fields was found.
- **Tooling limits at the time this was written**: a Semantic Scholar API call used
  during the underlying investigation was unreliable, so Crossref, OpenAlex, Europe
  PMC, and a general web search were used instead. Some "could not find" results
  above may reflect a tool failure. They do not necessarily mean the source
  doesn't exist.
