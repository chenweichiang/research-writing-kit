"""tools/refs/missing_refs.py and tools/refs/inbox_ingest.py: offline tests.
Tiny PDFs are written by hand (no PDF library); the content-checking tests need the external
`pdftotext` and skip without it. The BibTeX parser and the file-name-only paths are tested
without it. HOME is a temp dir in every CLI run, so the real ~/Downloads and ~/.Trash are never
touched."""
import csv
import os
import shutil
import sys
from pathlib import Path

import pytest

from conftest import load_tool, run_tool

needs_pdftotext = pytest.mark.skipif(shutil.which("pdftotext") is None,
                                     reason="pdftotext (poppler) not installed")

BIB = r"""
@article{have2019, author={Acar, Oguz and Tarakci, Murat}, title={Creativity under constraints}, year={2019}, doi={10.1/a}}
@article{inlit2020, author={Smith, Jane}, title={Learning to See in the Dark}, year={2020}, doi={10.1/b}}
@article{doi2021, author={Lee, Kim}, title={Paywalled Interaction Study}, year={2021}, doi={10.1145/3544548.3581234}}
@book{book1999, author={Brown, Tim}, title={Design Thinking Handbook}, year={1999}, isbn={9780000000001}}
@misc{web2017, author={Ng, Ada}, title={A Web Only Report}, year={2017}, url={https://example.org/report}}
@misc{bare2018, author={Wu, Lin}, title={An Unindexed Report}, year={2018}}
"""

INBOX_BIB = r"""
@article{lee2021, author={Lee, Kim and Park, Jun}, title={Tangible Feedback for Remote Collaboration in Design Studios}, year={2021}, doi={10.1145/3544548.3581234}}
@article{ono2019, author={Ono, Haruki}, title={Soft Robotic Skins as Expressive Interfaces}, year={2019}, doi={10.1016/j.destud.2019.01.004}}
@article{wu2018, author={Wu, Lin}, title={Speculative Kitchens and Domestic Futures}, year={2018}}
"""


