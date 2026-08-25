# The Method — Argumentation Moves (internal diagnostic)

> 🔴 **This is not a menu to sprinkle into a draft, and not something to teach the
> author.** It is a checklist *you* (Claude) consult while building the skeleton,
> to ask "is this argument actually doing work, or just asserting?" The author
> never needs to see these labels. Choosing a move for *this specific* argument is
> the point; pasting move-names into prose is the failure.
>
> Every move below carries a **When not to use**. That line matters more than the
> move itself: over-using a top-tier move is the most AI-looking kind of bombast
> there is. A move that isn't earned reads as performance.

## Why moves, not templates

Weak academic writing asserts; strong academic writing *moves* the reader from
something they accept to something they didn't. When a skeleton node's **move**
field is empty or just "state the finding," that node is usually a flat assertion
that a reviewer will push on. Naming the move forces the argument to earn its claim.

## Three parent principles (everything below is an application of these)

1. **One load-bearing concept, not a stack of points.** Strong papers rest almost
   the whole argument on *one* conceptual move driven all the way through. Average
   papers pile up five or six claims of equal weight. Before writing, answer: *which
   single sentence is this paper's load-bearing wall?* If you can't, the skeleton
   isn't done.
2. **Execute the move; don't announce it.** Strong writers never say "we now reframe
   the problem" — they reframe it, so the reader arrives at the conclusion as if
   they found it themselves. Rhetoric at its most efficient lets the reader walk;
   it doesn't push. ("First… second… finally…" is the announcing habit; it is also
   a standard AI tell.)
3. **Name things precisely enough that the name does half the arguing.** A tight
   coinage points by itself and needs no re-definition later. The inverse also
   holds: a loose new term is a concept show, and it hurts the thinking. Borrow an
   established term when one exists.

These three are also anti-homogenization principles: generic AI prose stacks
parallel points, announces its structure, and reaches for big loose words. The
parent principles are the opposite of each.

## The moves (pick the one that fits the node)

- **Open a gap.** Establish that something important is unknown / unresolved /
  mishandled, so the reader feels the need your work fills. (Most introductions.)
  *When not to use:* when the "gap" is only that nobody has done your exact
  combination yet — that's an absence, not a need. A gap must matter to someone
  besides you.
- **Concede, then rebut.** Grant the strongest version of the opposing view, then
  show where it fails or falls short. Buys credibility; disarms the obvious objection.
  *When not to use:* when the opposing view is not held in good faith, or when
  you'd be conceding a straw version. Too many concessions in a row read as evasive
  and drag the pace.
- **Reframe.** Show the usual framing of a problem is the wrong one, and a different
  frame dissolves or relocates it. High-value, high-risk — needs real support.
  *When not to use:* when the claim is already a marginal view that needs no
  flipping — forcing a reframe there is contrived. A reframe needs a *genuine*
  re-classification to stand on, otherwise it is sophistry.
- **Ground in a concrete case.** Move from abstraction to a specific instance the
  reader can see, then generalize back. Powerful for design/qualitative work.
  *When not to use:* the case must be real and checkable (an invented one collapses
  at the first question); don't stretch a case with no development into a long
  one; and don't stack more than three or four levels of "and this implies…".
- **Eliminate alternatives.** Rule out competing explanations to leave yours
  standing (abductive / eliminative). Requires you actually address the rivals.
  *When not to use:* when you can only rule out the rivals you happened to think
  of. If a reviewer can name a rival you didn't address, the move fails outright —
  write it as a limitation instead.
- **Build a chain.** Each step licenses the next; the conclusion follows only if
  every link holds. Make the load-bearing link explicit so you can defend it.
  *When not to use:* when a link is only plausible, not supported — a chain is as
  strong as its weakest step, and reviewers look for exactly that step. Long
  chains in a short paper look like over-reach.
- **Contrast / calibrate.** Place your result against a baseline or expectation so
  its size and direction are legible (this is where effect sizes + CIs live).
  *When not to use:* against a baseline nobody would defend (a strawman baseline
  flatters any result), or with a post-hoc split that has no theoretical reason —
  that is fishing, not calibration.

## How to use it in the skeleton

For each argument node:
1. Write the **claim**.
2. Ask: *which move earns this claim?* Put it in the `move` field.
3. Ask: *does the evidence in this node actually execute that move?* If the move is
   "eliminate alternatives" but no rival is addressed, the node is incomplete.
4. Check the move's *When not to use* line against this node honestly.
5. For core causal / eliminative nodes, record the **load-bearing assumption** the
   move depends on and any **open rebuttal** you haven't answered — that's the raw
   material for an honest limitations section (and for the optional Phase 4.5 check).

## Empirical-paper craft (Methods / Results / Discussion)

The moves above come mostly from theoretical and critical writing. Empirical
papers are won or lost on a different skill: *reporting* a study so that a
reviewer believes it. These are the recurring patterns in well-reported empirical
work, each with its own "when not to use".

