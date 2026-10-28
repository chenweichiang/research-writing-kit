#!/usr/bin/env python3
"""docx_diff.py: compare two Word files and list every change (for when a co-author returns
a file without tracked changes).

Why it exists: a co-author edits the Word file we sent and sends it back, very often with
"Track Changes" switched off. Someone then has to compare old and new paragraph by
paragraph and carry each change back into the source file (usually Markdown). This tool
lists what was modified, deleted, inserted or moved, so the changes can be applied one by
one (--json) and the author can read them at a glance (--out report).

How it differs from source_trace.py:
  docx_diff     old vs new: "what differs" in a returned file, paragraph by paragraph.
                It does not judge whether the new text has a source.
  source_trace  every sentence of a new draft: "can it be traced back to the original?"
                It is the source gate for our own rewrite of a co-author's manuscript.
  Run docx_diff first to see what the other person touched; after rewriting, run
  source_trace to confirm nothing was added from thin air.

What is compared: body paragraphs (headings included, with style and level), tables (cell
by cell), headers and footers, footnotes and endnotes. Images are compared by count and
by which paragraph holds them, not by content. The tool does not produce a docx with
tracked changes (use Word's Review > Compare for a visual version) and does not write back
to the source file. It also reports whether the new file still contains tracked changes
(w:ins / w:del) and lists its comments, so you know if the co-author did turn tracking on.

Alignment: identical paragraphs are matched first (difflib LCS); within each unmatched
stretch, paragraphs are paired by similarity (ratio >= --min-ratio means "modified",
otherwise one deletion plus one insertion). A deletion and an insertion with identical
text are reported as a "move". Paragraph numbers count non-empty paragraphs from 1.

Usage:
  docx_diff.py OLD.docx NEW.docx [--out report.md] [--json changes.json] [--context 1] [--min-ratio 0.5]
Exit codes: 0 no difference; 1 differences found; 2 read error (or missing dependency).
Needs lxml (installed together with python-docx): pip install python-docx
"""
import argparse
import difflib
import json
import re
import sys
import unicodedata
import zipfile

try:
    from lxml import etree
except ImportError:  # reported from main() with an install hint
    etree = None

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def q(tag):
    return "{%s}%s" % (W, tag)


TYPE_MOD, TYPE_ADD, TYPE_DEL, TYPE_MOVE, TYPE_CELL = "modified", "added", "deleted", "moved", "table cell modified"
TYPE_STYLE, TYPE_IMG = "style changed", "image changed"
ALL_TYPES = [TYPE_MOD, TYPE_ADD, TYPE_DEL, TYPE_MOVE, TYPE_CELL, TYPE_STYLE, TYPE_IMG]
R_BODY, R_TABLE, R_HEADER, R_FOOTER, R_FOOTNOTE, R_ENDNOTE = "body", "table", "header", "footer", "footnote", "endnote"
REGION_ORDER = [R_BODY, R_TABLE, R_HEADER, R_FOOTER, R_FOOTNOTE, R_ENDNOTE]
UNSIGNED = "(unsigned)"
# Heading style names: English Word ("Heading 1") and Chinese-locale Word ("標題 1").
HEADING_RE = re.compile(r"^(?:heading|標題)\s*(\d+)$", re.I)
# One CJK character, one Latin word, one whitespace run, or any other single character.
TOKEN_RE = re.compile(r"[一-鿿㐀-䶿]|[A-Za-z0-9_'’\-]+|\s+|.", re.S)


# ---------------------------------------------------------------- extraction
def para_text(p):
    """Paragraph text: only w:t (deleted runs hold w:delText, so they drop out, which shows
    the paragraph as it looks after 'accept all changes')."""
    out = []
    for el in p.iter():
        if el.tag == q("t"):
            out.append(el.text or "")
        elif el.tag == q("tab"):
            out.append("\t")
        elif el.tag == q("br"):
            out.append("\n")
    return "".join(out)


def para_images(p):
    return len(p.findall(".//w:drawing", NS)) + len(p.findall(".//w:pict", NS))


def unwrap(children):
    for el in children:
        if el.tag == q("sdt"):
            c = el.find("w:sdtContent", NS)
            if c is not None:
                yield from unwrap(list(c))
        else:
            yield el


