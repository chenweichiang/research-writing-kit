---
name: fetch-refs
description: Collect the PDFs of a paper's references so they can be verified. Use when the author says "get me the reference PDFs", "collect the references", "fetch references", "pull the cited papers". Multi-source, open-access first; verifies each PDF's content actually matches the citation before filing.
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

## Output
A folder of named PDFs + a manifest table (obtained / OA / paywalled-missing),
ready for `verify-citations`.
