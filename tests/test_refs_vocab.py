"""tools/refs (lit_map, snowball, retraction_scan, pdf_fetch) and tools/vocab/fetch_awl.
Every network function is replaced with canned data; the conftest fixture blocks
sockets, so a call that slips through fails the test instead of going online."""
import csv
import json
import sys
import urllib.error

import pytest

from conftest import load_tool, run_tool


def _main(monkeypatch, mod, *argv):
    monkeypatch.setattr(sys, "argv", ["prog", *map(str, argv)])
    return mod.main()


# ---------------------------------------------------------------- lit_map
def test_lit_map_selftest():
    r = run_tool("refs/lit_map.py", "--selftest")
    assert r.returncode == 0 and "all passed" in r.stdout


def test_lit_map_query(monkeypatch, tmp_path):
    lm = load_tool("refs/lit_map.py")
    works = [{"id": f"W{i}", "title": f"Paper {i}", "publication_year": 2025, "cited_by_count": i,
              "doi": f"https://doi.org/10.1000/p{i}", "referenced_works": ["https://openalex.org/R1"],
              "primary_location": {"source": {"display_name": "CHI"}}} for i in range(3)]
    classic = {"id": "https://openalex.org/R1", "title": "A Classic", "publication_year": 2007,
               "cited_by_count": 900, "doi": "https://doi.org/10.1000/classic"}
    calls = []

    def fake_get(url, email, retries=2):
        calls.append(url)
        if "filter=openalex:" in url:
            return {"results": [classic]}
        return {"results": works, "meta": {"next_cursor": None}}

    monkeypatch.setattr(lm, "get", fake_get)
    out, csv_out = tmp_path / "map.md", tmp_path / "refs.csv"
    _main(monkeypatch, lm, "--query", "design", "--limit", "10", "--email", "t@example.org",
          "--out", out, "--csv", csv_out)
    text = out.read_text(encoding="utf-8")
    assert "| 1 | 3 | 100% | 1 | 2007 | 900 | A Classic | 10.1000/classic |" in text
    rows = list(csv.DictReader(csv_out.open(encoding="utf-8")))
    assert rows[0]["title"] == "A Classic"
    assert any("title_and_abstract.search:design" in c for c in calls)


def test_lit_map_requires_email(monkeypatch):
    lm = load_tool("refs/lit_map.py")
    monkeypatch.delenv("OPENALEX_MAILTO", raising=False)
    with pytest.raises(SystemExit) as e:
        _main(monkeypatch, lm, "--query", "design", "--email", "")
    assert e.value.code == 2


# ---------------------------------------------------------------- snowball
SEED = {"id": "https://openalex.org/W1", "referenced_works": ["https://openalex.org/W7"],
        "related_works": []}


def _work(i, cites=10):
    return {"id": f"https://openalex.org/W{i}", "title": f"Citing paper {i}", "publication_year": 2024,
            "cited_by_count": cites, "doi": f"https://doi.org/10.1000/c{i}",
            "primary_location": {"source": {"display_name": "DIS"}}}


def test_snowball_forward(monkeypatch, tmp_path, capsys):
    sb = load_tool("refs/snowball.py")

    def fake(url, email):
        if "/works/doi:" in url:
            return SEED
        assert "filter=cites:W1" in url
        return {"results": [_work(2, 50), _work(3, 5)], "meta": {"next_cursor": None}}

    monkeypatch.setattr(sb, "http_json", fake)
    out = tmp_path / "fwd.csv"
    _main(monkeypatch, sb, "--doi", "10.1000/seed", "--out", out)
    rows = list(csv.DictReader(out.open(encoding="utf-8")))
    assert [r["doi"] for r in rows] == ["10.1000/c2", "10.1000/c3"]
    assert "incomplete" not in capsys.readouterr().err


def test_snowball_backward_from_bib(monkeypatch, tmp_path, capsys):
    sb = load_tool("refs/snowball.py")
    bib = tmp_path / "refs.bib"
    bib.write_text("@article{a,\n  title = {A},\n  doi = {10.1000/seed}\n}\n", encoding="utf-8")

    def fake(url, email):
        if "/works/doi:" in url:
            return SEED
        assert "openalex_id:W7" in url
        return {"results": [_work(7)]}

    monkeypatch.setattr(sb, "http_json", fake)
    _main(monkeypatch, sb, "--bib", bib, "--direction", "backward")
    assert "Citing paper 7" in capsys.readouterr().out


