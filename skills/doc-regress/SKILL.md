---
name: doc-regress
description: Build an "error regression suite" for a long document — once a mistake is caught, write it down as a standing check that scans the whole project and blocks the mistake from coming back. Use when the author says "don't let this happen again", "it gets worse every time I edit", "fixing A broke B", "set up regression checks for this paper", "keep this error from recurring", "I don't know whether the fix actually landed everywhere", or when a paper's numbers live in more than one place (text + tables + abstract). Works for papers, proposals, bids, teaching materials — any long document revised many times. The rules live in the author's project, version-controlled with the draft; this skill supplies the method, the bundled scaffold (`tools/regress/`) and the generic rules.
---

# doc-regress — error regression suite for long documents

> Generated from the Research Writing Kit; adapt to the project.
> This skill **does not edit the manuscript**. It builds scanners and reports what
> they find. Its value grows with the project's error history.

## What it solves

Repeated revision of a long document produces three kinds of error that no ordinary
linter (grammar, spelling, style) can see:

| | Symptom | Why linters miss it |
|---|---|---|
| **G1** | A newly added assertion was never checked | The new sentence is grammatical and reads clean |
| **G2** | A checker raised a false alarm and the "fix" broke something correct | Tools don't doubt themselves |
| **G3** | Editing A broke B, discovered many rounds later | Each edit is locally fine; the contradiction is across files |

## Boundary (which skill)

| The author wants | Skill | Difference |
|---|---|---|
| Check a draft's quality, typos, reviewer's eye | `paper-review` | One-off pass over one draft |
| Check that a citation says what the draft claims | `verify-citations` | Content correctness |
| Write, rewrite, resubmit | `co-author` | There is a *writing* act |
| **A standing check so a specific mistake can't recur** | **this skill** | **Builds a scanner, not prose; accumulates** |

One line: *"look at this draft" = paper-review; "make sure this never happens again"
= doc-regress.*

## Steps

### 1. Ask before building
- Where is the **source** (markdown / LaTeX / docx) and what is the built output?
- **What has already gone wrong?** No error history → no suite. Empty rules have no
  value and give false confidence.
- Is there an existing verify/build script to hook into?

### 2. Put the config in the project; the runner stays in the kit
Copy `tools/regress/rules.template.json` into the author's project as `regress.json`
and commit it there — the config *is* that project's error history and must travel
with the draft. The runner is the kit's `tools/regress/regress.py` (kit path is in
CLAUDE.md):

```bash
python3 tools/regress/regress.py --config regress.json            # human report
python3 tools/regress/regress.py --config regress.json --json     # for CI / scripts
```

