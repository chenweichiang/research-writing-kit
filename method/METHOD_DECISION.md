# Method Decision: Which Method Should This Topic Use

> This file answers **"which method should this topic use."** `METHOD_CARDS.md`
> answers "what does that method actually look like, and where does it usually go
> wrong." Phase 3.5 in `WORKFLOW.md` answers "can this design answer the question
> at all." The three run in that order; none replaces the others.
>
> Run this when: a new topic, a new proposal, deciding how to write up data you
> already have, or the author asks "what method should this be." When the method
> is settled and you reach the point of picking a specific statistical test or
> qualitative analytic approach, repeat the literature check for *that* narrower
> question (Step 3b). Don't reuse this document's defaults without checking.
> Retargeting to a different venue means repeating Steps 2 and 3: the venue's
> expectations changed, and so did what counts as a comparable study.

## 1. The core rule: check comparable papers first, whether or not you think you already know

Confidence is not evidence. Whether the answer feels obvious, half-remembered, or
genuinely unclear, the research design, the statistical test or model, and the
qualitative analytic approach all get checked against comparable published studies
before you decide what a field considers common or appropriate. The decision rules
and cards elsewhere in this kit only offer a starting point for checking: what a
field actually does for design, tests, coding approach, and reporting gets settled
by reading comparable papers.

**Write the pre-check judgment and the post-check judgment side by side** in the
decision memo, so it is visible whether checking the literature actually changed
anything. A decision made first, with supporting papers found afterward, defeats
the purpose of this step. **An approach you considered and then dropped after
checking also gets a one-line reason.** This step exists specifically because
silently dropping a correct approach for looking inconvenient is a real, observed
failure mode.

## 2. The nine-step procedure

Output: a project-root `method-decision.md`, one section per step below
(template: `templates/method-decision.template.md`).

1. **Claims first, method second.** List the research questions; tag each with a
   *question shape*. List the claims the paper wants to make and tag each with a
   *claim type*: causal, correlational, prevalence, experiential/interpretive,
   mechanism, design knowledge, feasibility, or interpretive argument. The claim
   determines the method: wanting to say "this improved outcomes" is a causal
   claim and needs a design that can rule out rival explanations; wanting to say
   "how students experienced X" needs none, and a pre/post test only props up a
   claim it can't actually carry.
2. **Map the conditions.** Who the participants are and how you'd actually reach
   them; the power relationship between researcher and participants (your own
   students, people you grade, a tool you built being rated by people you
   recruited); whether the data already exists or will be newly collected (and if
   it already exists, whether the analysis was planned before it was collected);
   time and staffing; ethics review; the target venue's methodological
   expectations (loop back to `venue-notes.md`). **Read the venue's current-year
   original documents** (the call for papers, the review rubric, author
   guidelines) for what it actually expects; this file and the method cards'
   venue notes are only a quick-reference, and anything you can only mark "not
   checked against the original" needs the original read before you rely on it.
3. **Find at least 8 comparable studies, read their methods sections, fill a
   comparison table.** Search your own local literature library first if you have
   one; then Semantic Scholar / OpenAlex / Crossref. At least half should come
   from the target venue or a genuinely comparable one, mostly from the last five
   years plus one or two field classics. Columns follow the extraction table in
   `templates/literature-matrix.template.md`: venue, question shape, design,
   sample, data, analysis, quality criteria, and criticized weaknesses or the
   authors' own stated limitations. Anything read only as an abstract is tagged
   `[abstract only]`. That tag can't cover more than half the set.
   3b. **Compare analysis methods specifically.** From the same batch, pull out
   each paper's actual analysis practice. For quantitative work: which test or model,
   how effect sizes and confidence intervals are reported, how multiple
   comparisons are corrected. For qualitative work: the analytic stance (reflexive thematic
   analysis / codebook-style coding / grounded theory / content analysis / …),
   the coding procedure, how agreement or reflexivity is handled, plus anything
   reviews or later literature have criticized about these choices. Do this for
   at least 5 papers and fill the memo's analysis-method comparison table. Keep a
   search trail the same way Phase 1 of the main workflow does. When the amount
   of table-reading is large, you can split it across a separate Claude
   conversation, but **every row still has to be traced back to the original
   text by whoever wrote the memo**: a delegated extraction is not itself
   evidence, and the person assembling the memo spot-checks it.
4. **Write down the observations.** What's mainstream, what's a minority practice
   and why its authors chose it, what weakness keeps recurring, and what the
   current project's own conditions rule out. The weaknesses of comparable
   studies are the reviewer's default list of objections to this one.
