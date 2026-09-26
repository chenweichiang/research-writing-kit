# CLAUDE.md: Bootstrap Protocol for the Research Writing Kit

> You (Claude) are reading this because a human opened this kit in Claude and wants to
> set up an AI-assisted academic-writing workflow. **The workflow runs on the author's
> own machine, in Claude Code.** That's the only place it can read/write their files,
> run the tools, and keep drafts away from third-party services. If you are in **Claude Code**, install here.
> If you are on **claude.ai** (web/desktop) with this repo connected, the author is not
> yet where the work happens: your first job is to walk this (likely non-technical)
> person onto Claude Code (follow `setup/WEB.md`), optionally interviewing them first
> so they arrive ready. claude.ai is the on-ramp, not the destination.
> **This file is not the workflow. It is the installer.** Your job is to
> interview this person, then generate a *personalized* set of skills and a
> CLAUDE.md tailored to them, so that from now on their own Claude can help
> them write papers and proposals the way this method prescribes.
>
> The person is very likely **not technical** and may be new to AI tools.
> Be warm, concrete, and plain-spoken. Never dump jargon. One question at a time.

---

## What this kit is (say this to the human, in their language, in 3 sentences)

1. This is a *method* for writing research papers and grant proposals with an AI,
   plus a small toolkit that installs itself.
2. The human owns the ideas and the argument; Claude finds and verifies sources,
   helps structure the argument, writes the prose, and checks its own work.
3. Right now Claude will ask a few questions and then set up tools that fit
   *this person's* field, language and target journals: papers are checked against
   published papers in their field, and letters against their own voice.

---

## The method in one breath (so you know what you are installing)

The whole thing rests on five ideas. Read `method/PHILOSOPHY.md` and
`method/IRON-RULES.md` in full before generating anything.

- **Skeleton first.** Never write prose from a blank page. Build an argument
  skeleton (claim → move → evidence → so-what per node) first; prose is bound to it.
- **Division of labor.** Human decides *what to say* and gives final sign-off.
  Claude does the finding, verifying, structuring, drafting, and self-checking.
- **No fabricated citations, ever.** Every reference must be really fetched and
  its support direction verified. Unverifiable → mark `❓unverified`, never fake it.
- **Papers sound like their field; letters sound like the author.** A paper, grant
  proposal or application is measured against the register of published papers in the
  same field (the p10-p90 band, not the median), never sanded into generic "AI prose"
  and never pushed into one person's idiolect. The author's own voice is kept for
  letters, cover letters and personal statements.
- **Honesty tooling.** Effect sizes + CIs (not just p-values), no third-party uploads,
  de-AI the prose before delivery, and a clean second pass reviews the work.

---

## BOOTSTRAP: run these phases in order

### Phase 0: Where is the author running you? (check this first, silently)

- **Claude Code** (you can read/write local files and run shell commands) → you're in
  the right place. Continue to Phase A and install here.
- **claude.ai web/desktop** (a GitHub connector lets you *read* this repo, but you
  cannot write to their disk or run programs) → the author is **not yet where the work
  happens**. The whole method depends on a machine that can hold files and run the
  tools privately. That's Claude Code. Your job here is to **walk them onto Claude
  Code**: follow `setup/WEB.md`. You *may* run the Phase A interview first (the answers
  carry over so they arrive ready), but the actual install happens in Claude Code, not
  in the web app. Do not fake a file-writing install from the browser.

If you can't tell which you are, ask one plain line: "Are you using Claude in a terminal
or a code editor, or on the claude.ai website/app?"

### Phase A: Interview (ask in the human's language, one at a time)

Keep it friendly. These map directly to what you'll generate. Suggested wording
is in `setup/INTERVIEW.md`. Adapt it, don't read it robotically.

1. **What do you write?** (e.g. HCI papers, education research, humanities essays,
   grant proposals, a thesis), and roughly what field/discipline.
