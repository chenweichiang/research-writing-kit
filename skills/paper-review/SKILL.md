---
name: paper-review
description: Five-layer quality check for an academic draft (any language). Use when the author says "check this paper", "proofread", "catch typos", "look at this as a reviewer", "paper review", "check before I submit", or asks whether the reported statistics are self-consistent / the numbers look suspicious. Mechanical layers run local tools when available (statistics = statcheck + scrutiny recomputation, not hand-rolled, when R is installed); semantic and logic layers are done by Claude under an anti-bias rubric. Unpublished drafts never leave the machine.
---

# Paper Review — five-layer quality check

> Generated from the Research Writing Kit; adapt to the author.
> Iron rules: **unpublished drafts never go to the cloud** (never suggest a public
> AI detector), **minimal-edit** (don't rewrite the author's voice), **every
> criticism carries a quote from the text**.

> Author profile (filled at setup): field `<FIELD>` · language(s) `<LANGUAGE>` ·
> venues `<VENUES>` · mode `<lite | full>`.

## Step 0 — Scope
Confirm (or infer): file path; language (own / second / mixed); target venue
(affects Layer 4 rubric); which layers to run (default all; "just typos" = layers 1–2).

## Layer 1 — Mechanical (bundled tools first, if usable; else careful read)
- **Bundled, zero-install (Chinese drafts):** run `tools/zh-tw/zh_localize.py` (Taiwan
  terms + 台/臺) and `tools/zh-tw/zh_ai_style.py` (Chinese AI fingerprint) directly —
  they need nothing installed. For the author's voice gate, `tools/zh-tw/voice_lint.py`.
- **Bundled (English drafts):** `tools/en/lt_check.sh` (grammar + US/UK spelling) if
  LanguageTool is installed; `tools/en/ai_style_diag.py` if the author built a corpus.
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
   `awl_families.tsv` for single-word diction (informal word not in the list + has an
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
5. **Related work:** positioned clearly? strawman? recent work in the last ~3 years that
   should be cited but isn't?
6. **Venue fit + current submission spec:** check the venue's **official current** page
   for length/format/blind rules — don't hardcode from memory, specs change yearly.
7. **Generative-AI disclosure:** did the author disclose AI use per the venue's policy?

## Layer 5 — Citation check (optional)
List all "claim + citation" pairs for human checking (citation hallucination is real).
With a local PDF library (full mode), verify "does source X support claim Y" against the
PDFs. Never upload unpublished text.

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