class Doc:
    """The blocks extracted from one file. paras: body paragraph sequence; cells:
    {(table, row, col): text}; the other regions are paragraph sequences."""

    def __init__(self, path):
        self.path = path
        self.notes = []          # parts that were not compared
        self.zf = zipfile.ZipFile(path)
        self.styles = self._style_names()
        self.paras, self.cells, self.table_dims = [], {}, {}
        self.regions = {R_HEADER: [], R_FOOTER: [], R_FOOTNOTE: [], R_ENDNOTE: []}
        self._body()
        self._headers_footers()
        self._notes("word/footnotes.xml", R_FOOTNOTE)
        self._notes("word/endnotes.xml", R_ENDNOTE)
        self.images = sum(p["imgs"] for p in self.paras)
        self.revisions = self._revisions()
        self.comments = self._comments()
        self.props = self._props()

    def _xml(self, name):
        try:
            return etree.fromstring(self.zf.read(name))
        except KeyError:
            return None

    def _style_names(self):
        root = self._xml("word/styles.xml")
        m = {}
        if root is not None:
            for s in root.findall("w:style", NS):
                n = s.find("w:name", NS)
                if n is not None:
                    m[s.get(q("styleId"))] = n.get(q("val"))
        return m

    def _record(self, p, idx, heading_ctx):
        ps = p.find("w:pPr/w:pStyle", NS)
        sid = ps.get(q("val")) if ps is not None else None
        style = self.styles.get(sid, sid or "Normal")
        m = HEADING_RE.match(style or "")
        return {"text": para_text(p), "style": style, "level": int(m.group(1)) if m else 0,
                "imgs": para_images(p), "index": idx}

    def _body(self):
        root = self._xml("word/document.xml")
        if root is None:
            raise ValueError("word/document.xml not found: this does not look like a docx file")
        body = root.find("w:body", NS)
        n, t, heading = 0, 0, ""
        for el in unwrap(list(body)):
            if el.tag == q("p"):
                r = self._record(el, 0, heading)
                if not r["text"].strip() and not r["imgs"]:
                    continue
                n += 1
                r["index"] = n
                if r["level"] or (r["style"] or "").lower() == "title":
                    heading = r["text"].strip()
                r["heading"] = heading
                self.paras.append(r)
            elif el.tag == q("tbl"):
                t += 1
                rows = el.findall("w:tr", NS)
                maxc = 0
                for ri, tr in enumerate(rows, 1):
                    tcs = tr.findall("w:tc", NS)
                    maxc = max(maxc, len(tcs))
                    for ci, tc in enumerate(tcs, 1):
                        txt = "\n".join(para_text(p) for p in tc.findall("w:p", NS)).strip()
                        self.cells[(t, ri, ci)] = {"text": txt, "heading": heading}
                self.table_dims[t] = (len(rows), maxc)

    def _part_paras(self, name, region, nodes_path):
        root = self._xml(name)
        if root is None:
            return
        for p in root.findall(nodes_path, NS):
            txt = para_text(p)
            if txt.strip():
                self.regions[region].append({"text": txt, "style": "", "level": 0, "imgs": 0,
                                             "index": len(self.regions[region]) + 1, "heading": name.split("/")[-1]})

    def _headers_footers(self):
        for nm in sorted(self.zf.namelist()):
            m = re.match(r"word/(header|footer)\d*\.xml$", nm)
            if m:
                try:
                    self._part_paras(nm, R_HEADER if m.group(1) == "header" else R_FOOTER, ".//w:p")
                except Exception as e:
                    self.notes.append(f"{nm} could not be read ({e}); not compared")

    def _notes(self, name, region):
        try:
            root = self._xml(name)
            if root is None:
                return
            for note in root:
                if note.get(q("type")) in ("separator", "continuationSeparator", "continuationNotice"):
                    continue
                for p in note.findall(".//w:p", NS):
                    txt = para_text(p)
                    if txt.strip():
                        self.regions[region].append({"text": txt, "style": "", "level": 0, "imgs": 0,
                                                     "index": len(self.regions[region]) + 1,
                                                     "heading": f"{region} {note.get(q('id'))}"})
        except Exception as e:
            self.notes.append(f"{name} could not be read ({e}); {region}s not compared")

    def _revisions(self):
        root = self._xml("word/document.xml")
        res = {"ins": {}, "del": {}}
        for kind in ("ins", "del"):
            for el in root.iter(q(kind)):
                a = el.get(q("author")) or UNSIGNED
                res[kind][a] = res[kind].get(a, 0) + 1
        return res

    def _comments(self):
        out = []
        try:
            croot = self._xml("word/comments.xml")
            if croot is None:
                return out
            droot = self._xml("word/document.xml")
            anchors = {}
            for s in droot.iter(q("commentRangeStart")):
                p = next((a for a in s.iterancestors() if a.tag == q("p")), None)
                anchors[s.get(q("id"))] = para_text(p) if p is not None else ""
            for c in croot.findall("w:comment", NS):
                cid = c.get(q("id"))
                text = "\n".join(para_text(p) for p in c.findall(".//w:p", NS)).strip()
                out.append({"author": c.get(q("author")) or UNSIGNED, "text": text,
                            "anchor": anchors.get(cid, "").strip()[:30]})
        except Exception as e:
            self.notes.append(f"comments could not be read ({e}); not compared")
        return out

    def _props(self):
        root = self._xml("docProps/core.xml")
        res = {"author": "", "last_modified_by": "", "modified": ""}
        if root is not None:
            for el in root:
                tag = etree.QName(el).localname
                if tag == "creator":
                    res["author"] = el.text or ""
                elif tag == "lastModifiedBy":
                    res["last_modified_by"] = el.text or ""
                elif tag == "modified":
                    res["modified"] = el.text or ""
        return res


