#!/usr/bin/env python3
"""anon_check.py: anonymization check before double-blind review: metadata, comments and tracked
changes, names and affiliations in the text, hyperlinks, embedded-image EXIF.

Why it exists: anonymity leaks raise no error. A docx's creator field, a tracked change's
author, an image's EXIF Artist tag are all visible to a reviewer who opens the file
properties, and completely invisible to the author looking at the Word window.

Usage:
  anon_check.py FILE_OR_FOLDER... --names "Jane Doe,Doe, J."
      [--affil "Example University,EU"] [--extra "janedoe,example.org"] [--json]

  - Reads .docx, .pdf, images (jpg/png/tif/heic ...) and folders (recursively).
  - Lists are comma-separated; "Doe, J." (surname, initial) is glued back together
    automatically. If a list contains a semicolon (;) it is split on semicolons only, so
    commas may be used inside an entry.
  - A two-word Latin name also gets its reversed forms ("Doe Jane", "Doe, Jane") added.

Severity: name / affiliation / extra string hit, metadata containing a name, EXIF GPS or
            author, leftover tracked changes or comments
          🟠 self-disclosure phrasing (a human must judge), identifiable metadata that is not a
            listed name, an empty run, an area that could not be checked
          🟢 the list of areas that were actually checked
Optional dependencies (degrade with a clear message, never silently): exiftool (image and
embedded-image EXIF), PyMuPDF (PDF files). Without exiftool the EXIF areas are reported as
"not checked" (🟠); without PyMuPDF a PDF is reported as unreadable (exit 2).
Exit codes: 0 = no ; 1 = at least one ; 2 = at least one file could not be read (takes
priority over 1)
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
import xml.etree.ElementTree as ET

RED, ORG, GRN = "🔴", "🟠", "🟢"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
IMG_EXT = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".heic", ".heif", ".webp", ".gif"}
HIT_CAP = 5            # at most this many entries per area and term; the rest are merged into "N more"

AUTHOR_TAGS = {"artist", "author", "creator", "ownername", "cameraownername", "by-line", "byline",
               "writer-editor", "copyright", "copyrightnotice", "rights", "credit", "xpauthor",
               "lastmodifiedby", "owner"}
SOFT_TAGS = {"serialnumber", "bodyserialnumber", "internalserialnumber", "lensserialnumber",
             "usercomment", "xpcomment"}
SKIP_GROUPS = {"System", "File", "ExifTool"}   # file name and path are not metadata
TRACK_TAGS = {"ins", "del", "moveFrom", "moveTo", "rPrChange", "pPrChange", "sectPrChange",
              "tblPrChange", "tcPrChange", "trPrChange", "numberingChange", "cellIns", "cellDel",
              "cellMerge", "tblGridChange"}

DISCLOSURE = [
    ("English self-disclosure", re.compile(r"\bour\s+(?:previous|prior|earlier)\s+(?:work|study|paper)", re.I)),
    ("English self-disclosure", re.compile(r"\bwe\s+(?:previously|earlier)\s+(?:showed|reported|proposed)", re.I)),
    ("English self-disclosure", re.compile(r"\b(?:in|see)\s+\[?our\b", re.I)),
    ("Chinese self-disclosure", re.compile(r"本研究團隊先前|筆者先前|作者先前")),
]


class Unreadable(Exception):
    pass


# ---------------------------------------------------------------- term lists and matching

def split_list(s):
    if not s:
        return []
    parts = re.split(r"[;；]", s) if re.search(r"[;；]", s) else re.split(r"[,，、]", s)
    out = []
    for p in (x.strip() for x in parts):
        if not p:
            continue
        if out and re.fullmatch(r"[A-Za-z]\.?(\s*[A-Za-z]\.)*", p):   # the "J." of "Doe, J."
            out[-1] += ", " + p
        else:
            out.append(p)
    return out


def build_terms(names, affil, extra):
    terms, seen = [], set()

    def add(kind, t):
        k = re.sub(r"\s+", " ", t.strip()).lower()
        if k and k not in seen:
            seen.add(k)
            terms.append((kind, t.strip()))

    for n in split_list(names):
        add("name", n)
        toks = n.split()
        if len(toks) == 2 and all(re.fullmatch(r"[A-Za-z][A-Za-z\-']+", t) for t in toks):
            add("name", f"{toks[1]} {toks[0]}")
            add("name", f"{toks[1]}, {toks[0]}")
    for a in split_list(affil):
        add("affiliation", a)
    for e in split_list(extra):
        add("extra string", e)
    return terms


def snippet(text, s, e):
    return text[max(0, s - 20):s] + "【" + text[s:e] + "】" + text[e:e + 20]


def find_hits(text, terms):
    """Return [(kind, term, 20 characters of context each side)]; only the first occurrence of each term in this text."""
    if not text or not text.strip():
        return []
    norm = re.sub(r"\s+", " ", text)
    low = norm.lower()
    nos = re.sub(r"\s+", "", text)
    nosl = nos.lower()
    out = []
    for kind, term in terms:
        t = re.sub(r"\s+", " ", term).strip().lower()
        i = low.find(t)
        if i >= 0:
            out.append((kind, term, snippet(norm, i, i + len(t))))
            continue
        tn = t.replace(" ", "")      # PDF text extraction often splits words or breaks lines: retry with whitespace removed
        if len(tn) >= 2:
            i = nosl.find(tn)
            if i >= 0:
                out.append((kind, term, snippet(nos, i, i + len(tn))))
    return out


class Report:
    def __init__(self, path, ftype):
        self.path, self.ftype = path, ftype
        self.checked = {}
        self.findings = []     # (sev, where, detail)
        self.notes = []
        self._cnt = {}

    def check(self, area, n=1):
        self.checked[area] = self.checked.get(area, 0) + n

    def add(self, sev, where, detail):
        self.findings.append((sev, where, detail))

    def hit(self, where, kind, term, snip):
        key = (where.split("：")[0].split(" ")[0], term)
        self._cnt[key] = self._cnt.get(key, 0) + 1
        if self._cnt[key] <= HIT_CAP:
            self.add(RED, where, f'matched {kind} "{term}" ...{snip}...')

    def scan(self, where, text, terms):
        for kind, term, snip in find_hits(text, terms):
            self.hit(where, kind, term, snip)

    def disclose(self, where, text):
        for label, rx in DISCLOSURE:
            m = rx.search(text or "")
            if m:
                key = ("disc", label, where.split(" ")[0])
                self._cnt[key] = self._cnt.get(key, 0) + 1
                if self._cnt[key] <= HIT_CAP:
                    self.add(ORG, where, f"{label} phrasing, for a human to judge: ...{snippet(text, m.start(), m.end())}...")

    def finish(self):
        for key, n in self._cnt.items():
            if n > HIT_CAP and key[0] != "disc":
                self.add(RED, key[0], f'"{key[1]}": {n - HIT_CAP} more not listed one by one')
            elif n > HIT_CAP:
                self.add(ORG, key[2], f"{key[1]}: {n - HIT_CAP} more not listed one by one")
        total = sum(self.checked.values())
        if total == 0:
            self.add(ORG, "whole file", "empty run: 0 items actually checked; this report is not evidence that the file is clean")

    def total(self):
        return sum(self.checked.values())

    def counts(self):
        return (sum(1 for f in self.findings if f[0] == RED), sum(1 for f in self.findings if f[0] == ORG))


# ---------------------------------------------------------------- exiftool

def exiftool_path():
    return shutil.which("exiftool")


def run_exiftool(files):
    exe = exiftool_path()
    if not exe:
        raise RuntimeError("exiftool not found (install it: https://exiftool.org, or brew install exiftool)")
    r = subprocess.run([exe, "-j", "-G1", "-s", "-a", "-charset", "filename=utf8"] + list(files),
                       capture_output=True, timeout=300)
    out = r.stdout.decode("utf-8", "replace").strip()
    if not out:
        raise RuntimeError("exiftool produced no output: " + r.stderr.decode("utf-8", "replace")[:200])
    data = json.loads(out)
    return {d.get("SourceFile"): d for d in data}


def eval_exif(r, area, where, tags, terms):
    n = 0
    for key, val in tags.items():
        if key == "SourceFile" or ":" not in key:
            continue
        group, tag = key.split(":", 1)
        if group in SKIP_GROUPS:
            continue
        if isinstance(val, list):
            val = ", ".join(str(v) for v in val)
        val = str(val).strip()
        n += 1
        low = tag.lower()
        hits = find_hits(val, terms)
        label = f"{where} {key}"
        short = val if len(val) <= 60 else val[:60] + "…"
        if not val:
            continue
        flagged = False
        if low.startswith("gps") and low != "gpsversionid":
            r.add(RED, label, f"contains GPS location data \"{short}\"")
            flagged = True
        elif low in AUTHOR_TAGS:
            r.add(RED, label, f'author / copyright field has a value "{short}"')
            flagged = True
        elif low in SOFT_TAGS:
            r.add(ORG, label, f'identifying field has a value "{short}"')
            flagged = True
        if hits and not flagged:
            for kind, term, snip in hits:
                r.hit(label, kind, term, snip)
        elif hits:
            for kind, term, snip in hits:
                r.add(RED, label, f'also matched {kind} "{term}"')
    r.check(area, n)


def check_images_exif(r, area, where_of, files, terms):
    """files: real paths; where_of: path -> display name."""
    r.check(area, 0)
    if not files:
        return
    try:
        res = run_exiftool(files)
    except Exception as e:
        r.add(ORG, area, f"not checked: {e}")
        return
    for f in files:
        tags = res.get(f)
        if tags is None:
            r.add(ORG, where_of(f), "exiftool returned nothing for this file")
            continue
        if "ExifTool:Error" in tags:
            r.add(ORG, where_of(f), f"exiftool cannot read it: {tags['ExifTool:Error']}")
            continue
        eval_exif(r, area, where_of(f), tags, terms)


# ---------------------------------------------------------------- docx

def local(tag):
    return tag.rsplit("}", 1)[-1]


def ptext(el):
    parts = []
    for ch in el:
        if ch.tag == W + "p":
            continue
        if ch.tag in (W + "t", W + "delText", W + "instrText"):
            parts.append(ch.text or "")
        elif ch.tag in (W + "tab", W + "br", W + "cr"):
            parts.append(" ")
        else:
            parts.append(ptext(ch))
    return "".join(parts)


def paragraphs(root):
    return [ptext(p) for p in root.iter(W + "p")]


def check_docx(path, terms):
    r = Report(path, "docx")
    try:
        zf = zipfile.ZipFile(path)
        names = zf.namelist()
    except Exception as e:
        raise Unreadable(f"not a valid docx: {e}")

    def parse(name):
        try:
            return ET.fromstring(zf.read(name))
        except KeyError:
            return None
        except ET.ParseError as e:
            r.add(ORG, name, f"XML parse failed, not checked: {e}")
            return None

    # --- document properties
    for fname, area, ident in (("docProps/core.xml", "core.xml fields", {"creator", "lastModifiedBy"}),
                               ("docProps/app.xml", "app.xml fields", {"Company", "Manager"})):
        r.check(area, 0)
        root = parse(fname)
        if root is None:
            r.notes.append(f"{fname} missing or unreadable")
            continue
        for el in root.iter():
            ln = local(el.tag)
            if len(el) or el is root:
                continue
            val = (el.text or "").strip()
            r.check(area)
            hits = find_hits(val, terms)
            if hits:
                for kind, term, snip in hits:
                    r.hit(f"{fname} {ln}", kind, term, snip)
            elif ln in ident and val:
                r.add(ORG, f"{fname} {ln}", f'has a value "{val}", not a listed name, but possibly identifying')
    r.check("custom.xml properties", 0)
    root = parse("docProps/custom.xml")
    if root is not None:
        for prop in root:
            nm = prop.get("name", "")
            val = "".join((c.text or "") for c in prop.iter() if c is not prop).strip()
            r.check("custom.xml properties")
            hits = find_hits(nm + " " + val, terms)
            if hits:
                for kind, term, snip in hits:
                    r.hit(f"custom.xml {nm}", kind, term, snip)
            elif val:
                r.add(ORG, f"custom.xml {nm}", f'custom property has a value "{val[:60]}"')

    # --- body, tables, footnotes, headers and footers
    for a in ("body and table paragraphs", "footnote and endnote paragraphs", "header and footer paragraphs"):
        r.check(a, 0)
    for n in sorted(names):
        if not re.fullmatch(r"word/[^/]+\.xml", n):
            continue
        base = n[5:-4]
        if base == "document":
            area, disc = "body and table paragraphs", True
        elif base in ("footnotes", "endnotes"):
            area, disc = "footnote and endnote paragraphs", True
        elif re.match(r"(header|footer)\d*$", base):
            area, disc = "header and footer paragraphs", False
        else:
            continue
        root = parse(n)
        if root is None:
            continue
        for i, t in enumerate(paragraphs(root), 1):
            if not t.strip():
                continue
            r.check(area)
            r.scan(f"{n} paragraph {i}", t, terms)
            if disc:
                r.disclose(f"{n} paragraph {i}", t)
    if r.checked.get("body and table paragraphs", 0) == 0:
        r.add(ORG, "body", "0 body paragraphs contain text: the file may be empty, or the text may be all in text boxes or images; look by hand")

    # --- comments, people list, tracked changes
    r.check("comments", 0)
    root = parse("word/comments.xml")
    if root is not None:
        cs = root.findall(W + "comment")
        r.check("comments", len(cs))
        if cs:
            authors = sorted({c.get(W + "author", "") for c in cs})
            r.add(RED, "word/comments.xml", f"{len(cs)} leftover comments, authors: {', '.join(authors)} (a review copy must have none)")
        for c in cs:
            r.scan("word/comments.xml comment author", c.get(W + "author", ""), terms)
            r.scan("word/comments.xml comment text", "".join(paragraphs(c)), terms)
    r.check("people list people.xml", 0)
    root = parse("word/people.xml")
    if root is not None:
        for el in root.iter():
            if local(el.tag) == "person":
                au = next((v for k, v in el.attrib.items() if local(k) == "author"), "")
                r.check("people list people.xml")
                if find_hits(au, terms):
                    r.scan("word/people.xml person", au, terms)
                elif au:
                    r.add(ORG, "word/people.xml", f'leftover author name "{au}" (left comments or revisions in this document at some point)')
    r.check("tracked-change scan (XML parts)", 0)
    for n in sorted(names):
        if not re.fullmatch(r"word/[^/]+\.xml", n) or n == "word/comments.xml":
            continue
        root = parse(n)
        if root is None:
            continue
        r.check("tracked-change scan (XML parts)")
        cnt, authors = 0, set()
        for el in root.iter():
            if el.tag.startswith(W) and local(el.tag) in TRACK_TAGS:
                cnt += 1
                authors.add(el.get(W + "author", ""))
        if cnt:
            r.add(RED, n, f"{cnt} leftover tracked changes, authors: {', '.join(sorted(authors))} (accept or reject every revision before submitting)")
            for au in authors:
                r.scan(f"{n} revision author", au, terms)

    # --- hyperlinks
    r.check("external link targets", 0)
    for n in sorted(names):
        if not n.endswith(".rels"):
            continue
        root = parse(n)
        if root is None:
            continue
        for rel in root:
            if rel.get("TargetMode") == "External":
                r.check("external link targets")
                r.scan(f"{n} link", rel.get("Target", ""), terms)

    # --- embedded images
    media = [n for n in names if n.startswith("word/media/") and not n.endswith("/")]
    if media:
        tmp = tempfile.mkdtemp(prefix="anon_")
        try:
            mp = {}
            for i, n in enumerate(media):
                p = os.path.join(tmp, f"{i:03d}{os.path.splitext(n)[1]}")
                with open(p, "wb") as f:
                    f.write(zf.read(n))
                mp[p] = n
            check_images_exif(r, "embedded-image EXIF tags", lambda f: mp[f], list(mp), terms)
            r.notes.append(f"{len(media)} embedded images were each read with exiftool")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    else:
        r.check("embedded-image EXIF tags", 0)
        r.notes.append("no embedded images")
    return r


# ---------------------------------------------------------------- pdf

def xmp_values(raw):
    root = ET.fromstring(raw)
    out = []

    def walk(el, prop):
        ln = local(el.tag)
        ns = el.tag[1:].split("}")[0] if el.tag.startswith("{") else ""
        if ns != RDF:
            prop = ln
        for k, v in el.attrib.items():
            if k.startswith("{") and k[1:].split("}")[0] not in (RDF, "http://www.w3.org/XML/1998/namespace", "http://www.w3.org/2000/xmlns/"):
                out.append((local(k), v))
        if len(el) == 0:
            t = (el.text or "").strip()
            if t:
                out.append((prop, t))
        for ch in el:
            walk(ch, prop)

    walk(root, "")
    return out


def _fitz():
    try:
        import pymupdf as fitz
    except ImportError:
        try:
            import fitz  # older package name
        except ImportError:
            raise Unreadable("PyMuPDF is required to check PDFs (pip install pymupdf)")
    return fitz


def check_pdf(path, terms):
    fitz = _fitz()
    r = Report(path, "pdf")
    try:
        doc = fitz.open(path)
        if doc.needs_pass:
            raise Unreadable("the PDF is password protected")
        npages = doc.page_count
    except Unreadable:
        raise
    except Exception as e:
        raise Unreadable(f"not a valid PDF: {e}")

    r.check("Info fields", 0)
    meta = doc.metadata or {}
    for key, label in (("author", "Author"), ("creator", "Creator"), ("producer", "Producer"),
                       ("title", "Title"), ("subject", "Subject"), ("keywords", "Keywords")):
        val = str(meta.get(key) or "").strip()
        r.check("Info fields")
        hits = find_hits(val, terms)
        if hits:
            for kind, term, snip in hits:
                r.hit(f"Info {label}", kind, term, snip)
        elif label == "Author" and val:
            r.add(ORG, "Info Author", f'has a value "{val}", not a listed name, but possibly identifying')

    r.check("XMP fields", 0)
    try:
        raw = doc.get_xml_metadata() or ""
        if not raw.strip():
            r.notes.append("no XMP block")
        else:
            for prop, val in xmp_values(raw.encode("utf-8")):
                r.check("XMP fields")
                hits = find_hits(val, terms)
                if hits:
                    for kind, term, snip in hits:
                        r.hit(f"XMP {prop}", kind, term, snip)
                elif prop.lower() in {"creator", "author", "contributor", "publisher", "rights", "lastmodifiedby", "owner"}:
                    r.add(ORG, f"XMP {prop}", f'has a value "{val}", not a listed name, but possibly identifying')
    except Exception as e:
        r.add(ORG, "XMP", f"not checked: {e}")

    r.check("page text (pages with text)", 0)
    chars = 0
    for i in range(npages):
        try:
            t = doc[i].get_text() or ""
        except Exception as e:
            r.add(ORG, f"page {i + 1}", f"text extraction failed, not checked: {e}")
            continue
        if t.strip():
            chars += len(t)
            r.check("page text (pages with text)")
            r.scan(f"page {i + 1}", t, terms)
            r.disclose(f"page {i + 1}", t)
    if chars == 0:
        r.add(ORG, "page text", f"empty run: no text could be extracted from {npages} pages; it may be a scan, so names and affiliations were not checked; use OCR or read page by page")

    imgs, seen = [], set()
    tmp = tempfile.mkdtemp(prefix="anon_")
    try:
        try:
            for pi in range(npages):
                for j, info in enumerate(doc[pi].get_images(full=True)):
                    xref = info[0]
                    if xref in seen:
                        continue
                    seen.add(xref)
                    if len(imgs) >= 100:
                        break
                    ex = doc.extract_image(xref)
                    if not ex:
                        continue
                    p = os.path.join(tmp, f"{len(imgs):03d}.{ex.get('ext', 'img')}")
                    with open(p, "wb") as f:
                        f.write(ex["image"])
                    imgs.append((p, f"page {pi + 1} image {j + 1}"))
        except Exception as e:
            r.notes.append(f"embedded-image extraction stopped ({e}); EXIF checked only for the {len(imgs)} images extracted")
        mp = dict(imgs)
        check_images_exif(r, "embedded-image EXIF tags", lambda f: mp[f], list(mp), terms)
        r.notes.append(f"only the {len(imgs)} images PyMuPDF could extract were checked (cap 100); vector graphics and metadata stripped by conversion cannot be seen")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return r


# ---------------------------------------------------------------- image files

def check_image(path, terms):
    r = Report(path, "image")
    if not os.access(path, os.R_OK):
        raise Unreadable("cannot read it")
    if not exiftool_path():
        raise Unreadable("exiftool not found, so images cannot be checked (install it: https://exiftool.org)")
    try:
        res = run_exiftool([path])
    except Exception as e:
        raise Unreadable(str(e))
    tags = res.get(path) or next(iter(res.values()), {})
    if "ExifTool:Error" in tags:
        raise Unreadable(f"exiftool cannot read it: {tags['ExifTool:Error']}")
    r.check("EXIF/XMP/IPTC tags", 0)
    eval_exif(r, "EXIF/XMP/IPTC tags", os.path.basename(path), tags, terms)
    if r.total() == 0:
        r.notes.append("this image has no metadata tags to check; if some were expected (e.g. HEIC), make sure exiftool can read the format")
    return r


# ---------------------------------------------------------------- main

def collect(paths):
    files, skipped, bad = [], 0, []
    for p in paths:
        if os.path.isdir(p):
            for d, dirs, fs in os.walk(p):
                dirs[:] = sorted(x for x in dirs if not x.startswith("."))
                for f in sorted(fs):
                    if f.startswith(".") or f.startswith("~$"):
                        continue
                    if os.path.splitext(f)[1].lower() in IMG_EXT | {".docx", ".pdf"}:
                        files.append(os.path.join(d, f))
                    else:
                        skipped += 1
        elif os.path.isfile(p):
            if os.path.splitext(p)[1].lower() in IMG_EXT | {".docx", ".pdf"}:
                files.append(p)
            else:
                bad.append((p, "unsupported extension (only docx, pdf and images)"))
        else:
            bad.append((p, "file or folder does not exist"))
    return files, skipped, bad


def render(r):
    lines = [f"=== {r.path}（{r.ftype}）==="]
    area_txt = ", ".join(f"{k} {v}" for k, v in r.checked.items())
    lines.append(f"Actually checked: {area_txt}; {r.total()} items in total")
    if r.total() == 0:
        lines.append("!!! empty run: 0 items actually checked in this file; do not treat it as clean !!!")
    zero = [k for k, v in r.checked.items() if v == 0]
    if zero:
        lines.append("0 items (nothing to check, or nothing found to check): " + ", ".join(zero))
    order = {RED: 0, ORG: 1}
    for sev, where, detail in sorted(r.findings, key=lambda f: order[f[0]]):
        lines.append(f"{sev} [{where}] {detail}")
    for n in r.notes:
        lines.append(f"Note: {n}")
    red, org = r.counts()
    lines.append(f"{GRN} Areas checked: {area_txt or 'none'}" + (" (no 🔴 findings)" if red == 0 else ""))
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--names", default="", help="author names, comma-separated")
    ap.add_argument("--affil", default="", help="affiliation names, comma-separated")
    ap.add_argument("--extra", default="", help="extra strings (account names, personal domains ...), comma-separated")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    terms = build_terms(a.names, a.affil, a.extra)
    if not terms:
        print("warning: no --names / --affil / --extra given: only metadata and leftover comments and revisions are checked, no name matching", file=sys.stderr)
    files, skipped, bad = collect(a.paths)
    reports = []
    for f in files:
        try:
            ext = os.path.splitext(f)[1].lower()
            rp = check_docx(f, terms) if ext == ".docx" else check_pdf(f, terms) if ext == ".pdf" else check_image(f, terms)
            rp.finish()
            reports.append(rp)
        except Unreadable as e:
            bad.append((f, str(e)))
    red = sum(r.counts()[0] for r in reports)
    org = sum(r.counts()[1] for r in reports)

    if a.json:
        print(json.dumps({
            "files": [{"path": r.path, "type": r.ftype, "checked": r.checked, "total_checked": r.total(),
                       "empty_run": r.total() == 0, "notes": r.notes,
                       "findings": [{"severity": s, "where": w, "detail": d} for s, w, d in r.findings]}
                      for r in reports],
            "unreadable": [{"path": p, "reason": m} for p, m in bad],
            "red": red, "orange": org}, ensure_ascii=False, indent=2))
    else:
        for r in reports:
            print(render(r))
            print()
        for p, m in bad:
            print(f"x unreadable {p}: {m}")
        if skipped:
            print(f"(skipped {skipped} files in folders that are not docx, pdf or images)")
        print(f"{RED} {red}, {ORG} {org}")
    sys.exit(2 if bad else (1 if red else 0))


if __name__ == "__main__":
    main()