def test_snowball_429_falls_back_to_semantic_scholar(monkeypatch, capsys):
    sb = load_tool("refs/snowball.py")
    monkeypatch.setattr(sb.time, "sleep", lambda s: None)

    def fake(url, email):
        if "openalex" in url:
            raise urllib.error.HTTPError(url, 429, "Too Many Requests", {}, None)
        return {"data": [{"citingPaper": {"title": "From S2", "year": 2023, "citationCount": 4,
                                          "externalIds": {"DOI": "10.1000/s2"}}}]}

    monkeypatch.setattr(sb, "http_json", fake)
    _main(monkeypatch, sb, "--doi", "10.1000/seed")
    captured = capsys.readouterr()
    assert "From S2" in captured.out and "Semantic Scholar fallback" in captured.err


# ---------------------------------------------------------------- retraction_scan
def test_retraction_scan(monkeypatch, tmp_path, capsys):
    rs = load_tool("refs/retraction_scan.py")
    monkeypatch.setattr(rs, "OA_DEAD", False)
    bib = tmp_path / "refs.bib"
    bib.write_text("@article{good, title={Good}, doi={10.1000/good}}\n"
                   "@article{bad, title={Bad}, doi={10.1000/bad}}\n"
                   "@book{old, title={An Old Book}}\n", encoding="utf-8")

    def fake(url, ua, timeout=25):
        bad = "bad" in url
        if "crossref" in url:
            msg = {"title": ["Bad" if bad else "Good"]}
            if bad:
                msg["updated-by"] = [{"type": "retraction", "DOI": "10.1000/notice"}]
            return {"message": msg}
        return {"is_retracted": bad}

    monkeypatch.setattr(rs, "get_json", fake)
    out = tmp_path / "report.json"
    code = _main(monkeypatch, rs, "--bib", bib, "--sleep", "0", "--out", out)
    assert code == 1
    rep = json.loads(out.read_text(encoding="utf-8"))
    assert rep["counts"] == {"OK": 1, "RETRACTED": 1, "NOT_FOUND": 0, "API_ERROR": 0, "NO_DOI": 1}
    assert rep["scanned"] == 2
    assert "RETRACTED bad" in capsys.readouterr().out


def test_retraction_scan_api_error_is_not_a_pass(monkeypatch):
    rs = load_tool("refs/retraction_scan.py")
    monkeypatch.setattr(rs, "OA_DEAD", False)

    def fake(url, ua, timeout=25):
        if "crossref" in url:
            return {"message": {"title": ["X"]}}
        raise urllib.error.HTTPError(url, 500, "err", {}, None)

    monkeypatch.setattr(rs, "get_json", fake)
    assert _main(monkeypatch, rs, "10.1000/x", "--sleep", "0") == 2


def test_retraction_scan_parsers(tmp_path):
    rs = load_tool("refs/retraction_scan.py")
    bib = tmp_path / "r.bib"
    bib.write_text("@article{k1,\n  _doi = {10.1/disabled},\n  title = {T {nested}},\n}\n"
                   "@comment{ignored}\n", encoding="utf-8")
    assert rs.parse_bib(bib) == [{"key": "k1", "title": "T {nested}", "doi": ""}]
    lst = tmp_path / "d.txt"
    lst.write_text("https://doi.org/10.1000/a  # note\n\n10.1000/b\n", encoding="utf-8")
    assert [e["doi"] for e in rs.parse_doi_list(lst)] == ["10.1000/a", "10.1000/b"]


# ---------------------------------------------------------------- pdf_fetch
def test_pdf_fetch_open_access_path(monkeypatch, tmp_path, capsys):
    pf = load_tool("refs/pdf_fetch.py")
    monkeypatch.setattr(pf, "extra_oa_urls", lambda doi: [f"https://oa.example.org/{doi}.pdf"])
    monkeypatch.setattr(pf, "oa_landing_urls", lambda doi: [])
    monkeypatch.setattr(pf, "resolve_title", lambda title, year="": ("", ""))

    def fake_get(url, timeout=45, cookies=None, referer=None, impersonate="chrome"):
        if "good" in url:
            return 200, "application/pdf", b"%PDF-1.4 fake", {}
        return 403, "text/html", b"<html>Just a moment...</html>", {}

    monkeypatch.setattr(pf, "http_get", fake_get)
    bib = tmp_path / "refs.bib"
    bib.write_text("@article{good,\n  title = {Good},\n  doi = {10.1000/good}\n}\n"
                   "@book{book1,\n  title = {A Book Without Any Identifier},\n  year = {1999}\n}\n",
                   encoding="utf-8")
    out = tmp_path / "pdfs"
    _main(monkeypatch, pf, "--bib", bib, "--out", out, "--no-browser", "10.1000/paywalled")
    assert (out / "good.pdf").read_bytes().startswith(b"%PDF-")
    text = capsys.readouterr().out
    assert "1/2 obtained" in text
    assert "[MANUAL] book1" in text and "[MISS] 10.1000/paywalled" in text


