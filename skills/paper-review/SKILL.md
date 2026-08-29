---
name: paper-review
description: Five-layer quality check for an academic draft (any language). Use when the author says "check this paper", "proofread", "catch typos", "look at this as a reviewer", "paper review", "check before I submit", asks whether the reported statistics are self-consistent / the numbers look suspicious, wants the draft checked against a reporting guideline (COREQ / SRQR / TREND / CONSORT / STROBE / PRISMA), or asks "which declarations am I missing before submitting". Reads the project's `ADJUDICATED.md` before reviewing (settled items are not re-raised). Mechanical layers run local tools when available (statistics = statcheck + scrutiny recomputation, not hand-rolled, when R is installed); semantic and logic layers are done by Claude under an anti-bias rubric. Unpublished drafts never leave the machine.
---

# Paper Review — five-layer quality check

> Generated from the Research Writing Kit; adapt to the author.
> Iron rules: **unpublished drafts never go to the cloud** (never suggest a public
> AI detector), **minimal-edit** (don't rewrite the author's voice), **every
> criticism carries a quote from the text**.

> Author profile (filled at setup): field `<FIELD>` · language(s) `<LANGUAGE>` ·
> venues `<VENUES>` · mode `<lite | full>`.

## Step 0 — Scope
🔴 **Read the project's `ADJUDICATED.md` first** (if there is none, ask whether an
equivalent record exists). Items listed there were checked and settled — an apparent
mismatch between a data field and the paper's wording, a number format that follows a
convention, a term kept on purpose. Do not re-raise them unless you have **new
evidence, stated explicitly**. A review that rediscovers a settled item costs a round
and makes the author answer the same question twice; a clean-context reviewer is the
most likely to do this, which is exactly why the file exists (see `doc-regress` §6).

Confirm (or infer): file path; language (own / second / mixed); target venue
(affects Layer 4 rubric); which layers to run (default all; "just typos" = layers 1–2).

> Boundary: this skill **checks and does not rewrite**. "Help me look at this" =
> paper-review; "help me fix / rewrite / resubmit" → `co-author` (Phase 0.5 onboards the
> existing draft). If the author asks for edits mid-review, hand over rather than drift.

## Layer 1 — Mechanical (bundled tools first, if usable; else careful read)
- **Bundled, zero-install (Chinese drafts):** run `tools/zh-tw/zh_localize.py` (Taiwan
  terms + 台/臺) and `tools/zh-tw/zh_ai_style.py` (Chinese AI fingerprint) directly —
  they need nothing installed. For the author's voice gate, `tools/zh-tw/voice_lint.py`.
- **Bundled (English drafts):** `tools/en/lt_check.sh` (grammar + US/UK spelling) if
  LanguageTool is installed; `tools/en/ai_style_diag.py` if the author built a corpus.
- **Bundled, zero-install (either language):** `tools/claims/overclaim_lint.py` — the
  overclaim candidates (`all / never / the only / proves / clearly / significantly`
  non-statistically, and the Chinese equivalents). Report-only; findings are adjudicated
  in Layer 3, not auto-fixed.
- **Quantitative drafts (if R + the packages are installed — see `setup/TOOLS.md`):**
  reported statistics get *recomputed*, not eyeballed. `statcheck` re-derives each
  APA-style test report (`t(28)=2.20, p=.03`) and flags rows where the p value doesn't
  match — `decision_error=TRUE` (the significance conclusion flips) is the serious kind.
  `scrutiny`'s GRIM test checks whether a reported mean is mathematically possible given
  N (integer scales) — `consistency=FALSE` means ask for the raw data. Limits: statcheck
  only parses APA-style reporting; mixed-model / CLMM tables escape it, so check those
  by hand against the stated method. **Don't hand-roll the recomputation when the
  packages are available.**
- **Lite / nothing installed:** do a careful mechanical pass yourself — typos,
  spacing/punctuation consistency, agreement, article/number, tense, US/UK mixing.
  For statistics, recompute what you can from the reported numbers and mark the
  verdicts lower-confidence than a package-verified pass.
Report, don't auto-apply; show a diff before any change. Collect into a "mechanical
fixes" list; filter false positives (proper nouns, terms of art).

