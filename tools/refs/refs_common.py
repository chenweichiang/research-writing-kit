#!/usr/bin/env python3
"""refs_common.py: shared helpers for missing_refs.py and inbox_ingest.py (stdlib only).

Not a command line tool; the two scripts import it (they add this folder to sys.path).
Contents:
  * a small BibTeX parser (braces and quotes, nested braces, concatenation with #)
  * the project file-naming rule (the same one tools/refs/pdf_fetch.py uses: <citekey>.pdf)
  * personal-library loading and the three-gate matcher (year + first-author surname +
    title similarity)
  * PDF text extraction through the external `pdftotext` binary (optional) and the
    content check that decides whether a PDF really is the cited paper
  * small file helpers (SHA-256, DOI extraction)
"""
import difflib
import hashlib
import os
import re
import shutil
import subprocess
import unicodedata

DEFAULT_PDFDIR = "refs-pdf"          # same default folder as pdf_fetch.py --out
TITLE_GATE = 0.55                    # third gate: minimum title similarity
AMBIGUITY_GAP = 0.15                 # best candidate must beat the runner-up by this much

STOP_LIB = {"a", "an", "the", "of", "on", "in", "for", "and", "to", "with", "as", "into", "from",
            "by", "at", "or", "is", "are", "be", "using", "via", "towards", "toward", "study",
            "case"}
STOP_VERIFY = {"the", "a", "an", "of", "in", "and", "for", "on", "to", "with", "as", "is", "its",
               "into", "through", "from", "by", "at", "or", "how", "what", "be", "are"}
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\"<>]+")


# ---------------------------------------------------------------- naming
def safe_name(name):
    """File stem for a cite key: identical to pdf_fetch.py's _safe()."""
    return re.sub(r"[^\w.\-]+", "_", name)[:120] or "ref"


def pdf_path(pdfdir, key):
    return os.path.join(pdfdir, safe_name(key) + ".pdf")


def covered_keys(entries, pdfdir):
    """Cite keys whose <pdfdir>/<safe(key)>.pdf already exists."""
    return {e["key"] for e in entries if os.path.isfile(pdf_path(pdfdir, e["key"]))}


# ---------------------------------------------------------------- text helpers
def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def toks(s):
    """Accent-folded lowercase alphanumeric tokens (no stop-word filter)."""
    return [t for t in re.split(r"[^a-z0-9]+", strip_accents(s).lower()) if t]


def content_toks(s):
    return [t for t in toks(s) if t not in STOP_LIB and len(t) >= 3]


def verify_toks(s):
    """Title words for the PDF content check (stop words and 1-2 letter words dropped)."""
    return [w for w in re.sub(r"[^a-z0-9]", " ", (s or "").lower()).split()
            if w not in STOP_VERIFY and len(w) > 2]


def years_in(s):
    return set(re.findall(r"(?:19|20)\d{2}", s))


def delatex(s):
    r"""Undo common BibTeX escapes: {\c{s}} -> s, {\'e} -> e, drop braces."""
    s = re.sub(r"\{\\[a-zA-Z]+\s*\{?([a-zA-Z])\}?\}", r"\1", s or "")
    s = re.sub(r"\\[a-zA-Z]+\{([a-zA-Z])\}", r"\1", s)
    s = re.sub(r"\\[\'\"`^~=.]", "", s)
    return s.replace("{", "").replace("}", "").replace("\\", "").strip()


def norm_doi(s):
    s = (s or "").strip().lower()
    s = re.sub(r"^https?://(dx\.)?doi\.org/", "", s)
    return s.rstrip(".,;)]}")


def dois_in(text):
    """DOIs in a string. File names often turn the slash into an underscore
    (`10.1145_3544548.3581234.pdf`), so both spellings are collected."""
    out = {norm_doi(m) for m in DOI_RE.findall(text or "")}
    for m in re.findall(r"10\.\d{4,9}_[^\s\"<>]+", text or ""):
        out.add(norm_doi(m.replace("_", "/", 1)))
    return {re.sub(r"\.pdf$", "", d) for d in out if d}


def surname(author):
    """First author's surname for display and file names (original case, LaTeX undone)."""
    a = delatex((author or "").strip())
    first = re.split(r"\s+and\s+", a)[0]
    if "," in first:
        return first.split(",")[0].strip()
    parts = first.split()
    return parts[-1].strip() if parts else ""