### Methods — transparent enough to believe and to replicate
- **The transparency ladder.** Three rungs, in order: how assignment was done →
  what participants in each condition actually did → **how alternative
  explanations were excluded**. A constraint on the design ("participants could not
  re-prompt the system") is itself causal evidence — say what you disallowed and why.
- **Make decisions visible.** "We conducted thematic analysis" is not a method.
  State the four to six real decision points (inductive vs deductive; semantic vs
  latent; the epistemological stance; what counted as a theme) and the reason for
  each. Otherwise the qualitative work invites the "anything goes" objection.
- **Mechanize the construct.** A fuzzy construct ("creativity", "engagement")
  becomes reportable when you show the path: explicit feature list → blind raters →
  inter-rater reliability → scoring formula. The reader must see *why these
  features*.
- **Open question before formal hypothesis.** Lead with the research question,
  then refine into testable sub-hypotheses. *When not to use:* when the literature
  already predicts a single direction strongly — an open RQ then reads as hedging.

### Qualitative rigour — pre-empt "this is just impression"
- **Admit the limitation first, then show the control.** Themes are *constructed*
  by the researcher, not "emerging" from the data. Say so, then list the mechanisms
  that keep the subjectivity in check (multiple independent coders, reliability
  coefficient, member checking or the reason for not doing it, a documented
  codebook history, reflexivity / positionality — the teacher-as-researcher power
  relation especially). Admission without control is abdication; control without
  admission looks naive.
- **The four items reviewers ask for:** saturation criterion; reflexivity /
  positionality statement; member checking (or why not); and, for translated
  quotes, **who translated, whether it was back-checked, and whether the original
  is provided**. Venue-named reporting checklists (COREQ, SRQR) ask precisely these.
- **Quotes are evidence, not decoration.** Every quote sits inside an analytic
  sentence ("this shows…"), embedded in the narrative rather than dropped as a
  block; choose the *representative* quote, not the most vivid one. State the
  criterion for what counts as a theme, and say explicitly that frequency is not
  importance.
- **An audit trail.** Report what each analysis stage produced (code list, theme
  map) and admit the process was recursive, not linear.

### Results — narrate in argument order, don't dump tables
- **Main effect → heterogeneity → so-what.** Order findings by what the argument
  needs, not by the statistical workflow (t-test → ANOVA → interaction). Each layer
  answers a different question.
- **Frame heterogeneity in one contrast sentence** ("no effect for group A; large
  gain for group B") with the slope figure to match. *When not to use:* a subgroup
  split with no theoretical expectation is fishing.
- **Let numbers and cases speak together.** In mixed-methods work, pair each
  quantitative relation with the qualitative case that shows the mechanism, in the
  same section — not interviews quarantined at the end.
- **Null and reversed results, told straight.** State the expectation → the result
  went the other way → what the qualitative data suggested about why. The force
  comes from *saying it didn't work and finding out why*, not from re-cutting the
  metric until something appears.

### Statistical reporting — the effect-size triple
- Never a bare "p < .001". Write the **effect in real units, the coefficient, and
  the interval** together (e.g. "+8.1 % (b = 0.31, 95 % CI [0.19, 0.43], p < .001)")
  so the reader sees significance and size at once. This is Iron Rule 4 as prose.
- **Correlation with a story.** A moderate correlation is a *lead*; the mechanism
  and direction come from the qualitative layer. Neither hide behind "correlation
  is not causation" nor stop at the correlation.
- **Report the ledger row, not a memory.** Every number in Results traces to the
  numbers ledger (`skills/doc-regress`); an unmatched number is a defect, not a
  rounding issue.

### Scale / instrument validation — so others dare to adopt it
- **Triangulate the constructs.** Show where each factor came from through
  *independent* sources (theory clusters → card sort → vocabulary check → factor
  analysis). Each layer from a different origin blocks the "invented factors" charge.
- **Confess the weak subscale and repair it.** A low reliability in one context is
  reported with its cause and a follow-up design — not buried.
- **Translate scores into design implications** (a low score on factor X → change
  what) so the instrument is actionable, and **declare the construct boundary**
  (where it applies, where it doesn't, how it may be modified) to protect
  comparability.

### Discussion — climb three floors
- **Mechanism → user strategy → system design.** Don't stop at "the problem is
  confirmed"; each floor answers what the previous one implies.
- **Promote a limitation to a contribution only when the data support it** — a
  negative finding can become a genuine theoretical point (a social dilemma, a
  trade-off). *When not to use:* when the "limitation" is a flaw in the data; then
  this move is whitewashing.
- **Name a phenomenon the existing frame missed** — the empirical form of parent
  principle 3. *When not to use:* when an existing term already fits, or when the
  coinage outruns what the data show.

> **Division of labour between the two halves of this file:** the moves teach how to
> *frame* an argument; the craft section teaches how to *report* a study. Theory and
> design essays lean on the first; empirical papers lean on the second. Both sit
> under the same iron rules: effect sizes + CIs, Likert as ordinal, seeds fixed,
> every number traceable.

## Honesty ceiling

Reviewers don't hand you "you're missing a premise" — they hand you a *defeating
argument*. So the real test of a move isn't logical validity alone; it's whether
the claim still stands after the strongest attack. Treat every move as defeasible.
If a node only survives because a rival wasn't considered, it doesn't survive —
write the limitation instead of hiding it.
