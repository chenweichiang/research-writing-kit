"""tools/rebuttal, tools/submissions, tools/regress."""
import json
import shutil
from datetime import date

from conftest import TOOLS, run_tool

REB = TOOLS / "rebuttal"
SUB = TOOLS / "submissions"
REG = TOOLS / "regress"


# ---------------------------------------------------------------- rebuttal
def _rebuttal(tmp_path, letter_edit=None):
    for n in ("points.template.tsv", "revisions.template.tsv", "response-letter.template.md"):
        shutil.copy(REB / n, tmp_path / n)
    letter = tmp_path / "response-letter.template.md"
    if letter_edit:
        letter.write_text(letter_edit(letter.read_text(encoding="utf-8")), encoding="utf-8")
    return run_tool("rebuttal/check_response.py", "--points", tmp_path / "points.template.tsv",
                    "--revisions", tmp_path / "revisions.template.tsv", "--letter", letter)


def test_check_response_templates_pass(tmp_path):
    r = _rebuttal(tmp_path)
    assert r.returncode == 0 and "all four checks pass" in r.stdout


def test_check_response_unanswered_point_fails(tmp_path):
    r = _rebuttal(tmp_path, lambda t: t.replace("R2.1", "R2.x"))
    assert r.returncode == 1 and "R2.1 does not appear in the letter" in r.stdout


# ---------------------------------------------------------------- submissions
HEADER = "manuscript_id\tproject\tvenue\tstatus\tsubmitted\tupdated\tnote\n"


def test_check_submissions_duplicate(tmp_path):
    (tmp_path / "p1").mkdir()
    today = date.today().isoformat()
    ledger = tmp_path / "SUBMISSIONS.tsv"
    ledger.write_text(HEADER + f"paper-a\tp1\tJournal A\tunder_review\t{today}\t{today}\t\n"
                               f"paper-a\tp1\tJournal B\tsubmitted\t{today}\t{today}\t\n",
                      encoding="utf-8")
    r = run_tool("submissions/check_submissions.py", "--ledger", ledger)
    assert r.returncode == 1 and "DUPLICATE SUBMISSION RISK" in r.stdout


def test_check_submissions_template_and_bad_status(tmp_path):
    r = run_tool("submissions/check_submissions.py", "--ledger", SUB / "SUBMISSIONS.template.tsv")
    assert r.returncode == 0
    ledger = tmp_path / "SUBMISSIONS.tsv"
    ledger.write_text(HEADER + "paper-a\t\tJournal A\tpending\t\t\t\n", encoding="utf-8")
    r = run_tool("submissions/check_submissions.py", "--ledger", ledger)
    assert r.returncode == 1 and "invalid status" in r.stdout


def test_style_reaudit_registry(tmp_path):
    (tmp_path / "p1").mkdir()
    (tmp_path / "p1" / "draft.md").write_text("text\n", encoding="utf-8")
    ledger = tmp_path / "SUBMISSIONS.tsv"
    ledger.write_text(HEADER + "paper-a\tp1\tJournal A\tdrafting\t\t\t\n", encoding="utf-8")
    targets = tmp_path / "style_targets.tsv"
    targets.write_text("target_id\tlang\tpath\tnote\npaper-a\ten\tp1/draft.md\tlatest\n", encoding="utf-8")
    r = run_tool("submissions/style_reaudit.py", "--ledger", ledger, "--targets", targets, "--check")
    assert r.returncode == 0, r.stdout + r.stderr
    targets.write_text("target_id\tlang\tpath\tnote\n", encoding="utf-8")
    r = run_tool("submissions/style_reaudit.py", "--ledger", ledger, "--targets", targets, "--check")
    assert r.returncode == 1 and "paper-a" in r.stdout


def test_style_reaudit_template_paths_missing():
    r = run_tool("submissions/style_reaudit.py", "--ledger", SUB / "SUBMISSIONS.template.tsv",
                 "--targets", SUB / "style_targets.template.tsv", "--check")
    assert r.returncode == 1 and "path not found" in r.stdout


