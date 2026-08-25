# Bundled tools

Small, local, privacy-respecting checkers you can run from day one. **The three
Chinese tools need nothing installed** (Python 3 standard library only) — they work
out of the box. The English tools need one or two free offline programs.

> Everything here runs **on your machine**; drafts never leave it. Never paste an
> unpublished draft into a cloud "AI detector."
>
> These are generalized from one researcher's toolkit. Adapt the word lists and
> rules to *your* field and voice — they're starting points, not gospel.

| Folder | Tool | One line |
|--------|------|----------|
| `zh-tw/` | `zh_localize.py` | mainland-vs-Taiwan terms + 台/臺 consistency |
| `zh-tw/` | `zh_ai_style.py` | Chinese AI syntax fingerprint |
| `zh-tw/` | `voice_lint.py` | your own voice rules as a hard gate |
| `claims/` | `uncited_claims_scan.py` | sentences that claim (numbers / causes / firsts) but cite nothing |
| `refs/` | `snowball.py` | forward / backward / related citation snowballing |
| `refs/` | `retraction_scan.py` | has anything you cite been retracted (Crossref + OpenAlex) |
| `vocab/` | `fetch_awl.py` | fetch Coxhead's AWL from the official VUW site into a local TSV (not shipped: CC BY-NC-ND) |
| `regress/` | `regress.py` + `dead_rule_check.py` | regression suite for long documents + false-green-light detector |
| `rebuttal/` | `check_response.py` | response-to-reviewers completeness |
| `submissions/` | `check_submissions.py` | duplicate-submission guard |
| `figures/` | `figure_a11y.py` | colour-vision accessibility of figures |
| `en/` | `lt_check.sh`, `ai_style_diag.py` | English grammar pass; English AI fingerprint vs your field |

## Chinese (`tools/zh-tw/`) — zero installs

| Tool | What it does | Run |
|------|--------------|-----|
| `zh_localize.py` | Flags mainland-Mandarin terms (反饋→回饋…) + 台/臺 consistency, with a false-positive whitelist. Report-only. | `python3 zh_localize.py draft.md` |
| `zh_ai_style.py` | Chinese AI syntax fingerprint: em-dash/semicolon/rule-of-three density, convergence words, sentence burstiness (heuristic). | `python3 zh_ai_style.py draft.md` |
| `voice_lint.py` | Mechanically enforces YOUR voice rules (config-driven). Exits non-zero until clean — use as a pre-delivery gate. | `python3 voice_lint.py draft.md [--rules voice_rules.json]` |

- `zh_ai_style.py` gets sharper if you point `--authored <folder>` at a folder of your
  own `.txt` writing — then words *you* genuinely use aren't flagged as AI tells.
  🔴 Point it at a folder holding **only your own writing** (keep a `voice-samples/`
  folder separate from your working drafts) — mixing AI drafts into the baseline
  cancels the diagnosis out. As a guard, files named with 草稿/draft/ai/claude/gpt are
  auto-skipped. Needs ~120+ Han chars to compute; for a short section use `voice_lint`.
- `voice_lint.py` ships generic defaults. Copy `templates/voice_rules.template.json`
  → `voice_rules.json`, edit it to match your own habits (what *you* never write), and
  pass `--rules voice_rules.json`. Build it from your `VOICE_PROFILE` (see `templates/`).

## Claims (`tools/claims/`) — zero installs

| Tool | What it does | Run |
|------|--------------|-----|
| `uncited_claims_scan.py` | Finds sentences that make a claim needing evidence — a number / % / p-value / N (quant), a causal verb (causal), "the first / only / to our knowledge" (super) — and carry **no citation marker**. English + Traditional Chinese triggers. Exits non-zero while unadjudicated findings remain. | `python3 uncited_claims_scan.py --src paper.md [--json report.json] [--only quant]` |

- Why it exists: citation-verification checks start from citation markers, so a
  sentence with no marker is never checked — and in design research those are the
  load-bearing ones ("17 student posters showed…", "improved by 23%"). This is the only
  pass that looks at them. It does **not** judge whether the claim is true.
- Each finding gets one of three dispositions: add a citation, name your own data
  source (put the number in the numbers ledger, see `regress/`), or soften the wording.
  Then silence it with a waiver on that line — `<!--uncited-ok: own data run3.csv-->`
  (Markdown) or `% uncited-ok: …` (LaTeX). The reason is mandatory; empty waivers are
  ignored, and every waiver is listed in the report so one cannot silently cover a
  whole paragraph.