Paths inside the config are relative to `--root` (default: the config's directory).
The generic rules are all **config-driven** — a rule whose key is empty reports itself
as *unconfigured* rather than silently passing:
- **R1 / R1-BIB citation integrity** (`ref_list` for numbered lists, `bib_files` for
  BibTeX) — dangling citation = FAIL; entry never cited = INFO.
- **R2 personal-data patterns** (`pii_patterns`, regexes for your country's ID /
  phone / account formats) — identifying data must not ride along in a deliverable.
- **R6 internal-note leakage** (`internal_words`) — TODOs, drafting prompts,
  instructions to the AI must not appear in the delivered version.
- **R-ATTR** (`entities`) — an entity must be accompanied by an attribution marker.
- **R-CORR** (`banned_claims`) — a corrected statement must not come back.
- **R-FACT** (`fact_ledger`) — known-wrong values FAIL near the fact's keyword.
- **R-STALE / R-LEDGER** (`ledger`) — the numbers ledger, §3.5.

### 3. Turn every real mistake into one rule
Ask "what has this document gotten wrong before?" and write each as a rule. **This is
where all the value is**; the scaffold is a container. Most mistakes fit one of the
config-driven shapes above (attribution marker → `entities`; a corrected statement →
`banned_claims`, with *why* it was wrong and the source; known-wrong values →
`fact_ledger`; numbers that live in several places → the ledger). A mistake that needs
code goes in a project file `my_rules.py` exposing `RULES = [fn(ctx), ...]`, run with
`--extra my_rules.py` — also committed with the draft.

### 3.5 Number-heavy documents: keep a numbers ledger

Papers, bids and reports state the same statistic in the text, a table and the
abstract. The most common error is **re-running the analysis and updating only one
place**. Per-rule checks can't keep up; a ledger can. Template:
`tools/regress/numbers-ledger.template.md`.

```tsv
# ID   current   old(value~anchor-regex; several separated by ;)   producing script   where in the text
IRR_ADD   9.20   8.22~[Aa]dditive|transitions   analysis/markers.py   §4.1 Table 4|§4.6 Table 6
```

Two rules read it:
- **R-STALE** — an old value recurs near its anchor → FAIL.
- **R-LEDGER** — the current value is nowhere in the draft → WARN (may be a rewording).

Calibration learned the hard way:
- 🔴 **Separators must not collide with regex.** Old values are separated by `;`; `|`
  belongs to the anchor's alternation. Mixing them once produced 70 false alarms.
- 🔴 **One ledger only.** Two files "kept in sync by hand" (a rich CSV the paper's
  waiver notes cite, a TSV the rules read) drift the first time one is edited.
  Generate the rules' file from the source file in step 0 of the verify script; hand
  edits to the generated file are overwritten on purpose.
- 🔴 **Record the value as written in the draft, not as computed.** `p < .001`, not
  `2.82e-05`; `.73`, not `0.73` when the venue drops leading zeros (accept both in the
  match); "94 % of the time", not `0.942`. Exact values go in a notes column. Split
  compound values (`3.63→4.23`, `0.75/0.73`, `0.67–0.87`) so each end is checked.
- R-STALE only guards a row whose *old* column is filled. A first-version ledger with
  `—` everywhere has run but defends nothing — don't count it as a verified line.

The workflow becomes: **re-run analysis → update the ledger → then edit the draft → run
regress to confirm both agree.** The order matters: editing the draft first means
R-STALE never sees the old value. Add columns for reproducibility (seed, timestamp,
exit code) if the analysis is re-run often.

### 4. Injection self-test (do not skip)
Every rule gets one test case: inject the mistake back in and confirm the rule fires.
**A check that never fires is worse than none — it gives false confidence.**

🔴 **Test execution, not registration.** A rule can be listed and still never run:
one that only understands numeric `[12]` references returns immediately on a BibTeX
project, reports `FAIL 0`, and citation integrity is never checked while the light
stays green. Two guards: the kit's generic rules report *unconfigured* instead of
returning quietly — treat that line as "not defended", not as a pass — and the bundled
detector checks the project's own rule code:

```bash
python3 tools/regress/dead_rule_check.py my_rules.py
```

It instruments each rule and counts the lines actually executed; below ~25 % it names
the rule as dead (an early return usually means a required setting is empty). Exit
code 1 = at least one dead rule; suitable for CI. A rule that doesn't apply to this
project is **removed from `RULES` with a note**, not left in place — a permanently dead
rule trains everyone to ignore the red.

Two more calibrations:
- **Measure the anchor window; don't guess it.** An anchor 65 characters from its
  number with a ±60 window never fires, and silent looks identical to passing. Take
  the anchor from the fragment *adjacent* to the number and confirm in the self-test.
- **When a fact is corrected, correct its test case too.** The test injects the "old"
  value; once the old value turns out to be right, the injection is a no-op and the
  rule looks broken. Fix the case, not the rule.

### 5. Hook into the existing verification
Attach to `verify.sh` / `make check` / CI / a pre-commit hook so it runs on every
change to the draft or the ledger.

### 6. Make settled decisions visible (`ADJUDICATED.md`)
Long documents get reviewed many times, and one class of finding is "looks wrong,
was checked, is right": a participant description that seems to contradict a data
field, a number format that follows a convention, a term kept on purpose. Once
settled, the decision usually sinks into one review report and is never seen again —
so **the next reviewer (human or agent) re-checks it and asks the author the same
question again**. Clean-context subagents do this most; their strength is the cost.

Keep `ADJUDICATED.md` in the project root: *apparent contradiction → ruling → basis
(file path) → status → still open*. Add an INFO rule that prints its entries on every
run (it judges nothing; it makes them visible). Reopening an entry requires stating
new evidence. `paper-review` reads this file at Step 0; `co-author` hands it to the
clean final reviewer.

## Five iron rules (each bought with a real error)

1. **Miss rather than mis-flag.** Unclear criteria → INFO, never FAIL. A false alarm's
   cost is "edited the correct thing into a wrong one", which is worse than a miss.
   Corollary: **bare small integers and common decimals are never registered as wrong
   values on their own — always with an anchor.** (A registered "32" matched a model
   name `…-32B`; "64" matched another group's *correct* new value.)
2. **Every mismatch a script reports is checked against the raw source by a human
   before anything is edited.** (A checker once reported five "orphan" references; they
   were cited in the half of the document it hadn't scanned. The "fix" undid a
   deliberate editorial decision.)
3. **Don't use English caption patterns on CJK text.** Characters like 表/式/圖 are
   ordinary morphemes (形式, 代表, 圖像); a naive pattern reports phantom equation
   numbers from table-of-contents page numbers and recognizes zero of the real
   references.
4. **After correcting a fact, re-check by concept, not by the string you just
   replaced.** One date error took four rounds to clear because each round found
   another format or wording. Register wrong values as a regex covering the variants.
5. **Your own additions are the audit blind spot; they get a separate pass.** Attention
   naturally goes to existing text. A sentence added to fill a widened date range
   passed every mechanical check and seven review rounds before the author caught it.
   **Structural fixes may not be made with facts** — if the range can't be filled,
   change the range.

## Output
After a run, report: current FAIL / WARN / INFO; self-test result (N/N rules proven
to fire; dead-rule check clean); one line on which mistakes can no longer recur.

**Do not say "the document has no errors."** A regression suite guarantees only that
*past* mistakes haven't returned; new ones need the uncited-claim scan
(`tools/claims/uncited_claims_scan.py`) and a human. Keep the two statements apart.
