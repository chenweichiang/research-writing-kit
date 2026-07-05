# Full mode — optional local power-ups (graceful degradation map)

> None of this is required. Lite mode (`LITE.md`) does the whole method with just
> Claude + the web. Add these **one at a time, only when the author hits a real wall.**
> For each capability: what lite mode does, and the optional upgrade. A generated
> skill must gate every reference to these behind "if installed."
>
> 📦 **Already bundled in `tools/`** (no big install): the Chinese checkers
> (`zh_localize`, `zh_ai_style`, `voice_lint` — zero-install, Python stdlib) and the
> English `lt_check.sh` (needs `brew install languagetool pandoc`) + `ai_style_diag.py`
> (needs a corpus you assemble). Those rows below are marked ✅bundled. See `tools/README.md`.

| Capability | Lite (default, no install) | Full (optional upgrade) |
|-----------|----------------------------|--------------------------|
| **Find literature** | WebSearch + Semantic Scholar / OpenAlex / Crossref | + a local full-text RAG over PDFs you hold (semantic search "which paper, which page") |
| **Fetch reference PDFs** | Open-access resolvers (Unpaywall/arXiv/author pages) | + institutional/library access (e.g. a university VPN) for paywalled full texts |
| **Verify citations** | Claude reads OA source, checks direction | + a multi-agent adversarial pass over a local PDF library |
| **Statistics / analysis** | Honest description + simple summaries | R (mixed models, Bayesian) / Python / a persistent Jupyter kernel — data stays local |
| **Grammar / style linting** | Claude's by-hand passes | ✅bundled `tools/en/lt_check.sh` (LanguageTool, offline) — `brew install languagetool pandoc` |
| **De-AI / voice checking** | Convergence-word + AI-syntax passes by hand | ✅bundled `tools/en/ai_style_diag.py` (percentiles vs a corpus you assemble — published papers only, never your own drafts) |
| **Traditional-Chinese-Taiwan** | Claude checks by hand | ✅bundled `tools/zh-tw/` (zero install): `zh_localize` (Taiwan terms), `zh_ai_style` (Chinese AI-tic), `voice_lint` (your voice rules). Official-term DB check = bring-your-own DB. |
| **PDF / typesetting** | Cleanest export + "layout still needs a pass" | Typst or Quarto/LaTeX with the venue's template and embedded fonts |

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
