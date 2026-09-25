#!/usr/bin/env python3
"""release_check.py: the maintainer's pre-release gate for this kit (not for authors).

Five checks, each one a thing that has to be true before a change ships:

  1 frontmatter  every skills/*/SKILL.md and agents/*.md opens with a YAML frontmatter
                 block that yaml.safe_load parses into a mapping
  2 fixtures     method_decision_check.py run on the blank templates prints exactly the
                 stored baseline in tests/fixtures/ (output and exit code)
  3 dashes       lines added relative to the base ref contain no em dash
  4 localize     added lines with Chinese in them carry no mainland-Mandarin term,
                 using the kit's own tools/zh-tw/zh_localize.py table
  5 privacy      no e-mail address, /Users/ home path, or institution name anywhere in
                 the tracked tree; NOTICE and README keep the author credit and the
                 repository URL (patterns live in release_check.json)

"Added lines" = the diff from merge-base(base, HEAD) to the working tree, plus every
line of untracked, non-ignored files. Check 5 scans whole files, not just added lines.

Needs PyYAML for check 1 (pip install pyyaml); without it check 1 fails rather than
passing silently. Everything else is the standard library plus git.

Usage:
  python3 tools/dev/release_check.py                     # all five, base origin/main
  python3 tools/dev/release_check.py --base <ref>        # e.g. the push's previous commit
  python3 tools/dev/release_check.py --only 3 4          # a subset
  python3 tools/dev/release_check.py --update-fixtures   # rewrite check 2 baselines, then review the diff
Exit code: 0 = all selected checks pass; 1 = at least one failed.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = Path(__file__).with_name("release_check.json")
HAN = re.compile(r"[㐀-鿿]")
MAX_SHOWN = 40


def load_config(path=CONFIG):
    cfg = json.loads(Path(path).read_text(encoding="utf-8"))
    return {k: v for k, v in cfg.items() if not k.startswith("_")}


def git(*args, root=ROOT):
    out = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {out.stderr.strip()}")
    return out.stdout


def is_text(path):
    try:
        head = Path(path).read_bytes()[:8192]
    except OSError:
        return False
    return b"\0" not in head


# ---------------------------------------------------------------- check 1
def frontmatter_problems(text):
    """Problems with one file's frontmatter (empty list = parses to a mapping)."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return ["no frontmatter: first line is not ---"]
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return ["frontmatter never closed with ---"]
    try:
        import yaml
    except ImportError:
        return ["PyYAML not installed (pip install pyyaml); cannot verify"]
    try:
        data = yaml.safe_load("\n".join(lines[1:end]))
    except yaml.YAMLError as e:
        return [f"yaml.safe_load failed: {' '.join(str(e).split())}"]
    if not isinstance(data, dict):
        return [f"frontmatter parses to {type(data).__name__}, not a mapping"]
    return []


def check_frontmatter(root=ROOT):
    files = sorted(root.glob("skills/*/SKILL.md")) + sorted(root.glob("agents/*.md"))
    if not files:
        return ["no skills/*/SKILL.md or agents/*.md found"], "0 files"
    bad = []
    for f in files:
        for p in frontmatter_problems(f.read_text(encoding="utf-8")):
            bad.append(f"{f.relative_to(root)}: {p}")
    return bad, f"{len(files)} files"


# ---------------------------------------------------------------- check 2
def method_decision_output(template, root=ROOT):
    """What the fixture stores: the exit code line, then stdout verbatim."""
    out = subprocess.run(
        [sys.executable, str(root / "tools/method/method_decision_check.py"), str(template)],
        cwd=root, capture_output=True, text=True, encoding="utf-8")
    return f"exit={out.returncode}\n{out.stdout}"


def check_fixtures(cfg, root=ROOT, update=False):
    bad = []
    pairs = cfg["method_decision_fixtures"]
    for template, fixture in pairs:
        got = method_decision_output(root / template, root)
        fx = root / fixture
        if update:
            fx.parent.mkdir(parents=True, exist_ok=True)
            fx.write_text(got, encoding="utf-8")
            continue
        if not fx.is_file():
            bad.append(f"{fixture}: baseline missing (create it with --update-fixtures)")
            continue
        want = fx.read_text(encoding="utf-8")
        if got != want:
            g, w = got.splitlines(), want.splitlines()
            n = next((i for i in range(min(len(g), len(w))) if g[i] != w[i]), min(len(g), len(w)))
            bad.append(f"{template}: output differs from {fixture} at line {n + 1}: "
                       f"baseline {w[n] if n < len(w) else '(end)'!r} / now {g[n] if n < len(g) else '(end)'!r}")
    return bad, f"{len(pairs)} template(s)" + (" (baselines rewritten)" if update else "")


# ---------------------------------------------------------------- added lines
def parse_unified_diff(diff):
    """[(path, new_line_no, text)] for every added line of a `git diff -U0` output."""
    out, path, n = [], None, 0
    for line in diff.split("\n"):
        if line.startswith("+++ "):
            p = line[4:]
            path = None if p == "/dev/null" else re.sub(r"^b/", "", p)
        elif line.startswith("@@"):
            m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)", line)
            n = int(m.group(1)) if m else 0
        elif line.startswith("+") and path is not None:
            out.append((path, n, line[1:]))
            n += 1
    return out