### 1e — Figure colour accessibility (run whenever there are figures)

```bash
python3 tools/figures/figure_a11y.py figures/*.png
```

Journals are mostly printed in black and white, and ~8% of men have a red-green colour
vision deficiency — a figure that separates series by hue alone collapses for both.
Most venues' figure guidelines say outright that colour must not be the only carrier.

- **FAIL** = two colours collapse under a CVD simulation while being far apart in the
  original → that pair is carried by hue alone. Add shape/linestyle/direct labels, or
  change palette.
- **WARN** = contrast ratio below 1.4:1 in print (WCAG suggests ≥3:1 for graphical objects).
- 🔴 **Open the simulated images it writes.** The simulation is a linear approximation:
  "these two collapse" is reliable, "this figure is fine" is not a guarantee.

## Layer 2 — Semantic proofreading (Claude, strictly constrained)
Constraints (counter LLM over-correction): **minimal edit** — change only what's
wrong, don't rewrite or alter the author's register; output `before → after` per
line; **never add or delete words you didn't flag**; mark uncertain ones `[?]` for the
author; put the total edit count at the top.

## Layer 3 — Wording (de-AI + corpus anchoring)
1. Flag **LLM convergence words** (empirically AI-tells): e.g. *delve, intricate,
   notably, crucial, pivotal, multifaceted, underscore, leverage, comprehensive, realm,
   landscape, testament, seamless, robust* (when overused) — and the equivalents in the
   author's language. Suggest more natural replacements.
2. Anchor key wording (contribution sentences, method verbs) to real academic
   frequency. **Bundled:** grep `data/academic-vocab/` — `avl_core_words.tsv` /
   `awl_families.tsv` (not shipped — if absent, run `tools/vocab/fetch_awl.py` once; it is git-ignored) for single-word diction (informal word not in the list + has an
   academic synonym → suggest upgrading), `acl_collocations.tsv` for phrase
   collocations. With a field corpus (full mode) also check real frequency there.
   🔴 Word lists are anchors, not auto-replace: the final call is Claude reading the
   context, minimal-edit, with a quote.
3. Term consistency across the whole draft.
4. **AI syntax-fingerprint pass** (beyond convergence words): em-dash / semicolon /
   rule-of-three density, sentence-length variance. Do punctuation surgery only on pure
   fillers; keep rhetoric doing conceptual work. Compare before/after. ⚠️ Never use a
   cloud detector — unpublished drafts stay local, and academic prose gives high false
   positives.
5. **Overclaim pass** (`tools/claims/overclaim_lint.py` from Layer 1, judged here).
   De-AI is not finished when the convergence words are gone: a draft that still says
   *proves*, *all*, *the only*, *clearly* reads as machine-written **and** hands a
   reviewer a substantive objection. Per candidate: does the reported evidence carry
   this word? Yes → keep (a real 0/72 or 100% result is data — softening data is its
   own error). No → converge (all→most, never→rarely, prove→show/suggest, the
   only→one of the few, clearly→delete, the most X→a more X). **Quoted source text
   and object-language in quotation marks are out of scope** — the scanner cannot tell
   whose words they are, so skip them by hand. Minimal edit, with a quote, as elsewhere
   in this layer.

## Layer 4 — Logic / argument / RQ (reviewer simulation — anti-bias rubric)
**Anti-bias instructions (mandatory — LLM reviewers empirically inflate scores):**
task = **find weaknesses**, no praise; assume you must write the reject and see if the
author can rebut; ignore length, author/institution prestige, confident tone; **every
criticism carries a quote + location**, no quote → not allowed.

Rubric (score each 🔴fatal / 🟡major / 🟢minor):
1. **Contribution type** (empirical / artifact / methodological / theoretical / dataset
   / survey / opinion): which is this, is the bar met, does the contribution sentence
   overclaim?
2. **RQ quality** (Feasible/Interesting/Novel/Ethical/Relevant) + **alignment chain**:
   RQ → method → results → conclusion, unbroken?
3. **Argument structure:** each claim's evidence present? is the limitations section
   honest about what it omits?