5. **List at least two candidate methods, each checked against a method card.**
   For every candidate, write out: which claims from Step 1 it can and can't
   support; the analysis method (able to point to specific rows in the Step 3b
   table); **how the core construct is actually measured or observed, and the
   most plausible alternative explanation** (a generated result that looks like
   it preserved brushwork might just be an artifact of the sampling settings; a
   construct measured only by stitching together adjacent proxy variables isn't
   measuring what it claims to); **an independent check beyond the
   researcher**: when the researcher is the sole judge, plan for at least one of
   a second coder, a blinded rater, an outside expert, or third-party data
   collection; narrowing the claim is not a substitute for this. This is the
   single item candidates most often skip, and it is worth naming explicitly
   because it is the one the internal blind test below (Section 4) found missing
   most often. How the sample size is justified (power analysis, information
   power, saturation, case-selection logic) depends on the method and the four
   are not interchangeable. Feasibility, and the objection a reviewer is most
   likely to raise. The decision index at the top of `METHOD_CARDS.md` is a
   starting point for this list; the card's own text is the final word.
6. **Align the decision with the claims.** Which candidate was chosen and why
   (loop back to Steps 1, 2, 4); why the others weren't. Every claim from Step 1
   goes into an alignment table; any claim the chosen method can't fully carry
   gets downgraded in the memo's own wording. Write "scores rose from pre- to
   post-test" and avoid the stronger claim "the intervention improved scores"
   whenever a testing effect can't be ruled out.
7. **Pre-mortem.** Assume the paper is rejected, or the project stalls, a year
   from now. Write the three most likely method-related reasons and one
   preventive action for each.
8. **Next actions.** Whether a design diagnostic is needed, sample size or
   information-power target, which reporting guideline applies, pre-registration,
   the ethics-review timeline, and data-collection checkpoints: who confirms the
   data actually arrived and is usable, and by when (attendance at a session is
   not the same thing as usable data).
9. **Format gate, then hand to the author.** Run
   `python3 tools/method/method_decision_check.py method-decision.md`. Only after
   it passes does the memo go to the author for sign-off in a language they can
   check; only after sign-off does analysis, or a design diagnostic, begin. The
   gate proves the memo covers everything it should. It does not prove the
   method chosen is the right one.

## 3. Finding comparable studies

