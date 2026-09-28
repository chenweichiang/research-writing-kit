"""tools/refs/pdf_fetch.py: OpenAIRE Graph API V3 parsing.

The old OpenAIRE Search API (`api.openaire.eu/search/publications`) was officially
retired 2026-05-31; calling it now just times out, and the code used to swallow that
into "no results" so nobody noticed the source had gone dark. This file locks down the
V3 replacement: the endpoint it must call, the shape of the JSON it must read, and the
junk-filtering / DOI-pinning rules that keep it from handing another paper's url (or an
author's institution home page) to the browser layer. Purely offline, every test
replaces `urllib.request.urlopen` with canned bytes; the conftest fixture that blocks
real sockets would fail the test if one slipped through.
"""
import io
import json

import pytest

from conftest import load_tool

pf = load_tool("refs/pdf_fetch.py")


@pytest.fixture(autouse=True)
def clear_cache():
    pf._OPENAIRE_CACHE.clear()
    yield
    pf._OPENAIRE_CACHE.clear()


# Trimmed from a real Graph API V3 response for 10.1145/3025453.3025766 (field names and
# nesting copied as-is). The SMARTech repository instance is added by hand, since this
# DOI happened to have none on the day the fixture was captured, and
# `organizations[].websiteurl` is a genuine V3 field, not an invented one.
FIXTURE = {"header": {"numFound": 1}, "results": [{
    "pids": [{"scheme": "doi", "value": "10.1145/3025453.3025766"}],
    "organizations": [{"legalName": "Georgia Institute of Technology",
                       "websiteurl": "http://www.gatech.edu/"}],
    "instances": [
        {"accessRight": {"label": "CLOSED"}, "hostedBy": {"value": "Unknown Repository"},
         "license": "https://www.acm.org/publications/policies/copyright_policy#Background",
         "urls": ["https://doi.org/10.1145/3025453.3025766"]},
        {"accessRight": {"label": "OPEN"}, "hostedBy": {"value": "Unknown Repository"},
         "urls": ["http://dl.acm.org/ft_gateway.cfm?id=3025766&type=pdf"]},
        {"accessRight": None, "hostedBy": {"value": "DBLP"},
         "urls": ["https://dblp.org/rec/conf/chi/SchlesingerEG17.html",
                  "https://doi.org/10.1145/3025453.3025766"]},
        {"accessRight": None, "hostedBy": {"value": "Unknown Repository"},
         "urls": ["https://dx.doi.org/10.1145/3025453.3025766"]},
        {"accessRight": {"label": "OPEN"}, "hostedBy": {"value": "SMARTech"},
         "urls": ["https://smartech.gatech.edu/handle/1853/99999"]},
    ]}]}


def _serve(monkeypatch, payload):
    def fake_urlopen(req, timeout=20):
        return io.BytesIO(json.dumps(payload).encode())
    monkeypatch.setattr(pf.urllib.request, "urlopen", fake_urlopen)


def _run(monkeypatch, payload, doi="10.1145/3025453.3025766"):
    _serve(monkeypatch, payload)
    return pf._openaire_raw(doi)


def test_institution_homepage_is_not_a_candidate(monkeypatch):
    """organizations[].websiteurl is the authors' institution home page, pure
    waste for the browser layer and never a route to the paper itself."""
    pdfs, lands = _run(monkeypatch, FIXTURE)
    assert "http://www.gatech.edu/" not in pdfs + lands


def test_license_page_is_not_a_candidate(monkeypatch):
    pdfs, lands = _run(monkeypatch, FIXTURE)
    assert not any("copyright_policy" in u for u in pdfs + lands)


def test_ft_gateway_is_recognised_as_pdf(monkeypatch):
    pdfs, lands = _run(monkeypatch, FIXTURE)
    assert any("ft_gateway" in u for u in pdfs)


def test_repository_landing_page_is_kept_as_a_landing_page(monkeypatch):
    pdfs, lands = _run(monkeypatch, FIXTURE)
    assert any("smartech" in u for u in lands), "the institutional repository record must reach L2"


def test_doi_dx_doi_dblp_scopus_are_excluded(monkeypatch):
    """doi.org / dx.doi.org are landing pages main() already visits on its own;
    dblp and scopus are bibliographic indexes, not full text."""
    pdfs, lands = _run(monkeypatch, FIXTURE)
    joined = pdfs + lands
    assert not any("doi.org" in u or "dblp.org" in u for u in joined)


def test_scopus_is_excluded(monkeypatch):
    payload = {"results": [{"pids": [{"value": "10.1/x"}], "instances": [{"urls": [
        "https://www.scopus.com/inward/record.url?partnerID=HzOxMe3b&scp=85076769076"]}]}]}
    assert _run(monkeypatch, payload, doi="10.1/x") == ([], [])


