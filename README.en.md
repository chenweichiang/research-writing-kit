# Research Writing Kit · 研究寫作套件

**Version `v1.4.0`** (2026-08) · Project page: <https://course.interaction.tw/research-writing-kit/en/>

**中文版 → [README.md](README.md)**

> A method for writing **research papers and grant proposals** with an AI, and it
> **installs and customizes itself**. You do not need to understand AI or know how to
> configure anything. Hand the folder to your Claude. It asks you a few questions, then
> builds the tools that fit you.

**中文摘要：** 這是一套用 AI 協助寫研究論文與計畫提案的方法，會自己安裝、自己客製。在
Claude Code 裡打開這個資料夾，說「讀 CLAUDE.md，幫我設定」，你的 Claude 會先訪談你，再依
你的領域、語言與文風生成專屬的寫作 skill。完整中文說明見 [README.md](README.md)；安裝器是
`CLAUDE.md`，方法本體在 `method/`。

---

## What this is

This is not a template you paste in. It is a **method**, plus a small toolbox that installs itself. A few principles:

- **You own the ideas and the argument. The AI does the legwork**: finds literature, verifies citations, builds the argument skeleton, writes the draft, and checks its own work.
- **Skeleton before prose**: no squeezing a draft out of a blank page (that squeezing is where "AI flavour" comes from). Build the argument structure first, then write the words to fit it.
- **Never fabricates a citation**: every reference is really fetched and its direction of support confirmed. If it cannot be found, it is marked "unverified". No pretending.
- **Sounds like you**: when you write in your native language, the prose is matched to your own voice, not sanded down into generic AI prose.
- **Honesty built in**: effect sizes with confidence intervals (not just p-values), data stays on your computer, a de-AI pass before delivery, a clean second review.

---

## How to use it

In the end, this method runs in **Claude Code on your own computer**. That is what keeps your data local and lets the tools run.
Pick a starting point based on what you have right now:

### Case A | You already have Claude Code on your computer

1. **Get this folder**: it is a public repo, no login needed. If you have git:
   `git clone https://github.com/chenweichiang/research-writing-kit.git`.
   If you would rather not install git, click the green **Code → Download ZIP** button on the
   GitHub page and unzip it. The only downside is that you cannot update later with a
   one-line `git pull`. Put it anywhere you like.
2. **Open Claude Code inside the folder**: open a terminal, `cd` into the folder, type `claude`.
3. **Paste this sentence**:
   > **"Read CLAUDE.md and set me up."** (Chinese: 「讀 CLAUDE.md，幫我設定。」)

### Case B | You are on claude.ai in the browser and do not have Claude Code yet

Connect this repo to the web version of Claude (through the GitHub connector) and tell it
**"Read CLAUDE.md and set me up."** It will **walk you step by step through installing Claude
Code on your computer and moving the folder there** (details in
[`setup/WEB.md`](setup/WEB.md)). Once that is done, go back to **step 2 of Case A** above.

> ⚠️ Claude Code needs a **paid Claude plan** (Pro, Max, Team, or API billing). **A free
> claude.ai account will not work.** The web version of Claude will remind you of this
> before it starts the install.

---

### After setup, your Claude does three things
1. **Asks you a few questions**: what you write, in which language, where you submit, and whether you have past writing of your own it can learn your voice from.
2. **Generates your own tools**: from your answers, it customizes the skills ("co-author", "pre-submission check", and so on) and installs them into your
   Claude.
3. **Teaches you the few sentences you will actually use**, and then you can start.

### Day-to-day use
Open Claude Code in the folder where your paper lives and say what you want in ordinary language (you can also type `/skill-name` directly):

