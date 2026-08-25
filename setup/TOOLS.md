# Full mode — optional local power-ups (graceful degradation map)

> None of this is required. Lite mode (`LITE.md`) does the whole method with just
> Claude + the web. Add these **one at a time, only when the author hits a real wall.**
> For each capability: what lite mode does, and the optional upgrade. A generated
> skill must gate every reference to these behind "if installed."
>
> 📦 **Already bundled in `tools/`** (no big install): the Chinese checkers
> (`zh_localize`, `zh_ai_style`, `voice_lint` — zero-install, Python stdlib), the
> English `lt_check.sh` (needs `brew install languagetool pandoc`) + `ai_style_diag.py`
> (needs a corpus you assemble), and the zero-install scanners `tools/refs/snowball.py`,
> `tools/refs/retraction_scan.py`, `tools/claims/uncited_claims_scan.py`, and the
> `tools/regress/` pair (`regress.py`, `dead_rule_check.py`) behind the `doc-regress`
> skill. Those rows below are marked ✅bundled. See `tools/README.md`.

| Capability | Lite (default, no install) | Full (optional upgrade) |
|-----------|----------------------------|--------------------------|
| **Find literature** | WebSearch + Semantic Scholar / OpenAlex / Crossref | + a local full-text RAG over PDFs you hold (semantic search "which paper, which page") |
| **Citation snowballing** (who cites X / what X cites / similar work) | ✅bundled `tools/refs/snowball.py` — Python stdlib only, free keyless APIs, works day one | (already full-strength; `--email` is optional politeness) |
| **Fetch reference PDFs** | Open-access resolvers (Unpaywall/arXiv/author pages) | + institutional/library access (e.g. a university VPN) for paywalled full texts |
| **Verify citations** | Claude reads OA source, checks direction | + a multi-agent adversarial pass over a local PDF library (skeptic template: `agents/citation-skeptic.md`) |
| **Retraction scan** (has anything I cite been retracted?) | ✅bundled `tools/refs/retraction_scan.py` — whole `.bib` against Crossref update relations + OpenAlex `is_retracted`; stdlib, needs only the network. Re-run before *every* delivery; RETRACTED hits are hand-checked (fuzzy matching misfires) | (already full-strength) |
| **Uncited-claims scan** (quantitative / causal / superlative sentences with no citation) | ✅bundled `tools/claims/uncited_claims_scan.py` — pure regex, zero LLM, Chinese + English. Each hit: cite it, point to your own data (ledger), or soften the wording; suppress with an inline waiver that carries a reason | (already full-strength) |
| **Document regression** (a caught error becomes a standing check) | ✅bundled `tools/regress/regress.py` + `dead_rule_check.py`, driven by a rules file (start from `rules.template.json`) kept *in the author's project*; includes the numbers-ledger checks (stale value recurs → FAIL, current value missing from draft → WARN). Method in `skills/doc-regress` | (already full-strength) |
| **Scanned / CJK PDF extraction** | Render pages to images and read visually (slow) | **MinerU** (`uv tool install mineru` or `pipx install mineru`) — scans, CJK layouts, tables, formulas → clean markdown |
| **Statistics / analysis** | Honest description + simple summaries | R (mixed models via `lme4`/`afex`, ordinal via `ordinal::clmm`, post-hoc via `emmeans`) / Python / a persistent Jupyter kernel — data stays local. **Bayesian, three roads:** formula-expressible hierarchical regression → `brms`; evidence for the null (BF01) → `BayesFactor`; discrete latent variables, custom distributions or samplers, JAGS ports → `nimble` (Stan cannot sample discrete parameters). All three report priors + convergence |
| **Design diagnosis** (can this design answer the question at all?) | Claude reasons about confounds and states the claim's ceiling honestly | R `DeclareDesign` — declare model / inquiry / data strategy / answer strategy, run Monte-Carlo diagnosis, read **coverage** (should be ≈.95), not just power; then `simr` for sample size. Only when new data will be collected *and* an effect claimed |
| **Statistical-consistency check of a draft** | Recompute reported numbers by hand, mark lower-confidence | R packages **statcheck** (recompute APA-style p values) + **scrutiny** (GRIM: is that mean possible given N) — `install.packages(c("statcheck","scrutiny"))` |
| **Grammar / style linting** | Claude's by-hand passes | ✅bundled `tools/en/lt_check.sh` (LanguageTool, offline) — `brew install languagetool pandoc`; optional LanguageTool n-gram data (~15 GB, auto-detected at `~/Corpora/lt-ngrams` or `$LT_NGRAMS`) adds statistical confusable-pair detection (affect/effect). Optional extras: **Harper** (offline, millisecond first pass on every save — editor plugin or CLI; LanguageTool stays the authoritative second pass) and, for Chinese, **autocorrect** (`brew install autocorrect`: full/half-width punctuation and CJK–Latin spacing) |
| **De-AI / voice checking** | Convergence-word + AI-syntax passes by hand | ✅bundled `tools/en/ai_style_diag.py` (percentiles vs a corpus you assemble — published papers only, never your own drafts) |
| **Traditional-Chinese-Taiwan** | Claude checks by hand | ✅bundled `tools/zh-tw/` (zero install): `zh_localize` (Taiwan terms), `zh_ai_style` (Chinese AI-tic), `voice_lint` (your voice rules). Official-term DB check = bring-your-own DB. |
| **PDF / typesetting** | Cleanest export + "layout still needs a pass" | Typst or Quarto/LaTeX with the venue's template and embedded fonts |

## Numeric pitfalls (check before trusting a number)

Two known traps that produce *wrong numbers with no warning*. A generated skill that
runs statistics locally must mention them.

- **scipy ≥ 1.17 `mannwhitneyu` with float32 input returns a wrong U and p, silently**
  (a regression introduced in 1.17.0; 1.16.x is unaffected; scipy issue #24777, still
  open at the time of writing). Pin `scipy<1.17` in the analysis environment, **and**
  cast inputs to float64 anyway as defense in depth — a collaborator's venv may not be
  pinned. Upgrading other packages can drag scipy up; assert the version after any
  environment change.
- **η² from `effectsize` on an `afex` / `Anova.mlm` object** — the overlapping-factor-
  name fix is unconfirmed; cross-check against the effect sizes `afex` reports itself.
  If they disagree, report neither until you know why.
- General rule: **suspiciously tidy numbers are a red flag** (an effect of exactly 0.5,
  exactly 2×, identical CIs across groups). That is usually a constant leaking from a
  broken pipeline, not a result — go back to the log and the exit code before it
  enters the draft.

## Principles for the installer
- **Privacy is non-negotiable in both modes:** unpublished drafts and raw data stay
  local. No cloud detectors, no public LLM uploads — that rule doesn't relax in full mode.
- **Corpus hygiene** (if you build a style baseline): the baseline holds **only other
  people's published papers**. Never mix in the author's own drafts/posters/co-authored
  work or admin junk — comparing the author's style against a baseline containing their
  own writing makes the de-AI diagnosis cancel itself out.
- **Don't over-install.** A cautious first-timer needs none of this. Suggest the single
  tool that unblocks the specific wall they hit, and stop.

> This kit deliberately does **not** ship the original author's private scripts,
> corpora, or server setup. Full mode here means "here's the *kind* of tool and why";
> the author's Claude helps them stand up their own, locally, if and when they want it.
