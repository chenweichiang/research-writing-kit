# Bundled tools

Small, local, privacy-respecting checkers you can run from day one. **The three
Chinese tools need nothing installed** (Python 3 standard library only) — they work
out of the box. The English tools need one or two free offline programs.

> Everything here runs **on your machine**; drafts never leave it. Never paste an
> unpublished draft into a cloud "AI detector."
>
> These are generalized from one researcher's toolkit. Adapt the word lists and
> rules to *your* field and voice — they're starting points, not gospel.

## Chinese (`tools/zh-tw/`) — zero installs

| Tool | What it does | Run |
|------|--------------|-----|
| `zh_localize.py` | Flags mainland-Mandarin terms (反饋→回饋…) + 台/臺 consistency, with a false-positive whitelist. Report-only. | `python3 zh_localize.py draft.md` |
| `zh_ai_style.py` | Chinese AI syntax fingerprint: em-dash/semicolon/rule-of-three density, convergence words, sentence burstiness (heuristic). | `python3 zh_ai_style.py draft.md` |
| `voice_lint.py` | Mechanically enforces YOUR voice rules (config-driven). Exits non-zero until clean — use as a pre-delivery gate. | `python3 voice_lint.py draft.md [--rules voice_rules.json]` |

- `zh_ai_style.py` gets sharper if you point `--authored <folder>` at a folder of your
  own `.txt` writing — then words *you* genuinely use aren't flagged as AI tells.
- `voice_lint.py` ships generic defaults. Copy `templates/voice_rules.template.json`
  → `voice_rules.json`, edit it to match your own habits (what *you* never write), and
  pass `--rules voice_rules.json`. Build it from your `VOICE_PROFILE` (see `templates/`).

## English (`tools/en/`) — one or two free installs

| Tool | What it does | Needs |
|------|--------------|-------|
| `lt_check.sh` | Offline grammar + US/UK spelling-consistency (LanguageTool), markup stripped by the bundled pandoc filter. | `brew install languagetool pandoc` |
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
cancels itself out. Exclude any of your own files with `--exclude yourname`.

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