def test_pdf_fetch_helpers(tmp_path):
    pf = load_tool("refs/pdf_fetch.py")
    assert pf.looks_pdf(b"%PDF-1.7") and not pf.looks_pdf(b"<html>")
    assert pf.is_bot_block(403, "text/html", b"<title>Just a moment...</title>",
                           {"cf-mitigated": "challenge"})
    bib = tmp_path / "r.bib"
    bib.write_text("@misc{lora,\n  title = {Low-Rank Adaptation},\n  eprint = {2106.09685},\n"
                   "  year = {2021}\n}\n", encoding="utf-8")
    e = pf._parse_bib(bib)[0]
    assert (e["key"], e["arxiv"], e["doi"], e["year"]) == ("lora", "2106.09685", "", "2021")
    assert pf.resolve_title("Too short") == ("", "")
    assert pf._safe("a/b c") == "a_b_c"


# ---------------------------------------------------------------- fetch_awl
RTF = (r"{\rtf1 Sublist 1 of the Academic Word List\par analyse\par \tab analysed\par "
       r"\tab analysis\par approach\par \tab approaches\par "
       r"Sublist 2 of the Academic Word List\par achieve\par \tab achievement\par}")


def test_fetch_awl_parse_rtf_and_html():
    fa = load_tool("vocab/fetch_awl.py")
    assert fa.parse_rtf(RTF) == [("analyse", 1, ["analysed", "analysis"]),
                                 ("approach", 1, ["approaches"]), ("achieve", 2, ["achievement"])]
    page = ("<main><h1>The Academic Word List</h1><p>analyse</p><ul><li>analysis</li>"
            "<li>analysed</li></ul><p>albeit</p></main>")
    assert fa.parse_sublist(page) == [("analyse", ["analysed", "analysis"]), ("albeit", [])]


def test_fetch_awl_main_write_and_check(monkeypatch, tmp_path, capsys):
    fa = load_tool("vocab/fetch_awl.py")
    monkeypatch.setattr(fa, "fetch", lambda url, timeout=30, binary=False: RTF.encode("latin-1"))
    out = tmp_path / "awl.tsv"
    assert _main(monkeypatch, fa, "--out", out) == 0
    assert fa.read_tsv(out)["analyse"] == (1, ["analysed", "analysis"])
    assert _main(monkeypatch, fa, "--check", out) == 0
    out.write_text("headword\tsublist\trelated_forms\nzzz\t1\t\n", encoding="utf-8")
    assert _main(monkeypatch, fa, "--check", out) == 1


def test_fetch_awl_network_failure(monkeypatch):
    fa = load_tool("vocab/fetch_awl.py")

    def down(url, timeout=30, binary=False):
        raise OSError("offline")

    monkeypatch.setattr(fa, "fetch", down)
    assert _main(monkeypatch, fa, "--source", "html", "--sleep", "0") == 2


# ---------------------------------------------------------------- OpenAlex key
@pytest.mark.parametrize("rel", ["refs/lit_map.py", "refs/snowball.py",
                                 "refs/retraction_scan.py", "refs/pdf_fetch.py"])
def test_openalex_key_goes_only_to_openalex_as_header(monkeypatch, rel):
    tool = load_tool(rel)
    monkeypatch.delenv("OPENALEX_API_KEY", raising=False)
    assert tool.oa_headers("https://api.openalex.org/works?search=x") == {}
    monkeypatch.setenv("OPENALEX_API_KEY", " k123 ")
    assert tool.oa_headers("https://api.openalex.org/works/doi:10.1/x") == {"Authorization": "Bearer k123"}
    # other hosts, and look-alike hosts, never receive the key
    assert tool.oa_headers("https://api.crossref.org/works/10.1/x") == {}
    assert tool.oa_headers("https://api.openalex.org.evil.example/works") == {}
    assert tool.oa_headers("https://api.semanticscholar.org/graph/v1/paper/x?openalex=1") == {}
