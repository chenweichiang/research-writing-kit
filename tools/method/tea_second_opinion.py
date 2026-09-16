#!/usr/bin/env python3
"""tea_second_opinion.py — a second opinion from Tea: give it your data and a study-design spec,
and it picks and runs the matching statistical test automatically.

Why this exists: Tea (Jun et al., UIST 2019; University of Washington, tea-lang-org/tea-lang,
still maintained as of 2026) auto-selects a statistical test from your variable types, study
design, and hypotheses. It only covers classical tests (t-test, Mann-Whitney, chi-square,
correlation, ANOVA family) -- no mixed models, ordinal regression, or Bayesian models -- so treat
it strictly as a **second opinion**: compare it against your method decision (`method/METHOD_DECISION.md`)
and what comparable papers actually did; if they disagree, find out why before writing anything
based on Tea's answer alone.

Install (Tea needs Python 3.10-3.13, and pins older numpy/pandas -- give it its own virtualenv
rather than your main one):
    python3.12 -m venv ~/.venvs/tea && ~/.venvs/tea/bin/pip install tea-lang

Usage:
    ~/.venvs/tea/bin/python tea_second_opinion.py --csv data.csv --spec spec.json
    ~/.venvs/tea/bin/python tea_second_opinion.py --example   # print an example spec

Example spec.json:
{
  "key": "id",
  "variables": [
    {"name": "cond", "data type": "nominal", "categories": ["A", "B"]},
    {"name": "score", "data type": "ratio"}
  ],
  "design": {"study type": "experiment", "independent variables": "cond", "dependent variables": "score"},
  "assumptions": {"Type I (False Positive) Error Rate": 0.05},
  "hypotheses": [{"vars": ["cond", "score"], "prediction": ["cond:A < B"]}]
}
"data type" can be nominal / ordinal (ordinal needs "categories" in order) / interval / ratio;
"study type" can be experiment / observational study (needs "contributor variables" and
"outcome variables" instead of independent/dependent).
"""
import argparse
import json
import sys

EXAMPLE = {
    "key": "id",
    "variables": [
        {"name": "cond", "data type": "nominal", "categories": ["A", "B"]},
        {"name": "score", "data type": "ratio"},
    ],
    "design": {"study type": "experiment", "independent variables": "cond", "dependent variables": "score"},
    "assumptions": {"Type I (False Positive) Error Rate": 0.05},
    "hypotheses": [{"vars": ["cond", "score"], "prediction": ["cond:A < B"]}],
}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv")
    ap.add_argument("--spec")
    ap.add_argument("--example", action="store_true")
    a = ap.parse_args()
    if a.example:
        print(json.dumps(EXAMPLE, ensure_ascii=False, indent=2))
        return
    if not (a.csv and a.spec):
        ap.error("give --csv and --spec (or --example to see a sample spec)")
    try:
        import tea
    except ImportError:
        sys.exit("tea is not installed here -- run this with the interpreter from the virtualenv "
                 "where you installed tea-lang (see the install note in this file's docstring)")
    spec = json.load(open(a.spec, encoding="utf-8"))
    tea.data(a.csv, key=spec.get("key"))
    tea.define_variables(spec["variables"])
    tea.define_study_design(spec["design"])
    tea.assume(spec.get("assumptions", {"Type I (False Positive) Error Rate": 0.05}))
    print("Tea's second opinion (classical tests only -- compare against method/METHOD_DECISION.md "
          "and what comparable papers did)\n")
    for h in spec["hypotheses"]:
        print(f"== hypothesis: {h['vars']} {h['prediction']}")
        try:
            print(tea.hypothesize(h["vars"], h["prediction"]))
        except Exception as e:  # Tea raises on combinations it doesn't support -- report as-is
            print(f"Tea could not handle this hypothesis: {type(e).__name__}: {e}")
        print()


if __name__ == "__main__":
    main()