| You say | Claude does | Skill / tool |
|---------|-------------|--------------|
| **"Help me write this paper / proposal"** | Co-authoring: find literature, build the argument skeleton, write the draft, self-check | `/co-author` |
| **"Check this before I submit"** | Pre-submission quality and format check (five layers) | `/paper-review` |
| **"Collect the PDFs of everything I cite"** | Collect and verify the references | `/fetch-refs` |
| **"Do these citations really support what I wrote?"** | Sentence-by-sentence check against the PDF text for direction of support; authoritative DOI check | `/verify-citations` (plus a `citation-skeptic` second review) |
| **"Who cited this? Is there follow-up work I missed?"** | Citation snowballing: from one paper (or a whole bibliography), grow a list of what you should have read but have not | `/fetch-refs` → `tools/refs/snowball.py` |
| **"The reviews came back, help me respond"** | Point-by-point response: split the comments → decide each point → revision table → response letter → completeness check before delivery | `/rebuttal` → `tools/rebuttal/check_response.py` |
| **"I want to expand this short paper into a full journal article"** | Onboards the existing draft through a reverse inventory, and checks text recycling and the disclosure wording (expansion is reuse by nature) | `/co-author` Phase 0.5 |
| **"I want to submit somewhere else too, is that okay?"** | Checks the submission ledger to confirm the same manuscript is not under review elsewhere at the same time | `tools/submissions/check_submissions.py` |
| **"Will this figure still make sense printed in black and white?"** | Figure colour accessibility: colour-blindness simulation plus grayscale contrast, with simulated images for you to look at | `/paper-review` → `tools/figures/figure_a11y.py` |
| **"Don't make that mistake again" / "fixing A broke B"** | Document regression: turn a caught mistake into a standing check, rescan the whole project after every edit, block it if it comes back | `/doc-regress` → `tools/regress/regress.py` |
| **"Has anything I cite been retracted?"** | Retraction scan: the whole bibliography checked against Crossref and OpenAlex, rerun before every delivery | `tools/refs/retraction_scan.py` |
| **"This sentence has no citation. Does it hold up?"** | Uncited-claims scan: finds quantitative, causal, and superlative sentences with no citation; for each one, add a citation, point to your own data, or soften the wording | `tools/claims/uncited_claims_scan.py` |
| **"Am I saying more than my data supports?"** | Overclaim scan: finds *all / never / the only / proves / clearly* and their Chinese equivalents — the other half of the de-AI pass | `tools/claims/overclaim_lint.py` |
| **"Do the numbers in the draft match the analysis output?"** | Numbers ledger reconciliation: every number traced back to the computation that produced it; update the ledger before the draft, and the regression check blocks old values from coming back | `/doc-regress` §3.5 |
| **"Typeset this as a submission PDF" / "Chinese PDF"** | Typesets in the venue's template; a second-language draft is delivered together with its back-translation | `/build-pdf` |
| **"Which statements am I still missing before I submit?"** | The six submission statements: AI-use disclosure, ethics/IRB, data availability, CRediT author contributions, conflicts of interest, preregistration | `/co-author` Phase 6-2a, `/paper-review` item 7 |

> The default is the **simplest mode**: just Claude and the internet, nothing to install.
> When you really need stronger tools (local statistics, a reference library, language
> checks), add them one at a time.

---

## Privacy

- This repo contains only the **method and the tools**. It holds nobody's drafts or data.

## Licensing

- **Code** (`tools/`): MIT. Use it, change it, sell it; just keep the copyright notice ([`LICENSE`](LICENSE)).
- **Method and documents** (`method/`, `skills/`, `agents/`, `templates/`, `setup/`, the READMEs): CC BY 4.0. Rewrite, translate, teach, make your own version. **The only condition is attribution** ([`LICENSE-DOCS`](LICENSE-DOCS)).
- **Third-party word lists** (`data/academic-vocab/`): the kit ships two, AVL and ACL (free for research and educational use, with attribution). The AWL is CC BY-NC-ND; you fetch it yourself with `tools/vocab/fetch_awl.py`, and the kit never redistributes it. None of these lists are covered by either licence above.
- Citation format and details: [`NOTICE.md`](NOTICE.md).
- The method itself requires that **unpublished drafts and raw research data always stay on your own computer**. Never upload them to the cloud or to a public
  AI detector. The personal setup you generate (voice profile, venue notes, skeleton) is not collected back into this repo either
  (see `.gitignore`).