def first_surname(author):
    """First author's surname as one lowercase accent-folded token ('Lee, Hao-Ping' -> lee)."""
    if not author:
        return ""
    sur = surname(author)
    sur = re.sub(r"\(.*?\)", "", sur)
    t = toks(sur)
    return t[0] if t else ""


def clean_title(t):
    t = delatex(t).replace(": ", "- ").replace(":", "-").replace("/", "-")
    return re.sub(r"\s+", " ", re.sub(r'[\\*?"<>|]', "", t)).strip().rstrip(".")[:150]


def author_year(e):
    return ("%s %s" % (surname(e.get("author", "")), e.get("year", ""))).strip()


# ---------------------------------------------------------------- BibTeX parser
_NAME_RE = re.compile(r"([A-Za-z_][\w\-:]*)\s*=\s*")


def _scan_braced(s, i):
    """s[i] == '{'. Return (inner text, index after the matching '}')."""
    depth, j, n = 0, i, len(s)
    while j < n:
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    return s[i + 1:], n


def _scan_quoted(s, i):
    """s[i] == '"'. Return (inner text, index after the closing quote); braces nest."""
    depth, j, n = 0, i + 1, len(s)
    while j < n:
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        elif c == '"' and depth == 0:
            return s[i + 1:j], j + 1
        j += 1
    return s[i + 1:], n


def _parse_value(s, i):
    """A field value: braced, quoted or bare pieces joined with '#'."""
    parts, n = [], len(s)
    while i < n:
        while i < n and s[i].isspace():
            i += 1
        if i >= n:
            break
        if s[i] == "{":
            txt, i = _scan_braced(s, i)
            parts.append(txt)
        elif s[i] == '"':
            txt, i = _scan_quoted(s, i)
            parts.append(txt)
        else:
            m = re.match(r"[^\s,#}]+", s[i:])
            if not m:
                break
            parts.append(m.group(0))
            i += m.end()
        while i < n and s[i].isspace():
            i += 1
        if i < n and s[i] == "#":
            i += 1
            continue
        break
    return re.sub(r"\s+", " ", "".join(parts)).strip(), i


def _parse_fields(body):
    out, i = {}, 0
    while True:
        m = _NAME_RE.search(body, i)
        if not m:
            return out
        val, i = _parse_value(body, m.end())
        out.setdefault(m.group(1).lower(), val)


def parse_bib(path):
    """Parse a .bib file. Returns a list of dicts with the keys
    key, type, author, year, title, doi, isbn, url.

    Good enough for typical Zotero / Better BibTeX exports: braced and quoted values,
    nested braces, '#' concatenation, @string/@comment/@preamble skipped. `editor` stands in
    for a missing `author`; `date` (biblatex) stands in for a missing `year`. A field spelled
    `_doi` or `_isbn` (the "deliberately unused" convention) is not read as `doi` / `isbn`.
    A DOI is also taken from a doi.org `url` when there is no `doi` field."""
    with open(path, encoding="utf-8", errors="ignore") as f:
        txt = f.read()
    entries, pos = [], 0
    head = re.compile(r"@(\w+)\s*\{")
    while True:
        m = head.search(txt, pos)
        if not m:
            return entries
        _inner, end = _scan_braced(txt, m.end() - 1)
        pos = end
        etype = m.group(1).lower()
        if etype in ("comment", "preamble", "string"):
            continue
        body = txt[m.end():end - 1]
        comma = body.find(",")
        if comma < 0:
            continue
        key = body[:comma].strip()
        fl = _parse_fields(body[comma + 1:])
        year = re.search(r"\d{4}", fl.get("year") or fl.get("date") or "")
        url = fl.get("url", "")
        doi = norm_doi(fl.get("doi", ""))
        if not doi and "doi.org/" in url:
            doi = norm_doi(url)
        entries.append({"key": key, "type": etype,
                        "author": fl.get("author") or fl.get("editor", ""),
                        "year": year.group(0) if year else "",
                        "title": fl.get("title", ""), "doi": doi,
                        "isbn": fl.get("isbn", ""), "url": url})


# ---------------------------------------------------------------- files
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def list_pdfs(root):
    """PDF files under root, recursively, sorted."""
    out = []
    for d, _dirs, files in os.walk(root):
        out += [os.path.join(d, n) for n in files if n.lower().endswith(".pdf")]
    return sorted(out)


