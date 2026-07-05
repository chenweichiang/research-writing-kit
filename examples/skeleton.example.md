# Skeleton (worked example) — an anonymized HCI-style paper

> A short, filled-in example of what a real `skeleton.md` looks like, so the
> author's Claude has a concrete target. Fictional content; any resemblance to a
> real study is coincidental.

Contribution claim (one sentence): A tangible desk widget that surfaces ambient
team availability reduces interruption-related task switches without lowering
felt connectedness.
Target venue (author's call): a mid-tier HCI conference (systems + study track).
Output language: English (author writes English → no voice-match; back-translation
to their native language for sign-off).

---

## Section: Introduction

### Node: the interruption gap
- **Claim:** Remote teams lack a low-effort, glanceable signal of when a colleague
  is interruptible, so they over-rely on synchronous pings.
- **Move:** open-gap
- **Evidence:** [Two field studies of remote-work interruption] — status: verified
  - *Source card:* Both report that ambiguous availability drives defensive
    always-on messaging; supports the "need a glanceable signal" claim.
- **So-what:** Motivates a tangible ambient display as the design response.
- Flags: —

### Node: why tangible, not another app
- **Claim:** A physical desk object is glanceable in a way an on-screen indicator
  is not, because it doesn't compete for the screen the interruption happens on.
- **Move:** reframe (the problem isn't "more presence data," it's "presence off the
  contested screen")
- **Evidence:** [Ambient/calm-tech design literature] — status: ❓unverified (need
  to confirm the specific claim about attention competition)
- **So-what:** Positions the artifact contribution against prior on-screen tools.
- Flags: `❓citation-unverified`

## Section: Study

### Node: the availability widget reduces interruptive switches
- **Claim:** With the widget, task switches attributable to incoming pings drop
  relative to baseline.
- **Move:** eliminate-alternatives (rule out novelty effect and self-selection)
- **Evidence:** [2-week within-subjects deployment, n=18] — status: needs-analysis
- **So-what:** The core empirical claim of the paper.
- Flags: `⚠needs-analysis`
- **Load-bearing assumptions / open rebuttals:** assumes the switch reduction is
  the widget, not a Hawthorne/novelty effect (needs the week-1-vs-week-2 contrast);
  single team, single org → generalization is an open rebuttal to state as a limit.

---

## Load-bearing assumptions & limitations (summary)
- Effect attributed to the widget rests on ruling out novelty (report the
  within-deployment trend + effect size with CI, not a bare p).
- Single team / single organization: scope the claim; don't generalize to all
  remote teams. This is a limitation to write honestly, not to hide.
