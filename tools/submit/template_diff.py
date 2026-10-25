#!/usr/bin/env python3
"""template_diff.py: format comparison of a manuscript docx against an official template docx.

Why it exists: a journal template's margins, fonts and line spacing cannot be judged by eye;
a 0.5 cm margin difference or a different East Asian font is invisible in Word's window but
shows up in the editorial office's format check. This tool lists the manuscript's actual
settings next to the template's, mismatches first.

Usage:
  template_diff.py manuscript.docx template.docx [--json] [--only-diff]
Scope:
  - every section: paper size, orientation, top/bottom/left/right margins, header and footer
    distance, column count, different first page
  - document defaults (fonts and paragraph settings)
  - style definitions: Normal, every paragraph style the manuscript actually uses, and the
    Title / Heading styles the template also has (font ascii and eastAsia, size, bold/italic,
    line spacing, space before/after, first-line indent, alignment)
  - styles the manuscript uses that the template lacks, PAGE field, header and footer text
Inheritance: a property a style does not set is looked up along basedOn, then docDefaults;
  if still not found it reads "not set (Word default applies)", and two unset sides count as
  consistent. Unset bold / italic / left alignment / space 0 / indent 0 are compared as their
  Word defaults.
Limits: compares style DEFINITIONS only, not direct formatting on paragraphs (a hand-set
  font or indent); theme fonts that cannot be resolved are reported by theme name.
Requires python-docx.
Exit codes: 0 = consistent; 1 = differences; 2 = read error (including python-docx missing)
"""
import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
UNSET = "not set (Word default applies)"
TOL_TWIPS = 15            # about 0.26 mm; rounding by layout software is not a mismatch
PAPERS = {(21.0, 29.7): "A4", (21.59, 27.94): "Letter", (29.7, 42.0): "A3", (17.6, 25.0): "B5",
          (21.59, 35.56): "Legal", (14.8, 21.0): "A5"}


