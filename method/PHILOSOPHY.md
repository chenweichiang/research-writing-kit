# The Method — Philosophy

> Why this workflow is shaped the way it is. If you only read one file to
> understand the spirit of the kit, read this one.

## The core bet: skeleton before prose

The single biggest cause of "AI writing" that reads flat, generic, and slightly
wrong is that the model was asked to *write* before the *argument* existed. When
prose is generated from a blank page, the model fills gaps with plausible filler,
and that filler is exactly what makes writing feel machine-made and what smooths
away an author's real thinking.

So the method inverts it. **Build the argument skeleton first.** Every section is
a node with four parts:

- **Claim** — what this passage is trying to establish.
- **Move** — which argumentative move it uses (open a gap, concede-then-rebut,
  reframe, ground in a concrete case…). See `ARGUMENTATION.md`.
- **Evidence** — which *verified* source, case, or analysis result backs it, with
  a citation.
- **So-what** — what this node does for the whole paper.

Prose is then written *bound to the skeleton*, with no room to wander into filler.
This is the anti-homogenization mechanism: the sameness comes from words the model
invents on its own, so we don't let it invent — we let it phrase an argument the
author owns.

## Division of labor

| The human (author) | Claude (co-author) |
|--------------------|--------------------|
| Decides **what to say** and what the contribution is | Finds and **verifies** the literature |
| Owns the argument and the ideas | Researches the **venue's** current format & review norms |
| Gives **final sign-off** | Designs method / runs quantitative or qualitative analysis when needed |
| Reads, reacts, iterates | **Writes the draft** bound to the skeleton |
| | **Checks its own work** every step before handing back |

The author is never asked to trust a black box. The reason Claude does the
verifying and self-checking is precisely so that what reaches the author is
*already clean enough to judge*. A half-checked draft wastes the author's
attention; the point of the labor split is to spend Claude's effort so the human
spends theirs only on what's genuinely theirs — the ideas.

## Two modes

- **Default: "write it all the way to good."** The author names a topic; Claude
  goes all the way to a *verified complete first draft* before handing back. The
  skeleton is built, but as an internal working file, not a gate. The author then
  steps in and iterates.
- **Skeleton-collaboration mode** (only when the author explicitly asks "just
  build the skeleton first" / "develop the argument, don't write yet"): the
  skeleton is handed over for approval before any prose is written.

Default to the first. Most authors want you to *handle it* and then react to
something substantial, not to approve an outline first.

## Why "sounds like the author" matters

When you write in the author's native language and you have samples of their real
writing, match their voice. Not as flattery — because the author's voice carries
their thinking, and generic academic prose quietly replaces the author's argument
with the model's defaults. Preserve their sentence rhythm, their connectives,
their register. **Passages the author wrote themselves are assets: preserve first,
rewrite only when necessary.**

Where you have no voice samples (common for a second language the author doesn't
write themselves), don't fake a voice. Aim instead for *faithful, strong academic
prose in the venue's register*, and — critically — give the author a way to check
that the meaning is right (e.g. a back-translation into a language they read).

## Honesty is built in, not bolted on

- **No fabricated citations.** This is the first rule for a reason (`IRON-RULES.md`).
- **Report effect sizes and confidence intervals, not just p-values.** Don't
  claim "no effect" from a non-significant p — that requires an equivalence test.
- **Data stays local.** Unpublished drafts and raw/participant data never go to a
  cloud tool or a public AI detector.
- **De-AI before delivery, and review with fresh eyes.** The writer's own
  self-review shares the writer's blind spots; a clean second pass catches what
  the drafting context hid.

These aren't add-ons for the finicky. They are what makes the output trustworthy
enough to put your name on.
