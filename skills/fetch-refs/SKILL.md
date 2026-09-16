---
name: fetch-refs
description: Collect the PDFs of a paper's references so they can be verified. Use when the author says "get me the reference PDFs", "collect the references", "fetch references", "pull the cited papers". Also does citation snowballing (bundled `tools/refs/snowball.py`) — "who cites this paper", "find follow-up work", "snowball the references", "forward citations" — and a literature map (`tools/refs/lit_map.py`, candidate classics by co-citation within a batch of literature, not global citation count; a starting point for judgment, not a verdict) — "what are the classics in this field", "who does everyone in this area cite". Multi-source, open-access first; verifies each PDF's content actually matches the citation before filing.
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
   title/authors/year line up (guards against "right link, wrong file"). Compare
   **phrase sequences, not bags of words**: in HCI/design, titles are full of
   *design / human / experience / tools*, so word overlap alone passes a completely
   different paper that cites the right one (a book's record matched to a paper that
   quotes it, at 67–83 % word overlap). Tiering: phrase similarity **≥ 0.85 →
   verified**; word overlap high but phrases short → **`LOW-CONFIDENCE`, kept but
   listed visibly for the author** — never silently passed; below that → rejected.
   Honest limit: papers that cite each other share surnames and vocabulary and no
   content check catches all of them; the aim is to turn silent passes into visible
   doubt, not to claim a clean filter.
3a. **An OA flag is not a download.** Index records (`oa_status=green`, a
   `best_oa_location` URL) point at institutional repositories that move or shut down
   while the index stays as it was. If the fetch fails, report "needs a browser" —
   don't argue from the flag that it should have worked, and don't retry to timeout.
4. File as `NN [Author Year] Title.pdf`; keep a manifest (what was found, what
   wasn't, and why; verification tier per file).
5. Paywalled with no OA version → record it as **not obtained**; do not fabricate
   content from the abstract.
6. **Mark the author's own works** (self-citations, co-authored prior work, an
   anonymous poster) in the manifest. If the collection is later fed into a style
   corpus as the "other people's writing" baseline, **remove those first** — a
   baseline containing the author's own prose cancels out the de-AI diagnosis.

## Full mode (bundled `tools/refs/pdf_fetch.py` + two installs)
`pip install curl_cffi patchright`, then:

```bash
python3 tools/refs/pdf_fetch.py --bib references.bib --out refs-pdf
python3 tools/refs/pdf_fetch.py --no-browser --out refs-pdf   # OA sources only, fast
```

It layers three ways of getting a file — open-access resolvers (incl. **Europe PMC,
CORE, OpenAIRE**, which the usual four miss), then a TLS-impersonating HTTP client,
then a **real Chrome on a persistent profile**.

🔴 **No DOI is not "unobtainable".** Bib entries without a `doi` field used to be
skipped before any source was tried — and arXiv preprints, whose bib carries only an
`eprint`, are exactly that case (measured: 13 of 24 entries in one bib, all freely
available, all skipped; 10/24 → 23/24 obtained after the fix). The tool now reads
`eprint` / arXiv URLs and, failing that, resolves the title on arXiv then OpenAlex —
**exact title match only**, because near-matches are collisions (`LoRA` vs `QA-LoRA`;
a three-word title vs an unrelated 1969 paper). Only books and chapters without a DOI
are handed back as `MANUAL` (find by ISBN). In lite mode do the same by hand: search
the title before declaring an entry unobtainable.

⚠️ **"The file matches the citation" does not mean "the file is complete."** Some
publisher links for books return a *preview* — front matter, chapter 1, and the full
bibliography (MIT Press: 245-page book → 51 pages; the title page is there, so a title
check passes). Used for citation verification, such a file gives **false negatives**:
a sentence cited from chapter 4 is not found, and the citation is wrongly marked
unsupported. Note the page count against the book's length in the manifest, mark
`PREVIEW-ONLY`, and say so when reporting. The verify-the-file-matches step
above stays mandatory either way. Only fetch what you are entitled to: this uses
*your own* access in a real browser session, exactly as you would by hand.

### Cloudflare is not a dead end (measured, 2026-08-30)
A previous version of this file said Cloudflare-fronted publishers "block automated
fetch even on VPN — fall back to browser view". The observation was right; the
conclusion was premature.

- **A TLS-impersonating client does not clear it.** curl_cffi fixes the JA3/TLS
  fingerprint and rescues edge-403s (T&F), but ACM / Wiley / SAGE / AIP / Elsevier
  still answer `cf-mitigated: challenge` + "Just a moment...". Blog posts claiming
  otherwise are not testing academic publishers.
