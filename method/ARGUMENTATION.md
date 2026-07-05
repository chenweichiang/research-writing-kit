# The Method — Argumentation Moves (internal diagnostic)

> 🔴 **This is not a menu to sprinkle into a draft, and not something to teach the
> author.** It is a checklist *you* (Claude) consult while building the skeleton,
> to ask "is this argument actually doing work, or just asserting?" The author
> never needs to see these labels. Choosing a move for *this specific* argument is
> the point; pasting move-names into prose is the failure.

## Why moves, not templates

Weak academic writing asserts; strong academic writing *moves* the reader from
something they accept to something they didn't. When a skeleton node's **move**
field is empty or just "state the finding," that node is usually a flat assertion
that a reviewer will push on. Naming the move forces the argument to earn its claim.

## The moves (pick the one that fits the node)

- **Open a gap.** Establish that something important is unknown / unresolved /
  mishandled, so the reader feels the need your work fills. (Most introductions.)
- **Concede, then rebut.** Grant the strongest version of the opposing view, then
  show where it fails or falls short. Buys credibility; disarms the obvious objection.
- **Reframe.** Show the usual framing of a problem is the wrong one, and a different
  frame dissolves or relocates it. High-value, high-risk — needs real support.
- **Ground in a concrete case.** Move from abstraction to a specific instance the
  reader can see, then generalize back. Powerful for design/qualitative work.
- **Eliminate alternatives.** Rule out competing explanations to leave yours
  standing (abductive / eliminative). Requires you actually address the rivals.
- **Build a chain.** Each step licenses the next; the conclusion follows only if
  every link holds. Make the load-bearing link explicit so you can defend it.
- **Contrast / calibrate.** Place your result against a baseline or expectation so
  its size and direction are legible (this is where effect sizes + CIs live).

## How to use it in the skeleton

For each argument node:
1. Write the **claim**.
2. Ask: *which move earns this claim?* Put it in the `move` field.
3. Ask: *does the evidence in this node actually execute that move?* If the move is
   "eliminate alternatives" but no rival is addressed, the node is incomplete.
4. For core causal / eliminative nodes, record the **load-bearing assumption** the
   move depends on and any **open rebuttal** you haven't answered — that's the raw
   material for an honest limitations section (and for the optional Phase 4.5 check).

## Honesty ceiling

Reviewers don't hand you "you're missing a premise" — they hand you a *defeating
argument*. So the real test of a move isn't logical validity alone; it's whether
the claim still stands after the strongest attack. Treat every move as defeasible.
If a node only survives because a rival wasn't considered, it doesn't survive —
write the limitation instead of hiding it.