# ---------------------------------------------------------------- differences
def tokens(s):
    return TOKEN_RE.findall(s)


def char_diff(old, new):
    a, b = tokens(old), tokens(new)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            out.append("".join(a[i1:i2]))
            continue
        if i2 > i1:
            out.append("[-" + "".join(a[i1:i2]) + "-]")
        if j2 > j1:
            out.append("{+" + "".join(b[j1:j2]) + "+}")
    return "".join(out)


def strip_punct(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0] not in "PZSC")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


class Differ:
    def __init__(self, old, new, min_ratio):
        self.old, self.new, self.min_ratio = old, new, min_ratio
        self.changes = []
        self.seq = 0

    def add(self, **kw):
        self.seq += 1
        kw.setdefault("old_index", None)
        kw.setdefault("new_index", None)
        kw.setdefault("old", "")
        kw.setdefault("new", "")
        kw["punct_only"] = False
        if kw["type"] in (TYPE_MOD, TYPE_CELL) and kw["old"] != kw["new"]:
            kw["punct_only"] = strip_punct(kw["old"]) == strip_punct(kw["new"])
        kw["diff"] = char_diff(kw["old"], kw["new"]) if kw["type"] in (TYPE_MOD, TYPE_CELL, TYPE_STYLE) else ""
        kw["_order"] = self.seq
        self.changes.append(kw)
        return kw

    def seq_region(self, region, olds, news):
        sm = difflib.SequenceMatcher(None, [norm(p["text"]) for p in olds],
                                     [norm(p["text"]) for p in news], autojunk=False)
        dels, adds = [], []     # changes not yet paired, for move detection
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                for k in range(i2 - i1):
                    o, n = olds[i1 + k], news[j1 + k]
                    if o["style"] != n["style"] or o["level"] != n["level"]:
                        self.add(type=TYPE_STYLE, region=region, heading=n.get("heading", ""),
                                 old_index=o["index"], new_index=n["index"], old=o["text"], new=n["text"],
                                 note=f"style {o['style']} → {n['style']}")
                    elif o["imgs"] != n["imgs"]:
                        self.add(type=TYPE_IMG, region=region, heading=n.get("heading", ""),
                                 old_index=o["index"], new_index=n["index"], old=o["text"], new=n["text"],
                                 note=f"images in this paragraph {o['imgs']} → {n['imgs']}")
                continue
            gold, gnew = olds[i1:i2], news[j1:j2]
            pairs, used_n = [], set()
            for oi, o in enumerate(gold):         # greedy: each old paragraph takes the most similar unused new one
                best, bj = 0.0, None
                for nj, n in enumerate(gnew):
                    if nj in used_n:
                        continue
                    r = difflib.SequenceMatcher(None, o["text"], n["text"], autojunk=False).ratio()
                    if r > best:
                        best, bj = r, nj
                if bj is not None and best >= self.min_ratio:
                    pairs.append((oi, bj))
                    used_n.add(bj)
            paired_o = {a for a, _ in pairs}
            # emit in document order, keyed mainly on the new position
            pair_by_new = {b: a for a, b in pairs}
            ev = []
            for oi, o in enumerate(gold):
                if oi not in paired_o:
                    ev.append((oi, 0, "del", oi, None))
            for nj in range(len(gnew)):
                ev.append((pair_by_new.get(nj, 10**6) if nj in pair_by_new else 10**6 + nj, 1,
                           "mod" if nj in pair_by_new else "add", pair_by_new.get(nj), nj))
            # simple ordering: deletions by old order, modifications/additions by new order, interleaved by old order
            ev.sort(key=lambda e: (e[0] if e[2] == "del" else (e[3] if e[2] == "mod" else 10**6 + e[4])))
            for _, _, kind, oi, nj in ev:
                if kind == "del":
                    o = gold[oi]
                    dels.append(self.add(type=TYPE_DEL, region=region, heading=o.get("heading", ""),
                                         old_index=o["index"], old=o["text"]))
                elif kind == "mod":
                    o, n = gold[oi], gnew[nj]
                    self.add(type=TYPE_MOD, region=region, heading=n.get("heading", ""),
                             old_index=o["index"], new_index=n["index"], old=o["text"], new=n["text"],
                             note=("images %d → %d" % (o["imgs"], n["imgs"])) if o["imgs"] != n["imgs"] else "")
                else:
                    n = gnew[nj]
                    adds.append(self.add(type=TYPE_ADD, region=region, heading=n.get("heading", ""),
                                         new_index=n["index"], new=n["text"]))
        # moves: a deletion and an addition with identical text
        for d in list(dels):
            for a in adds:
                if a["type"] == TYPE_ADD and norm(a["old"] + a["new"]) and norm(d["old"]) == norm(a["new"]):
                    a["type"] = TYPE_MOVE
                    a["old_index"], a["old"] = d["old_index"], d["old"]
                    a["note"] = (f"was in \"{d['heading'] or '(start of document)'}\" paragraph {d['old_index']}, "
                                 f"now in \"{a['heading'] or '(start of document)'}\" paragraph {a['new_index']}")
                    self.changes.remove(d)
                    dels.remove(d)
                    break

    def tables(self):
        keys = sorted(set(self.old.cells) | set(self.new.cells))
        for k in keys:
            t, r, c = k
            o, n = self.old.cells.get(k), self.new.cells.get(k)
            loc = f"table {t} (row {r}, column {c})"
            if o and n:
                if norm(o["text"]) != norm(n["text"]):
                    self.add(type=TYPE_CELL, region=R_TABLE, heading=n["heading"], old=o["text"], new=n["text"],
                             old_index=None, new_index=None, note=loc, table=[t, r, c])
            elif n:
                if n["text"].strip():
                    self.add(type=TYPE_ADD, region=R_TABLE, heading=n["heading"], new=n["text"],
                             note=loc + " cell added", table=[t, r, c])
            elif o["text"].strip():
                self.add(type=TYPE_DEL, region=R_TABLE, heading=o["heading"], old=o["text"],
                         note=loc + " cell deleted", table=[t, r, c])

    def run(self):
        self.seq_region(R_BODY, self.old.paras, self.new.paras)
        self.tables()
        for reg in (R_HEADER, R_FOOTER, R_FOOTNOTE, R_ENDNOTE):
            self.seq_region(reg, self.old.regions[reg], self.new.regions[reg])
        if self.old.images != self.new.images:
            self.add(type=TYPE_IMG, region=R_BODY, heading="(whole document)",
                     note=f"image count in the whole document {self.old.images} → {self.new.images}")
        self.changes.sort(key=lambda c: (REGION_ORDER.index(c["region"]), c["new_index"] or c["old_index"] or 0,
                                         c["_order"]) if c["region"] != R_TABLE else (1, 0, c["_order"]))
        for i, c in enumerate(self.changes, 1):
            c["id"] = i
            c.pop("_order", None)
        return self.changes


