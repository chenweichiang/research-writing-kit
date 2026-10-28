# Research Writing Kit · 研究寫作套件

[![version](https://img.shields.io/github/v/tag/chenweichiang/research-writing-kit?label=version&sort=semver&color=blue)](https://github.com/chenweichiang/research-writing-kit/tags) [![updated](https://img.shields.io/github/last-commit/chenweichiang/research-writing-kit/main?label=updated&color=green)](https://github.com/chenweichiang/research-writing-kit/commits/main) [![code MIT](https://img.shields.io/badge/code-MIT-lightgrey)](LICENSE) [![docs CC BY 4.0](https://img.shields.io/badge/docs-CC%20BY%204.0-lightgrey)](LICENSE-DOCS)

**Version `v1.11.2`** (2026-10-28) · Project page: <https://course.interaction.tw/research-writing-kit/en/>

**中文版 → [README.md](README.md)**

> A method for writing research papers and grant proposals with an AI, and it
> installs and customizes itself. You do not need to understand AI or know how to
> configure anything. Hand the folder to your Claude. It asks you a few questions, then
> builds the tools that fit you.

**中文摘要：** 這是一套用 AI 協助寫研究論文與計畫提案的方法，會自己安裝、自己客製。在
Claude Code 裡打開這個資料夾，說「讀 CLAUDE.md，幫我設定」，你的 Claude 會先訪談你，再依
你的領域、語言與目標期刊生成專屬的寫作 skill。完整中文說明見 [README.md](README.md)；安裝器是
`CLAUDE.md`，方法本體在 `method/`。

---

## What this is

This is a writing method, plus a small toolbox that installs itself: once installed, your Claude follows the method to find literature, build the argument, draft the prose and check its own work. A few principles:

- **You own the ideas and the argument. The AI does the legwork**: finds literature, verifies citations, builds the argument skeleton, writes the draft, and checks its own work.
- **Skeleton before prose**: no squeezing a draft out of a blank page (that squeezing is where "AI flavour" comes from). Build the argument structure first, then write the words to fit it.
- **Never fabricates a citation**: every reference is really fetched and its direction of support confirmed. If it cannot be found, it is marked "unverified". No pretending.
- **Papers sound like your field, letters sound like you**: papers, grant proposals and applications are measured against published papers in your field, so each language feature of the draft sits inside the range real papers use. They are neither sanded into generic AI prose nor pushed into one person's idiolect. Your own voice is kept for letters and personal statements.
- **Honesty built in**: effect sizes with confidence intervals (not just p-values), no handing data to third-party services, a de-AI pass before delivery, a clean second review.

---

## How to use it

In the end, this method runs in Claude Code on your own computer. That is what keeps your files on your own disk and lets the tools run.
Pick a starting point based on what you have right now:

### Case A | You already have Claude Code on your computer

1. **Get this folder**: it is a public repo, no login needed. If you have git:
   `git clone https://github.com/chenweichiang/research-writing-kit.git`.
   If you would rather not install git, click the green "Code → Download ZIP" button on the
   GitHub page and unzip it. The only downside is that you cannot update later with a
   one-line `git pull`. Put it anywhere you like.
2. **Open Claude Code inside the folder**: open a terminal, `cd` into the folder, type `claude`.
3. **Paste this sentence**:
   > **"Read CLAUDE.md and set me up."** (Chinese: 「讀 CLAUDE.md，幫我設定。」)

### Case B | You are on claude.ai in the browser and do not have Claude Code yet

Connect this repo to the web version of Claude (through the GitHub connector) and tell it
"Read CLAUDE.md and set me up." It will walk you step by step through installing Claude
Code on your computer and moving the folder there (details in
[`setup/WEB.md`](setup/WEB.md)). Once that is done, go back to step 2 of Case A above.

> ⚠️ Claude Code needs a paid Claude plan (Pro, Max, Team, or API billing). **A free
> claude.ai account will not work.** The web version of Claude will remind you of this
> before it starts the install.

---

### After setup, your Claude does three things
1. Asks you a few questions: what you write, in which language, where you submit, whether you can collect published papers from your field as a baseline, and whether you have letters or statements of your own it can learn your voice from.
2. Generates your own tools: from your answers, it customizes the skills ("co-author", "pre-submission check", and so on) and installs them into your
   Claude.
3. Teaches you the few sentences you will actually use, and then you can start.

### Day-to-day use
Open Claude Code in the folder where your paper lives and say what you want in ordinary language (you can also type `/skill-name` directly):

| You say | Claude does | Skill / tool |
|---------|-------------|--------------|
| "Help me write this paper / proposal" | Co-authoring: find literature, build the argument skeleton, write the draft, self-check | `/co-author` |
| "This reads like a translation / not like a paper in my field" | Native polish: first measures which language features of the draft sit outside the range of same-field papers; the editor subagent returns a change list only, and you decide on each item. Changed numbers, citations or terms are blocked | `/co-author` Phase 5.5 → `tools/register/register_profile.py`, `polish_check.py` |
| "Check this before I submit" | Pre-submission quality and format check (five layers) | `/paper-review` |
| "Collect the PDFs of everything I cite" | Collect and verify the references | `/fetch-refs` |
| "Do these citations really support what I wrote?" | Sentence-by-sentence check against the PDF text for direction of support; authoritative DOI check | `/verify-citations` (plus a `citation-skeptic` second review) |
| "Who cited this? Is there follow-up work I missed?" | Citation snowballing: from one paper (or a whole bibliography), grow a list of what you should have read but have not | `/fetch-refs` → `tools/refs/snowball.py` |
| "The reviews came back, help me respond" | Point-by-point response: split the comments → decide each point → revision table → response letter → completeness check before delivery | `/rebuttal` → `tools/rebuttal/check_response.py` |
| "I want to expand this short paper into a full journal article" | Onboards the existing draft through a reverse inventory, and checks text recycling and the disclosure wording (expansion is reuse by nature) | `/co-author` Phase 0.5 |
| "I want to submit somewhere else too, is that okay?" | Checks the submission ledger to confirm the same manuscript is not under review elsewhere at the same time | `tools/submissions/check_submissions.py` |
| "Will this figure still make sense printed in black and white?" | Figure colour accessibility: colour-blindness simulation plus grayscale contrast, with simulated images for you to look at | `/paper-review` → `tools/figures/figure_a11y.py` |
| "Don't make that mistake again" / "fixing A broke B" | Document regression: turn a caught mistake into a standing check, rescan the whole project after every edit, block it if it comes back | `/doc-regress` → `tools/regress/regress.py` |
| "Has anything I cite been retracted?" | Retraction scan: the whole bibliography checked against Crossref and OpenAlex, rerun before every delivery | `tools/refs/retraction_scan.py` |
| "This sentence has no citation. Does it hold up?" | Uncited-claims scan: finds quantitative, causal, and superlative sentences with no citation; for each one, add a citation, point to your own data, or soften the wording | `tools/claims/uncited_claims_scan.py` |
| "Am I saying more than my data supports?" | Overclaim scan: finds *all / never / the only / proves / clearly* and their Chinese equivalents (the other half of the de-AI pass) | `tools/claims/overclaim_lint.py` |
| "Do the numbers in the draft match the analysis output?" | Numbers ledger reconciliation: every number traced back to the computation that produced it; update the ledger before the draft, and the regression check blocks old values from coming back | `/doc-regress` §3.5 |
| "Typeset this as a submission PDF" / "Chinese PDF" | Typesets in the venue's template; a second-language draft is delivered together with its back-translation | `/build-pdf` |
| "Which statements am I still missing before I submit?" | The six submission statements: AI-use disclosure, ethics/IRB, data availability, CRediT author contributions, conflicts of interest, preregistration | `/co-author` Phase 6-2a, `/paper-review` item 7 |
| "Run everything before I send it" | Full polish: citations → proofreading → native polish → de-AI → overclaims → localization → regression → a new versioned PDF, in that order, one report at the end | `/co-author` "Full polish" |
| "Does this journal allow AI-written text? Can I use an AI-made figure?" | Publishers' generative-AI rules side by side (dated; re-read the original for every manuscript); if the venue forbids AI drafting you choose before any drafting starts, and the statement says what actually happened | `method/AI_DISCLOSURE.md`, `/co-author` Phase 1.5 |
| "Is this topic worth a full paper?" | Contribution gate: a clean reviewer judges as the venue's editor and picks one of five: write the full paper / shrink to a short paper or poster / change venue / collect more data first / not worth writing | `/co-author` Phase 1.5, `clean-reviewer` |
| "My co-author wrote this; my rewrite has to trace back to theirs" | Never edit the original, write changes as an edit layer; every sentence of the new draft compared with the original and the co-author's replies, untraceable methods and numbers flagged red | `method/COLLABORATION.md` → `tools/collab/source_trace.py` |
| "I'm over the page limit / word count" | Read how the limit is counted, find the pinned boundaries, budget per section, cut from light to heavy and report every cut; never shrink figures or trade evidence for pages | `method/COMPRESSION.md` |
| "Which version is this? Which file do I send?" | Version = times sent out . content . wording; the `VERSION` file is the only source, the changelog is written before the build, the delivery folder holds one version | `method/VERSIONING.md` → `tools/versioning/version_check.py` |
| "Are the figure numbers in the PDF right? Is that figure shrunk too far?" | Mechanical check of figures and tables in the typeset PDF: numbering gaps, mentions without captions, overflow past the column or page, text too small to read | `/paper-review` 1f → `tools/figures/figure_check.py` |
| "Which references do I still have to download?" / "I've downloaded them, file them" | The missing list after subtracting your own library; the PDFs in your downloads folder matched, verified, filed, and the folder tidied | `/fetch-refs` → `tools/refs/missing_refs.py`, `inbox_ingest.py` |
| "How many more review rounds? Are we going in circles?" | Review-round ledger: each round's fatal and major findings split into new and repeated; two rounds with nothing new means stop | `/paper-review` → `tools/review/review_rounds.py` |
| "Where should I send this?" | Venue comparison table: at least three candidates (one a safe fallback), every cell from this year's official page or the index with the date it was read, "not found" where it could not be filled, acceptance rates and review times never estimated; one recommendation underneath, the choice is yours | `/co-author` Phase 1.5 |
| "My co-author sent the Word file back without tracked changes" | Compares it with the version you sent, paragraph by paragraph: what was changed, added, deleted or moved, ready to carry back into the source one entry at a time | `method/COLLABORATION.md` → `tools/collab/docx_diff.py` |
| "I need a second coder and an agreement figure" | Turns the codebook and the responses into one offline coding page for the coder; the export goes back into the coding tables and gets per-code kappa. The page holds participants' answers and never goes online | `method/COLLABORATION.md` → `tools/collab/coding_pack.py` |
| "Can I submit this? What is still missing?" / "What time is the deadline here?" | Readiness verdict: re-read the official page, convert the deadline to your timezone, measure each hard requirement, scoring by a clean reviewer; reported as hard requirements, blockers, what only you can do, and the timeline | `/submit` → `tools/submit/deadline.py` |
| "Make the Word version" / "Does the format match the template?" / "Is the anonymization clean?" | Builds the Word file from source and compares it back, counts words with Word, diffs the format against the template, checks anonymity; your to-dos go in a separate file, never inside the delivered one | `/submit` → `tools/submit/` |
| "I submitted it, wrap it up" | Finds the confirmation e-mail, writes the submission record, marks the ledger submitted, puts the decision date in the calendar, bumps the major version and tags it | `/submit` section 6 |

> The default is the simplest mode: just Claude and the internet, nothing to install.
> When you really need stronger tools (local statistics, a reference library, language
> checks), add them one at a time.

---

## Privacy

- This repo contains only the method and the tools. It holds nobody's drafts or data.
- The bundled check tools and the statistics run on your computer. Online lookups send only bibliographic data such as DOIs, titles, and author names (see "External programs and services it uses").
- The method itself requires that **unpublished drafts and raw research data are not handed to third-party online services**: no public AI detectors, no pasting into other cloud AI tools.
- **Claude Code itself is a cloud model.** Whatever files it reads, drafts and data included, are sent to Anthropic for processing. If you work with participant data or confidential material, first check your institution's and ethics board's rules and your Claude account's data settings. Data those rules keep in-house should not be opened in Claude Code.
- The personal setup you generate (voice profile, venue notes, skeleton) is not collected back into this repo (see `.gitignore`).

## Licensing

- **Code** (`tools/`): MIT. Free to use, modify and sell, provided the copyright notice is kept ([`LICENSE`](LICENSE)).
- **Method and documents** (`method/`, `skills/`, `agents/`, `templates/`, `setup/`, the READMEs): CC BY 4.0. Rewrite, translate, teach, make your own version. The only condition is attribution ([`LICENSE-DOCS`](LICENSE-DOCS)).
- **Third-party word lists** (`data/academic-vocab/`): the kit ships two, AVL and ACL (free for research and educational use, with attribution). The AWL is CC BY-NC-ND; you fetch it yourself with `tools/vocab/fetch_awl.py`, and the kit never redistributes it. None of these lists are covered by either licence above.
- Citation format and details: [`NOTICE.md`](NOTICE.md).

---

## What is in the folder (complete list)

| Path | Contents |
|------|----------|
| `CLAUDE.md` | The installer: your Claude reads this to interview you and generate your personal setup. |
| `NOTICE.md` | Sharing terms and third-party data licences. |
| `method/` | The method itself, eleven files: `PHILOSOPHY.md` (mindset), `IRON-RULES.md` (the non-negotiables), `WORKFLOW.md` (the full pipeline, Phase 0 to 8, including 5.5 native polish), `ARGUMENTATION.md` (argument moves, used as an internal diagnostic), `RIGOR_PROCESS.md` (a thirteen-stage rigorous process from literature to reporting), `METHOD_DECISION.md` (the method-decision procedure and reporting guidelines), `METHOD_CARDS.md` (38 research-method cards with a decision index and condition-triggered warnings), `VERSIONING.md` (version numbers, changelog, delivery folders), `COLLABORATION.md` (co-authored manuscripts and multi-team proposals), `COMPRESSION.md` (cutting to a page or word limit), `AI_DISCLOSURE.md` (publishers' generative-AI rules and how to write the statement). |
| `skills/` | Eight skill templates (table below). |
| `agents/` | Five subagent templates (table below). |
| `tools/` | Forty-two local scripts plus shared modules, helper files and templates (table below); documented in `tools/README.md`. |
| `templates/` | Four blank files: `VOICE_PROFILE.template.md` (voice profile, for letters and statements), `venue-notes.template.md` (venue notes), `skeleton.template.md` (argument skeleton), `voice_rules.template.json` (hard voice rules). |
| `data/academic-vocab/` | Two open academic word lists shipped with the kit (`avl_core_words.tsv`, `acl_collocations.tsv`); the third, `awl_families.tsv`, is generated on your machine by `tools/vocab/fetch_awl.py`. The wording layer of the pre-submission check uses them as anchors; it never replaces words automatically. Licences in `NOTICE.md`. |
| `examples/skeleton.example.md` | A filled-in skeleton so Claude has a concrete reference. |
| `setup/` | `LITE.md` (zero-install mode), `TOOLS.md` (optional tools and the degradation map), `INTERVIEW.md` (interview wording), `WEB.md` (starting from claude.ai in the browser), `addons/zh-tw/README.md` (Traditional Chinese, Taiwan localization add-on). |

### The eight skills

Once installed, each one triggers either by saying what you want or by typing `/name`.

| skill | What it does | Tools it uses |
|-------|--------------|---------------|
| `co-author` | Collaborative writing from scratch (papers and proposals): skeleton → verification → drafting → pre-delivery gates. Also handles rewriting an existing draft, resubmitting elsewhere, expanding a short paper, and a co-author's manuscript; a one-line "full polish" | The three pre-delivery scans (retraction / uncited claims / regression), `check_submissions.py`, Phase 5.5 native polish (`register_profile.py`, `polish_check.py`, the two editor subagents), `clean-reviewer` for the contribution gate and the clean final review, `source_trace.py`, `docx_diff.py`, `coding_pack.py`, `figure_check.py`, `version_check.py` |
| `paper-review` | Five-layer pre-submission check: mechanical → wording → language → logic and reviewer's view → delivery completeness. Checks only; never rewrites the draft. Logs each round and says when to stop reviewing | The three Chinese tools (`voice_lint.py --paper`), `zh_gloss_scan.py --en`, `lt_check.sh`, `ai_style_diag.py`, `figure_a11y.py`, `figure_check.py`, `uncited_claims_scan.py`, `overclaim_lint.py`, `review_rounds.py`, `clean-reviewer` reviewer simulation (layer 4), (optional) R `statcheck` and `scrutiny` |
| `fetch-refs` | Collects the PDFs for a bibliography, confirms each file really matches its entry, files them with a manifest. Lists what you still have to download by hand and files your downloads. Includes citation snowballing | `pdf_fetch.py` (layered retrieval with failure classes), `missing_refs.py`, `inbox_ingest.py`, `snowball.py`, online APIs |
| `verify-citations` | Sentence-by-sentence check against the PDF: is the citation supported by the source, and in the right direction. Authoritative DOI check. Retraction scan | `retraction_scan.py`, `citation-skeptic` second review, (optional) MinerU |
| `rebuttal` | Response to reviewers: split the points → decide each → carry out the revisions → response letter → completeness check | `check_response.py` plus three templates, `clean-reviewer` drafts the verdict table, revised passages go through Phase 5.5 native polish, `de-cadencing-scholar`, (optional) `latexdiff` |
| `doc-regress` | Turns a caught mistake into a standing check; numbers ledger; dead-rule health check | `regress.py`, `dead_rule_check.py` plus two templates |
| `build-pdf` | Typesets a PDF in the venue's template; a second-language draft is delivered together with its back-translation; Traditional Chinese uses a Typst recipe | Typst, or Quarto / LaTeX |
| `submit` | The last mile: a readiness verdict (re-read the official page, convert the deadline to your timezone, scoring by `clean-reviewer`, never self-scored), building the Word file from source and comparing it back, counting words the venue's way, a format diff against the official template, a double-blind anonymization check, the upload package and field list; after sending, the confirmation e-mail, the submission record, the ledger and a major version bump with a tag | `deadline.py`, `docx_roundtrip.py`, `word_count.sh` (plus `wordcount_approx.py`), `template_diff.py`, `anon_check.py`, `version_check.py`, `check_submissions.py`, `clean-reviewer` |

### The five subagents

| agent | What it does | When it is sent in |
|-------|--------------|--------------------|
| `clean-reviewer` | Clean-context final review: carries none of the drafting history and reads the manuscript, a reviewer-comment verdict table or a page as a reviewer would, to find its real weaknesses. It needs the strongest model tier at the highest effort; since Claude Code 2.1.292 an Agent call can also pass the effort, but pinning it in the template's frontmatter sets it once instead of relying on every call to remember it | `co-author` Phase 6 final review, `paper-review` layer 4 reviewer simulation, `rebuttal` verdict table |
| `en-native-editor` | Native-English academic editor: moves features that sit outside the field's register range back into it, and fixes the surface transfer errors common to Chinese-L1 authors (articles, prepositions, collocations, tense). Returns a change list only and never edits the draft | `co-author` Phase 5.5 on English drafts (before de-cadencing) |
| `zh-tw-native-editor` | Native Taiwan academic-Chinese editor (zh-TW addon): the same register-range yardstick, for translationese, over-split sentences and non-Taiwan usage. Returns a change list only | `co-author` Phase 5.5 on Chinese drafts |
| `de-cadencing-scholar` | A native-speaker scholar's pass over an English draft: picks out the rhythm marks that make it "obviously AI-polished" and rewrites them (seven tics; the sixth is overclaiming, the seventh stock openings). Re-measures register afterwards so no feature is pushed out of the range | Before an English draft is delivered (after native polish); before a response letter is delivered |
| `citation-skeptic` | A calibrated second review of any citation flagged as "possibly wrong": assumes the citation is correct, and keeps the charge only if the PDF contradicts it word for word | When `verify-citations` raises a flag |

### Bundled tools (`tools/`, all of them)

| File | Purpose | Extra to install |
|------|---------|------------------|
| `common/md_prose.py` | Shared module: strips markdown / LaTeX layout syntax (frontmatter, tables, comments, code) and keeps only the prose. All four style tools depend on it. Not run directly | — |
| `zh-tw/zh_localize.py` | Mainland-vs-Taiwan term check and 台/臺 consistency (the two variant characters for "Tai"); report only, no rewriting | none |
| `zh-tw/zh_ai_style.py` | Chinese AI syntax fingerprint: dashes, rule-of-three lists, convergence words, sentence-length rhythm, density of the 「並非…而是」(not-X-but-Y) frame, and a list of sentences over 120 characters; can be compared against your own hand-written corpus | none |
| `zh-tw/voice_lint.py` | Your own hard voice rules (reads `voice_rules.json`); a gate before delivery, and it does not pass until clean. Also flags sentence-form headings and stock closers, and lists AI stock-phrase candidates for you to judge. For papers, proposals and applications add `--paper`, which switches to the template's paper rules (for example, the semicolons journals use are not blocked) | none |
| `zh-tw/zh_register.py` | Chinese register profile: 52 features (self-reference, translationese, linking words, metadiscourse, stance, punctuation, sentence length) against a corpus of same-field journal papers you assemble, with p10 / median / p90 for each. A scale, not a detector | your own corpus (30+ papers) |
| `zh-tw/zh_gloss_scan.py` | Parenthetical-gloss inventory: every aside of 12+ characters that is not a citation or cross-reference, so you can decide which become defining sentences, which stay, which go; `--en` lists English glosses after Chinese terms (repeats flagged as already glossed) and bare English words in Chinese prose, ranked | none |
| `zh-tw/zh_tw_terms.py` | Loader and matcher for the Taiwan-Mandarin term table, used by `zh_localize.py`; not run directly | — |
| `en/lt_check.sh` | English grammar plus US/UK spelling consistency (offline LanguageTool); if n-gram data is present, confused-word detection is added automatically | `brew install languagetool pandoc` |
| `en/lt_strip_noprose.lua` | The pandoc filter `lt_check.sh` uses to strip non-prose before checking; not run directly | (comes with pandoc) |
| `en/ai_style_diag.py` | English AI fingerprint: percentiles against a corpus of published papers in your field, including LLM convergence-word density with the words that carry it; automatically excludes your own drafts and template files so they do not contaminate the baseline | Your own corpus; reading PDFs needs `pdftotext` (`brew install poppler`) |
| `en/en_slop_terms.tsv` | The English LLM convergence-word list `ai_style_diag.py` reads (162 terms from slop-forensics, minus words HCI papers use anyway); not run directly | — |
| `refs/pdf_fetch.py` | Fetches reference PDFs in three layers: open-access resolvers (adds Europe PMC / CORE / OpenAIRE) → a browser-like HTTP client (`curl_cffi`) → your own Chrome on a persistent profile, using your own access. Publisher pages that turn away scripts (ACM / Wiley / SAGE / AIP / Elsevier) open only in that last layer. The browser layer pauses between items, handles at most 100 per run and never clicks a "verify you are human" check; publishers' terms allow single articles for your own research, not bulk downloading. Misses are classified `PAYWALL` / `CAPTCHA` / `NO-LINK`. Entries without a DOI are read from the arXiv `eprint`, then resolved by exact title match on arXiv / OpenAlex; only books go back to you | `pip install curl_cffi patchright` (without them: stdlib + OA sources) |
| `en/bundle_diag.py` | Lexical-bundle overuse diagnostic (English and Traditional Chinese): LLM prose leans on the same fixed collocations, so this measures their density and lists the hits | none |
| `en/metadiscourse_en.py` | English metadiscourse measurement (Hyland's framework): density per category, hedges, boosters, attitude markers and the rest, with p10 / median / p90 and a high/low direction; `--groups` compares against one venue, `--json` for scripts. A scale, not a detector: it shows where your distribution sits, it does not decide who wrote something | none |
| `en/biber_diag.py` | English syntactic-feature comparison (Biber tagger) against your field's corpus, to see which features you lean on and in which direction; `--groups` compares against one venue, `--json` for scripts; runs in a separate, optional environment that nothing else in the kit needs | `pip install pybiber spacy polars` plus a language model (give it its own virtualenv and record its interpreter as `BIBER_PYTHON`) |
| `register/register_profile.py` | The native-polish deviation list (Chinese and English): which features sit outside the p10–p90 band of same-field papers, which way to move them, and bounds per line range so an editor does not overshoot to the other end | your own corpus; the English syntax layer also needs the `biber_diag.py` environment (or run `--no-biber`) |
| `register/polish_check.py` | Checks an editor's change list before it touches the draft: numbers, citations, quotations and locked terms unchanged, growth within the word budget, no new forbidden forms, no register feature moving the wrong way; writes back with `--apply` only when everything passes. The change list is read as data, never executed | none |
| `figures/figure_a11y.py` | Figure colour accessibility: three colour-blindness simulations plus grayscale contrast; writes the simulated images for visual inspection | `pip install numpy pillow` (PDF figures also need `pymupdf`) |
| `figures/figure_check.py` | Figures and tables in the typeset PDF: caption numbering gaps and duplicates, mentions without a caption (across line breaks and plural forms), figures past the text column (yellow) or off the page (red), small text in vector figures, rasters shrunk until their text is unreadable (font size estimated from the effective dpi); writes a PNG crop of each figure for a visual pass | `pip install pymupdf` |
| `refs/snowball.py` | Citation snowballing: who cited this, what it cites, related work; aggregates and ranks across several seeds | none (needs internet) |
| `refs/retraction_scan.py` | Retraction scan: a `.bib` or a DOI list checked against Crossref update relations and OpenAlex `is_retracted`, two sources; entries without a DOI are listed separately and not counted as scanned | none (needs internet) |
| `refs/lit_map.py` | Literature map: who a batch of same-topic papers co-cite, ranked within the batch (global citation counts are ignored), as candidates for "the classics here"; the result still needs a human call | none (network) |
| `refs/missing_refs.py` | The missing list: bibliography entries with no PDF yet, minus what your own library already holds (year + first-author surname + title similarity), with DOI / URL / ISBN for the rest. Files already in the folder are re-verified too; doubtful ones go into `_check_present.md`, flagged only, never moved or deleted (`--no-check-present` turns this off) | none (content checks need `pdftotext`) |
| `refs/inbox_ingest.py` | Files the PDFs you downloaded by hand: matched to missing entries, content verified, renamed and filed, optionally copied into your library; only filed sources go to the Trash, nothing is deleted | content checks need `pdftotext` (`brew install poppler`) |
| `refs/refs_common.py` | Shared module: BibTeX parsing, the three-gate match, PDF content verification for the two tools above. Text is NFKC-normalised and ligatures rejoined before matching, Chinese titles are compared as strings, and an arXiv stamp on the first page more than two years later than the bibliography year downgrades the match to `LOW-CONFIDENCE`; not run directly | none (with OpenCC installed, Simplified text is converted to Traditional before comparing) |
| `claims/uncited_claims_scan.py` | Quantitative / causal / superlative claims with no citation (`.md`, `.tex`, `.qmd`; English and Chinese); after you decide each one, an exemption note can be added | none |
| `claims/overclaim_lint.py` | Overclaim candidates in four categories (absolute / intensifier / evidence-strength / superlative), English and Traditional Chinese. Two more: nobody-did-it claims ("to the best of our knowledge", "no prior research"; reported even with a citation nearby, because only a search trail can carry them) and official documents (guidelines, regulations, policies) cited without a year. Report-only; you judge each one against your evidence | none |
| `method/method_decision_check.py` | Format gate for a method-decision memo: were comparable studies actually compared, does every claim have a method that carries it. It does not judge whether the method is right | none |
| `method/analysis_plan_check.py` | Gate for the pre-data-collection plan: analysis methods, sample-size justification, deviation log and the rest. This is the one stage you cannot add afterwards | none |
| `method/tea_second_opinion.py` | A second opinion on statistics: give it your data and a study-design spec and it picks and runs the matching test, to check against the one you chose | Tea (Python 3.10-3.13, pins older numpy/pandas, give it its own virtualenv) |
| `regress/regress.py` | Document regression: scans the whole project by the project's `regress.json`; built-in rules for dangling citations, personal data, leftover to-dos, old values coming back, and missing attribution; project rules go in `--extra my_rules.py` | none |
| `regress/dead_rule_check.py` | Rule health check, three ways: which rules never actually run their body (an empty setting makes them return at the guard), which are written but never registered in `RULES`, and which call a name the file never defines | none |
| `regress/rules.template.json`, `regress/numbers-ledger.template.md` | Blank templates for the regression config and the numbers ledger | — |
| `rebuttal/check_response.py` | Response-letter completeness: is every point answered, was every promised change really made, does every declined point carry evidence | none |
| `rebuttal/points.template.tsv`, `revisions.template.tsv`, `response-letter.template.md` | Templates for the reviewer-point table, the revision table, and the response letter | — |
| `submissions/check_submissions.py` | Duplicate-submission guard plus a submission status overview (the same manuscript must not be under review in two places at once) | none |
| `submissions/style_reaudit.py` | After a style-measurement rule changes, re-runs the fingerprint tools over every manuscript on the submissions ledger, so older drafts do not stay judged by the old standard | none |
| `submissions/SUBMISSIONS.template.tsv` | Submission ledger template | — |
| `review/review_rounds.py`, `review/review-rounds.template.tsv` | Review-round ledger: fatal and major findings per round split into new and repeated; re-raising an adjudicated item without new evidence is blocked; two rounds with no new fatal or major finding recommends stopping | none |
| `collab/source_trace.py` | Sentence-by-sentence trace of a rewritten co-authored draft back to the original, the co-author's replies or the proposal; untraceable numbers, method words and site facts red, new literature claims orange | none (`.docx` needs `python-docx`, PDF needs `pdftotext`) |
| `collab/docx_diff.py` | For a Word file a co-author returns without tracked changes: compares it with the one you sent and lists every modification, insertion, deletion and move, paragraph by paragraph (table cells, headers, footers and footnotes included), and reports any tracked changes and comments left in it. `--out` writes a list to read, `--json` one to carry back into the source entry by entry | `pip install python-docx` |
| `collab/coding_pack.py` | Second-coder pack: a codebook plus response CSVs become one offline web page (one response at a time, number keys tick codes, one CSV exported at the end); `import` turns the export back into the project's 0/1 coding tables, `score` gives per-code Cohen's kappa, PABAK, prevalence and a bootstrap CI. The page holds participants' answers: open it locally or hand it to the coder directly | none for `build` and `import`; `score` needs `numpy` |
| `versioning/version_check.py` | Pre-delivery version check: `VERSION`, the top CHANGELOG section, one version in the delivery folder, the version in PDF metadata, no version in the submitted text, no reused tag. Fails when `VERSION` changed but the delivered files were not rebuilt, warns when a source file is newer than them, and prints the delivered files' absolute paths to quote in the report | none (PDF checks need poppler) |
| `submit/deadline.py` | Converts a deadline to your timezone (AoE, PST / PDT, `UTC+8`, IANA names; daylight saving decided by the date) and prints the time left and a suggested submit time 24 hours earlier | none |
| `submit/docx_roundtrip.py` | Turns a docx built from source back into text and compares it sentence by sentence with the source (in source but missing from the docx, in the docx but not in the source), then scans for leftovers: unresolved `[@key]`, `??`, TODO, 【待確認】, unreplaced `{{`, Word reference errors, runs of empty paragraphs | `brew install pandoc` (the empty-paragraph check also needs `python-docx`) |
| `submit/word_count.sh` | Asks Microsoft Word itself for the word count (many venues set the limit by Word's count), optionally with a PDF from Word. macOS + Word only; elsewhere it falls back to `wordcount_approx.py` and exits 3 to mark the number as approximate | macOS + Microsoft Word |
| `submit/wordcount_approx.py` | Approximate count (CJK characters + Latin words + digit runs); can differ from Word by ten percent or more, so it is always reported as approximate. `word_count.sh` uses it when Word is not available | reading `.docx` needs `pandoc` |
| `submit/template_diff.py` | Compares a manuscript docx with the official template docx, property by property: paper size, margins, header and footer distance, default fonts (Latin and East Asian separately), size, line spacing, space before and after, first-line indent, alignment, and styles the manuscript uses that the template lacks. Compares style definitions only; formatting set by hand on paragraphs needs a visual check | `pip install python-docx` |
| `submit/anon_check.py` | Double-blind anonymization check: the docx creator and last-modified-by, authors of tracked changes and comments, names and affiliations in the body, headers and footers, hyperlinks, PDF Author and XMP, and the EXIF (author, GPS) of embedded images and image files. Self-disclosure such as "our previous work" is listed in orange for you to judge, and it lists the areas it actually checked | image EXIF needs `exiftool`, PDFs need `pymupdf` |
| `vocab/fetch_awl.py` | Downloads Coxhead's AWL from the official VUW pages and writes `awl_families.tsv` locally; the list is not shipped because of its ND (no-derivatives) term | none (needs internet) |

---

## What appears on your computer after install

The installer (`CLAUDE.md`) asks whether you want this "for this paper only, or for everything", and then:

| Item | Where | Notes |
|------|-------|-------|
| Eight skills | `~/.claude/skills/<name>/SKILL.md` (global) or `.claude/skills/` in your paper folder (single project) | Rewritten from your answers; the originals are templates only. Your field, language, venues, and mode are filled in |
| Five subagents | `~/.claude/agents/` or the project's `.claude/agents/` | `clean-reviewer` for everyone; `citation-skeptic` if you verify citations; `en-native-editor` and `de-cadencing-scholar` if you write English; `zh-tw-native-editor` with the zh-TW addon. The installer adds the strongest model you have to each frontmatter |
| A new section in your `CLAUDE.md` | `~/.claude/CLAUDE.md` or the project's `CLAUDE.md` | Records your field, language, venues, mode (lite / full), the register corpus path and its journal folders, where the voice profile lives, and the path to the kit (`KIT PATH`). This is the only place on the machine that records it; if you move the kit, you change one line |
| `voice-samples/` | Your project or home folder | **Holds only writing you wrote yourself** (created only if you provided past writing); the style tools' `--authored` flag points here, never at a folder that mixes in AI drafts |
| Register corpus folder (`<corpus>/<journal>/*.txt`) | Where you choose | **Only other people's published papers** (full mode only), as plain text, one folder per journal; `register_profile.py` uses it as the yardstick |
| `VOICE_PROFILE.md`, `voice_rules.json` | Same place | The voice description and hard rules extracted from your letters and statements, used for letters, cover letters and statements; `voice_lint.py` reads the latter (add `--paper` for papers) |

Optional tools you have not installed are written into the generated skills as "use only if installed". They are never assumed to exist.

---

## What grows in your paper project

These are your files. They live in your paper folder; this repo never holds them. Keep them under version control together with the draft.

| File | Created by | Purpose |
|------|------------|---------|
| `skeleton.md` | `co-author` | The argument skeleton, the single source of truth; `## Progress` is written back at the end of each phase, and a new session reads it first |
| `venue-notes.md` | `co-author` | The target venue's current format, word limits, review norms, AI-disclosure policy, and preprint policy |
| `search-log.md` | `co-author` | Search log: which databases, query strings, dates, inclusion and exclusion. When a reviewer asks "why did you miss X", you can answer |
| `ADJUDICATED.md` | `co-author` / `paper-review` / `doc-regress` | Settled items: the list of "looks wrong, was checked, is actually right", so later checks do not raise them again |
| Reference PDF folder plus manifest | `fetch-refs` | Filed by hand as `NN [Author Year] Title.pdf`; `pdf_fetch.py` and `inbox_ingest.py` write `refs-pdf/<citekey>.pdf`; the manifest records what was found, what was not, the verification level (verified / LOW-CONFIDENCE), and self-citation flags |
| `snowball.csv` | `snowball.py` | Snowballing results (file name is configurable) |
| `regress.json`, `my_rules.py` (optional) | `doc-regress` | Regression config and project-specific rules; versioned with the draft |
| Numbers ledger (from `numbers-ledger.template.md`) | `doc-regress` / `co-author` Phase 3 | Every number in the draft traced to the computation that produced it; rerun the analysis → update the ledger → then edit the draft |
| `rebuttal/points.tsv`, `rebuttal/revisions.tsv`, `rebuttal/response-letter.md` | `rebuttal` | Reviewer points, revision table, response letter |
| `<figure>_a11y/` (`protan.png`, `deutan.png`, `tritan.png`, `grayscale.png`) | `figure_a11y.py` | Colour-blindness and grayscale simulations. Open them and look; the numbers are evidence and you make the call |
| JSON reports from the retraction and uncited-claims scans (optional) | `retraction_scan.py --out`, `uncited_claims_scan.py --json` | For CI or for the record; normally the terminal output is enough |
| Back-translation plus two PDFs | `co-author` / `build-pdf` | The sign-off point for a second-language draft: the original PDF and the back-translation PDF are delivered as a pair |
| `refs-pdf/_missing.md`, `_missing.tsv`, `_inbox_log.tsv` | `missing_refs.py`, `inbox_ingest.py` | The list of references for you to download (your library already subtracted); the record of filed downloads |
| `VERSION`, `CHANGELOG.md`, `latest/`, `versions/vX.Y.Z/` | `co-author` (`method/VERSIONING.md`) | The single source of the version, what changed in each version and why, the folder holding only the current delivery, a snapshot per version |
| `docs/received/YYYYMMDD-<source>/` | `co-author` (`method/COLLABORATION.md`) | Files a co-author sent, archived under their original names and never edited |
| `docs/source-trace.md` | `source_trace.py --report` | Sentence-by-sentence trace report for a co-authored draft |
| `docs/review-rounds.tsv` | `paper-review` | Review-round ledger; `review_rounds.py` reads it to judge convergence |
| `figures/ai-generation-log.md` | `co-author` | Engine, version, seed and full prompt of every AI-generated figure; captions and the statement are written from it |
| `SUBMISSIONS.tsv` | `check_submissions.py` | Lives one level above all your paper projects (one ledger for everything; the `SUBMISSIONS_TSV` environment variable points to it). A duplicate submission cannot be seen from inside a single project folder |

> This repo's `.gitignore` excludes `VOICE_PROFILE.md`, `venue-notes.md`, and `skeleton.md` so that nobody's personal setup flows back into the kit. In your own paper project, these files should be versioned together with the draft.

---

## External programs and services it uses (complete map)

> One-sentence version: Claude Code is enough to start. Everything else is "nice to
> have", and Claude suggests installing it only when you actually need it, one at a time.

### Required

| Tool | Purpose | How to get it |
|------|---------|---------------|
| Claude Code | Runs the whole method: interviews you, finds literature, builds the skeleton, writes the draft, checks its own work | [claude.com/claude-code](https://claude.com/claude-code) (needs a paid Claude plan: Pro, Max, Team, or API billing) |
| Python 3 | Runs the bundled local checking tools | macOS: install the Xcode Command Line Tools first (`xcode-select --install`) or `brew install python`; most Linux distributions ship it; Windows: download the installer from python.org |
| git | Downloads and updates this repo (`git clone` / `git pull`) | On macOS it comes with the Xcode Command Line Tools; or use Download ZIP on the GitHub page (no one-line updates afterwards) |

### Optional local programs (which feature uses it, how to install)

| Program | Used where | How to install |
|---------|------------|----------------|
| LanguageTool plus pandoc | `lt_check.sh` English grammar (`paper-review` layer 3); pandoc also builds the Word file in `submit` and lets `docx_roundtrip.py` and `wordcount_approx.py` read docx | `brew install languagetool pandoc`; n-gram data is optional, put it in `$LT_NGRAMS` |
| poppler (`pdftotext`, `pdfinfo`) | `ai_style_diag.py` reading PDFs; `verify-citations` reading reference PDFs; content checks in `missing_refs.py` and `inbox_ingest.py`; `source_trace.py` reading PDFs; `version_check.py` | `brew install poppler` |
| numpy, Pillow (plus pymupdf) | `figure_a11y.py` | `pip install numpy pillow` (add `pymupdf` for PDF figures) |
| pymupdf | `figure_check.py`, figures in the typeset PDF; `anon_check.py` reading PDFs | `pip install pymupdf` |
| python-docx | `source_trace.py` reading a co-author's Word file, `docx_diff.py` comparing a returned Word file, `template_diff.py` comparing against the template | `pip install python-docx` |
| exiftool | `anon_check.py` reading image EXIF (author, GPS); without it those areas are reported as not checked | `brew install exiftool` |
| Microsoft Word (macOS) | `word_count.sh` counting words the way Word does; without it the count is approximate | your own Office licence |
| numpy | `coding_pack.py score`, agreement and bootstrap CIs | `pip install numpy` |
| OpenCC | `missing_refs.py` and `inbox_ingest.py` convert Simplified to Traditional before comparing Chinese titles (compared as-is without it) | `pip install opencc-python-reimplemented` |
| MinerU | Extracting clean text from scanned or Chinese PDFs (`verify-citations`) | `uv tool install mineru`; in 4.x the batch command is `mineru-kit parse`; leave `--remote` off (it sends the file to MinerU's cloud) |
| R plus `statcheck`, `scrutiny` | `paper-review` layer 1: recomputes p-values and runs GRIM on reported means (falls back to manual arithmetic if not installed) | Install R, then `install.packages(c("statcheck","scrutiny"))` |
| R plus `DeclareDesign` | `co-author` Phase 3.5 design diagnosis (looks at coverage, not only power) | `install.packages("DeclareDesign")` |
| R or Python statistics | Local statistical analysis: mixed models (`lme4` / `afex`), ordinal Likert (`ordinal::clmm`), post-hoc comparisons and effect sizes; routing rules in `setup/TOOLS.md` | The computation runs on your computer; numerical pitfalls in `setup/TOOLS.md` |
| R Bayesian, three routes | Hierarchical models you can write as a formula → `brms`; a "no difference" conclusion needs BF01 → `BayesFactor`; discrete latent variables / mixture models / custom samplers / porting old JAGS models → `nimble` (BUGS syntax; Stan cannot express discrete parameters). All three must report priors and convergence diagnostics | `install.packages(c("brms","BayesFactor","nimble"))`; `brms` also needs CmdStan or rstan |
| Harper | A millisecond first pass on English grammar (reports on save; LanguageTool is still the main tool) | Editor plugin or CLI, offline |
| autocorrect | Tidies Chinese full-width / half-width punctuation and CJK-Latin spacing automatically | `brew install autocorrect` |
| Typst, or Quarto / LaTeX | `build-pdf` typesetting; Traditional Chinese uses the Typst recipe (`setup/addons/zh-tw/`) | Choose by the venue's official template; `latexdiff` gives `rebuttal` its revision diff |
| Jupyter | Rerunnable analysis notebooks | `pip install jupyterlab` |
| Your institution's library VPN | Full text behind paywalls (`fetch-refs`) | Depends on your institution |
| Local RAG | Semantic search over your own reference library (which paper, which page) | `setup/TOOLS.md` gives the direction, not an implementation |

### Online services Claude and the tools call (free, no install, no account)

| Service | Used where | What is sent |
|---------|------------|--------------|
| Crossref | `retraction_scan.py` (retraction update relations), `verify-citations` DOI and bibliographic checks | DOI only |
| OpenAlex | `retraction_scan.py` (`is_retracted`), `snowball.py`, `lit_map.py`, title lookup for entries without a DOI (optional free key `OPENALEX_API_KEY`: $0.10/day of usage without it, $1/day with it; a title search costs $0.001, a single DOI lookup is free) | DOI or title |
| Semantic Scholar | `snowball.py` fallback, citation lookups | DOI or title |
| Unpaywall, arXiv | `fetch-refs` fetching open-access PDFs | DOI |

The online services above receive only bibliographic data (DOIs, titles, author names). The one place manuscript text is sent is Claude Code itself (see "Privacy").

### Not included

A few things are left out on purpose, because they fall outside "papers and proposals" or depend on one specific machine or dataset:

- Producing a presentation video (script, voice-over, video assembly): outside the scope of papers and proposals, and every stage needs a self-hosted model.
- A reverse check ("does anyone in my library contradict me"): needs a full-text index of a local reference library and a local model for polarity judgments; `setup/TOOLS.md` gives the direction, without an implementation. The other half, "fill missing PDFs from my own library first", is included from v1.10.0 (`missing_refs.py --library`, matching on file names, no full-text index needed).
- The delegation table (which tier of subagent each step goes to): it is tied to a subscription plan and to this month's model names, and stops being true on a different plan or a later generation. The criteria are included (which steps are mechanical and can be downgraded, which are judgment work for your strongest model, stated in each skill and in the subagent templates); the model names are left out, because only you know which tiers you have.
- Checking every translated term in a draft against Taiwan's NAER terminology database (樂詞網): you would have to download and build that database yourself. For a single term, ask your Claude to look it up online.

---

## For advanced users
Every skill is a plain-Markdown `SKILL.md`, which Claude Code recognises automatically. To mount
one as a global skill by hand, copy or symlink `skills/<name>/` into `~/.claude/skills/`. The five
subagent templates in `agents/` work the same way: mount them in `~/.claude/agents/` (or the
project's `.claude/agents/`). Even so, let the install flow in `CLAUDE.md` customize them for you;
the originals are templates.

Two principles. A clean second review gets only file paths (never the main conversation's drafting
history, or the blind spots are shared). The final review and the citation second review are judgment
work: use your strongest model, and do not downgrade to save money. The mechanical scans (retraction,
uncited claims, regression) need no model; just run the scripts.

---

## Version history

What changed in each version is in [CHANGELOG.md](CHANGELOG.md).
