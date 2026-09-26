# Full mode: optional local power-ups (graceful degradation map)

> None of this is required. Lite mode (`LITE.md`) does the whole method with just
> Claude + the web. Add these **one at a time, only when the author hits a real wall.**
> For each capability: what lite mode does, and the optional upgrade. A generated
> skill must gate every reference to these behind "if installed."
>
> 📦 **Already bundled in `tools/`** (no big install): the Chinese checkers
> (`zh_localize`, `zh_ai_style`, `voice_lint`, zero-install, Python stdlib), the
> English `lt_check.sh` (needs `brew install languagetool pandoc`) + `ai_style_diag.py`
> (needs a corpus you assemble), `bundle_diag.py` + `metadiscourse_en.py` (zero-install,
> same corpus), and the zero-install scanners `tools/refs/snowball.py`,
> `tools/refs/retraction_scan.py`, `tools/refs/lit_map.py`,
> `tools/claims/uncited_claims_scan.py`, `tools/method/method_decision_check.py` +
> `tools/method/analysis_plan_check.py`, `tools/submissions/style_reaudit.py`, and the
> `tools/regress/` pair (`regress.py`, `dead_rule_check.py`) behind the `doc-regress`
> skill, and the native-polish pair `tools/register/register_profile.py` +
> `tools/register/polish_check.py` (zero-install; they need the register corpus below).
> Those rows below are marked ✅bundled. `tools/en/biber_diag.py` is the one
> English tool needing a dedicated environment (pybiber + spaCy). See `tools/README.md`.