def fmt(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")


def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


class Rows:
    def __init__(self):
        self.rows = []

    def add(self, item, a, b, same=None):
        if same is None:
            same = (a == b)
        self.rows.append({"item": item, "manuscript": a, "template": b, "same": bool(same)})


# ---------------------------------------------------------------- style resolution

class Doc:
    def __init__(self, path):
        try:
            from docx import Document
        except ImportError:
            raise RuntimeError("python-docx is required (pip install python-docx)")
        self.path = path
        self.d = Document(path)
        root = self.d.styles.element
        self.root = root
        self.by_id, self.by_name, self.default_para = {}, {}, None
        for s in root.findall(W + "style"):
            self.by_id[s.get(W + "styleId")] = s
            nm = s.find(W + "name")
            if nm is not None:
                self.by_name[nm.get(W + "val", "").lower()] = s
            if s.get(W + "type") == "paragraph" and s.get(W + "default") in ("1", "true"):
                self.default_para = s
        dd = root.find(W + "docDefaults")
        self.def_r = dd.find(f"{W}rPrDefault/{W}rPr") if dd is not None else None
        self.def_p = dd.find(f"{W}pPrDefault/{W}pPr") if dd is not None else None
        self.theme = self._theme()

    def _theme(self):
        out = {}
        try:
            for part in self.d.part.package.iter_parts():
                if str(part.partname).endswith("/theme/theme1.xml"):
                    root = ET.fromstring(part.blob)
                    for grp in ("major", "minor"):
                        f = root.find(f".//{A}{grp}Font")
                        if f is None:
                            continue
                        for k, tag in (("latin", "latin"), ("ea", "ea"), ("cs", "cs")):
                            e = f.find(A + tag)
                            out[(grp, k)] = (e.get("typeface") or "") if e is not None else ""
        except Exception:
            pass
        return out

    def name_of(self, s):
        return s.find(W + "name").get(W + "val")

    def chain(self, s):
        seen, out = set(), []
        while s is not None and id(s) not in seen:
            seen.add(id(s))
            out.append(s)
            b = s.find(W + "basedOn")
            s = self.by_id.get(b.get(W + "val")) if b is not None else None
        return out

    def lookup(self, style, part, getter):
        """Walk up basedOn, then docDefaults, for the first value set; None if not found."""
        for s in self.chain(style) if style is not None else []:
            pr = s.find(W + part)
            v = getter(pr) if pr is not None else None
            if v is not None:
                return v
        pr = self.def_r if part == "rPr" else self.def_p
        return getter(pr) if pr is not None else None

    def font(self, style, kind):
        """Return (string to compare, string to display)."""
        attr, theme_attr = ("ascii", "asciiTheme") if kind == "ascii" else ("eastAsia", "eastAsiaTheme")

        def g(pr):
            rf = pr.find(W + "rFonts")
            if rf is None:
                return None
            if rf.get(W + theme_attr):
                return ("theme", rf.get(W + theme_attr))
            if rf.get(W + attr):
                return ("name", rf.get(W + attr))
            return None
        v = self.lookup(style, "rPr", g)
        if v is None:
            return UNSET, UNSET
        if v[0] == "name":
            return v[1], v[1]
        t = v[1]
        grp = "major" if t.lower().startswith("major") else "minor"
        rest = t[5:].lower()
        k = "ea" if rest.startswith("eastasia") else "cs" if rest.startswith(("bidi", "cs")) else "latin"
        face = self.theme.get((grp, k), "")
        if face:
            return face, f"{face} (theme:{t})"
        return f"theme:{t}", f"theme:{t} (actual font not resolved)"

    def size(self, style):
        v = self.lookup(style, "rPr", lambda pr: pr.find(W + "sz").get(W + "val") if pr.find(W + "sz") is not None else None)
        if v is None:
            return UNSET
        return f"{fmt(int(v) / 2)} pt"

    def toggle(self, style, tag):
        def g(pr):
            e = pr.find(W + tag)
            if e is None:
                return None
            return e.get(W + "val", "1").lower() not in ("0", "false", "off")
        v = self.lookup(style, "rPr", g)
        return v

    def jc(self, style):
        v = self.lookup(style, "pPr", lambda pr: pr.find(W + "jc").get(W + "val") if pr.find(W + "jc") is not None else None)
        return v

    def line(self, style):
        def g(pr):
            sp = pr.find(W + "spacing")
            if sp is not None and sp.get(W + "line"):
                return (int(sp.get(W + "line")), sp.get(W + "lineRule", "auto"))
            return None
        v = self.lookup(style, "pPr", g)
        if v is None:
            return UNSET
        n, rule = v
        if rule == "exact":
            return f"exactly {fmt(n / 20)} pt"
        if rule == "atLeast":
            return f"at least {fmt(n / 20)} pt"
        return f"{fmt(n / 240)}x"

    def space(self, style, which):
        def g(pr):
            sp = pr.find(W + "spacing")
            if sp is None:
                return None
            if sp.get(W + which + "Lines") is not None:
                return ("lines", int(sp.get(W + which + "Lines")))
            if sp.get(W + which) is not None:
                return ("tw", int(sp.get(W + which)))
            return None
        v = self.lookup(style, "pPr", g)
        if v is None:
            return UNSET, "0 pt"
        if v[0] == "lines":
            s = f"{fmt(v[1] / 100)} lines"
        else:
            s = f"{fmt(v[1] / 20)} pt"
        return s, ("0 pt" if v[1] == 0 else s)

    def indent(self, style):
        def g(pr):
            e = pr.find(W + "ind")
            if e is None:
                return None
            d = {k: e.get(W + k) for k in ("firstLineChars", "firstLine", "hangingChars", "hanging")}
            return d if any(v is not None for v in d.values()) else None
        v = self.lookup(style, "pPr", g)
        if v is None:
            return UNSET, "first line 0"
        if v["firstLineChars"] is not None:
            s = f"first line {fmt(int(v['firstLineChars']) / 100)} chars"
        elif v["firstLine"] is not None:
            s = f"first line {fmt(int(v['firstLine']) / 20)} pt"
        elif v["hangingChars"] is not None:
            s = f"hanging {fmt(int(v['hangingChars']) / 100)} chars"
        else:
            s = f"hanging {fmt(int(v['hanging']) / 20)} pt"
        return s, ("first line 0" if re.fullmatch(r"(first line|hanging) 0( pt| chars)?", s) else s)

    def used_styles(self):
        """Paragraph styles the manuscript actually uses -> paragraph count (an unstyled paragraph counts as the default paragraph style)."""
        counts = {}
        body = self.d.element.body
        for p in body.iter(W + "p"):
            ps = p.find(f"{W}pPr/{W}pStyle")
            s = self.by_id.get(ps.get(W + "val")) if ps is not None else self.default_para
            if s is None:
                continue
            nm = self.name_of(s)
            counts[nm] = counts.get(nm, 0) + 1
        return counts


def pretty(nm):
    return re.sub(r"^(heading \d|title|subtitle)$", lambda m: m.group(1).capitalize(), nm)


def paper_name(wcm, hcm):
    for (pw, ph), nm in PAPERS.items():
        if abs(wcm - pw) < 0.1 and abs(hcm - ph) < 0.1:
            return nm
        if abs(wcm - ph) < 0.1 and abs(hcm - pw) < 0.1:
            return nm
    return "custom"


def sections_info(doc):
    out = []
    for sec in doc.d.sections:
        el = sec._sectPr
        cols = el.find(W + "cols")
        ncols = int(cols.get(W + "num", "1")) if cols is not None else 1
        w, h = sec.page_width, sec.page_height

        def tw(v):
            return None if v is None else round(v.twips)
        out.append({
            "w": tw(w), "h": tw(h), "orient": "landscape" if str(sec.orientation).endswith("LANDSCAPE (1)") or (w and h and w > h) else "portrait",
            "top": tw(sec.top_margin), "bottom": tw(sec.bottom_margin), "left": tw(sec.left_margin), "right": tw(sec.right_margin),
            "header": tw(sec.header_distance), "footer": tw(sec.footer_distance), "cols": ncols,
            "first": bool(sec.different_first_page_header_footer),
        })
    return out


def cm(tw):
    return None if tw is None else tw / 567.0


def hf_info(doc):
    """Return (has a PAGE field, header text, footer text); sections linked to the previous one are not counted twice."""
    has_page, htxt, ftxt = False, [], []
    for sec in doc.d.sections:
        for kind, store in (("header", htxt), ("footer", ftxt)):
            for suffix in ("", "first_page_", "even_page_"):
                part = getattr(sec, suffix + kind)
                if part.is_linked_to_previous:
                    continue
                el = part._element
                txt = " ".join(p.text for p in part.paragraphs if p.text.strip())
                if txt:
                    store.append(txt)
                for instr in el.iter(W + "instrText"):
                    if re.search(r"\bPAGE\b", instr.text or ""):
                        has_page = True
                for fs in el.iter(W + "fldSimple"):
                    if re.search(r"\bPAGE\b", fs.get(W + "instr", "")):
                        has_page = True
    return has_page, " | ".join(htxt), " | ".join(ftxt)


def compare(ms, tp):
    R = Rows()
    # --- sections
    sm, st = sections_info(ms), sections_info(tp)
    R.add("Section count", str(len(sm)), str(len(st)))
    for i in range(max(len(sm), len(st))):
        a = sm[i] if i < len(sm) else None
        b = st[i] if i < len(st) else None
        tag = f"Section {i + 1}"
        if a is None or b is None:
            R.add(f"{tag} exists", "yes" if a else "no", "yes" if b else "no")
            continue
        sa = f"{fmt(cm(a['w']))}×{fmt(cm(a['h']))} cm（{paper_name(cm(a['w']), cm(a['h']))}）"
        sb = f"{fmt(cm(b['w']))}×{fmt(cm(b['h']))} cm（{paper_name(cm(b['w']), cm(b['h']))}）"
        R.add(f"{tag} paper size", sa, sb, abs(a["w"] - b["w"]) <= TOL_TWIPS and abs(a["h"] - b["h"]) <= TOL_TWIPS)
        R.add(f"{tag} orientation", a["orient"], b["orient"])
        for key, nm in (("top", "top margin"), ("bottom", "bottom margin"), ("left", "left margin"), ("right", "right margin"),
                        ("header", "header distance"), ("footer", "footer distance")):
            va, vb = a[key], b[key]
            R.add(f"{tag} {nm}", f"{fmt(cm(va))} cm" if va is not None else UNSET,
                  f"{fmt(cm(vb))} cm" if vb is not None else UNSET,
                  (va is None and vb is None) or (va is not None and vb is not None and abs(va - vb) <= TOL_TWIPS))
        R.add(f"{tag} columns", str(a["cols"]), str(b["cols"]))
        R.add(f"{tag} different first page", "yes" if a["first"] else "no", "yes" if b["first"] else "no")

    # --- docDefaults
    for kind, nm in (("ascii", "default font (ascii)"), ("eastAsia", "default font (eastAsia)")):
        fa, fb = ms.font(None, kind), tp.font(None, kind)
        R.add(nm, fa[1], fb[1], fa[0] == fb[0])
    R.add("default font size", ms.size(None), tp.size(None))
    R.add("default line spacing", ms.line(None), tp.line(None))
    sa, sb = ms.space(None, "after"), tp.space(None, "after")
    R.add("default space after", sa[0], sb[0], sa[1] == sb[1])

    # --- styles
    used_m = ms.used_styles()
    used_t = tp.used_styles()
    order = ["Normal"] + [n for n, _ in sorted(used_m.items(), key=lambda kv: -kv[1]) if n != "Normal"]
    for n in used_t:
        if re.match(r"(heading \d|title|subtitle)$", n.lower()) and n not in order and n.lower() in ms.by_name:
            order.append(n)
    # the real name of Normal can differ by locale; the default paragraph style decides
    if ms.default_para is not None:
        order[0] = ms.name_of(ms.default_para)
    missing = []
    for nm in order:
        sm_ = ms.by_name.get(nm.lower())
        st_ = tp.by_name.get(nm.lower())
        if sm_ is None:
            continue
        if st_ is None:
            missing.append(f"{nm} ({used_m.get(nm, 0)} paragraphs)")
            continue
        lab = f'Style "{pretty(nm)}"'
        for kind, k in (("ascii", "font (ascii)"), ("eastAsia", "font (eastAsia)")):
            fa, fb = ms.font(sm_, kind), tp.font(st_, kind)
            R.add(f"{lab} {k}", fa[1], fb[1], fa[0] == fb[0])
        R.add(f"{lab} font size", ms.size(sm_), tp.size(st_))
        for tag, k in (("b", "bold"), ("i", "italic")):
            va, vb = ms.toggle(sm_, tag), tp.toggle(st_, tag)
            show = lambda v: UNSET if v is None else ("yes" if v else "no")
            R.add(f"{lab} {k}", show(va), show(vb), bool(va) == bool(vb))
        R.add(f"{lab} line spacing", ms.line(sm_), tp.line(st_))
        for which, k in (("before", "space before"), ("after", "space after")):
            xa, xb = ms.space(sm_, which), tp.space(st_, which)
            R.add(f"{lab} {k}", xa[0], xb[0], xa[1] == xb[1])
        ia, ib = ms.indent(sm_), tp.indent(st_)
        R.add(f"{lab} first-line indent", ia[0], ib[0], ia[1] == ib[1])
        ja, jb = ms.jc(sm_), tp.jc(st_)
        norm = lambda v: "left" if v in (None, "left", "start") else v
        R.add(f"{lab} alignment", UNSET if ja is None else ja, UNSET if jb is None else jb, norm(ja) == norm(jb))
    R.add("styles used by the manuscript but missing from the template", ", ".join(missing) if missing else "none", "n/a", not missing)

    # --- page numbers, headers and footers
    pa, ha, fa_ = hf_info(ms)
    pb, hb, fb_ = hf_info(tp)
    R.add("page number field (PAGE)", "yes" if pa else "no", "yes" if pb else "no")
    R.add("header text", ha or "(empty)", hb or "(empty)", re.sub(r"\s+", " ", ha) == re.sub(r"\s+", " ", hb))
    R.add("footer text", fa_ or "(empty)", fb_ or "(empty)", re.sub(r"\s+", " ", fa_) == re.sub(r"\s+", " ", fb_))
    return R.rows


def main():
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    ap.add_argument("manuscript")
    ap.add_argument("template")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--only-diff", action="store_true", help="list only the mismatching rows in the table")
    a = ap.parse_args()
    try:
        ms, tp = Doc(a.manuscript), Doc(a.template)
    except Exception as e:
        print(f"read error: {e}", file=sys.stderr)
        sys.exit(2)
    try:
        rows = compare(ms, tp)
    except Exception as e:
        print(f"comparison failed: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(2)
    rows.sort(key=lambda r: r["same"])      # stable sort: mismatches first
    diff = sum(1 for r in rows if not r["same"])
    if a.json:
        print(json.dumps({"rows": rows, "mismatch": diff}, ensure_ascii=False, indent=2))
    else:
        print(f"Manuscript: {a.manuscript}\nTemplate: {a.template}\n")
        print("| Item | Manuscript | Template | Same? |\n|---|---|---|---|")
        for r in rows:
            if a.only_diff and r["same"]:
                continue
            print(f"| {esc(r['item'])} | {esc(r['manuscript'])} | {esc(r['template'])} | {'yes' if r['same'] else 'no'} |")
        print(f"\nNote: {len(rows)} items compared; style definitions only, not direct formatting on paragraphs.")
        print(f"Mismatches: {diff}")
    sys.exit(1 if diff else 0)


if __name__ == "__main__":
    main()
