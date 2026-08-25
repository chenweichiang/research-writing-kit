#!/usr/bin/env python3
r"""regress.py — regression suite for long documents: every rule is a mistake you
actually made once, turned into a permanent mechanical check.

The only condition for adding a rule: the error really happened AND it has a clear
mechanical criterion. Do not build rules for errors you have never made — an
empty rule has no value and gives false safety.

🔴 Design rules (breaking them creates new errors):
  1. Prefer a miss to a false alarm. Unclear criteria -> INFO, never FAIL.
  2. In Chinese, 表 / 式 / 圖 are ordinary morphemes: never grab numbered
     references with r'表\s*\d+'.
  3. Before splitting Chinese list items on "；", remove parenthesised text
     (parentheses often contain semicolons).
  4. A rule that never fires is not a check. Run dead_rule_check.py and inject
     the error back once to prove the rule rings.

Config: a JSON file (copy `rules.template.json`), passed with --config. All paths
inside it are relative to --root (default: the config file's directory).
Numbers ledger: `numbers-ledger.template.md` (markdown table or TSV).

Usage:
  regress.py --config regress.json [--root DIR] [--json] [--extra my_rules.py]

`--extra` loads a Python file exposing `RULES = [fn, ...]`; each fn(ctx) may call
`ctx.rec(level, rule_id, msg, where)` and use `ctx.deliver_files()`,
`ctx.clean_text(path)`, `ctx.deliver_text()`. That is where project-specific
rules go — one per mistake, with a comment saying what went wrong and when.

Exit code: 1 if any FAIL, else 0.
"""
import argparse
import importlib.util
import inspect
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "common"))
from md_prose import mask_nonprose  # noqa: E402


class Ctx:
    """Everything a rule needs: config, root, result buckets, file helpers."""

    def __init__(self, cfg: dict, root: Path):
        self.cfg, self.root = cfg, root
        self.FAIL, self.WARN, self.INFO = [], [], []
        self._text_cache = {}

    def rec(self, level, rule, msg, where=""):
        bucket = {"FAIL": self.FAIL, "WARN": self.WARN}.get(level, self.INFO)
        bucket.append({"rule": rule, "msg": msg, "where": where})

    def unconfigured(self, rule_id, name, hint):
        """Rule exists but its setting is empty -> say so instead of passing silently.
        A rule with an empty list still "runs" (the loop just has nothing to loop
        over), so even dead-rule detection cannot see it. One project had three of
        these at once and a fully green report with zero coverage on three fronts."""
        self.rec("INFO", rule_id, f"'{name}' not configured -> NOT guarding. {hint} "
                                  "(fill it in, or drop the rule and note why)")

    def rel(self, p: Path) -> str:
        try:
            return str(p.relative_to(self.root))
        except ValueError:
            return str(p)

    # -- files --------------------------------------------------------------
    def all_files(self):
        """Every source file (internal working files included) — for PII rules."""
        src = self.root / self.cfg.get("src_dir", ".")
        return [p for p in sorted(src.glob("**/*.md")) if ".bak" not in p.name]

    def deliver_files(self):
        """Delivered body text only.
        ⚠️ Internal working files legitimately TALK ABOUT internal words and
           non-existent reference numbers; scanning them with body rules is a
           guaranteed false alarm (hit on the very first real run)."""
        src = self.root / self.cfg.get("src_dir", ".")
        out = []
        for g in self.cfg.get("deliver_globs") or ["*.md"]:
            out += [p for p in sorted(src.glob(g)) if ".bak" not in p.name]
        return out

    def clean_text(self, p: Path) -> str:
        """Approximate the delivered version: drop HTML comments, code fences,
        【pending markers】, and sections whose heading contains a skip word.
        ⚠️ Paragraphs are re-joined with a DOUBLE newline: paragraph-level rules
           split on it; joining with a single newline turns the whole file into one
           paragraph and every paragraph rule passes forever."""
        if p in self._text_cache:
            return self._text_cache[p]
        raw = mask_nonprose(p.read_text(encoding="utf-8"))
        skip_words = self.cfg.get("skip_sections") or []
        out, skip = [], False
        for blk in raw.split("\n\n"):
            s = blk.strip()
            if not s:
                continue
            if s.startswith("#"):
                skip = any(w in s for w in skip_words)
                if not skip:
                    out.append(s)
                continue
            if skip or (s.startswith("【") and s.endswith("】")):
                continue
            out.append(re.sub(r"【[^】]*】", "", s, flags=re.S))
        txt = "\n\n".join(out)
        self._text_cache[p] = txt
        return txt

    def deliver_text(self) -> str:
        return "\n\n".join(self.clean_text(f) for f in self.deliver_files())