2. **What language do you write in?** (the language of the *final paper*, which may
   differ from the language you're talking to me in right now.)
3. **Where do you submit?** Any target venues/journals/funders you know of, or
   "not sure yet." (This drives the venue-format research later.)
4. **Can you collect published papers from your field or target journals?** These
   are *other people's* papers, the register baseline for papers and proposals. Full
   mode: 30 or more (ideally published before 2023), 30 from one journal to compare
   against that journal alone. Lite mode: name 2–3 papers from the target journal plus
   its author guidelines. (Minimums and wording in `setup/INTERVIEW.md`.)
   **4b. Do you have 2–4 pieces of your own writing** (letters, statements, bios) I
   could learn your voice from? Optional, and used only for letters and personal
   statements. It must be prose *you actually wrote yourself*, not AI-written.
5. **How much setup do you want today?**
   - **Simple / web-only** (recommended to start): works with just Claude + the
     web, zero installs. → you'll configure the *lite* path (`setup/LITE.md`).
   - **Full power** (optional, later): local citation tools, corpora, stats.
     → mention it exists (`setup/TOOLS.md`), but don't force it now.
6. **Do you want the Traditional-Chinese-Taiwan localization pack?** (Only if they
   write Chinese for a Taiwan audience: Taiwan-vs-mainland term checking, etc.
   → `setup/addons/zh-tw/`. Skip entirely otherwise.)

If the human answers vaguely, pick sensible defaults and say what you chose.
Do not block on perfect answers.

### Phase B: Build a voice profile (only if they gave you samples in 4b)

The voice profile is used for letters, cover letters, bios and personal statements.
Papers, proposals and applications follow the field's register (Phase B2), not the
voice profile. If they provided their own writing:
- 🔴 **Put the samples in a dedicated `voice-samples/` folder** (in their project or
  home), holding **only their own writing**, never AI/co-authored drafts. The
  style tools' `--authored` flag points *here*, not at the project folder (a project
  folder also holds AI drafts, which would poison the baseline under the same
  corpus-hygiene rule as the English style tool). Name their files plainly; the tools also
  auto-skip anything containing "草稿/draft/ai/claude/gpt" as a second guard.
- Read the samples. Extract *observable* habits into a filled-in copy of
  `templates/VOICE_PROFILE.template.md`: typical sentence length and rhythm,
  favored connectives, punctuation habits, register, words they reach for,
  words they never use. Quote 3–5 real phrases as anchors.
- **Describe patterns, don't invent a persona.** If you can't tell, say so.
- Encourage 2–4 samples for a fuller profile; if they gave one short piece, note the
  profile is thin and will sharpen as they add writing.
- Save it where their Claude will find it (see Phase C for location).

If they gave no samples: skip. Letters then aim for plain, direct prose.

### Phase B2: Set up the register baseline (from their answer to Q4)

- **Full mode, papers supplied:** convert each paper to plain text (`pdftotext` for
  text PDFs; scanned Chinese PDFs need OCR such as MinerU) and keep only the body. Put
  them in one folder per journal: `<corpus>/<journal>/*.txt`. Minimums the tools
  enforce: 30 papers for a baseline, and 30 in a journal's folder to compare against
  that journal alone (fewer falls back to the whole corpus, with a note); a draft
  needs 1000+ Han characters (Chinese) or 800+ words (English) to be profiled.
- **Corpus hygiene:** only other people's published papers, never the author's drafts
  or AI-assisted text. Prefer papers published before 2023. Record the corpus path in
  their CLAUDE.md (`ZH_CORPUS_DIR` for Chinese, `CORPUS_DIR` for English) and list the
  journal folder names, so the skills and agents can pass `--venue`.
- **English Biber features** need the optional `pybiber` setup (`setup/TOOLS.md`). If
  it lives in its own Python environment, record that interpreter as `BIBER_PYTHON`.
  Without it, `tools/register/register_profile.py --no-biber` still gives the
  metadiscourse half.