# ---------------------------------------------------------------- personal library + matcher
def load_library(lib_dir):
    """[{name, path, ftoks, fyears}] for every PDF under lib_dir (recursive).
    Matching works on file names only, so name files `<Surname> <Year> - <Title>.pdf`."""
    out = []
    for p in list_pdfs(lib_dir):
        stem = os.path.basename(p)[:-4]
        out.append({"name": os.path.basename(p), "path": p,
                    "ftoks": set(toks(stem)), "fyears": years_in(stem)})
    return out


def title_sim(bib_title, lib):
    """Title similarity: max(recall, mixed recall/precision, sequence ratio) over content tokens."""
    bt = set(content_toks(bib_title))
    if not bt:
        return 0.0
    ft = lib["ftoks"]
    inter = bt & ft
    recall = len(inter) / len(bt)
    ft_content = {t for t in ft if t not in STOP_LIB and len(t) >= 3}
    precision = len(inter) / max(1, len(ft_content))
    seq = difflib.SequenceMatcher(None, " ".join(sorted(bt)), " ".join(sorted(ft_content))).ratio()
    return max(recall, 0.6 * precision + 0.4 * recall, seq)


def library_match(e, library, th=TITLE_GATE):
    """Three gates: same year in the file name, first-author surname in the file name, title
    similarity >= th. Returns ("confident", L) / ("ambiguous", [L, ...]) / ("none", None).
    Confident = a single candidate, or the best beats the runner-up by AMBIGUITY_GAP."""
    sur, yr = first_surname(e.get("author", "")), e.get("year", "")
    cands = []
    for L in library:
        if yr and yr not in L["fyears"]:
            continue
        if sur and sur not in L["ftoks"]:
            continue
        s = title_sim(e.get("title", ""), L)
        if s >= th:
            cands.append((s, L))
    cands.sort(key=lambda x: -x[0])
    if not cands:
        return "none", None
    if len(cands) == 1 or cands[0][0] - cands[1][0] >= AMBIGUITY_GAP:
        return "confident", cands[0][1]
    return "ambiguous", [L for _, L in cands[:3]]


def present_keys(entries, pdfdir):
    """Entries that already have a PDF in the project folder. Two rules:
      1. <pdfdir>/<citekey>.pdf exists (what pdf_fetch.py and inbox_ingest.py write);
      2. some other PDF in pdfdir matches the entry on file name with the same three gates as
         the library check (so a hand-filed `NN [Author Year] Title.pdf` counts).
    Returns (have, ambiguous): `have` is a set of keys (an ambiguous match counts as present);
    `ambiguous` maps key -> candidate file names, for the assistant to confirm."""
    have = covered_keys(entries, pdfdir)
    ambiguous = {}
    rest = [e for e in entries if e["key"] not in have]
    files = load_library(pdfdir) if rest and os.path.isdir(pdfdir) else []
    for e in rest:
        kind, hit = library_match(e, files)
        if kind == "confident":
            have.add(e["key"])
        elif kind == "ambiguous":
            have.add(e["key"])
            ambiguous[e["key"]] = [L["name"] for L in hit]
    return have, ambiguous


# ---------------------------------------------------------------- PDF text (pdftotext)
def have_pdftotext():
    return shutil.which("pdftotext") is not None


_TEXT_CACHE = {}


def pdf_pages(path):
    """Text of each page via `pdftotext`, or None when the tool is missing or fails."""
    if path in _TEXT_CACHE:
        return _TEXT_CACHE[path]
    pages = None
    exe = shutil.which("pdftotext")
    if exe:
        try:
            r = subprocess.run([exe, "-enc", "UTF-8", path, "-"], capture_output=True, timeout=120)
            if r.returncode == 0:
                pages = r.stdout.decode("utf-8", "ignore").split("\f")
                if pages and not pages[-1].strip():
                    pages.pop()
        except (OSError, subprocess.SubprocessError):
            pages = None
    _TEXT_CACHE[path] = pages
    return pages


def first_pages_text(path, n=2):
    pages = pdf_pages(path)
    return " ".join(pages[:n]) if pages else ""


