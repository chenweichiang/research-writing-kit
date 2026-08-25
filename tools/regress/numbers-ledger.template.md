# Numbers ledger

<!--
ONE ledger per project. Copy this file next to the manuscript (e.g. numbers-ledger.md)
and point `ledger` in regress.json at it. regress.py reads the table below.

Why a ledger: in a paper / proposal / annual report the same statistic appears in the
abstract, the body and a table. The most common error after re-running an analysis is
updating ONE of those places. Rule-by-rule checks cannot follow that; a ledger can.

Workflow: re-run analysis -> update the ledger FIRST -> then edit the manuscript ->
run regress.py to confirm both sides agree.

Columns (regress.py reads the first five; `note` is free text):
  id       stable identifier, never renamed once cited in a waiver
  current  the value AS WRITTEN IN THE MANUSCRIPT, not the computed value.
           Computed p = 2.82e-05 while the text says p < .001 -> record `< .001`;
           coverage 0.942 written as "94%" -> record `94%`. Put the exact value in `note`.
           `.73` and `0.73` are treated as the same value (APA drops the leading zero).
           Compound values MUST be split with `/` so each part is checked: `0.75/0.73`.
  stale    corrected OLD values in the form `value~anchor-regex`, several separated by `;`.
           The anchor is a distinctive fragment within +-60 chars of where the number
           appears; bare small integers (32, 48) MUST have an anchor or they will hit
           model numbers and other groups' correct values.
           Use `\|` inside a cell for the regex OR (a bare `|` would end the cell).
           `—` means "no stale value yet" (normal for a first ledger: R-STALE then
           guards nothing — do not count it as a verified defence).
  source   script / notebook that produces the number
  where    where it appears in the manuscript (section, table)

Rules fed by this table:
  R-STALE   a stale value reappears near its anchor      -> FAIL
  R-LEDGER  a current value is not found in the manuscript -> WARN (may be a rewording)

Keep only one ledger. Two files (a rich CSV + a TSV "converted from it") will drift:
one gets corrected, the other keeps being compared. If you need two formats,
GENERATE one from the other in your check script; never hand-maintain both.
-->

| id | current | stale | source | where | note |
|----|---------|-------|--------|-------|------|
| N_PARTICIPANTS | 40 | 38~participants | data/participants.csv | §3.1 | 2 excluded after screening 2026-05-02 |
| IRR_KAPPA | .82 | .78~[Kk]appa\|agreement | analysis/irr.py | §3.4, Table 2 | exact 0.8213; second coder round 2 |
| EFFECT_D | 0.61 | — | analysis/models.R | §4.2, Table 4 | Cohen's d, 95% CI [0.22, 1.00] |
| COVERAGE_PCT | 94% | — | analysis/coverage.py | Abstract, §4.1 | exact 0.942 |