---

## What is in the folder (complete list)

| Path | Contents |
|------|----------|
| `CLAUDE.md` | **The installer**: your Claude reads this to interview you and generate your personal setup. |
| `NOTICE.md` | Sharing terms and third-party data licences. |
| `method/` | **The method itself**, four files: `PHILOSOPHY.md` (mindset), `IRON-RULES.md` (the non-negotiables), `WORKFLOW.md` (the full eight-phase pipeline), `ARGUMENTATION.md` (argument moves, used as an internal diagnostic). |
| `skills/` | Seven skill templates (table below). |
| `agents/` | Two subagent templates (table below). |
| `tools/` | Sixteen local scripts plus helper files and templates (table below); documented in `tools/README.md`. |
| `templates/` | Four blank files: `VOICE_PROFILE.template.md` (voice profile), `venue-notes.template.md` (venue notes), `skeleton.template.md` (argument skeleton), `voice_rules.template.json` (hard voice rules). |
| `data/academic-vocab/` | Two open academic word lists shipped with the kit (`avl_core_words.tsv`, `acl_collocations.tsv`); the third, `awl_families.tsv`, is generated on your machine by `tools/vocab/fetch_awl.py`. The wording layer of the pre-submission check uses them as anchors, not for automatic replacement. Licences in `NOTICE.md`. |
| `examples/skeleton.example.md` | A filled-in skeleton so Claude has a concrete reference. |
| `setup/` | `LITE.md` (zero-install mode), `TOOLS.md` (optional tools and the degradation map), `INTERVIEW.md` (interview wording), `WEB.md` (starting from claude.ai in the browser), `addons/zh-tw/README.md` (Traditional Chinese, Taiwan localization add-on). |

### The seven skills

Once installed, each one triggers either by saying what you want or by typing `/name`.

| skill | What it does | Tools it uses |
|-------|--------------|---------------|
| `co-author` | Collaborative writing from scratch (papers and proposals): skeleton → verification → drafting → pre-delivery gates. Also handles rewriting an existing draft, resubmitting elsewhere, and expanding a short paper | The three pre-delivery scans (retraction / uncited claims / regression), `check_submissions.py`, the two subagents |
| `paper-review` | Five-layer pre-submission check: mechanical → wording → language → logic and reviewer's view → delivery completeness. Checks only; never rewrites the draft | The three Chinese tools, `lt_check.sh`, `ai_style_diag.py`, `figure_a11y.py`, `uncited_claims_scan.py`, `overclaim_lint.py`, (optional) R `statcheck` and `scrutiny` |
| `fetch-refs` | Collects the PDFs for a bibliography, confirms each file really matches its entry, files them with a manifest. Includes citation snowballing | `snowball.py`, online APIs |
| `verify-citations` | Sentence-by-sentence check against the PDF: is the citation supported by the source, and in the right direction. Authoritative DOI check. Retraction scan | `retraction_scan.py`, `citation-skeptic` second review, (optional) MinerU |
| `rebuttal` | Response to reviewers: split the points → decide each → carry out the revisions → response letter → completeness check | `check_response.py` plus three templates, `de-cadencing-scholar`, (optional) `latexdiff` |
| `doc-regress` | Turns a caught mistake into a standing check; numbers ledger; dead-rule health check | `regress.py`, `dead_rule_check.py` plus two templates |
| `build-pdf` | Typesets a PDF in the venue's template; a second-language draft is delivered together with its back-translation; Traditional Chinese uses a Typst recipe | Typst, or Quarto / LaTeX |

### The two subagents