def split_items(s: str):
    """Split on "；" / ";" AFTER stripping parentheses — a semicolon inside
    parentheses is not a separator. (Skipping this once over-counted an item list
    by 2, nearly causing an edit to the wrong number.)"""
    return [x for x in re.split(r"[；;]", re.sub(r"[（(][^）)]*[）)]", "", s)) if x.strip()]


# ═════════════════════════════════════════════════════════════════════════════
# Generic rules (config-driven)
# ═════════════════════════════════════════════════════════════════════════════
def r1_citations_numeric(ctx):
    """Citation integrity, numeric style: dangling citation = FAIL, orphan entry = INFO.
    ⚠️ If the document is split across files sharing ONE numbering, the scan must
       cover all of them — scanning half flags entries cited elsewhere as orphans."""
    ref_list = ctx.cfg.get("ref_list")
    if not ref_list:
        return ctx.unconfigured("R1", "ref_list (numbered reference list)",
                                "set ref_list, or use bib_files for BibTeX projects")
    rp = ctx.root / ref_list
    if not rp.exists():
        return ctx.rec("FAIL", "R1", f"ref_list not found: {ref_list}")
    refs = {int(m.group(1)) for l in rp.read_text(encoding="utf-8").split("\n")
            if (m := re.match(r"^\[(\d+)\]", l))}
    cites = set()
    for f in ctx.deliver_files():
        if f.resolve() == rp.resolve():
            continue
        for m in re.finditer(r"(?<!R)\[\d+(?:[,、\s]+\d+)*\]", ctx.clean_text(f)):
            cites |= {int(n) for n in re.findall(r"\d+", m.group(0))}
    for n in sorted(cites - refs):
        ctx.rec("FAIL", "R1", f"body cites [{n}] but the reference list has no such entry (dangling)")
    orphan = sorted(refs - cites)
    if orphan:
        ctx.rec("INFO", "R1", f"reference entries {orphan} never cited (fine for a bibliography; confirm intent)")


def r1_citations_bibtex(ctx):
    """Citation integrity, BibTeX / pandoc @key style: dangling = FAIL, orphan = INFO.

    🔴 Why this exists: the numeric rule returns immediately when `ref_list` is
    unset. A BibTeX project that only registered the numeric rule had a rule that
    ran, raised nothing, reported FAIL 0 — and never checked a single citation.
    Verify EXECUTION, not registration (see dead_rule_check.py)."""
    bibs = ctx.cfg.get("bib_files") or []
    if not bibs:
        return ctx.unconfigured("R1-BIB", "bib_files", "list your .bib files (relative to root)")
    entries = set()
    for b in bibs:
        fp = ctx.root / b
        if not fp.exists():
            ctx.rec("FAIL", "R1-BIB", f"bib file not found: {b}")
            continue
        entries |= set(re.findall(r"@\w+\s*\{\s*([^,\s]+)", fp.read_text(encoding="utf-8")))
    cited = set()
    for f in ctx.deliver_files():
        # comments already masked; @key allows : . - _ (legal pandoc citeproc chars)
        cited |= set(re.findall(r"@([A-Za-z][A-Za-z0-9_:.-]*\d{4}[a-z]*)", ctx.clean_text(f)))
    for k in sorted(cited - entries):
        ctx.rec("FAIL", "R1-BIB", f"dangling citation: body cites @{k}, bib has no such entry")
    orph = sorted(entries - cited)
    if orph:
        ctx.rec("INFO", "R1-BIB", f"{len(orph)} orphan bib entries (in bib, never cited; usually "
                                  f"leftovers): {', '.join(orph[:8])}" + (" ..." if len(orph) > 8 else ""))