| Capability | Lite (default, no install) | Full (optional upgrade) |
|-----------|----------------------------|--------------------------|
| **Find literature** | WebSearch + Semantic Scholar / OpenAlex / Crossref | + a local full-text RAG over PDFs you hold (semantic search "which paper, which page") |
| **Citation snowballing** (who cites X / what X cites / similar work) | ✅bundled `tools/refs/snowball.py`: Python stdlib only, free keyless APIs, works day one | (already full-strength; `--email` is optional politeness) |
| **Fetch reference PDFs** | Open-access resolvers (Unpaywall/arXiv/author pages) | ✅bundled `tools/refs/pdf_fetch.py`, layered: OA resolvers (+ Europe PMC / CORE / OpenAIRE, which the usual four miss) → `curl_cffi` (TLS impersonation, fixes edge-403s) → **a real Chrome on a persistent profile** (`pip install curl_cffi patchright`; patchright drives your installed Chrome, no second browser downloaded). Cloudflare-fronted publishers (ACM/Wiley/SAGE/AIP/Elsevier) are reachable this way. A TLS-impersonating client alone is *not* enough. Add your institutional access (library VPN / sign-in in that profile) for subscription full texts. **Misses are classified** `PAYWALL` / `CAPTCHA` / `NO-LINK`, which is the part that actually saves you time |
| **Verify citations** | Claude reads OA source, checks direction | + a multi-agent adversarial pass over a local PDF library (skeptic template: `agents/citation-skeptic.md`) |
| **Retraction scan** (has anything I cite been retracted?) | ✅bundled `tools/refs/retraction_scan.py`: whole `.bib` against Crossref update relations + OpenAlex `is_retracted`; stdlib, needs only the network. Re-run before *every* delivery; RETRACTED hits are hand-checked (fuzzy matching misfires) | (already full-strength) |
| **Uncited-claims scan** (quantitative / causal / superlative sentences with no citation) | ✅bundled `tools/claims/uncited_claims_scan.py`: pure regex, zero LLM, Chinese + English. Each hit: cite it, point to your own data (ledger), or soften the wording; suppress with an inline waiver that carries a reason | (already full-strength) |
| **Document regression** (a caught error becomes a standing check) | ✅bundled `tools/regress/regress.py` + `dead_rule_check.py`, driven by a rules file (start from `rules.template.json`) kept *in the author's project*; includes the numbers-ledger checks (stale value recurs → FAIL, current value missing from draft → WARN). Method in `skills/doc-regress` | (already full-strength) |
| **Scanned / CJK PDF extraction** | Render pages to images and read visually (slow) | **MinerU** (`uv tool install mineru` or `pipx install mineru`): scans, CJK layouts, tables, formulas → clean markdown |
| **Statistics / analysis** | Honest description + simple summaries | R (mixed models via `lme4`/`afex`, ordinal via `ordinal::clmm`, post-hoc via `emmeans`) / Python / a persistent Jupyter kernel. The computation runs locally. **Bayesian, three roads:** formula-expressible hierarchical regression → `brms`; evidence for the null (BF01) → `BayesFactor`; discrete latent variables, custom distributions or samplers, JAGS ports → `nimble` (Stan cannot sample discrete parameters). All three report priors + convergence |
| **Design diagnosis** (can this design answer the question at all?) | Claude reasons about confounds and states the claim's ceiling honestly | R `DeclareDesign`: declare model / inquiry / data strategy / answer strategy, run Monte-Carlo diagnosis, read **coverage** (should be ≈.95), not just power; then `simr` for sample size. Only when new data will be collected *and* an effect claimed |
| **Statistical-consistency check of a draft** | Recompute reported numbers by hand, mark lower-confidence | R packages **statcheck** (recompute APA-style p values) + **scrutiny** (GRIM: is that mean possible given N): `install.packages(c("statcheck","scrutiny"))`. **Run the local R packages, not the web versions**: see "Not recommended" below |
| **Grammar / style linting** | Claude's by-hand passes | ✅bundled `tools/en/lt_check.sh` (LanguageTool, offline): `brew install languagetool pandoc`; optional LanguageTool n-gram data (~15 GB, auto-detected at `~/Corpora/lt-ngrams` or `$LT_NGRAMS`) adds statistical confusable-pair detection (affect/effect). Optional extras: **Harper** (offline, millisecond first pass on every save: editor plugin or CLI; LanguageTool stays the authoritative second pass) and, for Chinese, **autocorrect** (`brew install autocorrect`: full/half-width punctuation and CJK–Latin spacing) |
| **De-AI / voice checking** | Convergence-word + AI-syntax passes by hand | ✅bundled `tools/en/ai_style_diag.py` (percentiles vs a corpus you assemble, published papers only, never your own drafts) |
| **Grammatical-register check** (beyond convergence words: nominalization, gerund clauses, dozens of Biber-style features) | Eyeball register by hand; the overclaim and convergence-word passes still run | ✅bundled `tools/en/biber_diag.py`, needs **pybiber + spaCy + polars** in a dedicated environment (keeps their pinned dependency versions off your main Python): `python3 -m venv ~/.venvs/biber && ~/.venvs/biber/bin/pip install pybiber spacy polars && ~/.venvs/biber/bin/python -m spacy download en_core_web_sm`, then `~/.venvs/biber/bin/python tools/en/biber_diag.py draft.md --corpus <dir> --groups <venue>`. Read it by direction: a feature is reduced only above p90 and restored below p10. Record that environment's python in the author's CLAUDE.md as `BIBER_PYTHON`, so `register_profile.py` can add this layer |
| **Lexical-bundle / metadiscourse checks** | Claude reads for repeated phrases and hedging/boosting by hand | ✅bundled, zero-install: `tools/en/bundle_diag.py` (over-used lexical bundles vs your corpus), `tools/en/metadiscourse_en.py` (Hyland stance/engagement/boosting-hedging markers vs your corpus, read by direction; `--groups <venue>` compares against one venue, `--json` for machines) |
| **Register baseline / native polish** (does the draft read like the field's papers? `method/WORKFLOW.md` Phase 5.5) | Compare by reading against the target journal's author guidelines plus 2–3 of its papers; write the deviations down as a reading, not a measurement (`setup/LITE.md`) | ✅bundled, zero-install: `tools/register/register_profile.py` (deviation list per line range: which features sit outside the p10–p90 band of same-field papers, which way to move them, with bounds and instances; `--exemplars` picks feel-reference paragraphs) + `tools/register/polish_check.py` (checks an editor's change list: invariants, word budget, forbidden forms, register direction; `--apply` writes back only when all pass). Chinese measurement: `tools/zh-tw/zh_register.py`. **Needs a register corpus** you assemble: at least **30** published papers by other people from the author's field, as plain text in `<corpus>/<venue>/*.txt` (one folder per journal; a journal folder is used on its own once it holds 30), each with 1000+ Chinese characters or 800+ English words of body text, ideally published before 2023. Convert PDFs with `pdftotext` (MinerU for scanned or CJK layouts). Record the corpus paths in the author's CLAUDE.md (`ZH_CORPUS_DIR` for Chinese, `CORPUS_DIR` for English; the English corpus is the same one `ai_style_diag.py` uses) |
| **Literature mapping / bibliometrics** (candidate classics by co-citation, full science maps) | ✅bundled `tools/refs/lit_map.py` (zero-install; a candidate list, judged by hand, see `method/RIGOR_PROCESS.md` stage 3) | + R **bibliometrix** and **openalexR** (`install.packages("bibliometrix")`, `remotes::install_github("ropensci/openalexR")`) for a full co-citation/science map from `lit_map.py --save-json`'s raw data; **PRISMA2020** (`install.packages("PRISMA2020")`) draws the flow diagram for a systematic/scoping review |
| **Large-scale literature screening** (hundreds of candidates, systematic/scoping review) | Read and triage by hand, fine under ~50–100 items | **ASReview** (`asreview lab`) in its own environment: `python3 -m venv ~/.venvs/asreview && ~/.venvs/asreview/bin/pip install asreview`. Active-learning screening; simulation studies report it can cut screening effort substantially at high recall targets, still a human decision per item, not an oracle |
| **Second opinion on which statistical test fits** | `method/METHOD_CARDS.md`'s decision index + the comparison table from Phase 3.0 | **Tea** (tealang) in its own environment (it pins to Python 3.10–3.13, likely to conflict with a newer default interpreter): `python3.11 -m venv ~/.venvs/tea && ~/.venvs/tea/bin/pip install tea-lang`: describes hypotheses and variable types, suggests a test. Covers classic tests only, not mixed/ordinal models; treat its answer as one input alongside the comparison table, not a verdict |
| **Argument mapping** (visualize the skeleton's move structure) | Prose skeleton nodes are enough for most drafts | **Argdown** (`npm install -g @argdown/cli`) renders a `.argdown` outline as an argument map, useful for a paper with an unusually tangled rebuttal structure, optional otherwise |
| **Chinese metadiscourse scale** (optional, Traditional-Chinese-Taiwan add-on) | `tools/zh-tw/zh_ai_style.py`'s heuristic metadiscourse markers | **zh-metadiscourse-scale**: a *scale*, not a detector; read its own documentation on what it does and does not claim before using it as a checklist item, not a pass/fail gate |
| **Traditional-Chinese-Taiwan** | Claude checks by hand | ✅bundled `tools/zh-tw/` (zero install): `zh_localize` (Taiwan terms), `zh_ai_style` (Chinese AI-tic + contrast-sentence total + long sentences, both ends), `voice_lint` (your voice rules + heading scan; `--paper` drops the personal-habit rules for papers), `zh_gloss_scan` (parenthetical asides), `zh_register` (register profile against same-field Taiwan journal papers; needs the register corpus above). Official-term DB check = bring-your-own DB; optional scale = `zh-metadiscourse-scale` above. |
| **PDF / typesetting** | Cleanest export + "layout still needs a pass" | Typst or Quarto/LaTeX with the venue's template and embedded fonts |

## Numeric pitfalls (check before trusting a number)

Two known traps that produce *wrong numbers with no warning*. A generated skill that
runs statistics locally must mention them.

- **scipy ≥ 1.17 `mannwhitneyu` with float32 input returns a wrong U and p, silently**
  (a regression introduced in 1.17.0; 1.16.x is unaffected; scipy issue #24777, still
  open at the time of writing). Pin `scipy<1.17` in the analysis environment, **and**
  cast inputs to float64 anyway as defense in depth. A collaborator's venv may not be
  pinned. Upgrading other packages can drag scipy up; assert the version after any
  environment change.
- **η² from `effectsize` on an `afex` / `Anova.mlm` object**: the overlapping-factor-
  name fix is unconfirmed; cross-check against the effect sizes `afex` reports itself.
  If they disagree, report neither until you know why.
- General rule: **suspiciously tidy numbers are a red flag** (an effect of exactly 0.5,
  exactly 2×, identical CIs across groups). That is usually a constant leaking from a
  broken pipeline, not a result. Go back to the log and the exit code before it
  enters the draft.

## Not recommended (and the lite alternative)

These looked useful during a survey of the field's tooling and were rejected for a
concrete reason, listed so you don't re-discover the same dead end:

- **SciScore, Penelope.ai**: upload the full manuscript to a third party. Lite
  alternative: the reporting-guideline checklist in `paper-review` Layer 4, done
  by hand.
- **statcheck and rSPRITE's web versions**: send your data to an external server.
  Lite alternative: the local R packages (`statcheck`, `scrutiny`), already in the
  table above, same checks, nothing leaves your machine.
- **Consensus, SciSpace**: uploaded documents are processed in the cloud, and
  neither publishes an independent accuracy evaluation you can check. Lite
  alternative: WebSearch + Semantic Scholar/OpenAlex, read the sources yourself.
- **CollabCoder**: a genuinely useful qualitative-coding comparison design, but it
  requires an OpenAI API key and sends interview data to OpenAI's servers. Lite
  alternative: a second human coder + `irr`-style agreement statistics in R.
- **PaperQA2**: defaults to calling a cloud model, and stands up a second search
  index that will drift from whatever local literature store you already keep.
  Lite alternative: your own local RAG (full mode) or WebSearch + manual reading
  (lite mode).

## Principles for the installer
- **Privacy is non-negotiable in both modes:** unpublished drafts and raw data go to
  no third-party service. No cloud detectors, no uploads to other public AI tools. That rule
  doesn't relax in full mode. Claude Code itself sends what it reads to Anthropic; say so to the author.
- **Corpus hygiene** (if you build a style or register baseline): the baseline holds
  **only other people's published papers**. Never mix in the author's own
  drafts/posters/co-authored work or admin junk. Comparing the author's style against a
  baseline containing their own writing makes the de-AI diagnosis cancel itself out, and
  a register baseline built from the author's own drafts would measure their habits, not
  the field's. The author's own writing belongs in `voice-samples/`, for letters and
  personal statements only.
- **Don't over-install.** A cautious first-timer needs none of this. Suggest the single
  tool that unblocks the specific wall they hit, and stop.

> This kit deliberately does **not** ship the original author's private scripts,
> corpora, or server setup. Full mode here means "here's the *kind* of tool and why";
> the author's Claude helps them stand up their own, locally, if and when they want it.
