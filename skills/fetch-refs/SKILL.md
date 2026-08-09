---
name: fetch-refs
description: Collect the PDFs of a paper's references so they can be verified. Use when the author says "get me the reference PDFs", "collect the references", "fetch references", "pull the cited papers". Also does citation snowballing (bundled `tools/refs/snowball.py`) — "who cites this paper", "find follow-up work", "snowball the references", "forward citations". Multi-source, open-access first; verifies each PDF's content actually matches the citation before filing.
---

# fetch-refs — collect reference PDFs

> Generated from the Research Writing Kit; adapt to what's installed.
> Feeds `verify-citations`. **Only download what you're authorized to** — respect
> paywalls and licenses; prefer open access.

## Input
A `.bib` file, a reference list, or a list of DOIs/titles.

## Lite mode (no installs — Claude + web)
For each reference:
1. Resolve identity: title + authors + year + DOI (Crossref lookup).
2. Find an **open-access** full text: Unpaywall / OpenAlex / Semantic Scholar /
   arXiv / the author's own page. Prefer the publisher's OA version, then a
   preprint.
3. **Verify the file matches the citation** before trusting it — open it, confirm
   title/authors/year line up (guards against "right link, wrong file").
4. File as `NN [Author Year] Title.pdf`; keep a manifest (what was found, what
   wasn't, and why).
5. Paywalled with no OA version → record it as **not obtained**; do not fabricate
   content from the abstract.

## Full mode (optional power-ups — see `setup/TOOLS.md`)
If the author has institutional access configured (e.g. a library VPN) and helper
tooling, use it to reach subscription full texts — but the verify-the-file-matches
step stays mandatory. ⚠️ Some publishers (Cloudflare-fronted) block automated
fetch even on VPN; fall back to browser view and mark `❓unverified`.

## Citation snowballing (bundled, zero-install)
Collecting reference PDFs is *backward* (what the draft cites). The kit's
`tools/refs/snowball.py` (Python stdlib only, kit path is in CLAUDE.md) adds three
directions — **forward** (who cites X: for related work, and for "you missed recent
work" checks), **backward** (what X cites), **related** (OpenAlex similar works).
With a whole `.bib` as seeds it aggregates: papers hitting more seeds (`seed_hits`)
are the most likely should-have-read literature.

```bash
# one paper: who cites it (sorted by citation count, top 30 printed)
python3 tools/refs/snowball.py --doi 10.1145/1240624.1240704 --direction forward --limit 100
# a whole bib as seeds: aggregate + dedupe, read high seed_hits first
python3 tools/refs/snowball.py --bib references.bib --direction forward --limit 50 --out snowball.csv
```

- Primary source OpenAlex; on 429 (daily quota, resets midnight UTC) forward falls
  back to Semantic Scholar automatically. backward/related need OpenAlex itself —
  a 429 there means **quota, not "no results"**; rerun after the reset.
- Passing `--email you@example.org` is optional but polite (OpenAlex's faster pool).
- Once candidates are chosen, add their DOIs to the `.bib` and run the collection
  flow above — discovery and fetching chain into one line.

## Output
A folder of named PDFs + a manifest table (obtained / OA / paywalled-missing),
ready for `verify-citations`. Snowballing adds a ranked candidate list (or CSV).