- Run `tools/register/register_profile.py --selftest` once, then one real profile on
  an existing draft, and show the author the deviation list so they see what it does.
- **Lite mode, or no corpus yet:** record the target journal's author-guidelines link
  and the 2–3 sample papers they named. The skills then compare by reading
  (`setup/LITE.md`) and must say so.

### Phase C: Generate their personalized setup

> **This phase runs in Claude Code.** If the author is on claude.ai, you should have
> sent them to `setup/WEB.md` in Phase 0 to get onto Claude Code first. Come back here
> once they're in a terminal inside the cloned kit.

Decide *where* to install based on how they answered Q5 and their comfort:

- **Global (all their projects):** `~/.claude/skills/<skill>/SKILL.md` and
  append to `~/.claude/CLAUDE.md`. Use this if they want it everywhere.
- **This-project only:** a `.claude/skills/` folder inside whatever paper folder
  they're working in. Safer default for a cautious first-timer.

Ask which they prefer in plain terms ("just for this paper, or for everything
you write?"). Then, generate (**do not copy verbatim**) from the templates in
`skills/`, filling in:

- their **field** and **target venue(s)** (into each skill's venue/format step),
- their **writing language** and the matching language toolchain (lite or full),
- their **register corpus** path and journal folders (or, in lite mode, the sample
  papers and guidelines to read), and their **voice profile** path for letters (or
  "no voice profile"),
- the **degraded vs full** tool references per `setup/TOOLS.md` (never reference a
  tool they haven't installed as if it exists, so gate it behind "if installed"),
- the **subagent templates** from `agents/` (into `~/.claude/agents/` or the
  project's `.claude/agents/`, matching the skills' scope):
  - `clean-reviewer` for everyone (the clean final review and reviewer simulation);
  - `citation-skeptic` for anyone who verifies citations;
  - `en-native-editor` and `de-cadencing-scholar` for authors who write English;
  - `zh-tw-native-editor` only with the zh-TW addon.

  Fill in the placeholders (`<KIT>`, `<CORPUS_DIR>`, `<ZH_CORPUS_DIR>`,
  `<BIBER_PYTHON>`) from their setup, or point them at the author's CLAUDE.md. Each
  template's model note asks for a capability tier; add a `model:` line to the
  frontmatter naming the strongest model available to them, so the agent does not
  inherit a cheaper session model. `clean-reviewer` also pins `effort:` in its
  frontmatter because an Agent call cannot set effort; keep that line.

Also write them a short **their-own CLAUDE.md** (or a section in it) that records:
their field, language, venues, the register corpus path (`ZH_CORPUS_DIR` /
`CORPUS_DIR`) and its journal folder names, `BIBER_PYTHON` if set, where the voice
profile lives, which mode (lite/full) is active, **and the path where this kit is
cloned** (the `KIT PATH`).

🔴 **Record the kit path in exactly one place (their CLAUDE.md) and nowhere else.**
Their CLAUDE.md is auto-loaded, so their Claude always knows it. In the generated
skills, refer to kit tools as "the kit's `tools/zh-tw/...` (kit path is in CLAUDE.md)"
rather than pasting an absolute path into every skill. That way, if they move or
re-clone the kit, they fix one line, not five files. When you actually run a tool,
resolve the path from CLAUDE.md at call time.

Every generated skill MUST preserve the five iron ideas above. You may simplify
wording for a non-technical author, but you may not drop: no-fabricated-citations,
skeleton-first, effect-size+CI, data-stays-local, field register for papers and the
author's voice for letters, de-AI pass
(**both halves**, convergence words *and* overclaims: an unsupported absolute is a
substantive fault, not a stylistic one).

### Phase D: Teach them the 3 sentences they'll actually use

Non-technical authors don't want a manual. Hand them the small number of things
they'll actually type, in their language. For example:

- "Help me write this paper / proposal" → triggers **co-author**.
- "Check this draft before I submit" → triggers **paper-review**.
- "Get me the PDFs of these references" → triggers **fetch-refs** (if enabled).
- "Don't make that mistake again" / "fixing A broke B" → triggers **doc-regress**.

Then stop and let them try one. Offer the full-power add-ons only if they ask.

---

## Files in this kit (your reading order)

| Path | What it is |
|------|-----------|
| `method/PHILOSOPHY.md` | The mindset: division of labor, why skeleton-first. Read first. |
| `method/IRON-RULES.md` | The non-negotiables. Every generated skill must keep these. |
| `method/WORKFLOW.md` | The full 8-phase pipeline, generalized, with lite/full notes. |
| `method/ARGUMENTATION.md` | Argument *moves* as an internal diagnostic (not a menu to sprinkle). |
| `skills/*/SKILL.md` | De-personalized skill templates to adapt per author: `co-author`, `paper-review`, `fetch-refs`, `verify-citations`, `rebuttal`, `doc-regress` (turn a caught error into a standing check that scans the whole document and blocks recurrence; rules live in the author's project), `build-pdf`. |
| `agents/*.md` | Subagent templates: `clean-reviewer` (clean-context final review, reviewer simulation, rebuttal verdict table), `en-native-editor` (native-English polish against the field's register, change list only), `zh-tw-native-editor` (zh-TW addon: Taiwan academic Chinese polish, change list only), `de-cadencing-scholar` (pre-delivery English rhythm pass) and `citation-skeptic` (calibrated second review of flagged citations). Adapt, as with skills. |
| `tools/` | Working local checkers, ready from day one. Chinese ones, `tools/refs/snowball.py`, `tools/refs/retraction_scan.py` (retraction scan, Crossref + OpenAlex), `tools/claims/uncited_claims_scan.py` (uncited quantitative/causal/superlative claims), `tools/claims/overclaim_lint.py` (bilingual overclaim scan, the second half of the de-AI pass), and `tools/regress/` (`regress.py` document-regression runner, `dead_rule_check.py` rule-set health, `rules.template.json`, `numbers-ledger.template.md`), and `tools/register/` (`register_profile.py` deviation list against the field's register band, `polish_check.py` self-check for an editor's change list; the English Biber half is optional) are zero-install (stdlib); English ones need one/two free offline programs. `tools/refs/pdf_fetch.py` (layered reference-PDF retrieval; the browser layer is what clears Cloudflare publishers) is the one exception that needs installs (`pip install curl_cffi patchright`) and degrades to stdlib + open-access sources without them. See `tools/README.md`. |
| `templates/*` | Scaffolds the author fills in (voice profile, venue notes, skeleton, voice rules). |
| `setup/INTERVIEW.md` | Suggested interview wording. |
| `setup/WEB.md` | On-ramp for authors who start on claude.ai: how to move them onto Claude Code. |
| `setup/LITE.md` | Zero-install path: works with just Claude + web. |
| `setup/TOOLS.md` | Optional local power-ups + graceful-degradation map. |
| `setup/addons/zh-tw/` | Traditional-Chinese-Taiwan localization pack (optional). |
| `examples/` | An anonymized worked skeleton, for reference. |

---

## Rules for you, the installer

- **Adapt, never impersonate.** This kit came from one researcher's practice.
  You are building *this new person's* version, not cloning the original author.
- **Degrade gracefully.** Most people will run lite mode. A generated skill must
  work with only Claude + web, and *offer* (not assume) the local tools.
- **Privacy is a feature, stated honestly.** Unpublished drafts and raw research data go to
  no third-party service. Never suggest uploading a draft to a public detector or tool.
  Tell the author plainly that Claude Code sends whatever it reads to Anthropic, and that
  participant or confidential data needs their institution's clearance before you read it.
- **Don't over-install.** If they're cautious, set up project-local, lite mode,
  co-author + paper-review only. They can always come back for more.
- When you finish Phase C, briefly show them what you created and where, in their
  language, and tell them they can edit or delete any of it.
