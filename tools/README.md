# Bundled tools

Small, local, privacy-respecting checkers you can run from day one. **The Chinese
tools need nothing installed** (Python 3 standard library only). They work
out of the box. The English tools need one or two free offline programs.

> Everything here runs **on your machine** and sends no draft text anywhere. Never paste an
> unpublished draft into a cloud "AI detector."
>
> These are generalized from one researcher's toolkit. Adapt the word lists and
> rules to *your* field and voice. They're starting points, not gospel.

| Folder | Tool | One line |
|--------|------|----------|
| `zh-tw/` | `zh_localize.py` | mainland-vs-Taiwan terms + 台/臺 consistency |
| `zh-tw/` | `zh_ai_style.py` | Chinese AI syntax fingerprint (+ contrast-sentence total, long-sentence list) |
| `zh-tw/` | `voice_lint.py` | your own voice rules as a hard gate (+ heading scan, stock closers, AI-phrase candidates) |
| `zh-tw/` | `zh_gloss_scan.py` | parenthetical asides to turn into definitions, keep, or cut; `--en`: English glosses and bare English words in Chinese prose |
| `zh-tw/` | `zh_register.py` | Chinese register profile: 52 features (self-reference, translationese, linking, metadiscourse, stance, punctuation, sentence length) vs same-field Taiwan journal papers |
| `register/` | `register_profile.py` | native-polish deviation list: which features sit outside the field's p10–p90 band, which way to move them, with bounds per line range (zh + en) |
| `register/` | `polish_check.py` | checks an editor's change list before it touches the draft: invariants, word budget, forbidden forms, register direction; `--apply` writes back only when all pass |
| `claims/` | `uncited_claims_scan.py` | sentences that claim (numbers / causes / firsts) but cite nothing |
| `claims/` | `overclaim_lint.py` | wording that says more than the data supports (EN + zh-TW) |
| `refs/` | `snowball.py` | forward / backward / related citation snowballing |
| `refs/` | `retraction_scan.py` | has anything you cite been retracted (Crossref + OpenAlex) |
| `refs/` | `pdf_fetch.py` | fetch reference PDFs: OA resolvers → TLS impersonation → real browser (needs `curl_cffi`, `patchright`) |
| `refs/` | `lit_map.py` | candidate classics by co-citation within a literature batch (not global citation count) |
| `refs/` | `missing_refs.py` | the reference PDFs still to download by hand (DOI / URL / ISBN links), after subtracting your own PDF library |
| `refs/` | `inbox_ingest.py` | files the PDFs you downloaded by hand: matches them to missing entries, verifies content, names them `<citekey>.pdf`, tidies the downloads folder |
| `method/` | `method_decision_check.py` | format gate for `method-decision.md` (English or zh-TW template) |
| `method/` | `analysis_plan_check.py` | format + timing gate for `analysis-plan.md`; `--phase6` checks deviations were recorded |
| `method/` | `tea_second_opinion.py` | second opinion on which classic statistical test fits (wraps Tea; optional install) |
| `vocab/` | `fetch_awl.py` | fetch Coxhead's AWL from the official VUW site into a local TSV (not shipped: CC BY-NC-ND) |
| `regress/` | `regress.py` + `dead_rule_check.py` | regression suite for long documents + false-green-light detector |
| `rebuttal/` | `check_response.py` | response-to-reviewers completeness |
| `submissions/` | `check_submissions.py` | duplicate-submission guard |
| `submissions/` | `style_reaudit.py` | re-run style/de-AI measurement on every drafting/under-review manuscript after a rule change |
| `review/` | `review_rounds.py` | review-round ledger: new vs repeated fatal/major findings, re-raised adjudicated items without new evidence, when to stop reviewing |
| `collab/` | `source_trace.py` | does every sentence of a rewritten co-authored draft trace back to the original, the co-author's replies or the proposal |
| `versioning/` | `version_check.py` | pre-delivery version check: `VERSION`, CHANGELOG, one-version delivery folder, PDF metadata, no version in the submitted text, no reused tag |
| `figures/` | `figure_a11y.py` | colour-vision accessibility of figures |
| `figures/` | `figure_check.py` | figures and tables in the typeset PDF: numbering, captions vs in-text references, overflow past the column or page, text shrunk too small (needs PyMuPDF) |
| `en/` | `lt_check.sh`, `ai_style_diag.py` | English grammar pass; English AI fingerprint vs your field (+ LLM convergence-word density, list in `en_slop_terms.tsv`) |
| `en/` | `biber_diag.py` | grammatical-register check, Biber-style features vs your field, read by direction; `--groups` for one venue, `--json` (needs pybiber + spaCy, dedicated env) |
| `en/` | `bundle_diag.py` | lexical bundles the draft over-uses relative to your field corpus |
| `en/` | `metadiscourse_en.py` | Hyland stance / engagement / boosting-hedging markers vs your field corpus, read by direction; `--groups` for one venue, `--json` |