# ---------------------------------------------------------------- content check
def _fold_name(x):
    """Surname normaliser for PDF text: drop stray accent marks and apostrophes (PDF text often
    splits diacritics into separate characters), fold to ASCII."""
    x = "".join(c for c in (x or "") if unicodedata.category(c) != "Sk" and c not in "'\u2019\u2018`")
    x = unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode().lower()
    return " ".join(re.sub(r"[^a-z0-9 ]", " ", x).split())


def title_phrase_score(title, head):
    """Best similarity (0 to 1) between the title and any same-length window of the front text.
    Phrase order matters: a bag of words is fooled by generic design / human / experience
    vocabulary."""
    t = re.sub(r"[^a-z0-9 ]", " ", (title or "").lower()).split()
    hw = re.sub(r"[^a-z0-9 ]", " ", head).split()
    if not t or len(hw) < len(t):
        return 0.0
    ts, w, best = " ".join(t), len(t), 0.0
    for i in range(0, len(hw) - w + 1, 2):
        r = difflib.SequenceMatcher(None, ts, " ".join(hw[i:i + w])).ratio()
        best = max(best, r)
        if best > 0.95:
            break
    return best


def identity_doubt(e, head, p1):
    """After a phrase match passes, ask: is this the paper, or a paper that mentions it?
    Returns a reason string, or "" when nothing looks off. Two signals:
      1. page 1 prints a DOI that is not the bib's, and the bib's DOI appears nowhere in the
         front pages (template placeholders and arXiv-DOI bibs are ignored);
      2. the title has three content words or fewer and the first author's surname is absent
         from the first eight pages (phrase matching cannot discriminate short titles)."""
    want = (e.get("doi") or "").lower().strip().replace("//", "/")
    if want and not want.startswith("10.48550/"):
        found = {x.rstrip(".,;)]").replace("//", "/") for x in DOI_RE.findall(p1)}
        found = {x for x in found if not re.search(r"(n{5,}|x{5,})", x)}
        if found and want not in found and want not in head.replace("//", "/"):
            return "page 1 prints DOI %s, not the bib's %s" % (sorted(found)[0], want)
    sn = _fold_name(surname(e.get("author", "")))
    n_words = len(verify_toks(e.get("title", "")))
    if sn and n_words <= 3 and sn not in _fold_name(head):
        return "title has only %d content words and first author %s is absent from the first 8 pages" % (
            n_words, sn)
    return ""


def excerpt_flag(head, npages):
    """A title check passing does not mean the file is complete: some publisher links for books
    return a preview (front matter, chapter 1, bibliography)."""
    if "bookpreview-pdf" in head or "book preview" in head:
        return " PREVIEW-ONLY(%dp, not the whole book)" % npages
    return ""


def verify(path, e):
    """Does this PDF look like the cited work? Returns (ok, npages, note).
    Notes: not-pdf; saved-UNVERIFIED(no-pdftotext); scanned(no-text); verified phrase X;
    LOW-CONFIDENCE ...; CONTENT-MISMATCH ...
    LOW-CONFIDENCE files are kept but must be shown to the author."""
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except OSError:
        return False, 0, "not-pdf"
    if data[:4] != b"%PDF" or len(data) < 8000:
        return False, 0, "not-pdf"
    pages = pdf_pages(path)
    if pages is None:
        return True, 0, "saved-UNVERIFIED(no-pdftotext)"
    n = len(pages)
    head = " ".join(pages[:8]).lower()
    p1 = (pages[0] if pages else "").lower()
    if len(head.strip()) < 80:
        return True, n, "scanned(no-text)"
    tt = verify_toks(e.get("title", ""))
    ov = len([w for w in tt if w in head]) / len(tt) if tt else 0
    sn = surname(e.get("author", "")).lower()
    ph = title_phrase_score(e.get("title", ""), head)
    excerpt = excerpt_flag(head, n)
    if ph >= 0.85:
        why = identity_doubt(e, head, p1)
        if why:
            return True, n, "LOW-CONFIDENCE phrase %.2f but %s; confirm it is the same paper%s" % (
                ph, why, excerpt)
        return True, n, "verified phrase %.2f%s" % (ph, excerpt)
    if ov >= 0.5 or (ov >= 0.3 and sn and sn in head):
        return True, n, "LOW-CONFIDENCE phrase %.2f / tokens %.0f%%; confirm it is the same paper" % (
            ph, ov * 100)
    return False, n, "CONTENT-MISMATCH phrase %.2f / tokens %.0f%%" % (ph, ov * 100)
