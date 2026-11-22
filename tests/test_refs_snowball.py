"""tools/refs/snowball.py: OpenCitations as a second source, cross-source merging, and the
Semantic Scholar pacing/backoff. Offline: http_json (or urlopen) is replaced with fakes.

The fake OpenCitations payload copies the real Index v2 shape: a JSON array whose
`citing`/`cited` fields hold several space-separated ids (omid:, openalex:, doi:) in no
fixed order, sometimes with no doi: at all."""
import csv
import io
import urllib.error

import pytest

from conftest import load_tool

SEED = "10.1145/2207676.2208538"

OC_CITATIONS = [
    {"citing": "omid:br/06010004801 openalex:W4407941986 doi:10.1145/3689050.3704422",
     "cited": "omid:br/061502990030 doi:10.1145/2207676.2208538"},
    {"citing": "omid:br/06010089436 doi:10.1145/3698061.3726947 openalex:W4411534394",
     "cited": "omid:br/061502990030 doi:10.1145/2207676.2208538"},
    {"citing": "omid:br/06010555555 openalex:W5 doi:10.1145/shared.paper",
     "cited": "omid:br/061502990030 doi:10.1145/2207676.2208538"},
    {"citing": "omid:br/06010999999 openalex:W1",            # no DOI: must not be invented
     "cited": "omid:br/061502990030 doi:10.1145/2207676.2208538"},
]
OC_REFERENCES = [
    {"citing": "omid:br/061502990030 doi:10.1145/2207676.2208538",
     "cited": "omid:br/06102657213 openalex:W128879900 doi:10.1145/229868.230031"},
    {"citing": "omid:br/061502990030 doi:10.1145/2207676.2208538",
     "cited": "omid:br/06103645528 doi:10.1145/1518701.1518765 openalex:W2127639440"},
]


def http_err(url, code, headers=None):
    return urllib.error.HTTPError(url, code, "err", headers or {}, None)


class Net:
    """Fake network: each source is independently "ok", "429" or "down"."""

    def __init__(self, oa="429", s2="429", oc="ok"):
        self.oa, self.s2, self.oc = oa, s2, oc
        self.urls = []

    def __call__(self, url, email):
        self.urls.append(url)
        if "opencitations" in url:
            if self.oc == "ok":
                return OC_CITATIONS if "/citations/" in url else OC_REFERENCES
            if self.oc == "429":
                raise http_err(url, 429)
            raise urllib.error.URLError("connection refused")
        if "semanticscholar" in url:
            if self.s2 == "ok":
                return {"data": [
                    {"citingPaper": {"title": "Via S2 only", "year": 2024, "venue": "CHI",
                                     "citationCount": 7, "externalIds": {"DOI": "10.1145/S2ONLY"}}},
                    {"citingPaper": {"title": "Shared Paper", "year": 2025, "venue": "UIST",
                                     "citationCount": 3, "externalIds": {"DOI": "10.1145/SHARED.PAPER"}}}]}
            raise http_err(url, 429)
        if "openalex" in url:
            if self.oa == "429":
                raise http_err(url, 429)
            if "/works/doi:" in url:
                return {"id": "https://openalex.org/W2139470221"}
            return {"results": [{
                "cited_by_count": 99, "publication_year": 2025,
                "primary_location": {"source": {"display_name": "UIST"}},
                "title": "Shared Paper", "doi": "https://doi.org/10.1145/Shared.Paper",
                "best_oa_location": {"pdf_url": "http://example.org/oa.pdf"}}],
                "meta": {"next_cursor": None}}
        raise AssertionError("unexpected URL: " + url)


@pytest.fixture
def sb():
    return load_tool("refs/snowball.py")


def run_main(sb, monkeypatch, capsys, net, direction="forward", out_csv=None):
    monkeypatch.setattr(sb, "http_json", net)
    monkeypatch.setattr(sb.time, "sleep", lambda *a: None)
    argv = ["snowball.py", "--doi", SEED, "--direction", direction, "--limit", "50"]
    if out_csv:
        argv += ["--out", str(out_csv)]
    monkeypatch.setattr(sb.sys, "argv", argv)
    sb.main()
    cap = capsys.readouterr()
    return cap.out, cap.err


def test_oc_doi_picks_the_doi_token_lowercased(sb):
    assert sb.oc_doi("omid:br/1 openalex:W2 doi:10.1145/3689050.3704422") == "10.1145/3689050.3704422"
    assert sb.oc_doi("omid:br/1 doi:10.1145/ABC.DEF openalex:W2") == "10.1145/abc.def"
    assert sb.oc_doi("omid:br/06010999999 openalex:W1") == ""
    assert sb.oc_doi("") == "" and sb.oc_doi(None) == ""


def test_opencitations_still_answers_when_openalex_and_s2_fail(sb, monkeypatch, capsys):
    net = Net(oa="429", s2="429", oc="ok")
    out, err = run_main(sb, monkeypatch, capsys, net)
    assert "10.1145/3689050.3704422" in out and "10.1145/3698061.3726947" in out
    assert "S2 not checked" in err
    assert SEED not in out.split("<")[0]   # the seed itself is never a result


def test_opencitations_failure_is_reported_and_does_not_hide_others(sb, monkeypatch, capsys):
    for mode in ("429", "down"):
        net = Net(oa="ok", s2="ok", oc=mode)
        out, err = run_main(sb, monkeypatch, capsys, net)
        assert any("OpenCitations not checked" in ln for ln in err.splitlines()), (mode, err)
        assert "Shared Paper" in out, mode