def test_url_embedding_another_dois_is_discarded(monkeypatch):
    """OpenAIRE sometimes merges a book chapter and its journal version into one
    record, or otherwise mixes in a neighbouring paper's url; either way, a url
    that names a different DOI must never be treated as this paper's."""
    payload = {"results": [{"pids": [{"value": "10.1145/3025453.3025766"}], "instances": [
        {"urls": ["https://x.example.org/doi/pdf/10.9999/other.paper"]}]}]}
    assert _run(monkeypatch, payload) == ([], [])


def test_doi_followed_by_a_path_is_still_this_paper(monkeypatch):
    """Fixed 2026-09-28: Frontiers' PDF link is `/articles/<doi>/pdf`. The old check
    matched the whole DOI-shaped substring including the trailing path, so it looked
    like a different (longer) DOI and the open-access PDF was thrown away. A DOI that
    is genuinely a *prefix* of a longer one (immediately followed by an alphanumeric
    character) must still be rejected."""
    doi = "10.3389/fpsyg.2020.01279"
    payload = {"results": [{"pids": [{"value": doi}], "instances": [{"urls": [
        "https://www.frontiersin.org/articles/10.3389/fpsyg.2020.01279/pdf",
        "https://x.example.org/doi/pdf/10.3389/fpsyg.2020.012790"]}]}]}
    pdfs, lands = _run(monkeypatch, payload, doi=doi)
    assert pdfs == ["https://www.frontiersin.org/articles/10.3389/fpsyg.2020.01279/pdf"]
    assert lands == []


def test_record_without_the_target_doi_in_pids_is_dropped_entirely(monkeypatch):
    """The pid filter is supposed to return only this paper; if the API ever changes
    behaviour and returns a neighbouring record instead, none of its urls are usable."""
    payload = {"results": [{"pids": [{"value": "10.9999/someone.elses.paper"}],
                            "instances": [{"urls": ["https://repo.example.edu/handle/1/2"]}]}]}
    assert _run(monkeypatch, payload) == ([], [])


def test_open_access_landing_pages_are_sorted_ahead_of_bibliographic_pages(monkeypatch):
    """Only the first four landing pages are kept, so an OPEN repository copy must not
    be crowded out by four PubMed-style bibliographic entries."""
    payload = {"results": [{"pids": [{"value": "10.1/x"}], "instances": [
        {"accessRight": None, "urls": [f"https://pubmed.ncbi.nlm.nih.gov/{n}" for n in range(4)]},
        {"accessRight": {"label": "OPEN"}, "urls": ["https://hdl.handle.net/11250/2736325"]}]}]}
    pdfs, lands = _run(monkeypatch, payload, doi="10.1/x")
    assert lands[0] == "https://hdl.handle.net/11250/2736325"


def test_the_endpoint_must_be_graph_api_v3(monkeypatch):
    """The old Search API was officially retired 2026-05-31 and now just times out
    without raising. This locks the endpoint down so nobody reintroduces it by accident."""
    seen = []

    def fake_urlopen(req, timeout=20):
        seen.append(req.full_url)
        return io.BytesIO(json.dumps(FIXTURE).encode())

    monkeypatch.setattr(pf.urllib.request, "urlopen", fake_urlopen)
    pf._openaire_raw("10.1145/3025453.3025766")
    assert seen and "/graph/v3/research-products?pid=" in seen[0]
    assert "/search/publications" not in seen[0]


def test_the_same_doi_is_only_looked_up_once(monkeypatch):
    """openaire_urls() wants the PDFs and oa_landing_urls() wants the landing pages;
    both call _openaire_raw() and must share one cached API call."""
    calls = []

    def fake_urlopen(req, timeout=20):
        calls.append(1)
        return io.BytesIO(json.dumps(FIXTURE).encode())

    monkeypatch.setattr(pf.urllib.request, "urlopen", fake_urlopen)
    pf.openaire_urls("10.1145/3025453.3025766")
    pf.oa_landing_urls("10.1145/3025453.3025766")
    assert len(calls) == 1


def test_a_failed_lookup_is_not_cached(monkeypatch):
    """A timeout must not be remembered as "this paper has nothing"; the next call
    for the same DOI has to retry the API, not just replay an empty result."""
    def fail_urlopen(req, timeout=20):
        raise OSError("timeout")

    monkeypatch.setattr(pf.urllib.request, "urlopen", fail_urlopen)
    assert pf._openaire_raw("10.1145/3025453.3025766") == ([], [])
    assert "10.1145/3025453.3025766" not in pf._OPENAIRE_CACHE

    monkeypatch.setattr(pf.urllib.request, "urlopen",
                        lambda req, timeout=20: io.BytesIO(json.dumps(FIXTURE).encode()))
    pdfs, _ = pf._openaire_raw("10.1145/3025453.3025766")
    assert pdfs, "a retry after a failure must reach the network again and succeed"


def test_an_exception_returns_two_empty_lists_not_an_empty_string(monkeypatch):
    def fail_urlopen(req, timeout=20):
        raise OSError("offline")

    monkeypatch.setattr(pf.urllib.request, "urlopen", fail_urlopen)
    assert pf._openaire_raw("10.1000/whatever") == ([], [])
