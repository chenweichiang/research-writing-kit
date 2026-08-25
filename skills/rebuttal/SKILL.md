---
name: rebuttal
description: Point-by-point response to reviewers, plus the revision table that backs it. Use when the author says "the reviews came back", "write a rebuttal", "respond to the reviewers", "major/minor revision", "point-by-point response", "response to reviewers", "R&R", or "revision table". Core rule — never change something that was right just to please a reviewer, and never leave a point unanswered.
---

# rebuttal — response to reviewers & revision table

> Generated from the Research Writing Kit; adapt to the author.

## What kills an R&R

Three failures, none of them about ability:

| Failure | What it looks like | Caught by |
|---|---|---|
| **Unanswered point** | The reviewer raised 14 things, the letter answers 11. Editors read them side by side. | Phase 1 numbering + Phase 5 check |
| **Promised, not done** | The letter says "we have revised this"; the manuscript is unchanged. | Phase 3 (every point maps to a location) |
| **Revised into a worse paper** | A correct claim or analysis is changed to satisfy a reviewer. | Phase 2 (DECLINE is a legitimate verdict) |

**🔴 The letter is an academic argument, not proof of obedience.** Reviewers can
misread, can ask for things outside the study's scope, and can contradict each other.
Accepting needs a reason; declining needs a better one — unreasoned compliance is as
unprofessional as unreasoned refusal.

## Phase 1 — Split (do not merge, do not skip)

Break the reviews into the smallest answerable units, numbered `R<reviewer>.<n>`
(the editor's own letter is `E.<n>`). **One sentence with two demands is two rows** —
merging is how you answer half of something the reviewer remembers asking in full.

Tag each: **type** (substantive / addition / clarity / format / misread), **severity**
(BLOCK / MAJOR / MINOR), and **conflict** — when two reviewers want opposite things,
flag it, then say so explicitly in the letter and explain which way you went.

Record in `rebuttal/points.tsv` (template in `tools/rebuttal/`).

## Phase 2 — Decide every verdict *before* editing

| Verdict | When | Requires |
|---|---|---|
| `ACCEPT` | The point is right | Say what you will actually change, not "this will be corrected" |
| `PARTIAL` | Right direction, too big an ask (e.g. a whole new experiment) | How far you went, why not further, and what you offer instead |
| `DECLINE` | Misread, out of scope, or it would make the paper worse | **Evidence**: where the manuscript already answers it, or the methodological reason |

Deciding while you edit means drifting into accepting everything.

🔴 **The right fix for a `misread` is not to comply — it is to rewrite so it cannot be
misread again.** If a reviewer read it wrong, the passage was probably unclear. Explain
the intent in the letter *and* fix the passage; that persuades more than defending it.

## Phase 3 — Revise, with locations

Record every change in `rebuttal/revisions.tsv`: `point_id | location | before | after`.

- `location` must be findable: `S4.2, 2nd paragraph` — not "the Method section"
- `DECLINE` rows use `-` for location but **must** fill `evidence`
- If the manuscript is in git: one commit per point, message starting with the point id.
  The table can then be generated from the log.

## Phase 4 — Write the letter

Four beats per point: **quote it → respond → say where you changed it → paste the new text.**

Tone: thank without grovelling ("we thank the reviewer for pointing this out" is
enough); hold your ground without fighting ("we understand this concern, but…" rather
than "the reviewer has misunderstood"); never promise future work to dodge something
you should handle now.

Think in the author's language, write in the venue's. **An English letter goes through
`paper-review` Layer 3 and a de-cadencing pass** (`agents/de-cadencing-scholar.md`,
file path only) before it ships — editors read many letters and an LLM-polished
cadence is as visible there as in the paper.

## Phase 5 — Verify before sending 🔴

```bash
python3 tools/rebuttal/check_response.py \
    --points rebuttal/points.tsv \
    --revisions rebuttal/revisions.tsv \
    --letter rebuttal/response-letter.md
```

Checks four things a human rereading their own letter will miss: every point answered;
every ACCEPT/PARTIAL mapped to a real location; every DECLINE carrying evidence; no
orphan point numbers (the classic renumbering slip). Non-zero exit = not ready to send.

## Deliverables

- the response letter (or the venue's required format)
- the revision table, if the venue asks for one
- **clean** manuscript, plus a **marked** one where required
  (`latexdiff old.tex new.tex > diff.tex`, or tracked changes in Word)

## Venue differences — check the current cycle, don't assume

Response rules differ as much as submission rules. Look them up for the current cycle
and **record them in the project's `venue-notes.md`** (the same file `co-author`
Track B writes), so the next revision round doesn't rediscover them:

- **ACM/IEEE conference rebuttals**: often a hard character limit, and usually **no new
  experiments** — clarification only
- **Journal major revision**: normally unlimited, expects point-by-point + marked copy
- **Double-blind**: nothing in the letter may identify you — institution, project name,
  or a self-citation phrased as your own

## Not this skill

Quality of the revised prose → `paper-review`. Finding literature a reviewer asked for
→ `fetch-refs`. Checking that your citations say what you claim → `verify-citations`.