- Recognises `\cite{}`, pandoc `[@key]`, numeric `[12]`, APA `(Chen, 2024)`, Chicago
  `(Dunne and Raby 2013)` and `Chen et al. (2024)`. Inline math is kept (statistics live
  there); display math, code, comments and table column specs are masked.

## Rebuttal (`tools/rebuttal/`) — zero installs

| Tool | What it does | Run |
|------|--------------|-----|
| `check_response.py` | Completeness check for a response-to-reviewers letter: every point answered, every promised change mapped to a real location, every DECLINE carrying evidence, no orphan point numbers. | `python3 check_response.py --points points.tsv --revisions revisions.tsv --letter letter.md` |

- Templates for all three files are in the same folder. It checks **completeness, not
  quality** — every point being answered doesn't mean it's answered well.
- The three failures it exists to stop: a point never answered, a change promised but
  never made, and point numbers renumbered without updating the letter.

## Submissions (`tools/submissions/`) — zero installs

| Tool | What it does | Run |
|------|--------------|-----|
| `check_submissions.py` | Duplicate-submission guard + status overview from one central ledger. Flags the same manuscript under review in two places, stale statuses, and moved project folders. | `python3 check_submissions.py --ledger SUBMISSIONS.tsv` |

- 🔴 **Keep ONE ledger, above all your project folders.** Simultaneous submission is a
  *cross-project* problem — a retitled manuscript sent to a second venue looks clean
  from inside either folder. A copy per project defeats the whole point.
- Never change a `manuscript_id` when you retarget to another venue; that id is what
  makes the guard work. Rows marked `unknown` provide **no** protection.

## Regression suite (`tools/regress/`) — zero installs

| Tool | What it does | Run |
|------|--------------|-----|
| `regress.py` | A regression suite for a long, repeatedly revised document: every rule is a mistake you actually made once, kept as a permanent check. Generic rules are config-driven (`rules.template.json`): dangling / orphan citations (numeric or BibTeX), personal-data patterns, internal words leaking into the delivered text, entity attribution, corrected claims that must not return, and a **numbers ledger** (R-STALE: a corrected old value comes back → FAIL; R-LEDGER: a current value is missing → WARN). Project rules go in a small Python file passed with `--extra`. | `python3 regress.py --config regress.json [--extra my_rules.py] [--json]` |
| `dead_rule_check.py` | The false-green-light detector: traces each rule and reports any whose body barely executes (an early return because its setting is empty). "The rule is in the list" is not the same as "the rule ran". | `python3 dead_rule_check.py regress.py --config regress.json` |

- Start by copying `rules.template.json` → `regress.json` and
  `numbers-ledger.template.md` → `numbers-ledger.md` next to your manuscript.
  Unconfigured rules are reported as `[INFO] … NOT guarding` rather than passing
  silently — fill them in, or accept that they guard nothing.
- 🔴 Only add a rule for an error that **really happened** and has a clear mechanical
  criterion. Prefer a miss to a false alarm: unclear criteria go to INFO, never FAIL.
- 🔴 Keep **one** numbers ledger and record values **as written in the manuscript**
  (`p < .001`, `94%`), not the computed ones; put exact values in the note column.
  Split compound values with `/`; give every stale value an anchor regex (`38~participants`).
- After writing a rule, inject the error back once and confirm it rings; then run
  `dead_rule_check.py`. A check that never fires is worse than no check.

## Figures (`tools/figures/`) — needs numpy + Pillow

| Tool | What it does | Run |
|------|--------------|-----|
| `figure_a11y.py` | Colour-vision accessibility: simulates three CVD types plus greyscale, flags colour pairs that collapse, and writes the simulated images for you to look at. | `python3 figure_a11y.py figures/*.png` |

- Journals are mostly printed in black and white and ~8% of men have a red-green colour
  vision deficiency; a figure separating series by hue alone fails for both. This shows
  up in review as "the figure is hard to read" without the author learning why.
- 🔴 **Open the simulated images.** "These two collapse" is reliable; "this figure is
  fine" is not a guarantee — the simulation is a linear approximation, not a model of
  vision. Add `pymupdf` if you want to check PDF figures.

## References (`tools/refs/`) — zero installs

