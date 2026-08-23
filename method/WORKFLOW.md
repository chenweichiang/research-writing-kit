# The Method — The Full Pipeline

> The 7-phase pipeline, generalized and language-neutral. This is what the
> `co-author` skill orchestrates. Each phase notes what it needs in **lite mode**
> (Claude + web only) versus **full mode** (optional local tools from
> `setup/TOOLS.md`). Nothing here requires the full tools; they only make it faster
> or more rigorous.

## Phase 0 — Intake (the author decides what to write)

Get: (1) the topic, sources, or which existing draft to work on — messy is fine;
(2) the **target venue and output language**; (3) whether there's existing data to
analyze; (4) the mode (default "write it to good", or explicit skeleton-first);
(5) whether there's an **existing draft** to work from → if so, Phase 0.5 first.

## Phase 0.5 — Onboard an existing draft (only if one exists)

Before writing a single new word:
1. **Provenance triage.** Which passages did the author write themselves vs
   AI/mixed? Author-written = voice asset → preserve, minimal edits only, no
   wholesale rewrite. Only AI/mixed/authorized passages get heavy edits. When
   unsure, ask.
2. **Reverse-extract the skeleton** from the existing draft (claim / evidence /
   so-what per section) so the old draft enters the same source-of-truth system.
3. **Treat all existing citations as unverified** — re-run verification; re-check
   format against the *new* target venue. "Fact-locked" ≠ "check-exempt": names,
   dates, spellings still get checked against authoritative sources (an old typo
   protected as "don't rewrite" will otherwise propagate).
4. **Produce a disposition table**: mark each section keep / light-edit / rewrite /
   new-write, one reason each, plus a content-gap list.
5. **Read a real sample of the material before judging feasibility** — never judge
   research value from filenames, file counts, or folder structure. Sample-read
   3–5 items across the quality spectrum first.

> **Before a journal/conference submission, check the ledger.** Simultaneous
> submission is forbidden almost everywhere and is a *cross-project* problem: the same
> manuscript, retitled and sent to a second venue, looks clean from inside either
> project folder. Keep one `SUBMISSIONS.tsv` above all projects
> (`tools/submissions/check_submissions.py`), never change a `manuscript_id` when you
> retarget, and update the row the day a status changes — a stale "under review" from
> eight months ago guards nothing.

> **Inventory text recycling when onboarding an existing draft.** Every onboarding case
> *is* reuse: a short paper being extended, a talk becoming an article, last year's
> proposal, a student report. Reuse is legitimate — **not disclosing it is not**, and
> similarity software matches you against your own earlier work. Method and background
> can be reused within reason; **results and discussion cannot**. Rewrite what you can,
> cite yourself for what you can't, and state the extension in the cover letter.
> Conference-to-journal extension is the normal case and usually welcome, but venues
> state how much new material they expect. If the source is student work, the authorship
> and consent questions are separate from the recycling one — settle both.

## Phase 1 — Two-track scouting

### Track A — Literature & prior work (classics + recent hot)
- **Lite:** WebSearch + Semantic Scholar / OpenAlex citation graphs to find what
  the field considers canonical and what's newly hot around your seed papers.
- **Full:** also query a local literature RAG for full-text you already hold.
- 🔴 Whatever you hold locally is a *convenience sample*, not "what the field's
  classics are." "Not in my library" ≠ "doesn't exist." Let the citation graph,
  not your shelf, decide what should be cited. Never invent a citation to fill a gap.

### Track B — Venue format & review norms (do this every time, for the current cycle)
Standards and formats change yearly — memory and last-cycle impressions are traps.
Research the **current** official call: length limits, format rules, required
attachments/templates, blind-review rules, and what reviewers actually weigh.
Grab the official template (or, absent one, measure the format of the author's
past submitted PDFs). Save findings to `venue-notes.md` in the project folder —
you'll write to it and tick against it at final check.

**Record the preprint policy while you are there.** Venues differ sharply: most accept
preprints, a few treat them as prior publication and will desk-reject, and some require
the preprint link and version to be declared at submission. Note whether you may post,
when, any embargo after acceptance, and whether the accepted manuscript and the version
of record are treated differently. ⚠️ A preprint server is **not** a submission — but
two journals at once is; keep the two questions apart.

## Phase 1.5 — Direction summary (non-blocking by default)

Compress "gap / angle + contribution claim + main argument line + recommended
venue (with alternatives and why)" to **one page** and show the author.
🔴 **The target venue is the author's call, not an internal decision** — surface
"where to submit" as explicit options (it affects their tenure points, timeline,
cost). In default mode you may proceed on the recommended venue while the question
is out; in skeleton mode, wait for the nod.

## Phase 2 — Verify & fetch (kill hallucinated citations)

- **Lite:** open each source, read enough to confirm it says what you cite it for
  and in the right direction; check DOIs/ISBNs against Crossref / OpenLibrary.
- **Full:** `fetch-refs` (multi-source + institutional access) to pull full texts,
  then `verify-citations` (an agent per paper actually reads the PDF).