## Chinese (`tools/zh-tw/`): zero installs

| Tool | What it does | Run |
|------|--------------|-----|
| `zh_localize.py` | Flags mainland-Mandarin terms (反饋→回饋…) + 台/臺 consistency, with a false-positive whitelist. Report-only. The table is `zh_tw_terms.tsv` (~170 terms with context rules, vetted against Taiwan-authored journal papers; part-sourced from MIT-licensed projects, see `NOTICE.md`). | `python3 zh_localize.py draft.md` |
| `zh_ai_style.py` | Chinese AI syntax fingerprint: em-dash/semicolon/rule-of-three density, convergence words, sentence burstiness (heuristic); density of the 「並非…而是」 not-X-but-Y frame (≥0.6/k → review each); every sentence over 120 Han characters listed (enumerations exempt). | `python3 zh_ai_style.py draft.md` |
| `voice_lint.py` | Mechanically enforces YOUR voice rules (config-driven). Exits non-zero until clean. Use as a pre-delivery gate. Four rule kinds: `hard` (counted), `soft` (density), `report` (listed, never counted: default AI stock phrases), `headings` (one regex over Markdown/Typst heading lines; sentence-form or question titles are flagged, rewrite as noun phrases). `--paper` for papers, proposals and applications: drops the rules that are personal habit but common in journal papers (semicolon, 乃/則是/抑或), reports 綜上所述/整體而言 instead of counting them, and keeps the general-quality rules; the rules file's `paper` section controls it. | `python3 voice_lint.py draft.md [--rules voice_rules.json] [--paper]` |
| `zh_register.py` | Register profile of a Chinese draft against a corpus of same-field published papers you assemble: 52 features, 49 of them rates per 1000 Han characters (本研究/本文, 進行, 透過, 具有, 的/之, linking words, metadiscourse, stance, 「；」「：」, dashes, contrast frames) plus sentence and clause length, each with the corpus p10/median/p90 and the draft's percentile. Quotations in 「」 are not counted. Descriptive only; which way to fix is `tools/register/register_profile.py`'s job. Needs ≥30 papers (`<corpus>/<venue>/*.txt`); a `--venue` with ≥30 papers is used on its own. | `python3 zh_register.py draft.md --corpus <dir> [--venue J] [--json]` |
| `zh_gloss_scan.py` | Lists every full-width parenthetical of 12+ characters that is not a citation or a cross-reference. Decide each: plain-language note → a defining sentence at first mention, in place; specification list → keep; restatement → cut. Do not collect them into a glossary. `--en` lists instead (1) English glosses after Chinese terms, grouped, the first occurrence for a human to judge and every later one flagged as already glossed (those are almost always cut), and (2) bare English words in Chinese prose ranked by frequency, lowercase words first (proper nouns, model and software names may stay; the rest usually becomes Chinese). Code, tables, headings, citations, URLs, front matter and the reference list are skipped. Report-only. | `python3 zh_gloss_scan.py draft.md [--min 12 \| --en]` |

- `zh_ai_style.py` gets sharper if you point `--authored <folder>` at a folder of your
  own `.txt` writing, then words *you* genuinely use aren't flagged as AI tells.
  🔴 Point it at a folder holding **only your own writing** (keep a `voice-samples/`
  folder separate from your working drafts). Mixing AI drafts into the baseline
  cancels the diagnosis out. As a guard, files named with 草稿/draft/ai/claude/gpt are
  auto-skipped. Needs ~120+ Han chars to compute; for a short section use `voice_lint`.
- `voice_lint.py` ships generic defaults. Copy `templates/voice_rules.template.json`
  → `voice_rules.json`, edit it to match your own habits (what *you* never write), and
  pass `--rules voice_rules.json`. Build it from your `VOICE_PROFILE` (see `templates/`).
  Papers, proposals and applications follow the field's register, not your personal
  voice, so run them with `--paper`.

