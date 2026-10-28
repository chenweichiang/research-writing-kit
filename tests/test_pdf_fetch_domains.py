"""tools/refs/pdf_fetch.py and refs_common.py: publisher rules match on the host name,
not on a substring of the whole URL."""
from conftest import load_tool

pf = load_tool("refs/pdf_fetch.py")
rc = load_tool("refs/refs_common.py")


def test_on_domain_matches_host_and_subdomains_only():
    assert pf.on_domain("https://onlinelibrary.wiley.com/doi/10.1/x", "onlinelibrary.wiley.com")
    assert pf.on_domain("https://www.tandfonline.com/doi/full/10.1/x", "tandfonline.com")
    assert not pf.on_domain("https://onlinelibrary.wiley.com.example.org/doi/10.1/x", "onlinelibrary.wiley.com")
    assert not pf.on_domain("https://example.org/?next=dl.acm.org", "dl.acm.org")
    assert not pf.on_domain("", "dl.acm.org")


def test_publisher_patterns_ignore_lookalike_hosts():
    assert pf.publisher_patterns("https://dl.acm.org/doi/10.1145/1", "10.1145/1") == ["https://dl.acm.org/doi/pdf/10.1145/1"]
    assert pf.publisher_patterns("https://example.org/dl.acm.org/doi/10.1145/1", "10.1145/1") == []


def test_entitlement_block_reads_host_and_path():
    assert pf.entitlement_block("https://www.tandfonline.com/doi/abs/10.1/x")
    assert pf.entitlement_block("https://www.tandfonline.com/doi/full/10.1/x") is None
    assert pf.entitlement_block("https://example.org/tandfonline.com/doi/abs/10.1/x") is None
    assert pf.entitlement_block(None) is None


def test_doi_is_read_from_a_doi_url_with_or_without_scheme(tmp_path):
    bib = tmp_path / "refs.bib"
    bib.write_text("@article{a, title={A}, year={2020}, url={https://doi.org/10.1234/ABC}}\n"
                   "@article{b, title={B}, year={2021}, url={dx.doi.org/10.5678/def}}\n"
                   "@article{c, title={C}, year={2022}, url={https://example.org/doi.org/10.9/zzz}}\n", encoding="utf-8")
    doi = {e["key"]: e["doi"] for e in rc.parse_bib(bib)}
    assert doi["a"] and doi["a"].lower() == "10.1234/abc"
    assert doi["b"] and doi["b"].lower() == "10.5678/def"
    assert not doi["c"]