| agent | What it does | When it is sent in |
|-------|--------------|--------------------|
| `de-cadencing-scholar` | A native-speaker scholar's pass over an English draft: picks out the rhythm marks that make it "obviously AI-polished" and rewrites them (six tics; the sixth is overclaiming) | Before an English draft is delivered; before a response letter is delivered |
| `citation-skeptic` | A calibrated second review of any citation flagged as "possibly wrong": assumes the citation is correct, and keeps the charge only if the PDF contradicts it word for word | When `verify-citations` raises a flag |

### Bundled tools (`tools/`, all of them)

| File | Purpose | Extra to install |
|------|---------|------------------|
| `common/md_prose.py` | Shared module: strips markdown / LaTeX layout syntax (frontmatter, tables, comments, code) and keeps only the prose. All four style tools depend on it. Not run directly | — |
| `zh-tw/zh_localize.py` | Mainland-vs-Taiwan term check and 台/臺 consistency (the two variant characters for "Tai"); report only, no rewriting | none |
| `zh-tw/zh_ai_style.py` | Chinese AI syntax fingerprint: dashes, rule-of-three lists, convergence words, sentence-length rhythm; can be compared against your own hand-written corpus | none |
| `zh-tw/voice_lint.py` | Your own hard voice rules (reads `voice_rules.json`); a gate before delivery, and it does not pass until clean | none |
| `en/lt_check.sh` | English grammar plus US/UK spelling consistency (offline LanguageTool); if n-gram data is present, confused-word detection is added automatically | `brew install languagetool pandoc` |
| `en/lt_strip_noprose.lua` | The pandoc filter `lt_check.sh` uses to strip non-prose before checking; not run directly | (comes with pandoc) |
| `en/ai_style_diag.py` | English AI fingerprint: percentiles against a corpus of published papers in your field; automatically excludes your own drafts and template files so they do not contaminate the baseline | Your own corpus; reading PDFs needs `pdftotext` (`brew install poppler`) |
| `figures/figure_a11y.py` | Figure colour accessibility: three colour-blindness simulations plus grayscale contrast; writes the simulated images for visual inspection | `pip install numpy pillow` (PDF figures also need `pymupdf`) |
| `refs/snowball.py` | Citation snowballing: who cited this, what it cites, related work; aggregates and ranks across several seeds | none (needs internet) |
| `refs/retraction_scan.py` | Retraction scan: a `.bib` or a DOI list checked against Crossref update relations and OpenAlex `is_retracted`, two sources; entries without a DOI are listed separately and not counted as scanned | none (needs internet) |
| `claims/uncited_claims_scan.py` | Quantitative / causal / superlative claims with no citation (`.md`, `.tex`, `.qmd`; English and Chinese); after you decide each one, an exemption note can be added | none |
| `claims/overclaim_lint.py` | Overclaim candidates in four categories (absolute / intensifier / evidence-strength / superlative), English and Traditional Chinese. **Report-only** — you judge each one against your evidence | none |
| `regress/regress.py` | Document regression: scans the whole project by the project's `regress.json`; built-in rules for dangling citations, personal data, leftover to-dos, old values coming back, and missing attribution; project rules go in `--extra my_rules.py` | none |
| `regress/dead_rule_check.py` | Rule health check: which rules can never fire again (their anchor text has been edited away) | none |
| `regress/rules.template.json`, `regress/numbers-ledger.template.md` | Blank templates for the regression config and the numbers ledger | — |
| `rebuttal/check_response.py` | Response-letter completeness: is every point answered, was every promised change really made, does every declined point carry evidence | none |
| `rebuttal/points.template.tsv`, `revisions.template.tsv`, `response-letter.template.md` | Templates for the reviewer-point table, the revision table, and the response letter | — |
| `submissions/check_submissions.py` | Duplicate-submission guard plus a submission status overview (the same manuscript must not be under review in two places at once) | none |
| `submissions/SUBMISSIONS.template.tsv` | Submission ledger template | — |
| `vocab/fetch_awl.py` | Downloads Coxhead's AWL from the official VUW pages and writes `awl_families.tsv` locally; the list is not shipped because of its ND (no-derivatives) term | none (needs internet) |