- ⚠️ Some publishers block automated fetch; if you can only view in a browser,
  mark `❓unverified` rather than treating it as confirmed.

## Phase 3 — Method / analysis (in parallel with the skeleton)

Decide whether this paper needs to *design a method* (collecting new data) or
*analyze existing data*.
- **Design:** follow the venue's methodological playbook; estimate power/sample.
- **Analyze — lite:** describe the design honestly and state what analysis is
  appropriate; do simple summaries carefully. **Full:** run it in R/Python/Jupyter.
- Iron rules: **data stays local; effect sizes + CIs; Likert → ordinal models,
  not means; seeds fixed.** Fold results (numbers + effect sizes) back into the
  skeleton nodes that need them.

## Phase 4 — Build the argument skeleton

Output a structured skeleton; each argument node has four fields:
**claim / move / evidence (a *verified* source, with a source card for anything the
author hasn't read) / so-what**, plus flags: `⚠needs-method`, `⚠needs-analysis`,
`❓citation-unverified`. Core causal/eliminative nodes also get a
`load-bearing-assumptions / open-rebuttals` field.
🔴 The skeleton lives as `skeleton.md` **in the project folder**, not in the chat —
any new session reads `skeleton.md` + `venue-notes.md` before doing anything.

### Phase 4.5 — Formalize the core claim (optional; only if there's one core causal claim)
For a paper with a single core causal or eliminative claim, you can stress-test it
with a formal checker to surface hidden premises and un-answered rebuttals, then
fold those into the skeleton's limitations. This is an **internal diagnostic**, not
a deliverable, and it checks *validity, not truth* (see the honesty-ceiling note in
`IRON-RULES.md`). Purely descriptive / review papers skip this.

## Phase 5 — Write the complete first draft (bound to the skeleton, into the format)

Write section by section, strictly bound to the skeleton — no filler (this is the
anti-homogenization point). Follow `venue-notes.md` for structure and format.
- **Default mode:** write the whole first draft (the author needs something
  substantial to react to). **Skeleton mode:** deliver section by section.
- 🔴 **Into the format from version one; the output is a formatted document**, not
  raw markdown (Iron Rule 7).
- **In the author's own language:** match the `VOICE_PROFILE`, then run the
  language toolchain (lite: careful self-review against the voice profile + an
  AI-tic pass; full: the local linters/corpora in `setup/TOOLS.md`).
- **In a second language the author doesn't write:** write strong academic prose,
  de-AI it, and produce an **independent back-translation** for the author to
  sign off on.

## Phase 6 — Whole-draft verification (before handing back — you do all of it)

1. Re-verify **every** in-text citation against the source.
2. Final format check against `venue-notes.md`, every official hard rule.
3. Language toolchain clean (per language).
4. **A clean second-pass review** with no drafting context, reviewer's eyes.
5. Produce the **verification report** (citations / format tick-sheet / toolchain /
   `❓unverified` list).
6. Deliver = the formatted document + the report (+ back-translation if second-lang).

## Phase 7 — Iterate with the author (repeat until good)

The author reads the complete draft and says what to change.
- 🔴 **Skeleton = source of truth.** Substantive changes (argument, evidence,
  structure) get written back into `skeleton.md`. Pure wording polish doesn't.
- If the author says "this citation feels off" → go back to Phase 1–2, swap the
  evidence in that node only; don't rebuild the argument.
- Every iteration is re-formatted and re-delivered, not a markdown diff.
- After big changes, re-run the affected checks (citations / format / and if the
  core claim's structure changed, Phase 4.5). Finish with a full `paper-review`.

## Phase 8 — After acceptance (submission is not the end)

The most error-prone stage, because by now everyone has relaxed — and a proof, once
signed off, is printed.

### 8.1 Reviews came back
→ the `rebuttal` skill: split the reviews into smallest units, decide every verdict
*before* editing, map each accepted point to a real location in the manuscript, then
verify completeness mechanically. **Declining is legitimate**; declining without
evidence is not, and neither is accepting something that makes the paper worse.

### 8.2 Proofs
Typically a 48–72 hour window, and **for errors only** — substantive changes at this
stage get refused or trigger re-review.

Check: author names and order · funder/grant ids · figure numbers still matching their
in-text references · no table row dropped in typesetting · references not mangled by
the production system · DOIs resolving · and, for non-Latin names and institutions,
that the typesetter did not substitute characters or break the encoding. If any number
changed, re-run your numbers ledger.

### 8.3 Rights and licence — read before signing
CC-BY vs a traditional transfer is a real choice. ⚠️ **A funder may mandate open
access**; discovering that after signing a transfer is an expensive mistake. Decide
what you need to keep: repository deposit, classroom use, reuse in a future book. Every
co-author, students included, must know and agree to the terms.

### 8.4 Dissemination and closing the loop
Post the preprint or repository copy according to the embargo you recorded in Phase 1
(the accepted manuscript and the version of record usually have different rules). Then
**update the submission ledger to `published`** — a ledger that is not updated means
the next duplicate-submission check runs on stale data. Record the DOI in the project
README: you will need it when you cite yourself, and it is the evidence behind any
future text-recycling disclosure.