def r2_pii(ctx):
    """Personal-data patterns must not travel with the document.
    Config `pii_patterns`: [[name, regex], ...]. Matches preceded by an official
    document-number cue (`pii_skip_before` regex) are ignored."""
    pats = ctx.cfg.get("pii_patterns") or []
    if not pats:
        return ctx.unconfigured("R2", "pii_patterns", "add ID / phone / account regexes for your country")
    skip = ctx.cfg.get("pii_skip_before") or ""
    for f in ctx.all_files():
        t = f.read_text(encoding="utf-8")
        for name, p in pats:
            for m in re.finditer(p, t):
                if skip and re.search(skip, t[max(0, m.start() - 12):m.start()]):
                    continue
                ctx.rec("FAIL", "R2", f"possible {name}: {m.group(0)}", ctx.rel(f))


def r6_internal_language(ctx):
    """Delivered text must not contain internal working vocabulary (TODO, TBD, notes)."""
    words = ctx.cfg.get("internal_words") or []
    if not words:
        return ctx.unconfigured("R6", "internal_words", "list markers like TODO / TBD / 'internal note'")
    for f in ctx.deliver_files():
        t = ctx.clean_text(f)
        for b in words:
            if b in t:
                i = t.index(b)
                ctx.rec("FAIL", "R6", f"internal word '{b}' visible in delivered text",
                        f"{ctx.rel(f)}: ...{' '.join(t[max(0, i - 24):i + 26].split())}...")


# ── Numbers ledger ────────────────────────────────────────────────────────────
def _split_md_row(line):
    """Split a markdown table row on unescaped `|`; `\\|` inside a cell becomes `|`."""
    cells = re.split(r"(?<!\\)\|", line.strip().strip("|") if line.strip().startswith("|") else line)
    return [c.replace("\\|", "|").strip() for c in cells]


def ledger_rows(ctx):
    """Rows of the numbers ledger: dicts id/cur/old/src/where (+note).
    Accepts a markdown table (`| id | current | stale | source | where | note |`)
    or a TSV with the same column order. `#` lines, header and separator rows skipped."""
    path = ctx.cfg.get("ledger")
    if not path or not (ctx.root / path).exists():
        return []
    out = []
    for line in (ctx.root / path).read_text(encoding="utf-8").split("\n"):
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("<!--"):
            continue
        if s.startswith("|"):
            if re.fullmatch(r"\|[\s:|-]+\|", s):
                continue                       # separator row
            c = _split_md_row(s)
        elif "\t" in s:
            c = [x.strip() for x in s.split("\t")]
        else:
            continue
        if len(c) < 5 or c[0].lower() in ("id", "識別碼"):
            continue
        out.append(dict(id=c[0], cur=c[1], old=c[2], src=c[3], where=c[4],
                        note=c[5] if len(c) > 5 else ""))
    return out


def _num_variants(v: str):
    """Accept APA leading-zero-dropped forms: `.73` <-> `0.73`. Otherwise a ledger
    that records 0.73 while the manuscript writes .73 misfires on EVERY such value."""
    v = v.strip()
    out = {v}
    if re.fullmatch(r"0\.\d+", v):
        out.add(v[1:])
    elif re.fullmatch(r"\.\d+", v):
        out.add("0" + v)
    return out


def _find_value(val, text):
    return [m for v in _num_variants(val)
            for m in re.finditer(r"(?<![\d.])" + re.escape(v) + r"(?![\d.])", text)]