---

## What appears on your computer after install

The installer (`CLAUDE.md`) asks whether you want this "for this paper only, or for everything", and then:

| Item | Where | Notes |
|------|-------|-------|
| Seven skills | `~/.claude/skills/<name>/SKILL.md` (global) or `.claude/skills/` in your paper folder (single project) | **Rewritten from your answers**, not copied as-is; your field, language, venues, and mode are filled in |
| Two subagents | `~/.claude/agents/` or the project's `.claude/agents/` | Installed only if you write English or verify citations |
| A new section in your `CLAUDE.md` | `~/.claude/CLAUDE.md` or the project's `CLAUDE.md` | Records your field, language, venues, mode (lite / full), where the voice profile lives, and **the path to the kit (`KIT PATH`)**. This is the only place on the machine that records it; if you move the kit, you change one line |
| `voice-samples/` | Your project or home folder | **Holds only writing you wrote yourself** (created only if you provided past writing); the style tools' `--authored` flag points here, never at a folder that mixes in AI drafts |
| `VOICE_PROFILE.md`, `voice_rules.json` | Same place | The voice description and hard rules extracted from your past writing; `voice_lint.py` reads the latter |

Optional tools you have not installed are written into the generated skills as "use only if installed". They are never assumed to exist.

---

## What grows in your paper project

These are **your** files (in your paper folder, not in this repo). Keep them under version control together with the draft.

| File | Created by | Purpose |
|------|------------|---------|
| `skeleton.md` | `co-author` | The argument skeleton, the single source of truth; `## Progress` is written back at the end of each phase, and a new session reads it first |
| `venue-notes.md` | `co-author` | The target venue's current format, word limits, review norms, AI-disclosure policy, and preprint policy |
| `search-log.md` | `co-author` | Search log: which databases, query strings, dates, inclusion and exclusion. When a reviewer asks "why did you miss X", you can answer |
| `ADJUDICATED.md` | `co-author` / `paper-review` / `doc-regress` | Settled items: the list of "looks wrong, was checked, is actually right", so later checks do not raise them again |
| Reference PDF folder plus manifest | `fetch-refs` | Named `NN [Author Year] Title.pdf`; the manifest records what was found, what was not, the verification level (verified / LOW-CONFIDENCE), and self-citation flags |
| `snowball.csv` | `snowball.py` | Snowballing results (file name is configurable) |
| `regress.json`, `my_rules.py` (optional) | `doc-regress` | Regression config and project-specific rules; versioned with the draft |
| Numbers ledger (from `numbers-ledger.template.md`) | `doc-regress` / `co-author` Phase 3 | Every number in the draft traced to the computation that produced it; rerun the analysis → update the ledger → then edit the draft |
| `rebuttal/points.tsv`, `rebuttal/revisions.tsv`, `rebuttal/response-letter.md` | `rebuttal` | Reviewer points, revision table, response letter |
| `<figure>_a11y/` (`protan.png`, `deutan.png`, `tritan.png`, `grayscale.png`) | `figure_a11y.py` | Colour-blindness and grayscale simulations. **Open them and look.** The numbers are evidence, not the verdict |
| JSON reports from the retraction and uncited-claims scans (optional) | `retraction_scan.py --out`, `uncited_claims_scan.py --json` | For CI or for the record; normally the terminal output is enough |
| Back-translation plus two PDFs | `co-author` / `build-pdf` | The sign-off point for a second-language draft: the original PDF and the back-translation PDF are delivered as a pair |
| `SUBMISSIONS.tsv` | `check_submissions.py` | **Lives one level above all your paper projects** (one ledger for everything; the `SUBMISSIONS_TSV` environment variable points to it). A duplicate submission cannot be seen from inside a single project folder |

> This repo's `.gitignore` excludes `VOICE_PROFILE.md`, `venue-notes.md`, and `skeleton.md` so that **nobody's personal setup flows back into the kit**. In your own paper project, these files should be versioned together with the draft.