- **A real browser does.** Driving your installed Chrome on a persistent profile
  clears the challenge on all of them; ACM yields the PDF directly.

### The part that matters more than the hit rate: say *why* it failed
Reporting everything unobtained as one "needs a browser" bucket is what makes a
collection run useless — the author cannot tell which items deserve five more
minutes. Classify instead:

| tag | meaning | what the author should do |
|---|---|---|
| `PAYWALL` | no entitlement | no tool fixes this — ILL, ask the author, look for an author-hosted copy |
| `CAPTCHA` | a human must clear it once | clear it in the profile, then re-run (it expires — warm right before the batch) |
| `NO-LINK` | page rendered, no PDF found | **the only bucket where the tooling can still improve** |
| `CHALLENGE`/`TIMEOUT`/`ERROR` | transient | re-run |

On a real 46-reference bibliography this moved 11/46 → 30/46, and — more usefully —
left **zero** items in `NO-LINK`: every remaining miss was a genuine entitlement gap
the author could act on.

### Field notes worth knowing before you write your own
- **`/doi/pdf/` is often not a PDF.** Wiley's returns a 49 KB HTML viewer shell (the
  file is at `/doi/pdfdirect/`); SAGE's `/doi/reader/` and `/doi/epub/` are shells too;
  T&F's returns the landing page itself. **Always check the `%PDF-` magic bytes** —
  never the extension or the content-type.
- **You cannot build Elsevier's URL.** It is `/pii/{PII}/pdfft?md5=…`, a one-time
  per-session token readable only off the rendered page, and it then returns an HTML
  interstitial that hops once more. Capture the response body instead.
- **Link discovery needs three signals**: URL shape, link text, **and class /
  aria-label / title**. An icon link has empty `textContent` — one journal portal
  ships `<a href="/submission/api/download?id=…" class="icon pdf"></a>`, where only
  the class gives it away. Missing that signal missed the article 100% of the time.
- **Scope the candidates.** SAGE reference lists link other papers' PDFs; without a
  same-host-or-contains-our-DOI filter you cheerfully download the wrong file.
- **Hanging is worse than failing** — a failure moves on, a hang takes the batch with
  it. Three guards earn their keep: an `AbortController` on the in-page fetch (the
  browser's `fetch()` has no timeout; one non-responding URL hung a run for 193 s), a
  dialog/popup handler on every page (a login dialog freezes the whole tab), and
  downloads on a throwaway page (navigating the main page can make Chrome close it,
  after which *every* remaining item fails).
- ❌ **Zotero translation-server cannot do this.** It looks like the perfect answer —
  700+ publisher translators — and its metadata is excellent, but `attachments` is
  always null in every output format: the server has no attachment-download capability
  at all. It is a metadata service, not a retrieval service.

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

## Literature map (`lit_map.py`): candidate classics and recent high-impact work
Snowballing answers "who does this one paper connect to"; `lit_map.py` answers
"**who does this whole batch of literature co-cite**" — a starting point for judging
what counts as a classic (a classic is not just "highest global citation count"; see
`method/RIGOR_PROCESS.md` stage 3).

```bash
python3 tools/refs/lit_map.py --query "research through design" --from-year 2007 --limit 200 --out map.md --csv refs.csv
python3 tools/refs/lit_map.py --dois seeds.txt --out map.md      # a hand-picked seed set instead
```

- Output: a co-citation ranking (count, share, number of distinct venues citing it) +
  the most-cited recent work in the window.
- **This is a candidate list, not a verdict**: still check by hand whether each one is
  cited across different camps, whether it's been replicated or overturned, and whether
  it's since been retracted — "cited by N distinct venues" is a rough proxy, not proof.
- `--save-json` saves the raw OpenAlex data if you want to hand it to a full
  bibliometric mapping tool (e.g. R's `bibliometrix`) for a complete science map.
  **Query with `title_and_abstract`**, not full-text search — full-text search surfaces
  cross-field high-citation noise (a methodology paper used everywhere, unrelated to
  your topic). **OpenAlex bills by usage**; a 429 means the day's quota is spent.
- When the candidate list runs into the hundreds and you need a systematic or scoping
  review, screen with **ASReview** (`asreview lab`, local, optional install — see
  `setup/TOOLS.md`) rather than reading all of them.

## Output
A folder of named PDFs + a manifest table (obtained / OA / paywalled-missing),
ready for `verify-citations`. Snowballing adds a ranked candidate list (or CSV); the
literature map adds a co-citation ranking.