## Register and native polish (`tools/register/`): zero installs, needs a corpus

The native-polish step (`method/WORKFLOW.md` Phase 5.5) defines "reads like a native
scholar of this field" as "each register feature falls inside the p10–p90 band of
same-field published papers", so the yardstick is a corpus you assemble, never the
author's own drafts (see `setup/TOOLS.md` for the corpus layout and minimums).

| Tool | What it does | Run |
|------|--------------|-----|
| `register_profile.py` | Applies a per-feature policy (band: back into the band from either side; cap: may only go down; locked: never up; report: stance, left to the author) to the measurements (`zh-tw/zh_register.py`; `en/metadiscourse_en.py` plus `en/biber_diag.py` when `--biber-python` or `$BIBER_PYTHON` points at its environment) and writes the deviation list an editor works from: to fix / locked / for the author / inside the band, with counts, bounds for the editor's line range and instances. `--exemplars N` picks paragraphs near the venue median as a feel reference. `--policy-file` overrides a policy. | `python3 register_profile.py draft.md --lang zh --corpus <dir> --venue J --lines 40-120 --out dev.md` |
| `polish_check.py` | Applies a change list (`E = [("original", "replacement"), ...]`, read as data and never executed; JSON also accepted) to an in-memory copy and checks it: numbers, citations, comments, quoted text, math, LaTeX commands, Latin words (zh) and `--lock` terms unchanged; growth within `--grow-budget`; contrast frames, stock metadiscourse, dashes, sentence-initial 然而, mainland terms and `--forbid-file` forms not increased; no more over-long sentences; and, with a corpus, register direction for the whole draft. `--apply` writes back only when everything passes. | `python3 polish_check.py --draft draft.md --edits e.py --lang zh --corpus <dir> --venue J --grow-budget 10` |

Both have `--selftest`, which builds a synthetic corpus in a temporary folder.

## Claims (`tools/claims/`): zero installs

| Tool | What it does | Run |
|------|--------------|-----|
| `uncited_claims_scan.py` | Finds sentences that make a claim needing evidence (a number / % / p-value / N (quant), a causal verb (causal), "the first / only / to our knowledge" (super)) and carry **no citation marker**. English + Traditional Chinese triggers. Exits non-zero while unadjudicated findings remain. | `python3 uncited_claims_scan.py --src paper.md [--json report.json] [--only quant]` |

- Why it exists: citation-verification checks start from citation markers, so a
  sentence with no marker is never checked, and in design research those are the
  load-bearing ones ("17 student posters showed…", "improved by 23%"). This is the only
  pass that looks at them. It does **not** judge whether the claim is true.
- Each finding gets one of three dispositions: add a citation, name your own data
  source (put the number in the numbers ledger, see `regress/`), or soften the wording.
  Then silence it with a waiver on that line: `<!--uncited-ok: own data run3.csv-->`
  (Markdown) or `% uncited-ok: …` (LaTeX). The reason is mandatory; empty waivers are
  ignored, and every waiver is listed in the report so one cannot silently cover a
  whole paragraph.
- Recognises `\cite{}`, pandoc `[@key]`, numeric `[12]`, APA `(Chen, 2024)`, Chicago
  `(Dunne and Raby 2013)` and `Chen et al. (2024)`. Inline math is kept (statistics live
  there); display math, code, comments and table column specs are masked.

| Tool | What it does | Run |
|------|--------------|-----|
| `overclaim_lint.py` | Flags wording that claims more than the evidence supports, in four categories (absolute / intensifier / evidence-strength / superlative), English and Traditional Chinese. **Report-only: never edits, never blocks.** | `python3 overclaim_lint.py draft.md [--lang auto\|en\|zh] [--json out.json]` |

- Why it exists: de-AI has two halves. Style tools remove convergence words and
  cadence; nothing else looks at *saying more than the data supports*. Strip the
  convergence words but leave "this proves", "all participants", "the only study",
  and the draft still reads as machine-written, and unlike a cadence tic, an
  unsupported absolute is a **substantive** fault that costs a reviewer's trust in
  everything else you wrote.