# ---------------------------------------------------------------- regress
def _project(tmp_path, body):
    (tmp_path / "content" / "part1").mkdir(parents=True)
    (tmp_path / "content" / "part1" / "a.md").write_text(body, encoding="utf-8")
    cfg = json.loads((REG / "rules.template.json").read_text(encoding="utf-8"))
    cfg["deliver_globs"] = ["part1/*.md"]
    cfg["ledger"] = None
    cfg["banned_claims"] = [["founded in 1987", "registry says 1988"]]
    (tmp_path / "regress.json").write_text(json.dumps(cfg), encoding="utf-8")
    return tmp_path / "regress.json"


def test_regress_template_config_runs():
    r = run_tool("regress/regress.py", "--config", REG / "rules.template.json")
    assert r.returncode == 0 and "NOT guarding" in r.stdout


def test_regress_catches_internal_word_and_banned_claim(tmp_path):
    cfg = _project(tmp_path, "# Intro\n\nThe studio was founded in 1987. TODO check this.\n")
    r = run_tool("regress/regress.py", "--config", cfg, "--json")
    assert r.returncode == 1
    rules = {d["rule"] for d in json.loads(r.stdout)["fail"]}
    assert "R-CORR" in rules and any(x.startswith("R6") for x in rules), rules


def test_regress_clean_project(tmp_path):
    cfg = _project(tmp_path, "# Intro\n\nThe studio was founded in 1988.\n")
    r = run_tool("regress/regress.py", "--config", cfg)
    assert r.returncode == 0, r.stdout


def test_dead_rule_check_flags_unconfigured_rules():
    r = run_tool("regress/dead_rule_check.py", REG / "regress.py", "--config", REG / "rules.template.json")
    assert r.returncode == 1 and "dead rule(s)" in r.stdout


def _dead_lines(*args):
    r = run_tool("regress/dead_rule_check.py", *args)
    return r, {ln.split()[1]: ln for ln in r.stdout.splitlines() if ln.startswith(("[OK]", "[FAIL]"))
               and len(ln.split()) > 2 and ln.split()[1].startswith("r")}


def test_dead_rule_check_catches_guard_return_above_threshold():
    """Negative samples: with an empty config both rules return on their guard, yet
    execute more than 25 % of their lines, which the ratio alone called [OK]."""
    r, lines = _dead_lines(REG / "regress.py", "--config", REG / "rules.template.json")
    assert r.returncode == 1
    for name in ("r_entity_attribution", "r_corrected_claims"):
        assert lines[name].startswith("[FAIL]") and "guard return" in lines[name], lines[name]


def test_dead_rule_check_passes_the_same_rules_once_configured(tmp_path):
    cfg = _project(tmp_path, "# Intro\n\nThe studio was founded in 1988 by Lee (supervised).\n")
    d = json.loads(cfg.read_text(encoding="utf-8"))
    d["entities"] = {"names": ["Lee"], "marks": ["supervised"]}
    cfg.write_text(json.dumps(d), encoding="utf-8")
    _, lines = _dead_lines(REG / "regress.py", "--config", cfg)
    for name in ("r_entity_attribution", "r_corrected_claims"):
        assert lines[name].startswith("[OK]"), lines[name]


def test_dead_rule_check_return_inside_loop_is_not_a_guard(tmp_path):
    skel = tmp_path / "skel.py"
    skel.write_text(
        "ITEMS = ['a', 'b']\n"
        "SETTING = []\n\n"
        "def r_loop_return():\n"
        "    for x in ITEMS:\n"
        "        if x == 'a':\n"
        "            return x\n"
        "    return None\n\n"
        "def r_short_guard():\n"
        "    if not SETTING:\n"
        "        return None\n"
        "    return len(SETTING)\n\n"
        "RULES = [r_loop_return, r_short_guard]\n", encoding="utf-8")
    r, lines = _dead_lines(skel)
    assert lines["r_loop_return"].startswith("[OK]"), lines["r_loop_return"]
    assert lines["r_short_guard"].startswith("[FAIL]") and "guard return" in lines["r_short_guard"]
    assert r.returncode == 1