def test_records_without_doi_are_skipped_and_counted(sb, monkeypatch, capsys):
    out, err = run_main(sb, monkeypatch, capsys, Net(oa="429", s2="429", oc="ok"))
    assert "W1" not in out
    assert "skipped 1 record(s) without a DOI" in err


def test_merge_on_lowercased_doi_counts_one_seed_once(sb, monkeypatch, capsys, tmp_path):
    p = tmp_path / "o.csv"
    run_main(sb, monkeypatch, capsys, Net(oa="ok", s2="ok", oc="ok"), out_csv=p)
    rows = list(csv.DictReader(io.StringIO(p.read_text(encoding="utf-8"))))
    shared = [r for r in rows if r["doi"].lower() == "10.1145/shared.paper"]
    assert len(shared) == 1
    shared = shared[0]
    assert shared["seed_hits"] == "1"
    assert {"openalex", "opencitations"} <= set(shared["sources"].split(";"))
    assert shared["title"] == "Shared Paper"
    only_oc = next(r for r in rows if r["doi"] == "10.1145/3698061.3726947")
    assert only_oc["sources"] == "opencitations" and only_oc["title"] == ""


def test_backward_uses_references_and_related_skips_opencitations(sb, monkeypatch, capsys):
    net = Net(oa="429", s2="429", oc="ok")
    out, _ = run_main(sb, monkeypatch, capsys, net, "backward")
    assert any("/references/doi:" in u for u in net.urls)
    assert "10.1145/229868.230031" in out and "10.1145/1518701.1518765" in out
    net = Net(oa="429", s2="429", oc="ok")
    run_main(sb, monkeypatch, capsys, net, "related")
    assert not any("opencitations" in u for u in net.urls)


class Resp:
    def __init__(self, body=b"[]"):
        self.body = body

    def read(self):
        return self.body

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def test_opencitations_gets_no_email_and_no_key(sb, monkeypatch):
    seen = []
    monkeypatch.setenv("S2_API_KEY", "k-test")
    monkeypatch.setattr(sb.urllib.request, "urlopen",
                        lambda req, timeout=None: seen.append(dict((k.lower(), v) for k, v in req.header_items()))
                        or Resp())
    sb.http_json("https://api.opencitations.net/index/v2/citations/doi:10.1/x", "me@example.org")
    assert "@" not in seen[0]["user-agent"] and "x-api-key" not in seen[0]


def test_s2_key_goes_only_to_semantic_scholar(sb, monkeypatch):
    monkeypatch.setattr(sb, "_S2_KEY_OFF", False)
    monkeypatch.setenv("S2_API_KEY", "k-test")
    assert sb.s2_auth("https://api.semanticscholar.org/graph/v1/paper/x") == {"x-api-key": "k-test"}
    assert sb.s2_auth("https://api.openalex.org/works") == {}
    monkeypatch.delenv("S2_API_KEY")
    assert sb.s2_auth("https://api.semanticscholar.org/graph/v1/paper/x") == {}


def test_s2_backoff_retries_503_then_succeeds(sb, monkeypatch):
    calls, sleeps = [], []
    monkeypatch.setattr(sb, "_S2_LAST", None)
    monkeypatch.setattr(sb.time, "sleep", lambda s: sleeps.append(s))

    def fake(req, timeout=None):
        calls.append(1)
        if len(calls) < 3:
            raise http_err(req.full_url, 503)
        return Resp(b"{}")
    monkeypatch.setattr(sb.urllib.request, "urlopen", fake)
    req = sb.urllib.request.Request("https://api.semanticscholar.org/graph/v1/paper/x")
    sb.s2_open(req, 5)
    assert len(calls) == 3
    assert 2 in sleeps and 4 in sleeps   # exponential backoff, not one fixed wait


def test_s2_gives_up_after_three_retries(sb, monkeypatch):
    monkeypatch.setattr(sb, "_S2_LAST", None)
    monkeypatch.setattr(sb.time, "sleep", lambda s: None)
    calls = []

    def fake(req, timeout=None):
        calls.append(1)
        raise http_err(req.full_url, 429)
    monkeypatch.setattr(sb.urllib.request, "urlopen", fake)
    with pytest.raises(urllib.error.HTTPError):
        sb.s2_open(sb.urllib.request.Request("https://api.semanticscholar.org/graph/v1/paper/x"), 5)
    assert len(calls) == 4


def test_rate_limited_key_falls_back_to_shared_pool(sb, monkeypatch, capsys):
    monkeypatch.setattr(sb, "_S2_KEY_OFF", False)
    monkeypatch.setattr(sb, "_S2_LAST", None)
    monkeypatch.setattr(sb.time, "sleep", lambda s: None)
    keyed = []

    def fake(req, timeout=None):
        has_key = any(k.lower() == "x-api-key" for k in req.headers)
        keyed.append(has_key)
        if has_key:
            raise http_err(req.full_url, 429)
        return Resp(b"{}")
    monkeypatch.setattr(sb.urllib.request, "urlopen", fake)
    req = sb.urllib.request.Request("https://api.semanticscholar.org/graph/v1/paper/x",
                                    headers={"x-api-key": "k-test"})
    sb.s2_open(req, 5)
    assert keyed == [True, False]
    assert sb._S2_KEY_OFF is True
    assert "shared pool" in capsys.readouterr().err


def test_other_hosts_get_a_single_try(sb, monkeypatch):
    calls = []

    def fake(req, timeout=None):
        calls.append(1)
        raise http_err(req.full_url, 503)
    monkeypatch.setattr(sb.urllib.request, "urlopen", fake)
    with pytest.raises(urllib.error.HTTPError):
        sb.s2_open(sb.urllib.request.Request("https://api.openalex.org/works"), 5)
    assert len(calls) == 1
