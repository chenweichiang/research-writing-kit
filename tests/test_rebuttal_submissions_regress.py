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


def test_regress_banned_claim_is_case_insensitive(tmp_path):
    cfg = _project(tmp_path, "# Intro\n\nFounded in 1987, the studio grew.\n")
    r = run_tool("regress/regress.py", "--config", cfg, "--json")
    assert "R-CORR" in {d["rule"] for d in json.loads(r.stdout)["fail"]}, r.stdout


def test_regress_bib_keys_without_year_and_quarto_crossrefs(tmp_path):
    cfg = _project(tmp_path, "# Intro\n\nWe used OpenCV [@opencv] and a tool [@lee2020, 12]. "
                             "See @fig-setup and @tbl-results. Mail me at me@example.org.\n")
    (tmp_path / "refs.bib").write_text("@software{opencv,\n  title = {OpenCV}\n}\n"
                                       "@article{lee2020,\n  title = {T}\n}\n", encoding="utf-8")
    d = json.loads(cfg.read_text(encoding="utf-8"))
    d["bib_files"] = ["refs.bib"]
    cfg.write_text(json.dumps(d), encoding="utf-8")
    out = json.loads(run_tool("regress/regress.py", "--config", cfg, "--json").stdout)
    bib = [x["msg"] for lvl in ("fail", "info") for x in out[lvl] if x["rule"] == "R1-BIB"]
    # a key without a year is cited, not an orphan; @fig-/@tbl- and emails are not citations
    assert bib == [], bib


def test_regress_clean_project(tmp_path):
    cfg = _project(tmp_path, "# Intro\n\nThe studio was founded in 1988.\n")
    r = run_tool("regress/regress.py", "--config", cfg)
    assert r.returncode == 0, r.stdout


def test_dead_rule_check_flags_unconfigured_rules():
    r = run_tool("regress/dead_rule_check.py", REG / "regress.py", "--config", REG / "rules.template.json")
    assert r.returncode == 1 and "dead rule(s)" in r.stdout


def _stale_msgs(cfg):
    r = run_tool("regress/regress.py", "--config", cfg, "--json")
    out = json.loads(r.stdout)
    return {lvl: [d for d in out[lvl] if d["rule"] in ("R-STALE", "R-LEDGER-CFG")]
            for lvl in ("fail", "warn", "info")}


def _set_ledger(cfg, value):
    d = json.loads(cfg.read_text(encoding="utf-8"))
    d["ledger"] = value
    cfg.write_text(json.dumps(d), encoding="utf-8")


def test_regress_stale_ledger_not_configured(tmp_path):
    cfg = _project(tmp_path, "# Intro\n\nText.\n")
    m = _stale_msgs(cfg)
    assert not m["warn"] and len(m["info"]) == 1 and "not configured" in m["info"][0]["msg"]


def test_regress_stale_ledger_file_missing_is_not_reported_as_unconfigured(tmp_path):
    cfg = _project(tmp_path, "# Intro\n\nText.\n")
    _set_ledger(cfg, "moved-away.md")
    m = _stale_msgs(cfg)
    assert [d["rule"] for d in m["warn"]] == ["R-LEDGER-CFG"]
    assert "moved-away.md" in m["warn"][0]["msg"] and "not there" in m["warn"][0]["msg"]
    assert not any("not configured" in d["msg"] for d in m["info"]), m["info"]


def test_regress_stale_ledger_without_rows(tmp_path):
    cfg = _project(tmp_path, "# Intro\n\nText.\n")
    (tmp_path / "ledger.md").write_text("# numbers ledger\n", encoding="utf-8")
    _set_ledger(cfg, "ledger.md")
    m = _stale_msgs(cfg)
    assert not m["warn"] and len(m["info"]) == 1
    assert "no rows" in m["info"][0]["msg"] and "not configured" not in m["info"][0]["msg"]


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
