# The Method — Iron Rules

> The non-negotiables. Every generated skill must preserve all of these. You may
> simplify the *wording* for a non-technical author; you may not drop the *rule*.
> If following a rule and pleasing the author conflict, follow the rule and
> explain why.

## 1. Never fabricate a citation

Every reference that enters a draft must be **really obtained** and its **support
direction verified** — i.e. you actually read enough of the source to confirm it
says what you're citing it for, and in the right direction. If you cannot get the
full text or verify it, mark it `❓unverified` and never present it as established.
A plausible-looking citation you did not verify is a fabrication.

## 2. Build the skeleton; don't gate by default

Always build the argument skeleton (`skeleton.md`) before writing prose — it's
the quality engine and the cross-session source of truth. But in default mode you
do **not** wait for the author to approve it. Send a one-page direction summary as
*non-blocking* (they can interrupt anytime — early interruption is cheap), and
keep going. Only in explicit skeleton-collaboration mode do you wait for sign-off.

## 3. The author signs off in a language they can actually check

Working language for thinking and the skeleton = the author's strongest language.
If the final paper is in a language the author does **not** write themselves,
deliver a **back-translation** into a language they read so they can verify the
meaning — and produce that back-translation with an **independent pass** (fed only
the finished text, not the skeleton or intent), so the writer's blind spots show.

## 4. Data stays local; report effect sizes + CIs

Follow the venue's methodological expectations. Profile the data before analyzing.
Don't treat Likert items as continuous. Fix random seeds. Report effect sizes with
confidence intervals, not bare p-values. Never claim "no difference" from p > .05
(use an equivalence/Bayesian test). **Unpublished drafts and raw data never leave
the author's machine** — no cloud detectors, no public LLM uploads.

The details that reviewers actually catch:
- **Likert.** A single item is ordinal → cumulative-link / ordered-probit models
  (`clmm`, `ordinal`), not means. A multi-item *summed scale* may be treated as
  approximately continuous, but then report its reliability (Cronbach's alpha or
  omega) — no alpha, no scale.
- **ART only for continuous DVs.** Aligned Rank Transform is for factorial designs
  with a continuous outcome. Feeding it Likert, ordinal, count, or binary outcomes
  inflates Type I error (Tsandilas 2024). Those go to `clmm` (ordinal) or GLMMs
  (Poisson / negative-binomial / binomial).
- **Multiple comparisons.** Any correction must be named (Tukey, Holm, FDR…), with
  the family it was applied over.
- **SESOI is declared at design time.** Equivalence / "no meaningful difference"
  claims need a smallest effect size of interest that was chosen *and justified*
  before the data existed; a SESOI picked after seeing the result is not one.
- **Bayesian: three roads, one reporting rule.** If the model is a hierarchical
  regression you can write as a formula → `brms`. If the question is "evidence for
  the null" (BF01) → `BayesFactor`. If the model needs discrete latent variables,
  a custom distribution, or a custom sampler (mixtures, latent classes, HMM states,
  a JAGS legacy model) → `nimble`. All three report priors, a prior-sensitivity
  note, and convergence diagnostics.
- **Design before power.** If the paper will *claim* an effect from new data, first
  ask whether the design can answer the question at all (bias and coverage, not
  just power — see `WORKFLOW.md` Phase 3.5). A single-group pre/post cannot separate
  the intervention from testing/maturation: add a control, or downgrade the claim
  to non-causal in the text.

## 5. "Sounds like the author" only where you can be sure

Match the author's voice when writing in a language they write themselves and you
have real samples (a filled-in `VOICE_PROFILE`). In a language they don't write,
there is no "their voice" to match — aim for faithful, strong academic prose
instead of pretending. Preserve author-written passages; rewrite them only for
real errors or necessary structural fixes.

## 6. Delivery comes with a verification report

Every first draft or major revision you hand back includes: a citation-by-citation
verification result, a point-by-point check against the venue's *current* official
rules, proof the language toolchain is clean, and the `❓unverified` list. Don't
hand over anything you haven't cleaned yourself first — the author needs a
reasonably complete, checked version to be able to judge it.

## 7. The deliverable is formatted, from the first version

Deliver in the venue's format — the official template, or, absent one, the format
of the author's previously submitted documents (margins, font sizes, section
styles, table style). Layout is itself a review item. `skeleton.md` and draft
markdown are *internal working files*, never the thing you hand over. Don't ship
raw markdown as if it were the paper.

## 8. Files are the only authority — the conversation is not

Long sessions drift: after a context compaction the model still carries a half-
decayed story of what was decided, and it fights the files without noticing. That
is the structural cause of "it keeps changing the wrong thing," not a memory lapse.
So:
- **Every phase ends by writing back** to `skeleton.md`'s `## Progress` block: what
  is done, what's next, open questions, known risks, which files were touched. A
  rule that only says "read" and never "write" guarantees the file falls behind.
- **The first action of a new session, or after a compaction,** is to re-read
  `skeleton.md`, `venue-notes.md`, and the numbers ledger — and to say so plainly
  ("the conversation is not authoritative; the files are"). What the files don't
  record did not happen; to continue an earlier judgement, find it in the files
  first, and if it isn't there, redo it or ask.
- **When they conflict, the files win**, and the conflict is reported (it usually
  means the previous round skipped the write-back).
- **Numbers included.** Every number in the draft traces to the computation that
  produced it, in the numbers ledger (`skills/doc-regress`, template in
  `tools/regress/numbers-ledger.template.md`). Re-run the analysis → update the
  ledger → *then* edit the prose → run the regression check. Reversing the order
  hides the stale value from the check.

---

### A note on the "honesty ceiling" (for any formal-checking add-on)

If you use a formal argument checker (e.g. an SMT solver or a defeasible-argument
tool) to stress-test a core causal claim, remember what it does and doesn't prove:
it checks *validity and formal acceptance*, not *truth*. The propositions and
attacks are ones you encoded — garbage in, garbage out — so the formalization
itself must be human-reviewed. It complements adversarial human review; it never
replaces it.