Query order: your own local literature library, if you keep one, first (fast, and
biases toward the reading you've already vetted), then Semantic Scholar,
OpenAlex, and Crossref for anything the local library doesn't have. Neither source
alone is enough: a personal library is a convenience sample of what you happened
to collect. It does not survey the field, and a keyword search alone under-counts
papers that use different vocabulary for the same design.

When there are many candidate papers and reading every methods section yourself
is the bottleneck, you can split the extraction work across a separate Claude
conversation (or several): one paper per thread, each returning the extracted
table row plus the exact quoted sentence it came from. **Every row still traces
back to the original text**; a summary produced by a conversation that never
opened the PDF is not evidence, and the person compiling the memo spot-checks a
sample of the returned rows against the source before trusting the rest.

## 4. Output and the one hard gate

- `method-decision.md` in the project folder (template:
  `templates/method-decision.template.md`), checked with
  `python3 tools/method/method_decision_check.py method-decision.md`
  (`--selftest` runs the checker's own regression tests).
- **When the project will collect new data, or claim an effect from data it
  already has, also produce `analysis-plan.md`** (template:
  `templates/analysis-plan.template.md`), checked with
  `python3 tools/method/analysis_plan_check.py analysis-plan.md` before data
  collection starts, and again with `--phase6` before delivery (it also checks
  that any deviation from the plan during data collection got logged).

**Why the analysis plan is the one genuinely hard gate in this whole process.**
Everything else here can be revisited and corrected after the fact: a weak
method-decision memo can be rewritten, a missed comparable study can be added
later, even a chosen test can sometimes be swapped before submission. A
pre-registered analysis plan cannot: it only does its job if it exists *before*
the data does. Writing it after the data is in hand and calling it a plan
protects against nothing, because every "flexible" analysis choice (which
exclusion rule, which scoring method, which model) can then be quietly picked to
favor the result you already have, and there is no way for a reader to tell the
difference from the outside. This is why it is the only step in this file backed
by a mechanical, non-negotiable gate. Every other step here relies on a
checklist to use your own judgment against.

## 5. Tools

- **`tools/refs/lit_map.py`**: given a batch of references, surfaces candidate
  classics and co-cited papers. Useful for Step 3's "what does this field
  actually treat as canonical" question, and as a check on whether the comparable
  studies you found were pulled from a genuinely diverse citation neighborhood.
  A neighborhood dominated by one small clique that cites itself is a warning
  sign worth checking.
- **`tools/method/tea_second_opinion.py`**: a second opinion for simple designs'
  classic tests (two-group difference, correlation, chi-square, one-way ANOVA).
  It does **not** cover mixed models or ordinal regression. When its suggestion
  disagrees with this file's default rules or with what the comparable papers
  actually did, that disagreement is a reason to look closer. Don't treat the
  tool's suggestion as an automatic tiebreaker.
- **Design diagnostics**: R's `DeclareDesign` package (see `WORKFLOW.md` Phase
  3.5). Only relevant when new data will be collected *and* an effect will be
  claimed; it diagnoses whether the design itself can answer the question
  (coverage, not just power) before any test is chosen.

## 6. Lite mode (no local tools installed)

Every step above still gets done by hand; the tools only save time or catch
mechanical slips.

- **No local literature library**: search Semantic Scholar, OpenAlex, and
  Crossref directly (web search or their free APIs). Screen by abstract first,
  then read full text for the roughly eight papers that will actually go into the
  comparison table.
- **No `lit_map.py`**: track by hand which papers keep reappearing in the
  reference lists of your comparable-study set; a paper cited by most of them is
  a plausible classic, but verify it by reading it. Don't trust the count
  alone.
- **No `tea_second_opinion.py`**: for a simple two-group or correlational
  design, reason through the test choice by hand against the cross-method tables
  in `METHOD_CARDS.md`, and note in the memo that no automated second opinion was
  run.
- **No R / `DeclareDesign`**: reason through Phase 3.5's questions in prose:
  what besides the intervention could move the outcome, and does the design let
  you tell them apart? State the claim's ceiling honestly in the limitations
  section. Do not skip the question just because the tool isn't installed.
- **No format-gate script**: manually check the finished `method-decision.md`
  against every section heading in `templates/method-decision.template.md`: every
  section present, every field either filled in or marked "not applicable +
  why," nothing left blank.

## 7. The honesty boundary, and an internal blind test

Method choice rarely has one correct answer. The same topic usually has two or
three defensible options. The memo is judged on whether the claims and the method
actually line up, and whether it anticipated what a reviewer would object to.
It is not judged by matching some reference answer.

An internal blind test on seven past cases, scored against a single reviewer who
already knew the cases, found: following this nine-step procedure anticipated
the real method-related problem in the case 78% of the time, against 36% for the
same judgment made before checking the comparable literature. This single
reviewer already knew the cases, so treat the comparison as a lower bound on
rigor; it is not an independent validation. **The single item
most often missed was an independent check beyond the researcher** (Step 5).

## 8. Reporting guidelines

Journals, especially in education and health, often require a checklist for one of these guidelines, and reviewers use them as a completeness check. Look up what the target venue requires when you choose the venue, because many items (for example, the prior relationship between interviewer and participants) cannot be added after data collection.

| Study type | Guideline | Notes |
|---|---|---|
| Qualitative (interviews, focus groups) | COREQ (32 items) or SRQR (21 items) | COREQ assumes structured coding and multiple coders, which sits uneasily with reflexive thematic analysis; Braun & Clarke proposed their own reporting guidance (RTARG, 2024). Coding of texts, logs or questionnaires will leave some COREQ items not applicable; say which and why. |
| Randomized trials | CONSORT (CONSORT-SPI for social and psychological interventions) | Also applies to a wait-list design when allocation is randomized. |
| Non-randomized interventions (single-group pre–post, non-randomized wait-list or staggered start) | TREND | The most common design in classroom research. |
| Observational or cross-sectional | STROBE | Survey-style studies. |
| Systematic reviews and meta-analyses | PRISMA 2020 | Includes a search flow diagram; the R package `PRISMA2020` draws it. |
| Scoping reviews and method maps | PRISMA-ScR (Tricco et al. 2018) | Judging a scoping review by PRISMA 2020 standards leads to mismatched criticism. |
| Mixed methods | GRAMMS | |

A completed checklist shows the report is complete. It does not show the study was done well.

## 9. See also

Method-specific analysis cards live in `METHOD_CARDS.md`: grouped quantitative,
qualitative, mixed/design-research, and arts/practice-based. It opens with two
sections worth reading before Step 5 above: a **decision index** (by question
shape: candidate methods, what each can and can't support, how to justify a
sample size, and the objection each draws most often) and a set of
**condition-triggered warnings** (what changes when the researcher is also the
instructor, when there's only one class or cohort, when the analysis plan was
written after the data was already collected, when the research object is the
researcher's own work, or when ethics approval hasn't come through yet). Step 5
starts from those two sections, then reads the full card for whichever methods
are candidates.