---

## External programs and services it uses (complete map)

> One-sentence version: **Claude Code is enough to start**. Everything else is "nice to
> have", and Claude suggests installing it only when you actually need it, one at a time.

### Required

| Tool | Purpose | How to get it |
|------|---------|---------------|
| **Claude Code** | Runs the whole method: interviews you, finds literature, builds the skeleton, writes the draft, checks its own work | [claude.com/claude-code](https://claude.com/claude-code) (needs a paid Claude plan: Pro, Max, Team, or API billing) |
| **Python 3** | Runs the bundled local checking tools | macOS: install the Xcode Command Line Tools first (`xcode-select --install`) or `brew install python`; most Linux distributions ship it; Windows: download the installer from python.org |
| **git** | Downloads and updates this repo (`git clone` / `git pull`) | On macOS it comes with the Xcode Command Line Tools; or use Download ZIP on the GitHub page (no one-line updates afterwards) |

### Optional local programs (which feature uses it, how to install)

| Program | Used where | How to install |
|---------|------------|----------------|
| **LanguageTool** plus **pandoc** | `lt_check.sh` English grammar (`paper-review` layer 3) | `brew install languagetool pandoc`; n-gram data is optional, put it in `$LT_NGRAMS` |
| **poppler** (`pdftotext`) | `ai_style_diag.py` reading PDFs; `verify-citations` reading reference PDFs | `brew install poppler` |
| **numpy**, **Pillow** (plus **pymupdf**) | `figure_a11y.py` | `pip install numpy pillow` (add `pymupdf` for PDF figures) |
| **MinerU** | Extracting clean text from scanned or Chinese PDFs (`verify-citations`) | `uv tool install mineru` |
| **R** plus `statcheck`, `scrutiny` | `paper-review` layer 1: recomputes p-values and runs GRIM on reported means (falls back to manual arithmetic if not installed) | Install R, then `install.packages(c("statcheck","scrutiny"))` |
| **R** plus `DeclareDesign` | `co-author` Phase 3.5 design diagnosis (looks at coverage, not only power) | `install.packages("DeclareDesign")` |
| **R** or **Python** statistics | Local statistical analysis: mixed models (`lme4` / `afex`), ordinal Likert (`ordinal::clmm`), post-hoc comparisons and effect sizes; routing rules in `setup/TOOLS.md` | Data stays on your computer throughout; numerical pitfalls in `setup/TOOLS.md` |
| **R** Bayesian, three routes | Hierarchical models you can write as a formula → `brms`; a "no difference" conclusion needs BF01 → `BayesFactor`; **discrete latent variables / mixture models / custom samplers / porting old JAGS models → `nimble`** (BUGS syntax; Stan cannot express discrete parameters). All three must report priors and convergence diagnostics | `install.packages(c("brms","BayesFactor","nimble"))`; `brms` also needs CmdStan or rstan |
| **Harper** | A millisecond first pass on English grammar (reports on save; LanguageTool is still the main tool) | Editor plugin or CLI, offline |
| **autocorrect** | Tidies Chinese full-width / half-width punctuation and CJK-Latin spacing automatically | `brew install autocorrect` |
| **Typst**, or **Quarto** / **LaTeX** | `build-pdf` typesetting; Traditional Chinese uses the Typst recipe (`setup/addons/zh-tw/`) | Choose by the venue's official template; `latexdiff` gives `rebuttal` its revision diff |
| **Jupyter** | Rerunnable analysis notebooks | `pip install jupyterlab` |
| Your institution's library **VPN** | Full text behind paywalls (`fetch-refs`) | Depends on your institution |
| Local **RAG** | Semantic search over your own reference library (which paper, which page) | `setup/TOOLS.md` gives the direction, not an implementation |

### Online services Claude and the tools call (free, no install, no account)

| Service | Used where | What is sent |
|---------|------------|--------------|
| **Crossref** | `retraction_scan.py` (retraction update relations), `verify-citations` DOI and bibliographic checks | DOI only |
| **OpenAlex** | `retraction_scan.py` (`is_retracted`), `snowball.py`, title lookup for entries without a DOI | DOI or title |
| **Semantic Scholar** | `snowball.py` fallback, citation lookups | DOI or title |
| **Unpaywall**, **arXiv** | `fetch-refs` fetching open-access PDFs | DOI |

**Manuscript text is never sent.** The online services only receive bibliographic data such as DOIs, titles, and author names. Unpublished drafts and raw research data always stay on your computer.

### Deliberately not shipped

The original author's toolchain has a few more pieces, but they are **not shipped**. Not forgotten: they fall outside "papers and proposals", or they are tied to one specific machine.

- **present-video** (the presentation-video pipeline: TTS with a cloned voice, Whisper transcription checks, local image generation): outside the scope of papers and proposals, and every stage needs a self-hosted model.
- **paper-healthcheck**: checks whether the author's **own local toolchain** is broken or has upstream updates. It does not check a manuscript, and it knows nothing about what your toolchain looks like.
- **contradiction_scan / backfill_from_lit** ("does anyone in my library contradict me" / "fill missing PDFs from the local library first"): need a full-text index of a local reference library and a local LLM for polarity judgments; `setup/TOOLS.md` gives the direction, not an implementation.
- **zh_term_check** (checks every translated term in a draft against the NAER terminology database, 樂詞網): needs the 樂詞網 database, which you would have to download and build yourself (bring your own). For a single term, just ask your Claude to look it up online.

---

## For advanced users
Every skill is a plain-Markdown `SKILL.md`, which Claude Code recognises automatically. To mount
one as a global skill by hand, copy or symlink `skills/<name>/` into `~/.claude/skills/`. The two
subagent templates in `agents/` work the same way: mount them in `~/.claude/agents/` (or the
project's `.claude/agents/`). Even so, let the install flow in `CLAUDE.md` customize them for you
rather than copying the originals as-is.

Two principles. **A clean second review gets only file paths** (not the main conversation's drafting
history, or the blind spots are shared). **The final review and the citation second review are judgment
work: use your strongest model, and do not downgrade to save money.** The mechanical scans (retraction,
uncited claims, regression) need no model; just run the scripts.

---

## Version history

- **v1.4.0** (2026-08-29): **The de-AI pass gets its missing half — removing overclaims.**
  Adds `tools/claims/overclaim_lint.py` (English + Traditional Chinese; four categories:
  absolute, intensifier, evidence-strength, superlative; **report-only, never edits**).
  Why: strip the convergence words and the cadence but leave *proves*, *all*, *the only*,
  *clearly*, and the draft still reads as machine-written — and unlike a rhythm tic, an
  unsupported absolute is a **substantive** fault. A reviewer who reads "this proves" under
  an n=12 study stops trusting everything else in the paper. Every hit is judged by hand:
  evidence carries it → keep (a real 0/72 or 100% result *is* data, and softening data is
  its own dishonesty); it doesn't → converge. **Quoted source text and object-language in
  quotation marks are out of scope.** Wired into `/co-author` Phase 5 and 6-3 (rerun every
  delivery — each round of new prose grows the absolutes back), `/paper-review` Layers 1
  and 3, and `method/WORKFLOW.md` Phases 5 and 6; `de-cadencing-scholar` goes from five
  tics to six.

- **v1.3.0** (2026-08-25): **Adds the gates that are easiest to skip before delivery and hardest to fix
  afterwards.** New seventh skill `doc-regress` (a caught mistake becomes a standing check, so fixing A
  no longer breaks B; rules are versioned with the draft; includes the numbers ledger template
  `tools/regress/numbers-ledger.template.md`, plus `regress.py` and `dead_rule_check.py`). New
  `tools/refs/retraction_scan.py` (retraction scan, Crossref plus OpenAlex, **rerun on every delivery**:
  retractions keep happening, and clean last time does not mean clean this time) and
  `tools/claims/uncited_claims_scan.py` (quantitative / causal / superlative claims with no citation;
  citation checking only looks at sentences that carry a citation marker, so these are its blind spot).
  Co-authoring gains the iron rule "the file is the single source of truth" (progress written back
  after every phase; after context compaction, reread the file before acting), a Phase 1A search log,
  Phase 3.5 design diagnosis (judge coverage, not only power; adding participants to a biased design
  makes it worse; a single-group pre/post design needs a control or is downgraded to non-causal), a
  Phase 6 pre-delivery checklist (retractions / uncited claims / numbers ledger reconciliation / figure
  provenance / the six submission statements / final review with `ADJUDICATED.md` attached), and
  Phase 7 "update the ledger before the draft". The pre-submission check gains Step 0 (read
  `ADJUDICATED.md`; settled items are not raised again), four qualitative items and reporting
  guidelines (COREQ / SRQR / TREND / CONSORT / PRISMA), search strategy, the six statements, and the
  uncited-claims scan. Citation verification gains clause-level judgments, quote grounding, severity
  weighting, and retractions. Reference collection gains three rules. The response to reviewers gets
  the English de-cadencing pass. The Traditional Chinese add-on gains Typst. The four style tools
  (Chinese and English) get a batch of measurement bug fixes. Method documents updated to match: the
  workflow is now 8 phases; the iron rules gain statistical details (ART only for continuous DVs,
  single-item Likert goes to an ordinal model, SESOI declared at design time, the three-route Bayesian
  split); every argument move gains a "when not to use it" and the craft of empirical papers;
  `setup/TOOLS.md` gains numerical pitfalls and Harper / autocorrect. The README becomes a complete
  inventory: the seven skills with their names and trigger phrases, every file in `tools/`, what
  appears on your computer after install, what grows in a paper project, and which external programs
  and online services are used by what and what data they receive. The AWL is no longer shipped;
  `tools/vocab/fetch_awl.py` fetches it instead.
- **v1.2.0** (2026-08-24): **Fixes a batch of measurement bugs that produced wrong numbers.** The style
  diagnosis tools (four, Chinese and English) were counting markdown layout syntax as prose
  punctuation: YAML frontmatter and table separator rows counted as dashes, text inside HTML comments
  counted as body text, the semicolons in pandoc multi-key citations counted as style, and bold
  headings broke sentence splitting so two or three sentences were glued into one. Measured on a real
  submission: mean sentence length 44.22 words (99th percentile) → 26.52 words (53rd percentile).
  **Editing to the old numbers would have broken sentences that were fine.** The stripping rules were
  factored out into `tools/common/md_prose.py`, shared by Chinese and English. Also fixed: the
  Semantic Scholar fallback in `snowball.py` never fired (on hitting the daily quota, the first call
  returned 429 and the whole seed was skipped).
  New: the `rebuttal` skill (point-by-point decisions, revision table, completeness check), the
  submission ledger with duplicate-submission guard, and the figure colour accessibility check;
  co-authoring gains Phase 8 "after acceptance" (proofs / copyright / dissemination), text-recycling
  disclosure, and a preprint policy check.
- **v1.1.0** (2026-08): The pre-submission check adds statistical recomputation (statcheck recomputes
  p-values, GRIM checks whether reported means are possible; enabled only if R is installed, otherwise
  falls back to manual arithmetic). New citation snowballing tool `tools/refs/snowball.py` (zero
  install). Citation verification supports scanned and Chinese PDFs (optional MinerU). English grammar
  checking can automatically add n-gram confused-word detection (optional). New `agents/` with two
  subagent templates: the de-AI rhythm pass before English delivery, and the citation second review.
- **v1.0.0** (2026-07): First release: the method itself, five skill templates, Chinese and English
  checking tools, the self-install flow.