- **Judge every hit; do not batch-replace.** Evidence carries it → keep. A real 0/72
  or 100% result *is* data, and softening data is its own kind of dishonesty. Evidence
  doesn't carry it → converge: all→most, never→rarely, prove→show/suggest, the only→one
  of the few, clearly/obviously→delete, significantly (non-statistical)→markedly or
  delete, the most X→a more X (Chinese: 完全→幾乎、永遠→往往、證明了→顯示、唯一→之一、最→較).
- **Out of scope: quoted source text and object-language in quotation marks.** The
  scanner cannot tell whose words a sentence carries, so it will flag a quotation that
  is perfectly correct to keep verbatim. Skip those by hand.
- Where it runs: English: after `ai_style_diag.py` / LanguageTool, before the
  de-cadencing pass (`agents/de-cadencing-scholar.md`, whose tic #6 is this list).
  Chinese: after `voice_lint.py` is clean, before `zh_ai_style.py`. Rerun on **every**
  delivery: new paragraphs bring new absolutes back.
- Exit code is 0 by design (it is a report). `--strict` exits 1 while candidates remain,
  for a CI gate. Use it only if you want delivery blocked on a list that always needs
  a human decision.

## Rebuttal (`tools/rebuttal/`): zero installs

| Tool | What it does | Run |
|------|--------------|-----|
| `check_response.py` | Completeness check for a response-to-reviewers letter: every point answered, every promised change mapped to a real location, every DECLINE carrying evidence, no orphan point numbers. | `python3 check_response.py --points points.tsv --revisions revisions.tsv --letter letter.md` |

- Templates for all three files are in the same folder. It checks **completeness, not
  quality**: every point being answered doesn't mean it's answered well.
- The three failures it exists to stop: a point never answered, a change promised but
  never made, and point numbers renumbered without updating the letter.

## Submissions (`tools/submissions/`): zero installs

| Tool | What it does | Run |
|------|--------------|-----|
| `check_submissions.py` | Duplicate-submission guard + status overview from one central ledger. Flags the same manuscript under review in two places, stale statuses, and moved project folders. | `python3 check_submissions.py --ledger SUBMISSIONS.tsv` |

- 🔴 **Keep ONE ledger, above all your project folders.** Simultaneous submission is a
  *cross-project* problem. A retitled manuscript sent to a second venue looks clean
  from inside either folder. A copy per project defeats the whole point.
- Never change a `manuscript_id` when you retarget to another venue; that id is what
  makes the guard work. Rows marked `unknown` provide **no** protection.

## Review rounds (`tools/review/`): zero installs

| Tool | What it does | Run |
|------|--------------|-----|
| `review_rounds.py` | A ledger of every fatal and major finding per review round (`docs/review-rounds.tsv`, one row each; template `review-rounds.template.tsv`). `repeat_of` blank = new, or the id it repeats (an earlier round's id or an `ADJUDICATED.md` `A` number). Prints new vs repeated counts per round; re-raising an adjudicated or `declined` item without new evidence in `note` is an error (exit 1); **two consecutive rounds with no new fatal and no new major = recommend stopping**. `--suggest` lists "new" findings whose summary resembles an earlier one. Dispositions: `fixed` / `declined` / `pending` / `withdrawn` (Chinese aliases accepted). | `python3 review_rounds.py docs/review-rounds.tsv [--adjudicated ADJUDICATED.md] [--suggest] [--json]` |

- A reviewer simulation always finds something. Without the ledger a review has no end,
  and the author gets asked about the same settled point in new words every round.

## Co-authored manuscripts (`tools/collab/`): zero installs (python-docx / pdftotext for those formats)

| Tool | What it does | Run |
|------|--------------|-----|
| `source_trace.py` | Sentence by sentence, can each sentence of a rewritten draft be traced back to the sources (original manuscript, the co-author's replies, the proposal, analysis reports)? Coverage by character bigrams (Chinese) or words (English) against the best-matching source sentence, with a neighbour window for split and merged sentences: traced ≥ 0.70, rewritten 0.40–0.70, untraced < 0.40. 🔴 = untraced and about the study itself (numbers, method words, course / students / site facts), or a number found in no source, or a rewrite carrying in a 12+ character span with a method word or number the source lacks; 🟠 = an untraced literature claim (send it to citation verification); 🟡 = other untraced lines (usually connectives; still check that they add no claim). Reads `.md .txt .typ .tex`, `.docx` (python-docx), `.pdf` (pdftotext). `--gate` exits 1 on any 🔴. | `python3 source_trace.py --orig original.docx replies.md proposal.pdf --draft new.docx [--report out.md] [--gate]` |

- It exists because an AI rewrite of a co-author's paper added a dozen statements the
  original never made, two of them claims about procedures never carried out. "Traced"
  measures overlapping wording, not identical meaning: the rewritten and 🟡 lines still
  need a human eye. Method: `method/COLLABORATION.md`.

## Versioning (`tools/versioning/`): zero installs (pdfinfo / pdftotext for PDF checks)

| Tool | What it does | Run |
|------|--------------|-----|
| `version_check.py` | Checks the rules in `method/VERSIONING.md` before a delivery: `VERSION` holds a valid `X.Y.Z` (two-part legacy numbers warn); the topmost CHANGELOG section carries the same number; the delivery folder (`latest/`, or `最新交付/`) holds exactly one version and it is `VERSION`; delivered PDFs carry the number in their metadata; a `--submission` PDF has no version string or review-copy footer in its text; `VERSION` was not already tagged with changes after the tag (a delivered number being reused). Exit 1 on any FAIL. | `python3 version_check.py <project dir> [--latest latest] [--submission submission.pdf ...] [--json]` |

## Regression suite (`tools/regress/`): zero installs

| Tool | What it does | Run |
|------|--------------|-----|
| `regress.py` | A regression suite for a long, repeatedly revised document: every rule is a mistake you actually made once, kept as a permanent check. Generic rules are config-driven (`rules.template.json`): dangling / orphan citations (numeric or BibTeX), personal-data patterns, internal words leaking into the delivered text, entity attribution, corrected claims that must not return, and a **numbers ledger** (R-STALE: a corrected old value comes back → FAIL; R-LEDGER: a current value is missing → WARN). Project rules go in a small Python file passed with `--extra`. | `python3 regress.py --config regress.json [--extra my_rules.py] [--json]` |
| `dead_rule_check.py` | The false-green-light detector: traces each rule and reports any that leaves through a guard `return` or barely executes its body (an early return because its setting is empty); also `r_*` functions written but never registered in `RULES` (unless listed in `RULES_DEREGISTERED`), and rules that call an undefined name. "The rule is in the list" is not the same as "the rule ran". | `python3 dead_rule_check.py regress.py --config regress.json [--extra my_rules.py]` |

- Start by copying `rules.template.json` → `regress.json` and
  `numbers-ledger.template.md` → `numbers-ledger.md` next to your manuscript.
  Unconfigured rules are reported as `[INFO] … NOT guarding` rather than passing
  silently. Fill them in, or accept that they guard nothing.
- 🔴 Only add a rule for an error that **really happened** and has a clear mechanical
  criterion. Prefer a miss to a false alarm: unclear criteria go to INFO, never FAIL.
- 🔴 Keep **one** numbers ledger and record values **as written in the manuscript**
  (`p < .001`, `94%`), not the computed ones; put exact values in the note column.
  Split compound values with `/`; give every stale value an anchor regex (`38~participants`).
- After writing a rule, inject the error back once and confirm it rings; then run
  `dead_rule_check.py`. A check that never fires is worse than no check.

## Figures (`tools/figures/`): needs numpy + Pillow (`figure_check.py`: PyMuPDF)

| Tool | What it does | Run |
|------|--------------|-----|
| `figure_a11y.py` | Colour-vision accessibility: simulates three CVD types plus greyscale, flags colour pairs that collapse, and writes the simulated images for you to look at. | `python3 figure_a11y.py figures/*.png` |
| `figure_check.py` | Mechanical check of figures and tables in a **typeset PDF**: caption numbering (gaps, duplicates), every figure/table mentioned in the text and every mention captioned (references are matched across line breaks, plural forms such as "Figures 1, 2, and 5" are expanded, appendix tables are kept apart), vector figures and images running past the text column (🟡) or off the page (🔴) (white margins inside an image and clipped vector patterns do not count), text in vector figures under `--min-pt`, and rasters shrunk until their text is unreadable (font size estimated from the effective dpi, assuming the figure was drawn for 300 dpi). Writes a cropped PNG of every figure plus `_review_checklist.md` for a visual pass. Chinese (圖／表) and English captions. Exit 1 = some 🔴, 2 = PyMuPDF missing. | `python3 figure_check.py paper.pdf [--out figcheck/] [--min-pt 6] [--min-dpi 200] [--json]` |

- Journals are mostly printed in black and white and ~8% of men have a red-green colour
  vision deficiency; a figure separating series by hue alone fails for both. This shows
  up in review as "the figure is hard to read" without the author learning why.
- 🔴 **Open the simulated images.** "These two collapse" is reliable; "this figure is
  fine" is not a guarantee. The simulation is a linear approximation, not a model of
  vision. Add `pymupdf` if you want to check PDF figures.
- `figure_check.py` exists because a figure shrunk to save a page ended up with ~3 pt
  axis labels and nobody noticed until the author did. Run it after every compression
  (`method/COMPRESSION.md`) and before every delivery. In a review copy, comment markers
  create reference noise; judge on the submission build. The font-size estimate for
  raster figures is an estimate: look at the crops.

## References (`tools/refs/`): zero installs

| Tool | What it does | Run |
|------|--------------|-----|
| `snowball.py` | Citation snowballing: forward ("who cites X"), backward ("what X cites"), related. Multi-seed aggregation. Papers hitting more seeds (`seed_hits`) are the most likely should-have-read literature. OpenAlex primary, Semantic Scholar fallback on quota; free keyless APIs, stdlib only. | `python3 snowball.py --doi <doi> --direction forward` |
| `pdf_fetch.py` | Fetch reference PDFs in three layers (bib entries without a DOI are read from `eprint`/arXiv URLs, then resolved by **exact** title match on arXiv → OpenAlex, throttled; only books/chapters come back as `MANUAL`): open-access resolvers (adds Europe PMC / CORE / OpenAIRE) → `curl_cffi` TLS impersonation → a real Chrome on a persistent profile, which is what actually clears Cloudflare at ACM/Wiley/SAGE/AIP/Elsevier (TLS impersonation alone does not). Misses are tagged `PAYWALL` / `CAPTCHA` / `NO-LINK` so you know which are worth another five minutes. **Not stdlib**: `pip install curl_cffi patchright`; without them it degrades to urllib + OA sources and says so. Only fetches what you are entitled to. | `python3 pdf_fetch.py --bib references.bib --out refs-pdf` |
| `retraction_scan.py` | Retraction check for everything you cite: each DOI is asked of Crossref (Retraction Watch data arrives as `update-to` / `updated-by` relations) **and** OpenAlex (`is_retracted`); flagged if either says so. Input: a `.bib`, a one-DOI-per-line file, or DOIs on the command line. Exit 1 = retracted found, 2 = some queries failed. | `python3 retraction_scan.py --bib references.bib [--out report.json]` |
| `lit_map.py` | Literature map: co-citation ranking within a batch of literature (candidate classics, a starting point, judged by hand, see `method/RIGOR_PROCESS.md` stage 3) + most-cited recent work in a year window. Query by `title_and_abstract` (full-text search surfaces cross-field noise); OpenAlex bills by usage, 429 = daily quota spent. | `python3 lit_map.py --query "<topic>" --from-year 2010 --limit 200 --out map.md [--csv refs.csv] [--save-json]` |
| `missing_refs.py` | The list of reference PDFs the author still has to download by hand: `.bib` entries with no `<pdfdir>/<citekey>.pdf` (a hand-filed `NN [Author Year] Title.pdf` that matches the entry also counts), minus whatever the author's own PDF library already holds (three gates: year + first-author surname + title similarity; ambiguous matches are listed for you, not the author). Writes `_missing.md` (doi.org links, URLs, ISBNs) and `_missing.tsv`. `--apply` copies unique library matches into the project. No network. | `python3 missing_refs.py --bib references.bib [--pdfdir refs-pdf] [--library ~/papers] [--apply]` |
| `inbox_ingest.py` | Files the PDFs the author downloaded by hand (publisher file names, default `~/Downloads`, last 72 hours): matches each to a missing entry by DOI, title and content, verifies the content like any fetched PDF, names it `<citekey>.pdf` and logs it in `_inbox_log.tsv`. Not filed, and listed for you: DOI right but content wrong (supplement, erratum), one file matching several entries, files matching nothing (left in place), content mismatch. `--to-library` also copies into your library (deduplicated by SHA-256); `--clean` moves only filed sources to the Trash, never deletes. Preview by default. Content checks need `pdftotext`; without it, matching falls back to DOI and file name and says so. | `python3 inbox_ingest.py --bib references.bib [--pdfdir refs-pdf] [--hours 72 \| --all] [--apply] [--library DIR --to-library] [--clean]` |

- A 429 from OpenAlex is a **daily quota wall** (resets midnight UTC), not "no
  results". Rerun later. `--email you@example.org` is optional but gets you the
  polite (faster) pool.
- 🔴 `retraction_scan.py` reports **`NO_DOI` entries separately and never counts them
  as scanned**: retraction matching runs on DOI records, so a book or early paper
  without a DOI is outside what the tool can check. It is not verified, and rerunning will
  not change it. `API_ERROR` is likewise not a pass; the exit code says the scan is
  incomplete. A `RETRACTED` hit still needs a human to read the notice.
- The three reference tools chain: `pdf_fetch.py` gets what it can into `refs-pdf/`,
  `missing_refs.py` lists only what is still missing and not in your library, and once
  the author has downloaded those, `inbox_ingest.py` files them into the same
  `refs-pdf/<citekey>.pdf` layout that `verify-citations` reads.
- `lit_map.py --dois seeds.txt` takes a hand-picked seed set instead of a query.
  For a full bibliometric science map from the same raw data, pass `--save-json`
  and hand it to R's `bibliometrix` (see `setup/TOOLS.md`).

## Method decision (`tools/method/`): zero installs (except the optional Tea wrapper)

| Tool | What it does | Run |
|------|--------------|-----|
| `method_decision_check.py` | Format gate for `method-decision.md`: checks the required sections exist (claims, comparable-studies table, analysis-method table, candidates with independent-check field, claim-alignment table, premortem). Recognizes both the English template and the zh-TW one. Passing proves the sections exist, not that the method is right. | `python3 method_decision_check.py method-decision.md [--selftest]` |
| `analysis_plan_check.py` | Format + timing gate for `analysis-plan.md`: checks required sections exist and, in the default mode, that the plan's commit date precedes the recorded data-collection start date. `--phase6` instead checks the deviations section was filled in (or explicitly says "no deviations") before delivery. | `python3 analysis_plan_check.py analysis-plan.md [--phase6] [--selftest]` |
| `tea_second_opinion.py` | Optional wrapper around Tea (tealang, needs its own environment, see `setup/TOOLS.md`): describe hypotheses and variable types, get a second opinion on which classic statistical test fits. Covers classic tests only, not mixed/ordinal models, one input alongside the comparison table, not a verdict. | `python3 tea_second_opinion.py --spec spec.json` |

- Both check scripts exist to catch the same failure mode as `dead_rule_check.py`
  elsewhere in this kit: "the section is in the file" is not the same as "the
  section says something real". They check structure, and the judgment (is this
  the right method, does the independent-check field name an actual person) stays
  with the author and Claude.
- `analysis_plan_check.py`'s timing check is the one hard gate in the whole method
  pipeline (see `method/WORKFLOW.md` Phase 3.0): pre-registration only has value
  ahead of the data, so the check is deliberately strict about the date rather than
  just checking the file exists.

## English (`tools/en/`): one or two free installs

| Tool | What it does | Needs |
|------|--------------|-------|
| `lt_check.sh` | Offline grammar + US/UK spelling-consistency (LanguageTool), markup stripped by the bundled pandoc filter. Auto-mounts optional LanguageTool n-gram data (~15 GB, `~/Corpora/lt-ngrams` or `$LT_NGRAMS`) for statistical confusable-pair detection (affect/effect); runs fine without it. | `brew install languagetool pandoc` |
| `ai_style_diag.py` | English AI fingerprint as **percentiles** vs a baseline corpus of published papers in your field, including **LLM convergence-word density** (`en_slop_terms.tsv` beside the script: 162 terms derived from sam-paech/slop-forensics, MIT, minus words HCI papers use anyway. Rebuild the filter against your own field's corpus if the vocabularies overlap) and a **contrast-sentence total** (`not…but` + "X, not Y" + `rather than` + `instead of` + `not only`, `--show-contrast` lists every hit; `--gate` exits non-zero above the baseline's 90th percentile). The words/sentences that carry each number are printed. | a corpus you assemble; `pdftotext` only for PDF input |
| `biber_diag.py` | Grammatical-register check: dozens of Biber-style features (nominalization rate, sentence-final gerund clauses, passive voice, and more) vs the same baseline corpus, reported as percentiles with items outside the baseline's 5th/95th flagged individually. A single overall percentile can hide a feature sitting at several times the baseline median. Read by direction: the Reinhart et al. fixes (nominalizations back to verbs, split trailing -ing clauses) apply only above p90; below p10 the fix runs the other way. `--groups <venue>` compares against one venue (whole corpus if it has under 30 papers), `--json` feeds `register/register_profile.py`. | pybiber + spaCy + polars in a dedicated env, see `setup/TOOLS.md` |
| `bundle_diag.py` | Lexical bundles (recurring 3–5-word phrases) the draft uses far more than the baseline does, the phrase-level layer between single convergence words and whole-sentence cadence. | same corpus as `ai_style_diag.py` |
| `metadiscourse_en.py` | Hyland stance / engagement / boosting-hedging markers vs the baseline, with p10/median/p90 per marker and a direction flag. A draft that under-uses hedges and reader-engagement relative to expert writing reads more certain than the evidence supports. `--matches` prints which sentences carry each marker; `--groups <venue>` compares against one venue; `--json` for `register/register_profile.py`. | same corpus as `ai_style_diag.py` |

```bash
# LanguageTool grammar deep-pass
tools/en/lt_check.sh draft.md                 # default en-US
tools/en/lt_check.sh draft.tex --variant en-GB

# English style fingerprint (needs your own baseline corpus of ≥30 published papers)
python3 tools/en/ai_style_diag.py draft.md --corpus ~/my-field-corpus
python3 tools/en/ai_style_diag.py draft.md --corpus ~/my-field-corpus --gate           # revision-round gate
python3 tools/en/bundle_diag.py draft.md --corpus ~/my-field-corpus
python3 tools/en/metadiscourse_en.py draft.md --corpus ~/my-field-corpus --matches
python3 tools/en/metadiscourse_en.py draft.md --corpus ~/my-field-corpus --groups <venue>  # one venue
~/.venvs/biber/bin/python tools/en/biber_diag.py draft.md --corpus ~/my-field-corpus   # dedicated env
~/.venvs/biber/bin/python tools/en/biber_diag.py draft.md --corpus ~/my-field-corpus --groups <venue> --json
```

🔴 **`ai_style_diag.py` corpus hygiene:** the baseline holds **only other people's
published papers**: never your own drafts/posters/co-authored work, or the diagnosis
cancels itself out. Exclude any of your own files with `--exclude yourname`. As a
second line of defence the tool also drops versioned draft filenames (`*_v0.0.48.txt`)
and files whose first 3000 characters carry anonymised-submission or template markers
(`ANONYMOUS AUTHOR`, `Affiliations withheld`, venue placeholder titles), and prints
`excluded N (reasons)`: a measured 56%-contaminated baseline had hidden three
metrics that should have read above the 90th percentile.

## What is NOT bundled (and why)

- **Official-terminology term-checking** (against a national term database): the
  original relies on a proprietary 1.8M-entry Taiwan term DB that can't be
  redistributed. `zh_localize.py` covers the common mainland-vs-Taiwan cases; a full
  term-consistency check is a "bring your own term DB" upgrade.
- **Statistics, literature RAG, batch summarization**: these need heavier local
  infrastructure (R, a vector DB, a local LLM). See `../setup/TOOLS.md`. They're
  optional full-mode upgrades, and your Claude can help you stand up your own.
- **Anyone's corpora or drafts**: never shipped. The kit ships methods and tools, not
  writing or data.

## Vocabulary: `tools/vocab/`

| Script | What it does | Needs |
|--------|--------------|-------|
| `fetch_awl.py` | Downloads the official "AWL Sublist Families" document (Victoria University of Wellington) and writes `data/academic-vocab/awl_families.tsv` (`headword`, `sublist`, `related_forms`) so `paper-review` Layer 3 can grep it. The AWL is CC BY-NC-ND 3.0; the ND term forbids redistributing a re-formatted copy, so the kit ships the fetcher, not the data, and the TSV is git-ignored. HTML sublist pages are the fallback source (`--source html`). | none (internet) |

```bash
python3 tools/vocab/fetch_awl.py            # once; writes data/academic-vocab/awl_families.tsv
python3 tools/vocab/fetch_awl.py --check data/academic-vocab/awl_families.tsv   # re-verify later
```

Cite the list as Coxhead (2000), *TESOL Quarterly* 34(2). Non-commercial use only.