def r_stale_values(ctx):
    """R-STALE: a corrected OLD value must not reappear.

    🔴 Stale-value format: `value~anchor-regex`, several separated by `;` (`|` is
       reserved for the anchor's OR). The first version used `|` for both and
       scanned anchor fragments as stale values: 70 false alarms in one run.
    🔴 Bare small integers (32 / 48 / 64) MUST carry an anchor or they hit model
       numbers and other groups' correct values.
    🔴 Anchor = a distinctive fragment right next to the target. One anchor sat 65
       chars from its value with a ±60 window: the rule never fired."""
    rows = ledger_rows(ctx)
    if not rows:
        return ctx.unconfigured("R-STALE", "ledger", "point `ledger` at your numbers ledger")
    t = ctx.deliver_text()
    armed = 0
    for r in rows:
        if r["old"] in ("—", "", "-"):
            continue
        for item in r["old"].split(";"):
            val, _, anchor = item.strip().partition("~")
            if not val:
                continue
            armed += 1
            for m in _find_value(val, t):
                win = t[max(0, m.start() - 60):m.start() + 60]
                if anchor and not re.search(anchor, win):
                    continue
                ctx.rec("FAIL", "R-STALE",
                        f"{r['id']}: stale value {val} is back (current {r['cur']}, source {r['src']})",
                        " ".join(win.split()))
    if not armed:
        # Every `stale` cell is still "—": the rule runs but guards nothing yet.
        ctx.rec("INFO", "R-STALE", "ledger has no stale values yet — R-STALE has nothing to guard "
                                   "(normal for a first ledger; do not count it as a verified defence)")


def r_ledger_present(ctx):
    """R-LEDGER: every CURRENT value in the ledger must actually appear in the
    manuscript — otherwise an edit was missed or the ledger is behind.
    Missing -> WARN only: rewording can legitimately make a number disappear, and
    an unclear criterion never FAILs (design rule 1).
    Compound values split on `/`: `0.75/0.73` -> both must be present."""
    rows = ledger_rows(ctx)
    if not rows:
        return  # R-STALE already reported the unconfigured ledger
    t = ctx.deliver_text()
    for r in rows:
        cur = r["cur"]
        if cur in ("—", "", "-"):
            continue
        for v in cur.split("/"):
            if not _find_value(v, t):
                ctx.rec("WARN", "R-LEDGER",
                        f"{r['id']}: current value {v.strip()} not found in the manuscript "
                        f"(source {r['src']}, expected at {r['where']})")


# ── Example project-rule shapes (config-driven; each came from a real mistake) ──
def r_entity_attribution(ctx):
    """Some entity must always be accompanied by an attribution marker.
    Origin: other people's / students' works were written into a personal-
    achievement section, passed every mechanical check, survived seven rounds.
    Config `entities`: {"names": [...], "marks": [...]} — a paragraph that mentions
    a name without any mark FAILs."""
    ent = ctx.cfg.get("entities") or {}
    names, marks = ent.get("names") or [], ent.get("marks") or []
    if not names:
        return ctx.unconfigured("R-ATTR", "entities", "list entities needing attribution + accepted markers")
    for f in ctx.deliver_files():
        for para in re.split(r"\n\s*\n", ctx.clean_text(f)):
            for w in names:
                if w in para and not any(k in para for k in marks):
                    ctx.rec("FAIL", "R-ATTR", f"'{w}' needs attribution; this paragraph has none",
                            f"{ctx.rel(f)}: {' '.join(para.split())[:60]}...")


def r_corrected_claims(ctx):
    """A statement that was corrected once must not come back. One entry per catch,
    each with WHY it is wrong and where that was verified — so whoever wants to
    write it back can see the reason. Config `banned_claims`: [[phrase, why], ...]."""
    banned = ctx.cfg.get("banned_claims") or []
    if not banned:
        return ctx.unconfigured("R-CORR", "banned_claims", "register a corrected phrase after each catch")
    for f in ctx.deliver_files():
        t = ctx.clean_text(f)
        for bad, why in banned:
            if bad in t:
                i = t.index(bad)
                ctx.rec("FAIL", "R-CORR", f"corrected statement '{bad}' is back — {why}",
                        f"{ctx.rel(f)}: ...{' '.join(t[max(0, i - 20):i + 24].split())}...")