def make_pdf(path, title="", author="", pages=6, text=True):
    """A minimal valid PDF (Helvetica, uncompressed). text=False gives blank pages (like a scan)."""
    def esc(s):
        return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    objs = {1: "<< /Type /Catalog /Pages 2 0 R >>",
            3: "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"}
    kids = []
    nxt = 4
    for i in range(pages):
        lines = []
        if text:
            if i == 0:
                lines += [(80, title, 14), (110, author, 11)]
            lines += [(140 + k * 15, "Body text line %d on page %d about method results discussion."
                       % (k, i), 8) for k in range(40)]
        stream = "".join("BT /F1 %d Tf 50 %d Td (%s) Tj ET\n" % (sz, 800 - y, esc(t))
                         for y, t, sz in lines)
        objs[nxt] = ("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
                     "/Resources << /Font << /F1 3 0 R >> >> /Contents %d 0 R >>" % (nxt + 1))
        objs[nxt + 1] = "<< /Length %d >>\nstream\n%sendstream" % (len(stream), stream)
        kids.append("%d 0 R" % nxt)
        nxt += 2
    objs[2] = "<< /Type /Pages /Kids [%s] /Count %d >>" % (" ".join(kids), pages)
    pad = " " * 9000
    objs[nxt] = "<< /Length %d >>\nstream\n%s\nendstream" % (len(pad), pad)
    out = bytearray(b"%PDF-1.4\n")
    offs = {}
    for n in sorted(objs):
        offs[n] = len(out)
        out += ("%d 0 obj\n%s\nendobj\n" % (n, objs[n])).encode("latin-1")
    xref = len(out)
    out += ("xref\n0 %d\n0000000000 65535 f \n" % (nxt + 1)).encode()
    for n in range(1, nxt + 1):
        out += ("%010d 00000 n \n" % offs[n]).encode()
    out += ("trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (nxt + 1, xref)).encode()
    Path(path).write_bytes(bytes(out))


def trash_of(home):
    p = (Path(home) / ".Trash") if sys.platform == "darwin" else (
        Path(home) / ".local" / "share" / "Trash" / "files")
    p.mkdir(parents=True, exist_ok=True)
    return p


# ------------------------------------------------------------------ BibTeX parser
def test_parse_bib_formats(tmp_path):
    rc = load_tool("refs/refs_common.py")
    bib = tmp_path / "x.bib"
    bib.write_text(r'''
@comment{ignored = {x}}
@string{jn = "Journal"}
@inproceedings{Key:1,
  booktitle = {Conference Name},
  title     = "A {Quoted} Title with {nested {braces}}",
  author    = {M{\"u}ller, Anna and Smith, Bob},
  date      = {2022-05-01},
  doi       = {https://doi.org/10.1145/3544548.3581234},
  _isbn     = {9780000000001},
}
@book{ed1,
  editor = {Lee, Kim},
  title = {Edited} # { Volume},
  year = 1999,
  url = {https://doi.org/10.5555/abc.def},
}
''', encoding="utf-8")
    es = rc.parse_bib(bib)
    assert [e["key"] for e in es] == ["Key:1", "ed1"]
    a, b = es
    assert a["title"] == "A {Quoted} Title with {nested {braces}}"   # booktitle did not leak in
    assert rc.delatex(a["title"]) == "A Quoted Title with nested braces"
    assert a["year"] == "2022" and a["type"] == "inproceedings"
    assert a["doi"] == "10.1145/3544548.3581234"
    assert a["isbn"] == ""                                            # `_isbn` is "deliberately unused"
    assert rc.first_surname(a["author"]) == "muller"
    assert b["author"] == "Lee, Kim" and b["year"] == "1999"
    assert b["title"] == "Edited Volume"
    assert b["doi"] == "10.5555/abc.def"                              # taken from a doi.org url


def test_safe_name_matches_pdf_fetch():
    rc = load_tool("refs/refs_common.py")
    pf = load_tool("refs/pdf_fetch.py")
    for k in ("lee2021", "Key:1", "a/b c", "x" * 200, "!!!"):
        assert rc.safe_name(k) == pf._safe(k)


def test_dois_in_publisher_filename():
    rc = load_tool("refs/refs_common.py")
    assert "10.1145/3544548.3581234" in rc.dois_in("10.1145_3544548.3581234.pdf")
    assert "10.1016/j.destud.2019.01.004" in rc.dois_in("see https://doi.org/10.1016/j.destud.2019.01.004.")


# ------------------------------------------------------------------ missing_refs
def make_project(tmp):
    tmp = Path(tmp)
    bib = tmp / "refs.bib"
    bib.write_text(BIB, encoding="utf-8")
    pdfdir = tmp / "refs-pdf"
    pdfdir.mkdir()
    (pdfdir / "have2019.pdf").write_bytes(b"%PDF-x")
    lib = tmp / "library"
    (lib / "sub").mkdir(parents=True)
    (lib / "sub" / "Smith 2020 - Learning to See in the Dark.pdf").write_bytes(b"%PDF-lit")
    return bib, pdfdir, lib


def test_library_hit_is_not_listed(tmp_path):
    mr = load_tool("refs/missing_refs.py")
    rc = load_tool("refs/refs_common.py")
    bib, pdfdir, lib = make_project(tmp_path)
    entries = rc.parse_bib(bib)
    have = rc.covered_keys(entries, pdfdir)
    missing = [e for e in entries if e["key"] not in have]
    assert sorted(e["key"] for e in missing) == ["bare2018", "book1999", "doi2021", "inlit2020", "web2017"]
    conf, amb, todo = mr.classify(missing, rc.load_library(lib))
    assert [e["key"] for e, _ in conf] == ["inlit2020"]               # found recursively
    assert "inlit2020" not in [e["key"] for e in todo]


def test_groups_and_outputs(tmp_path):
    mr = load_tool("refs/missing_refs.py")
    rc = load_tool("refs/refs_common.py")
    bib, pdfdir, lib = make_project(tmp_path)
    entries = rc.parse_bib(bib)
    missing = [e for e in entries if e["key"] != "have2019"]
    _, _, todo = mr.classify(missing, rc.load_library(lib))
    groups, md, tsv = mr.write_outputs(str(pdfdir), todo)
    assert [e["key"] for e in groups["doi"]] == ["doi2021"]
    assert [e["key"] for e in groups["isbn"]] == ["book1999"]
    assert [e["key"] for e in groups["url"]] == ["web2017"]
    assert [e["key"] for e in groups["none"]] == ["bare2018"]
    text = Path(md).read_text(encoding="utf-8")
    assert "https://doi.org/10.1145/3544548.3581234" in text
    assert "ISBN 9780000000001" in text and "https://example.org/report" in text
    rows = list(csv.DictReader(open(tsv, encoding="utf-8"), delimiter="\t"))
    assert len(rows) == 4 and rows[0]["key"] == "doi2021"


def test_ambiguous_is_not_auto_copied(tmp_path):
    mr = load_tool("refs/missing_refs.py")
    rc = load_tool("refs/refs_common.py")
    bib, pdfdir, lib = make_project(tmp_path)
    (lib / "Smith 2020 - Learning to See in the Dark Room.pdf").write_bytes(b"%PDF")
    missing = [e for e in rc.parse_bib(bib) if e["key"] == "inlit2020"]
    conf, amb, _ = mr.classify(missing, rc.load_library(lib))
    assert conf == [] and [e["key"] for e, _ in amb] == ["inlit2020"]


def test_year_and_surname_gates(tmp_path):
    rc = load_tool("refs/refs_common.py")
    lib = tmp_path / "lib"
    lib.mkdir()
    (lib / "Smith 2019 - Learning to See in the Dark.pdf").write_bytes(b"%PDF")   # wrong year
    (lib / "Jones 2020 - Learning to See in the Dark.pdf").write_bytes(b"%PDF")   # wrong surname
    (lib / "Smith 2020 - Cooking Pasta.pdf").write_bytes(b"%PDF")                 # wrong title
    e = {"key": "k", "author": "Smith, Jane", "year": "2020", "title": "Learning to See in the Dark"}
    assert rc.library_match(e, rc.load_library(lib)) == ("none", None)


def test_apply_copies_into_project(tmp_path):
    bib, pdfdir, lib = make_project(tmp_path)
    r = run_tool("refs/missing_refs.py", "--bib", bib, "--pdfdir", pdfdir, "--library", lib, "--apply",
                 home=tmp_path)
    assert r.returncode == 0, r.stderr
    assert (pdfdir / "inlit2020.pdf").read_bytes() == b"%PDF-lit"
    assert "library match 1" in r.stdout
    assert (pdfdir / "_missing.md").exists() and (pdfdir / "_missing.tsv").exists()


def test_dry_run_does_not_copy_and_no_library_is_reported(tmp_path):
    bib, pdfdir, lib = make_project(tmp_path)
    r = run_tool("refs/missing_refs.py", "--bib", bib, "--pdfdir", pdfdir, "--library", lib, home=tmp_path)
    assert r.returncode == 0 and "add --apply" in r.stdout
    assert not (pdfdir / "inlit2020.pdf").exists()
    r = run_tool("refs/missing_refs.py", "--bib", bib, "--pdfdir", pdfdir, home=tmp_path)
    assert r.returncode == 0 and "NOT checked against your own PDFs" in r.stdout
    assert "inlit2020" in (pdfdir / "_missing.tsv").read_text(encoding="utf-8")   # not subtracted
    r = run_tool("refs/missing_refs.py", "--bib", bib, "--pdfdir", pdfdir, "--apply", home=tmp_path)
    assert r.returncode != 0                                                      # --apply needs --library


def test_default_pdfdir_is_refs_pdf(tmp_path):
    bib, _pdfdir, _lib = make_project(tmp_path)
    r = run_tool("refs/missing_refs.py", "--bib", bib, home=tmp_path, cwd=tmp_path)
    assert r.returncode == 0, r.stderr
    assert (tmp_path / "refs-pdf" / "_missing.md").exists()


def test_hand_filed_names_count_as_present(tmp_path):
    rc = load_tool("refs/refs_common.py")
    pdfdir = tmp_path / "refs-pdf"
    pdfdir.mkdir()
    (pdfdir / "03 [Lee 2020] Designing tangible interfaces.pdf").write_bytes(b"%PDF-x")
    (pdfdir / "04 [Zed 1999] Something unrelated.pdf").write_bytes(b"%PDF-x")
    (pdfdir / "exact2018.pdf").write_bytes(b"%PDF-x")
    es = [{"key": "lee2020", "author": "Lee, Kim", "year": "2020", "title": "Designing Tangible Interfaces"},
          {"key": "wu2018", "author": "Wu, Lin", "year": "2018", "title": "An Unindexed Report"},
          {"key": "exact2018", "author": "Q, R", "year": "2018", "title": "Whatever"}]
    have, amb = rc.present_keys(es, pdfdir)
    assert have == {"lee2020", "exact2018"} and amb == {}
    (pdfdir / "05 [Lee 2020] Designing tangible interfaces revisited.pdf").write_bytes(b"%PDF-x")
    (pdfdir / "03 [Lee 2020] Designing tangible interfaces.pdf").unlink()
    (pdfdir / "06 [Lee 2020] Designing tangible interfaces II.pdf").write_bytes(b"%PDF-x")
    have, amb = rc.present_keys(es[:1], pdfdir)
    assert have == {"lee2020"} and len(amb["lee2020"]) == 2


def test_missing_refs_cli_respects_hand_filed_pdf(tmp_path):
    bib = tmp_path / "r.bib"
    bib.write_text("@article{lee2020, author={Lee, Kim}, title={Designing tangible interfaces}, "
                   "year={2020}, doi={10.1/x}}\n@article{wu2018, author={Wu, Lin}, "
                   "title={An Unindexed Report}, year={2018}, doi={10.1/y}}\n", encoding="utf-8")
    pdfdir = tmp_path / "refs-pdf"
    pdfdir.mkdir()
    (pdfdir / "03 [Lee 2020] Designing tangible interfaces.pdf").write_bytes(b"%PDF-x")
    r = run_tool("refs/missing_refs.py", "--bib", bib, "--pdfdir", pdfdir, home=tmp_path)
    assert r.returncode == 0, r.stderr
    rows = list(csv.DictReader(open(pdfdir / "_missing.tsv", encoding="utf-8"), delimiter="\t"))
    assert [x["key"] for x in rows] == ["wu2018"]


def test_inbox_skips_hand_filed_entries(ib):
    ib.populate()
    ib.pdfdir.mkdir()
    (ib.pdfdir / "01 [Lee and Park 2021] Tangible Feedback for Remote Collaboration in Design Studios.pdf"
     ).write_bytes(b"%PDF-x")
    r = ib.run("--all")
    assert r.returncode == 0, r.stderr
    assert "Missing 2" in r.stdout and "lee2021" not in r.stdout.split("Still missing")[0].split("Matched")[1]


# ------------------------------------------------------------------ inbox_ingest
class Inbox:
    """A project, an inbox at HOME/Downloads (the default location) and a trash at HOME."""

    def __init__(self, tmp):
        self.home = Path(tmp)
        self.bib = self.home / "refs.bib"
        self.bib.write_text(INBOX_BIB, encoding="utf-8")
        self.pdfdir = self.home / "refs-pdf"
        self.inbox = self.home / "Downloads"
        self.inbox.mkdir()
        self.trash = trash_of(self.home)
        self.lib = self.home / "library"
        self.lib.mkdir()

    def populate(self):
        make_pdf(self.inbox / "10.1145_3544548.3581234.pdf",
                 "Tangible Feedback for Remote Collaboration in Design Studios", "Kim Lee, Jun Park")
        make_pdf(self.inbox / "speculative.pdf", "Speculative Kitchens and Domestic Futures", "Lin Wu")
        shutil.copy(self.inbox / "speculative.pdf", self.inbox / "speculative (1).pdf")
        make_pdf(self.inbox / "10.1016_j.destud.2019.01.004.pdf",
                 "Supplementary Material Appendix Tables", "Anonymous")      # right DOI, other content
        make_pdf(self.inbox / "invoice.pdf", "Hotel Invoice Booking Confirmation", "Front Desk")

    def run(self, *extra, env=None):
        return run_tool("refs/inbox_ingest.py", "--bib", self.bib, "--pdfdir", self.pdfdir, *extra,
                        home=self.home, env=env)


@pytest.fixture
def ib(tmp_path):
    return Inbox(tmp_path)


def test_scan_inbox_merges_identical_copies(ib):
    ii = load_tool("refs/inbox_ingest.py")
    ib.populate()
    spec = [f for f in ii.scan_inbox(str(ib.inbox), None) if f["name"].startswith("speculative")]
    assert len(spec) == 1 and spec[0]["name"] == "speculative.pdf"   # shortest name kept
    assert len(spec[0]["dups"]) == 1


def test_hours_window(ib):
    ii = load_tool("refs/inbox_ingest.py")
    ib.populate()
    old = ib.inbox / "invoice.pdf"
    os.utime(old, (1_000_000_000, 1_000_000_000))
    names = {f["name"] for f in ii.scan_inbox(str(ib.inbox), 72)}
    assert "invoice.pdf" not in names and "speculative.pdf" in names
    assert "invoice.pdf" in {f["name"] for f in ii.scan_inbox(str(ib.inbox), None)}


@needs_pdftotext
def test_match_tiers(ib):
    ii = load_tool("refs/inbox_ingest.py")
    rc = load_tool("refs/refs_common.py")
    ib.populate()
    missing = rc.parse_bib(ib.bib)
    assign, conflicts, mismatches, unmatched = ii.match(ii.scan_inbox(str(ib.inbox), None), missing)
    assert sorted(assign) == ["lee2021", "wu2018"]
    assert assign["lee2021"][1]["doi"] and assign["lee2021"][1]["tier"] == "verified"
    assert [e["key"] for _, e, _ in mismatches] == ["ono2019"]       # right DOI, wrong content: reported
    assert [f["name"] for f in unmatched] == ["invoice.pdf"]
    assert conflicts == []


@needs_pdftotext
def test_preview_writes_nothing(ib):
    ib.populate()
    r = ib.run("--all")
    assert r.returncode == 0, r.stderr
    assert "Preview only" in r.stdout and "Matched (2)" in r.stdout
    assert not ib.pdfdir.exists() or not list(ib.pdfdir.glob("*.pdf"))
    assert len(list(ib.inbox.iterdir())) == 5 and not list(ib.trash.iterdir())


@needs_pdftotext
def test_apply_library_clean(ib):
    ib.populate()
    (ib.lib / "Someone 2000 - Old.pdf").write_bytes(b"%PDF-old")
    r = ib.run("--all", "--apply", "--library", ib.lib, "--to-library", "--clean")
    assert r.returncode == 0, r.stderr + r.stdout
    assert sorted(p.name for p in ib.pdfdir.glob("*.pdf")) == ["lee2021.pdf", "wu2018.pdf"]
    log = list(csv.DictReader(open(ib.pdfdir / "_inbox_log.tsv", encoding="utf-8"), delimiter="\t"))
    assert sorted(x["key"] for x in log) == ["lee2021", "wu2018"]
    assert {x["source"] for x in log} == {"10.1145_3544548.3581234.pdf", "speculative.pdf"}
    names = sorted(p.name for p in ib.lib.iterdir())
    assert "Lee 2021 - Tangible Feedback for Remote Collaboration in Design Studios.pdf" in names
    assert "Wu 2018 - Speculative Kitchens and Domestic Futures.pdf" in names
    assert "Someone 2000 - Old.pdf" in names
    # only filed sources and their identical copy go to the Trash; the rest stays
    assert sorted(p.name for p in ib.inbox.iterdir()) == ["10.1016_j.destud.2019.01.004.pdf", "invoice.pdf"]
    assert len(list(ib.trash.iterdir())) == 3
    # a second run finds nothing missing among the filed ones and does not refile
    r2 = ib.run("--all")
    assert r2.returncode == 0 and "Missing 1" in r2.stdout


@needs_pdftotext
def test_library_dedupe_by_content_in_subfolder(ib):
    ib.populate()
    (ib.lib / "sub").mkdir()
    shutil.copy(ib.inbox / "speculative.pdf", ib.lib / "sub" / "something else entirely.pdf")
    r = ib.run("--all", "--apply", "--library", ib.lib, "--to-library")
    assert r.returncode == 0, r.stderr
    assert not (ib.lib / "Wu 2018 - Speculative Kitchens and Domestic Futures.pdf").exists()
    assert "already in library" in r.stdout and "same content as something else entirely.pdf" in r.stdout
    assert (ib.lib / "Lee 2021 - Tangible Feedback for Remote Collaboration in Design Studios.pdf").exists()


@needs_pdftotext
def test_scanned_pdf_falls_back_to_filename_and_doi(ib):
    make_pdf(ib.inbox / "10.1145_3544548.3581234.pdf", pages=4, text=False)       # DOI in the name
    make_pdf(ib.inbox / "Speculative Kitchens and Domestic Futures scan.pdf", pages=5, text=False)
    r = ib.run("--all")
    assert r.returncode == 0, r.stderr
    assert "lee2021" in r.stdout and "DOI match, scanned(no-text)" in r.stdout
    assert "wu2018" in r.stdout and "LOW-CONFIDENCE file name title similarity" in r.stdout


def test_without_pdftotext_uses_filenames_only(ib, tmp_path):
    empty = tmp_path / "emptybin"
    empty.mkdir()
    make_pdf(ib.inbox / "10.1145_3544548.3581234.pdf", "Tangible Feedback", "Kim Lee")
    make_pdf(ib.inbox / "speculative kitchens domestic futures.pdf", "x", "y")
    make_pdf(ib.inbox / "invoice.pdf", "Hotel Invoice", "Desk")
    r = ib.run("--all", "--apply", env={"PATH": str(empty)})
    assert r.returncode == 0, r.stderr + r.stdout
    assert "`pdftotext` (poppler) not found" in r.stdout
    assert sorted(p.name for p in ib.pdfdir.glob("*.pdf")) == ["lee2021.pdf", "wu2018.pdf"]
    log = list(csv.DictReader(open(ib.pdfdir / "_inbox_log.tsv", encoding="utf-8"), delimiter="\t"))
    assert {x["key"]: x["tier"] for x in log} == {"lee2021": "verified", "wu2018": "low"}
    assert (ib.inbox / "invoice.pdf").exists()


def test_clean_requires_apply_and_to_library_requires_library(ib):
    ib.populate()
    assert ib.run("--all", "--clean").returncode != 0
    assert ib.run("--all", "--apply", "--to-library").returncode != 0
    assert ib.run("--all", "--to-library", "--library", ib.lib).returncode != 0
    assert len(list(ib.inbox.iterdir())) == 5


def test_clean_refused_without_trash_folder(ib):
    ib.populate()
    for p in (ib.home / ".Trash", ib.home / ".local"):
        if p.exists():
            shutil.rmtree(p)
    r = ib.run("--all", "--apply", "--clean")
    assert r.returncode != 0 and "Refusing --clean" in r.stdout
    assert len(list(ib.inbox.iterdir())) == 5 and not ib.pdfdir.exists() or not list(ib.pdfdir.glob("*.pdf"))


def test_missing_inbox_folder_is_reported(ib):
    shutil.rmtree(ib.inbox)
    r = ib.run("--all")
    assert r.returncode != 0 and "Inbox folder not found" in r.stdout
