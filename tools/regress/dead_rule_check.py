#!/usr/bin/env python3
"""dead_rule_check.py — find rules that are registered but never really execute
(the false-green-light detector).

🔴 Why: a project confirmed "all 8 rules are in RULES" and called it verified, but
one rule returned on its first line every time (it needed a numbered reference
list; the project used BibTeX). No error, FAIL 0 in every report — and citation
integrity had never been checked once.

Checking "is the rule in the list" always passes. What must be checked is
"does the rule's body execute". This script traces each rule with `sys.settrace`
and counts distinct lines executed; below the threshold the rule is called dead.

Typical cause: the setting a rule needs is empty (ref_list / bib_files /
entities / ...). Fix: fill it in, or remove the rule from RULES and note why.
Leaving it in place makes this detector print the same [FAIL] forever, which
people learn to ignore — that is the false green light again.

Works with the kit's regress.py (rules take a ctx built from --config) and with
standalone skeletons (module-level RULES of zero-argument functions, or a
`for fn in [...]` list inside main()).

Usage:
  dead_rule_check.py path/to/regress.py --config regress.json [--root DIR]
                     [--extra my_rules.py] [--threshold 25]
Exit codes: 0 = no dead rule; 1 = dead rule(s); 2 = could not load
"""
import argparse
import ast
import contextlib
import importlib.util
import inspect
import io
import pathlib
import sys


def load(path):
    path = pathlib.Path(path).resolve()
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location("regress_under_test", path)
    m = importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(m)
    return m


def rules_from_main_ast(path, mod):
    """Recover `for fn in [r1, r2, ...]` inside main() without executing main()."""
    tree = ast.parse(pathlib.Path(path).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.For) and isinstance(node.iter, ast.List):
            names = [e.id for e in node.iter.elts if isinstance(e, ast.Name)]
            fns = [getattr(mod, n) for n in names if callable(getattr(mod, n, None))]
            if len(fns) >= 2:
                return fns
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("regress_py", help="the regress.py to test")
    ap.add_argument("--config", help="JSON config (needed for the kit's regress.py)")
    ap.add_argument("--root", help="project root (default: config dir)")
    ap.add_argument("--extra", help="extra RULES file, as passed to regress.py")
    ap.add_argument("--threshold", type=float, default=25.0,
                    help="executed-line %% below which a rule is called dead (default 25)")
    a = ap.parse_args()

    try:
        R = load(a.regress_py)
    except Exception as e:  # noqa: BLE001
        print(f"[FAIL] cannot load {a.regress_py}: {type(e).__name__}: {e}")
        return 2
    rules = list(getattr(R, "RULES", None) or [])
    if not rules:
        rules = rules_from_main_ast(a.regress_py, R) or []
    if not rules:
        print("[FAIL] no rule list found (neither module-level RULES nor `for fn in [...]` in main())")
        return 2
    if a.extra and hasattr(R, "load_extra"):
        rules += R.load_extra(a.extra)

    ctx = None
    if hasattr(R, "load_config"):
        if not a.config:
            print("[FAIL] this regress.py needs --config (its rules take a ctx)")
            return 2
        ctx = R.load_config(a.config, a.root)
    else:  # standalone skeleton: try to hand it delivered text if it exposes one
        for name in ("_deliver_text", "deliver_text"):
            if hasattr(R, name):
                v = getattr(R, name)
                ctx = v() if callable(v) else v
                break

    dead = 0
    print(f"rules: {len(rules)} (threshold: <{a.threshold:.0f}% of lines executed = dead)")
    for f in rules:
        name = getattr(f, "__name__", "<lambda>")
        if name == "<lambda>":
            print(f"{'[--]':<7}{name:<26} skipped (a forwarding lambda; measuring it is meaningless)")
            continue
        code = f.__code__
        total = len({ln for _, _, ln in code.co_lines() if ln})
        hit = set()          # distinct line numbers executed (loops must not inflate)

        def tr(fr, ev, _a):
            if fr.f_code is code and ev == "line":
                hit.add(fr.f_lineno)
            return tr

        nparams = len(inspect.signature(f).parameters)
        sys.settrace(tr)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                f(ctx) if nparams else f()
        except Exception:  # noqa: BLE001 — a crash still counts the lines it reached
            pass
        finally:
            sys.settrace(None)
        pct = len(hit) / total * 100 if total else 0.0
        bad = pct < a.threshold
        dead += bad
        print(f"{('[FAIL]' if bad else '[OK]'):<7}{name:<26} {len(hit):4d}/{total:3d} lines "
              f"({pct:5.1f}%)" + ("  <- early return: the setting it needs is probably empty" if bad else ""))
    print(f"\n[{'FAIL' if dead else 'OK'}] {dead} dead rule(s)" if dead else "\n[OK] no dead rules")
    return 1 if dead else 0


if __name__ == "__main__":
    sys.exit(main())