# ---------------------------------------------------------------- report
def short(s, n=60):
    s = s.replace("\n", " ⏎ ")
    return s if len(s) <= n else s[:n] + "…"


def build_report(old, new, changes, ctx):
    L = ["# docx comparison report", "", f"- Old: {old.path}", f"- New: {new.path}", ""]
    L.append("## File information")
    for k, label in (("author", "Author"), ("last_modified_by", "Last modified by"), ("modified", "Modified")):
        L.append(f"- {label}: old {old.props[k] or '(empty)'}; new {new.props[k] or '(empty)'}")
    ins, dele = new.revisions["ins"], new.revisions["del"]
    L.append("")
    if ins or dele:
        who = ", ".join(sorted(set(ins) | set(dele)))
        L.append(f"- Tracked changes: the new file **has** tracked changes (authors: {who}; "
                 f"{sum(ins.values())} insertions, {sum(dele.values())} deletions). "
                 "The other person did turn tracking on; reading the revisions directly is more accurate.")
    else:
        L.append("- Tracked changes: the new file has none (w:ins and w:del are both 0).")
    if new.comments:
        L.append(f"- Comments: the new file has {len(new.comments)}")
        for c in new.comments:
            L.append(f"  - {c['author']} (anchored at \"{c['anchor']}\"): {short(c['text'], 200)}")
    else:
        L.append("- Comments: the new file has none.")
    if old.comments:
        L.append(f"- The old file also has {len(old.comments)} comments (not listed).")
    for n in old.notes + new.notes:
        L.append(f"- Not compared: {n}")
    L.append(f"- Image count: old {old.images}, new {new.images} (counts only, not content)")

    L += ["", "## Summary"]
    if not changes:
        L.append("The two files have identical content.")
    else:
        cnt = {}
        for c in changes:
            cnt[c["type"]] = cnt.get(c["type"], 0) + 1
        L.append(f"{len(changes)} changes: " + ", ".join(f"{t} {cnt[t]}" for t in ALL_TYPES if t in cnt))
        secs = []
        for c in changes:
            h = c["heading"] or "(start of document)"
            if h not in secs:
                secs.append(h)
        L.append("Sections affected: " + "; ".join(secs))

    trivial = [c for c in changes if c["punct_only"]]
    main = [c for c in changes if not c["punct_only"]]
    L += ["", "## Change list"]
    if trivial:
        L.append(f"({len(trivial)} more changes are punctuation or whitespace only; see the folded section at the end)")
    for c in main:
        L += ["", _entry(c, old, new, ctx)]
    if trivial:
        L += ["", "## Punctuation or whitespace only (folded)", f"{len(trivial)} changes: " +
              "; ".join(f"#{c['id']} ({c['heading'] or 'start'}, paragraph {c['new_index'] or c['old_index'] or '-'})"
                        for c in trivial)]
        L.append("For details use --json; these entries have punct_only set to true.")
    L += ["", "---", "Reminder: for a visual, change-by-change view open both files in Word with Review > Compare; "
          "this tool does not produce a docx with tracked changes."]
    return "\n".join(L) + "\n"