4. **Method rigor:** effect sizes + CIs? multiple-comparison correction? Likert handled
   as ordinal? seeds? (qualitative: reliability / codebook / audit trail).
   - **4a. Qualitative — four items a qualitative reviewer always asks:** (i) **saturation**
     — is the criterion stated? (there is no power analysis for interviews; arguing
     sample size with statistical logic reads as inexperience); (ii) **reflexivity /
     positionality** — if the researcher is also the participants' teacher, that is a
     power relation with systematic effects on what students say; what was done to
     reduce it? (iii) **member checking** — done, or a reason given; (iv) 🔴 **quote
     translation procedure** — when interview quotes are translated for the paper: who
     translated, was it checked, are original-language quotes provided? Keep this
     separate from the back-translation iron rule for the *author's own* prose — that
     rule is about sign-off, this one is about evidence fidelity. Most often omitted,
     most often caught.
   - **4b. Reporting guideline:** pick by design — COREQ / SRQR (qualitative), TREND
     (non-randomized intervention), CONSORT (RCT), STROBE (observational), PRISMA
     (systematic review). If the target journal names one, that one wins; a required
     checklist that isn't attached means "revise before review".
   - **4c. Search strategy:** for drafts with a review-like component, are databases,
     query strings, dates, and inclusion/exclusion criteria reported? Without them the
     review isn't reproducible and "why did you miss X" has no answer.
5. **Related work:** positioned clearly? strawman? recent work in the last ~3 years that
   should be cited but isn't?
6. **Venue fit + current submission spec:** check the venue's **official current** page
   for length/format/blind rules — don't hardcode from memory, specs change yearly.
7. **Submission declarations — six items.** Missing ones are desk-reject or
   post-publication-accountability problems, not formatting. Check each for *required /
   present / accurate*:
   - 🔴 **Generative-AI use disclosure** — tools and tasks listed per the venue's policy
     (most ACM venues and journals now require it). Check it **matches reality**: a draft
     co-written with an LLM that declares "language polishing only" is a false
     disclosure. The same policies forbid uploading a manuscript to a public LLM for
     review — the external basis for this skill's "drafts stay local" rule.
   - **Research ethics** — approval or exemption number and institution in the Method;
     consent and identifiable-data handling stated.
   - **Data and code availability** — present, and true? ("available" with no link, or a
     key raw file that in fact isn't shared).
   - **Author contributions (CRediT)** — with multiple authors, especially students.
   - **Competing interests and funding** — disclosed, or an explicit "none".
   - **Pre-registration** — for quantitative effect claims: link present? Any hint of
     one that doesn't exist, or a post-hoc registration written as if prior?
   > Rule: **"the venue didn't ask" ≠ "not needed"** — AI disclosure and ethics go in
   > regardless. Reviewing your own pipeline's draft: same table as `co-author` 6-2a.

## Layer 5 — Citation check (optional)
1. List all "claim + citation" pairs for human checking (citation hallucination is real).
   With a local PDF library (full mode), verify "does source X support claim Y" against
   the PDFs via `verify-citations`. Never upload unpublished text.
2. 🔴 **Uncited-claim scan** — the item most often skipped and most worth running:

   ```bash
   python3 tools/claims/uncited_claims_scan.py --src <draft>
   ```

   Step 1 only covers sentences that carry a citation marker. Quantitative, causal and
   superlative claims *without* one ("41 students showed…", "improved by 23%", "the
   first to…") are a structural blind spot of citation verification — and they are
   where the author's own evidence lives. Regex only, no LLM, any language. Each hit:
   add a citation · point to the data source · soften the wording. When reviewing
   someone else's draft this layer is where "where does that number come from?" gets
   asked. Superlative hits over-report in humanities prose (idioms read as novelty
   claims); for argument-driven papers run `--only quant causal`.

## Output
```
# Paper Review: <file>
Venue: <target> | Language: <lang> | Layers: <layers>
## 🔴 Fatal   ## 🟡 Major   ## 🟢 Minor
## Mechanical fixes (Layer 1)
## Semantic diff (Layer 2, before→after)
## Wording suggestions (Layer 3)
## Citations to verify (Layer 5)
```
Each issue: location + quote + problem + concrete fix. End with a pre-submission
checklist for the target venue.
