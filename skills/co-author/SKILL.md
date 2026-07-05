---
name: co-author
description: Collaborative long-form academic writing — papers AND grant/funding proposals. Use when the author says "help me write this paper", "turn these sources into a paper", "develop this", "build the skeleton", "co-author", or wants to write a grant/funding/fellowship proposal, or has an existing draft to rewrite/upgrade/resubmit ("rewrite this", "it got rejected, submit elsewhere", "turn this talk/old proposal into a journal paper" → Phase 0.5). Division of labor = the author decides what to say and gives final sign-off; Claude verifies literature, researches the venue's current format and review norms, designs method / runs analysis when needed, writes the draft, and self-checks every step. Default = "write it all the way to a verified complete draft"; only build-skeleton-first when the author explicitly asks. For check-only (don't rewrite) → paper-review; for slides → a deck skill.
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

## The pipeline (see `method/WORKFLOW.md` for the full version)

- **Phase 0 — Intake:** topic/sources, target venue + output language, existing data?,
  mode, existing draft? (→ 0.5).
- **Phase 0.5 — Onboard existing draft:** provenance triage (preserve author-written
  passages), reverse-extract skeleton, treat old citations as unverified, disposition
  table, read a real sample before judging.
- **Phase 1 — Two-track scouting:** (A) literature via citation graphs + web, holdings
  are a convenience sample not the canon; (B) the venue's **current** format & review
  norms → `venue-notes.md`.
- **Phase 1.5 — Direction summary:** one page (gap/angle + contribution + main line +
  recommended venue as explicit options). Non-blocking in default mode.
- **Phase 2 — Verify & fetch:** read each source enough to confirm direction; check
  DOIs/ISBNs; `❓unverified` for anything you couldn't confirm.
- **Phase 3 — Method/analysis:** design or analyze; data local, effect sizes + CIs,
  Likert ordinal, seeds fixed; fold results back into skeleton nodes.
- **Phase 4 — Skeleton:** each node = claim / move / evidence(+source card) / so-what,
  with flags; core causal nodes get load-bearing-assumptions. Save `skeleton.md` in the
  project folder. (Optional Phase 4.5 formal check for a single core causal claim.)
- **Phase 5 — Write the full first draft:** bound to the skeleton, into the format.
  Own language → voice-match + language toolchain. Second language → strong prose,
  de-AI, independent back-translation for sign-off.
- **Phase 6 — Whole-draft verification (you do all of it):** re-verify every citation,
  final format check, toolchain clean, clean second-pass review, verification report.
- **Phase 7 — Iterate:** author reacts; substantive changes written back to
  `skeleton.md`; swap evidence per node without rebuilding the argument; finish with
  `paper-review`.

## What this skill orchestrates (adapt to what's installed)

- Literature: web + citation graphs (lite) / `fetch-refs` + `verify-citations` + local
  RAG (full).
- Venue norms: web search of the official call → `venue-notes.md`.
- Method/analysis: describe honestly (lite) / R · Python · Jupyter (full).
- Language: voice profile + careful AI-tic pass (lite) / local linters + corpora (full,
  see `setup/TOOLS.md`; Traditional-Chinese-Taiwan authors: `setup/addons/zh-tw/`).
- Finish: `paper-review` + a PDF build (`build-pdf`).

## Not this skill
- **Check/proofread only, don't rewrite** → `paper-review`.
- **Just fetch reference PDFs** → `fetch-refs`. **Just check citation direction** →
  `verify-citations`. **Slides** → a deck skill.
- One line: *"help me look at this" = paper-review; "help me write/rewrite/resubmit" =
  co-author.*