def _entry(c, old, new, ctx):
    loc = c["heading"] or "(start of document)"
    idx = []
    if c["old_index"]:
        idx.append(f"old paragraph {c['old_index']}")
    if c["new_index"]:
        idx.append(f"new paragraph {c['new_index']}")
    head = f"### #{c['id']} {c['type']} | {c['region']} | {loc}" + (f" | {', '.join(idx)}" if idx else "")
    L = [head]
    if c.get("note"):
        L.append(f"- Note: {c['note']}")
    if ctx:
        src = new.paras if c["new_index"] else old.paras
        i = (c["new_index"] or c["old_index"] or 0) - 1
        if c["region"] == R_BODY and i >= 0:
            for p in src[max(0, i - ctx):i]:
                L.append(f"- Preceding text: {short(p['text'], 40)}")
    if c["type"] in (TYPE_MOD, TYPE_CELL):
        L += [f"- Old text: {c['old']}", f"- New text: {c['new']}", f"- Diff: {c['diff']}"]
    elif c["type"] == TYPE_ADD:
        L.append(f"- New text: {c['new']}")
    elif c["type"] == TYPE_DEL:
        L.append(f"- Old text: {c['old']}")
    elif c["type"] == TYPE_MOVE:
        L.append(f"- Text: {c['new']}")
    elif c["type"] == TYPE_STYLE:
        L.append(f"- Text: {short(c['new'], 80)}")
    return "\n".join(L)


# ---------------------------------------------------------------- entry point
def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError, OSError):
            pass
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    ap.add_argument("old")
    ap.add_argument("new")
    ap.add_argument("--out", help="write the markdown report to this file (default: print to the screen)")
    ap.add_argument("--json", help="write the structured change list to this file")
    ap.add_argument("--context", type=int, default=1,
                    help="how many preceding paragraphs to show for locating each change (default 1)")
    ap.add_argument("--min-ratio", type=float, default=0.5,
                    help="similarity at or above which two paragraphs count as 'modified' (default 0.5)")
    a = ap.parse_args(argv)
    if etree is None:
        print("error: this tool needs lxml. Install it with: pip install python-docx", file=sys.stderr)
        return 2
    try:
        old, new = Doc(a.old), Doc(a.new)
    except Exception as e:
        print(f"read error: {e}", file=sys.stderr)
        return 2
    changes = Differ(old, new, a.min_ratio).run()
    report = build_report(old, new, changes, a.context)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(report)
    else:
        print(report)
    if a.json:
        keys = ("id", "type", "region", "heading", "old_index", "new_index", "old", "new", "diff", "punct_only", "note")
        data = [{k: c.get(k, "") for k in keys} for c in changes]
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    return 1 if changes else 0


if __name__ == "__main__":
    sys.exit(main())