| Tool | What it does | Run |
|------|--------------|-----|
| `snowball.py` | Citation snowballing: forward ("who cites X"), backward ("what X cites"), related. Multi-seed aggregation — papers hitting more seeds (`seed_hits`) are the most likely should-have-read literature. OpenAlex primary, Semantic Scholar fallback on quota; free keyless APIs, stdlib only. | `python3 snowball.py --doi <doi> --direction forward` |
| `retraction_scan.py` | Retraction check for everything you cite: each DOI is asked of Crossref (Retraction Watch data arrives as `update-to` / `updated-by` relations) **and** OpenAlex (`is_retracted`); flagged if either says so. Input: a `.bib`, a one-DOI-per-line file, or DOIs on the command line. Exit 1 = retracted found, 2 = some queries failed. | `python3 retraction_scan.py --bib references.bib [--out report.json]` |

- A 429 from OpenAlex is a **daily quota wall** (resets midnight UTC), not "no
  results" — rerun later. `--email you@example.org` is optional but gets you the
  polite (faster) pool.
- 🔴 `retraction_scan.py` reports **`NO_DOI` entries separately and never counts them
  as scanned**: retraction matching runs on DOI records, so a book or early paper
  without a DOI is outside what the tool can check — not verified, and rerunning will
  not change it. `API_ERROR` is likewise not a pass; the exit code says the scan is
  incomplete. A `RETRACTED` hit still needs a human to read the notice.

## English (`tools/en/`) — one or two free installs

| Tool | What it does | Needs |
|------|--------------|-------|
| `lt_check.sh` | Offline grammar + US/UK spelling-consistency (LanguageTool), markup stripped by the bundled pandoc filter. Auto-mounts optional LanguageTool n-gram data (~15 GB, `~/Corpora/lt-ngrams` or `$LT_NGRAMS`) for statistical confusable-pair detection (affect/effect); runs fine without it. | `brew install languagetool pandoc` |
| `ai_style_diag.py` | English AI fingerprint as **percentiles** vs a baseline corpus of published papers in your field. | a corpus you assemble; `pdftotext` only for PDF input |

```bash
# LanguageTool grammar deep-pass
tools/en/lt_check.sh draft.md                 # default en-US
tools/en/lt_check.sh draft.tex --variant en-GB

# English style fingerprint (needs your own baseline corpus of ≥30 published papers)
python3 tools/en/ai_style_diag.py draft.md --corpus ~/my-field-corpus
```

🔴 **`ai_style_diag.py` corpus hygiene:** the baseline holds **only other people's
published papers** — never your own drafts/posters/co-authored work, or the diagnosis
cancels itself out. Exclude any of your own files with `--exclude yourname`. As a
second line of defence the tool also drops versioned draft filenames (`*_v0.0.48.txt`)
and files whose first 3000 characters carry anonymised-submission or template markers
(`ANONYMOUS AUTHOR`, `Affiliations withheld`, venue placeholder titles), and prints
`excluded N (reasons)` — a measured 56%-contaminated baseline had hidden three
metrics that should have read above the 90th percentile.

## What is NOT bundled (and why)

- **Official-terminology term-checking** (against a national term database): the
  original relies on a proprietary 1.8M-entry Taiwan term DB that can't be
  redistributed. `zh_localize.py` covers the common mainland-vs-Taiwan cases; a full
  term-consistency check is a "bring your own term DB" upgrade.
- **Statistics, literature RAG, batch summarization**: these need heavier local
  infrastructure (R, a vector DB, a local LLM). See `../setup/TOOLS.md` — they're
  optional full-mode upgrades, and your Claude can help you stand up your own.
- **Anyone's corpora or drafts**: never shipped. The kit ships methods and tools, not
  writing or data.

## Vocabulary — `tools/vocab/`

| Script | What it does | Needs |
|--------|--------------|-------|
| `fetch_awl.py` | Downloads the official "AWL Sublist Families" document (Victoria University of Wellington) and writes `data/academic-vocab/awl_families.tsv` — `headword`, `sublist`, `related_forms` — so `paper-review` Layer 3 can grep it. The AWL is CC BY-NC-ND 3.0; the ND term forbids redistributing a re-formatted copy, so the kit ships the fetcher, not the data, and the TSV is git-ignored. HTML sublist pages are the fallback source (`--source html`). | none (internet) |

```bash
python3 tools/vocab/fetch_awl.py            # once; writes data/academic-vocab/awl_families.tsv
python3 tools/vocab/fetch_awl.py --check data/academic-vocab/awl_families.tsv   # re-verify later
```

Cite the list as Coxhead (2000), *TESOL Quarterly* 34(2). Non-commercial use only.