def r_fact_ledger(ctx):
    """Fact ledger: known WRONG values FAIL when they appear on the same line as
    the fact's keyword. Config `fact_ledger`:
      [{"name": ..., "anchor": regex, "wrong": [[regex, why], ...]}, ...]
    ⚠️ Register only known-wrong values. Do not generalise to "anything outside
       the allowed set is suspicious" — in timeline prose that produced 12 false
       alarms out of 12.
    ⚠️ Write the wrong value as a regex covering every spelling; registering one
       format missed the fourth recurrence.
    ⚠️ Window = same line only. Comparing across table rows always misfires."""
    facts = ctx.cfg.get("fact_ledger") or []
    if not facts:
        return ctx.unconfigured("R-FACT", "fact_ledger", "register known-wrong values per fact")
    for f in ctx.deliver_files():
        t = ctx.clean_text(f)
        for fact in facts:
            for bad, why in fact.get("wrong") or []:
                for mm in re.finditer(bad, t):
                    ls = t.rfind("\n", 0, mm.start()) + 1
                    le = t.find("\n", mm.end())
                    if re.search(fact["anchor"], t[ls: le if le != -1 else len(t)]):
                        ctx.rec("FAIL", "R-FACT", f"known-wrong value near '{fact['name']}' — {why}",
                                f"{ctx.rel(f)}: ...{' '.join(t[max(0, mm.start() - 30):mm.end() + 30].split())}...")


RULES = [r1_citations_numeric, r1_citations_bibtex, r2_pii, r6_internal_language,
         r_stale_values, r_ledger_present,
         r_entity_attribution, r_corrected_claims, r_fact_ledger]


# ═════════════════════════════════════════════════════════════════════════════
def load_config(path, root=None):
    path = Path(path).resolve()
    cfg = json.loads(path.read_text(encoding="utf-8"))
    cfg = {k: v for k, v in cfg.items() if not k.startswith("_")}   # `_comment` keys
    return Ctx(cfg, Path(root).resolve() if root else path.parent)


def load_extra(path):
    spec = importlib.util.spec_from_file_location("regress_extra", Path(path).resolve())
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    rules = getattr(m, "RULES", None)
    if not rules:
        sys.exit(f"[FAIL] {path}: no RULES list")
    return list(rules)


def run_rule(fn, ctx):
    """Rules take ctx; zero-argument rules (server-style skeletons) still work."""
    if len(inspect.signature(fn).parameters) == 0:
        return fn()
    return fn(ctx)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True, help="JSON config (start from rules.template.json)")
    ap.add_argument("--root", help="project root for relative paths (default: config dir)")
    ap.add_argument("--extra", help="Python file with project rules: RULES = [fn(ctx), ...]")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    a = ap.parse_args()

    ctx = load_config(a.config, a.root)
    rules = list(RULES) + (load_extra(a.extra) if a.extra else [])
    for fn in rules:
        try:
            run_rule(fn, ctx)
        except Exception as e:  # noqa: BLE001 — a crashing rule must be visible, not silent
            ctx.rec("WARN", fn.__name__, f"rule crashed: {type(e).__name__}: {e}")

    if a.json:
        print(json.dumps({"fail": ctx.FAIL, "warn": ctx.WARN, "info": ctx.INFO},
                         ensure_ascii=False, indent=1))
        return 1 if ctx.FAIL else 0

    print(f"=== regression suite: {len(rules)} rules (each one a mistake made once) ===\n")
    for lvl, items in (("FAIL", ctx.FAIL), ("WARN", ctx.WARN), ("INFO", ctx.INFO)):
        for d in items:
            print(f"[{lvl}] [{d['rule']}] {d['msg']}")
            if d["where"]:
                print(f"       {d['where']}")
    print(f"\n--- FAIL {len(ctx.FAIL)} | WARN {len(ctx.WARN)} | INFO {len(ctx.INFO)} ---")
    if not ctx.FAIL:
        print("[OK] no FAIL: none of the mistakes made before has come back.")
        print("     (This is not 'the document is correct' — new mistakes need a human.)")
    return 1 if ctx.FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
