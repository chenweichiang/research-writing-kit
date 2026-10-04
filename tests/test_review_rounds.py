"""tools/review/review_rounds: the review-round convergence ledger."""
import json
import shutil
from pathlib import Path

from conftest import ROOT, load_tool, run_tool

rr = load_tool("review/review_rounds.py")

HEAD = "round\tdate\tversion\tid\tseverity\trepeat_of\tdisposition\tnote\tsummary\n"
ADJ = "| # | Date | Item | Ruling | Basis |\n|---|---|---|---|---|\n| A15 | 2026-09-05 | Ethics | Leave out | Author |\n"


def write(tmp, body, adj=True):
    p = tmp / "docs"
    p.mkdir(exist_ok=True)
    led = p / "review-rounds.tsv"
    led.write_text(HEAD + body, encoding="utf-8")
    if adj:
        (tmp / "ADJUDICATED.md").write_text(ADJ, encoding="utf-8")
    return led


def test_converged_after_two_clean_rounds(tmp_path):
    led = write(tmp_path,
                "1\t2026-09-01\t0.1.0\tK1\tfatal\t\tfixed\t\tDe-identification rule added late\n"
                "2\t2026-09-05\t0.2.0\tL1\tmajor\tK1\tfixed\t\tDe-identification rule still late\n"
                "3\t2026-09-09\t0.3.0\tM1\tmajor\tL1\tfixed\t\tThe same thing a third time\n")
    r = run_tool("review/review_rounds.py", led)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "recommend stopping" in r.stdout      # rounds 2 and 3 hold only repeats


def test_not_converged_when_new_major(tmp_path):
    led = write(tmp_path,
                "1\t2026-09-01\t0.1.0\tK1\tfatal\t\tfixed\t\tA\n"
                "2\t2026-09-05\t0.2.0\tL1\tmajor\t\tfixed\t\tB a wholly new problem\n")
    ok, why = rr.converged(rr.table(rr.load(str(led))))
    assert not ok
    assert "major 1" in why


def test_not_converged_names_the_round_with_new_findings(tmp_path):
    # the latest round is clean but the one before it is not: the message names the earlier round
    led = write(tmp_path,
                "1\t2026-09-01\t0.1.0\tK1\tfatal\t\tfixed\t\tA\n"
                "2\t2026-09-05\t0.2.0\tL1\tmajor\t\tfixed\t\tB a wholly new problem\n"
                "3\t2026-09-09\t0.3.0\tM1\tmajor\tL1\tfixed\t\tB again\n")
    ok, why = rr.converged(rr.table(rr.load(str(led))))
    assert not ok
    assert why.startswith("round 2 ") and "major 1" in why, why


def test_reraising_adjudicated_without_evidence_fails(tmp_path):
    led = write(tmp_path, "1\t2026-09-01\t0.1.0\tK1\tfatal\tA15\tdeclined\t\tEthics exemption not stated\n")
    r = run_tool("review/review_rounds.py", led)
    assert r.returncode == 1
    assert "without stating new evidence" in r.stdout


def test_reraising_with_evidence_ok(tmp_path):
    led = write(tmp_path, "1\t2026-09-01\t0.1.0\tK1\tfatal\tA15\tdeclined\tNew evidence: the venue's 10-01 rule requires it\tEthics\n")
    assert run_tool("review/review_rounds.py", led).returncode == 0


def test_prior_declined_counts_as_settled(tmp_path):
    led = write(tmp_path,
                "1\t2026-09-01\t0.1.0\tK1\tmajor\t\tdeclined\t\tOver the page limit\n"
                "2\t2026-09-05\t0.2.0\tL1\tmajor\tK1\tdeclined\t\tOver the page limit again\n")
    assert run_tool("review/review_rounds.py", led).returncode == 1   # re-raising a declined item needs new evidence too


def test_dangling_repeat(tmp_path):
    led = write(tmp_path, "1\t2026-09-01\t0.1.0\tK1\tmajor\tZ9\tfixed\t\tx\n")
    r = run_tool("review/review_rounds.py", led)
    assert r.returncode == 1
    assert "is in no earlier round" in r.stdout


def test_bad_severity_and_withdrawn_excluded(tmp_path):
    led = write(tmp_path,
                "1\t2026-09-01\t0.1.0\tK1\tminor\t\tfixed\t\tx\n"
                "1\t2026-09-01\t0.1.0\tK2\tfatal\t\twithdrawn\t\tReviewer misjudged\n")
    rows = rr.load(str(led))
    assert any("severity" in e for e in rr.check(rows, set()))
    assert rr.table(rows)["1"]["fatal_new"] == 0      # a withdrawn finding is not counted as new


def test_suggest_flags_disguised_repeat(tmp_path):
    led = write(tmp_path,
                "1\t2026-09-01\t0.1.0\tK1\tfatal\t\tfixed\t\tThe de-identification rule for Latin words was added only in the second pass and screens only the resampled part\n"
                "2\t2026-09-05\t0.2.0\tL4\tfatal\t\tpending\t\tDe-identification rule for Latin words was added only in the second pass; only the resampled part is screened\n")
    r = run_tool("review/review_rounds.py", led, "--suggest")
    assert "L4 ~ round 1 K1" in r.stdout


def test_chinese_disposition_aliases(tmp_path):
    led = write(tmp_path,
                "1\t2026-09-01\t0.1.0\tK1\tmajor\t\t裁定不改\t\t頁數超過\n"
                "1\t2026-09-01\t0.1.0\tK2\tfatal\t\t撤回\t\t審查誤判\n"
                "1\t2026-09-01\t0.1.0\tK3\tmajor\t\t待裁定\t\t圖 2 看不清\n"
                "2\t2026-09-05\t0.2.0\tL1\tmajor\tK1\t已改\t\t頁數又超過\n")
    rows = rr.load(str(led))
    assert [r["disposition"] for r in rows] == ["declined", "withdrawn", "pending", "fixed"]
    assert rr.table(rows)["1"]["withdrawn"] == 1
    r = run_tool("review/review_rounds.py", led)
    assert r.returncode == 1                      # K1 was ruled 裁定不改 (declined): the repeat needs new evidence
    assert "without stating new evidence" in r.stdout
    assert not any("disposition" in e for e in rr.check(rows, set()))


def test_template_ledger_is_sound():
    tpl = ROOT / "tools" / "review" / "review-rounds.template.tsv"
    r = run_tool("review/review_rounds.py", tpl, "--json")
    assert r.returncode == 0, r.stdout
    data = json.loads(r.stdout)
    assert data["errors"] == [] and data["converged"] is False