def added_lines(base, root=ROOT):
    mb = git("merge-base", base, "HEAD", root=root).strip()
    diff = git("diff", "--no-color", "--no-ext-diff", "--unified=0", "--no-renames", mb, root=root)
    rows = parse_unified_diff(diff)
    for rel in git("ls-files", "--others", "--exclude-standard", root=root).splitlines():
        f = root / rel
        if f.is_file() and is_text(f):
            for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").split("\n"), 1):
                rows.append((rel, i, line))
    return rows


# ---------------------------------------------------------------- check 3
def dash_hits(rows, chars):
    rx = re.compile("[" + "".join(re.escape(c) for c in chars) + "]")
    return [(p, n, t) for p, n, t in rows if rx.search(t)]


def check_dashes(rows, cfg):
    hits = dash_hits(rows, cfg["dash_chars"])
    return [f"{p}:{n}: {t.strip()[:100]}" for p, n, t in hits], f"{len(rows)} added line(s)"


# ---------------------------------------------------------------- check 4
def _zh_localize():
    sys.path.insert(0, str(ROOT / "tools/zh-tw"))
    import zh_localize
    return zh_localize


def mainland_hits(rows, exclude=()):
    zl = _zh_localize()
    out = []
    for p, n, t in rows:
        if p in exclude or not HAN.search(t):
            continue
        for _i, cn, tw, _ctx in zl.check_terms(t):
            out.append((p, n, cn, tw))
    return out


def check_localize(rows, cfg):
    hits = mainland_hits(rows, set(cfg.get("localize_exclude", [])))
    zh = sum(1 for p, _n, t in rows if HAN.search(t))
    return [f"{p}:{n}: {cn} -> {tw}" for p, n, cn, tw in hits], f"{zh} added line(s) with Chinese"


# ---------------------------------------------------------------- check 5
def privacy_line_hits(line, cfg, exempt=False):
    """[(pattern name, matched text)] for one line after the allow-lists are removed."""
    allow = list(cfg.get("privacy_allow_everywhere", []))
    if exempt:
        allow += cfg.get("privacy_exempt_allow", [])
    for a in allow:
        line = re.sub(a, " ", line)
    return [(p["name"], m.group()) for p in cfg["privacy_patterns"]
            for m in re.finditer(p["regex"], line)]


def repo_files(root=ROOT):
    tracked = git("ls-files", root=root).splitlines()
    untracked = git("ls-files", "--others", "--exclude-standard", root=root).splitlines()
    return sorted(set(tracked + untracked))


def check_privacy(cfg, root=ROOT, files=None):
    skip = set(cfg.get("privacy_skip_files", []))
    exempt = set(cfg.get("privacy_exempt_files", []))
    bad, n = [], 0
    for rel in files if files is not None else repo_files(root):
        f = root / rel
        if rel in skip or not f.is_file() or not is_text(f):
            continue
        n += 1
        for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").split("\n"), 1):
            for name, got in privacy_line_hits(line, cfg, rel in exempt):
                bad.append(f"{rel}:{i}: {name}: {got}")
    return bad, f"{n} file(s)"


# ---------------------------------------------------------------- main
NAMES = {1: "frontmatter parses (skills, agents)",
         2: "method_decision_check.py output matches baseline",
         3: "no em dash in added lines",
         4: "no mainland terms in added Chinese lines",
         5: "no personal data (e-mail, home paths, institutions)"}


def run(only, base, cfg, root=ROOT, update=False):
    """[(number, name, problems, scope)] for the selected checks."""
    results, rows = [], None
    for k in only:
        try:
            if k in (3, 4) and rows is None:
                rows = added_lines(base, root)
            if k == 1:
                bad, scope = check_frontmatter(root)
            elif k == 2:
                bad, scope = check_fixtures(cfg, root, update)
            elif k == 3:
                bad, scope = check_dashes(rows, cfg)
            elif k == 4:
                bad, scope = check_localize(rows, cfg)
            else:
                bad, scope = check_privacy(cfg, root)
        except Exception as e:  # noqa: BLE001  a crash is a failure, never a pass
            bad, scope = [f"check crashed: {type(e).__name__}: {e}"], "not run"
        results.append((k, NAMES[k], bad, scope))
    return results


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", default="origin/main", help="ref the added lines are measured from")
    ap.add_argument("--config", default=str(CONFIG))
    ap.add_argument("--only", nargs="+", type=int, choices=sorted(NAMES), default=sorted(NAMES))
    ap.add_argument("--update-fixtures", action="store_true",
                    help="rewrite the check 2 baselines from the current templates")
    a = ap.parse_args(argv)

    cfg = load_config(a.config)
    results = run(a.only, a.base, cfg, ROOT, a.update_fixtures)
    failed = 0
    print(f"release check | base {a.base}")
    for k, name, bad, scope in results:
        print(f"[{'FAIL' if bad else 'PASS'}] {k} {name} ({scope}): {len(bad)} problem(s)")
        for b in bad[:MAX_SHOWN]:
            print(f"       {b}")
        if len(bad) > MAX_SHOWN:
            print(f"       ... {len(bad) - MAX_SHOWN} more")
        failed += bool(bad)
    print(f"\n{len(results) - failed}/{len(results)} checks pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
