# CLAUDE.md — Bootstrap Protocol for the Research Writing Kit

> You (Claude) are reading this because a human opened Claude Code inside this
> repository and wants to set up an AI-assisted academic-writing workflow.
> **This file is not the workflow. It is the installer.** Your job is to
> interview this person, then generate a *personalized* set of skills and a
> CLAUDE.md tailored to them — so that from now on their own Claude can help
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
   *this person's* field, language, and writing voice.

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
- **The author's voice is an asset.** Match the human's own writing voice when
  writing in their native language; never sand it into generic "AI prose."
- **Honesty tooling.** Effect sizes + CIs (not just p-values), data stays local,
  de-AI the prose before delivery, and a clean second pass reviews the work.

---

## BOOTSTRAP — run these phases in order

### Phase A — Interview (ask in the human's language, one at a time)

Keep it friendly. These map directly to what you'll generate. Suggested wording
is in `setup/INTERVIEW.md` — adapt it, don't read it robotically.

1. **What do you write?** (e.g. HCI papers, education research, humanities essays,
   grant proposals, a thesis) — and roughly what field/discipline.
2. **What language do you write in?** (the language of the *final paper*, which may
   differ from the language you're talking to me in right now.)
3. **Where do you submit?** Any target venues/journals/funders you know of, or
   "not sure yet." (This drives the venue-format research later.)
4. **Do you have 2–4 pieces of your own past writing** I could learn your voice
   from? (Any prose *you actually wrote yourself*, not AI-written. Optional but
   makes "sounds like you" possible. If none, we skip voice-matching and just
   aim for clear, strong academic prose.)
5. **How much setup do you want today?**
   - **Simple / web-only** (recommended to start): works with just Claude + the
     web, zero installs. → you'll configure the *lite* path (`setup/LITE.md`).
   - **Full power** (optional, later): local citation tools, corpora, stats.
     → mention it exists (`setup/TOOLS.md`), but don't force it now.
6. **Do you want the Traditional-Chinese-Taiwan localization pack?** (Only if they
   write Chinese for a Taiwan audience — Taiwan-vs-mainland term checking, etc.
   → `setup/addons/zh-tw/`. Skip entirely otherwise.)

If the human answers vaguely, pick sensible defaults and say what you chose.
Do not block on perfect answers.

### Phase B — Build a voice profile (only if they gave you samples)

If they provided their own writing:
- Read the samples. Extract *observable* habits into a filled-in copy of
  `templates/VOICE_PROFILE.template.md`: typical sentence length and rhythm,
  favored connectives, punctuation habits, register, words they reach for,
  words they never use. Quote 3–5 real phrases as anchors.
- **Describe patterns, don't invent a persona.** If you can't tell, say so.
- Save it where their Claude will find it (see Phase C for location).

If they gave no samples: skip. The generated skills will target "clear, strong
academic prose in <their venue's> register" instead of "sounds like them."

### Phase C — Generate their personalized setup

Decide *where* to install based on how they answered Q5 and their comfort:

- **Global (all their projects):** `~/.claude/skills/<skill>/SKILL.md` and
  append to `~/.claude/CLAUDE.md`. Use this if they want it everywhere.
- **This-project only:** a `.claude/skills/` folder inside whatever paper folder
  they're working in. Safer default for a cautious first-timer.

Ask which they prefer in plain terms ("just for this paper, or for everything
you write?"). Then, **generate — do not copy verbatim** — from the templates in
`skills/`, filling in:

- their **field** and **target venue(s)** (into each skill's venue/format step),
- their **writing language** and the matching language toolchain (lite or full),
- their **voice profile** path (or "no voice profile — aim for venue register"),
- the **degraded vs full** tool references per `setup/TOOLS.md` (never reference a
  tool they haven't installed as if it exists — gate it behind "if installed").

Also write them a short **their-own CLAUDE.md** (or a section in it) that records:
their field, language, venues, where the voice profile lives, and which mode
(lite/full) is active. This is what their Claude reads next time.

Every generated skill MUST preserve the five iron ideas above. You may simplify
wording for a non-technical author, but you may not drop: no-fabricated-citations,
skeleton-first, effect-size+CI, data-stays-local, voice-preservation, de-AI pass.

### Phase D — Teach them the 3 sentences they'll actually use

Non-technical authors don't want a manual. Hand them the small number of things
they'll actually type, in their language. For example:

- "Help me write this paper / proposal" → triggers **co-author**.
- "Check this draft before I submit" → triggers **paper-review**.
- "Get me the PDFs of these references" → triggers **fetch-refs** (if enabled).

Then stop and let them try one. Offer the full-power add-ons only if they ask.

---

## Files in this kit (your reading order)

| Path | What it is |
|------|-----------|
| `method/PHILOSOPHY.md` | The mindset: division of labor, why skeleton-first. Read first. |
| `method/IRON-RULES.md` | The non-negotiables. Every generated skill must keep these. |
| `method/WORKFLOW.md` | The full 7-phase pipeline, generalized, with lite/full notes. |
| `method/ARGUMENTATION.md` | Argument *moves* as an internal diagnostic (not a menu to sprinkle). |
| `skills/*/SKILL.md` | De-personalized skill templates to adapt per author. |
| `templates/*` | Scaffolds the author fills in (voice profile, venue notes, skeleton). |
| `setup/INTERVIEW.md` | Suggested interview wording. |
| `setup/LITE.md` | Zero-install path — works with just Claude + web. |
| `setup/TOOLS.md` | Optional local power-ups + graceful-degradation map. |
| `setup/addons/zh-tw/` | Traditional-Chinese-Taiwan localization pack (optional). |
| `examples/` | An anonymized worked skeleton, for reference. |

---

## Rules for you, the installer

- **Adapt, never impersonate.** This kit came from one researcher's practice.
  You are building *this new person's* version, not cloning the original author.
- **Degrade gracefully.** Most people will run lite mode. A generated skill must
  work with only Claude + web, and *offer* — not assume — the local tools.
- **Privacy is a feature.** Unpublished drafts and raw research data stay on the
  author's machine. Never suggest uploading a draft to a public detector or tool.
- **Don't over-install.** If they're cautious, set up project-local, lite mode,
  co-author + paper-review only. They can always come back for more.
- When you finish Phase C, briefly show them what you created and where, in their
  language, and tell them they can edit or delete any of it.
