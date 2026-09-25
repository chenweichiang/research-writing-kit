"""tools/dev/release_check.py. Strings that would trip check 5 or check 4 are built
at run time so this file itself stays clean under the release check."""
import subprocess

import pytest

from conftest import ROOT, load_tool, run_tool

rc = load_tool("dev/release_check.py")
CFG = rc.load_config()
EM = chr(0x2014)
HOME_DIR = "/" + "Users" + "/alice/work"
EMAIL, HOME, INST_A, INST_B, SITE, DEPT = (p["name"] for p in CFG["privacy_patterns"])


def test_frontmatter_problems():
    ok = "---\nname: x\ndescription: \"a: b\"\n---\nbody\n"
    assert rc.frontmatter_problems(ok) == []
    assert rc.frontmatter_problems("# no frontmatter\n")
    assert rc.frontmatter_problems("---\nname: x\n")
    bad = rc.frontmatter_problems("---\nname: x\ndescription: a: b\n---\n")
    assert bad and "safe_load failed" in bad[0]
    assert "not a mapping" in rc.frontmatter_problems("---\njust text\n---\n")[0]


def test_frontmatter_of_shipped_skills_and_agents():
    bad, scope = rc.check_frontmatter()
    assert bad == [] and scope.endswith("files")


def test_method_decision_output_matches_fixtures():
    bad, _ = rc.check_fixtures(CFG)
    assert bad == []


def test_fixture_mismatch_is_reported(tmp_path):
    fx = tmp_path / "fx.txt"
    fx.write_text("exit=0\nsomething else\n", encoding="utf-8")
    cfg = dict(CFG, method_decision_fixtures=[["templates/method-decision.template.md", str(fx)]])
    bad, _ = rc.check_fixtures(cfg)
    assert len(bad) == 1 and "differs" in bad[0] and "line 1" in bad[0]


def test_parse_unified_diff_line_numbers():
    diff = ("diff --git a/x.md b/x.md\n--- a/x.md\n+++ b/x.md\n@@ -3,0 +4,2 @@\n+one\n+two\n"
            "@@ -9 +11 @@\n-old\n+new\n--- a/gone.md\n+++ /dev/null\n@@ -1 +0,0 @@\n-bye\n")
    assert rc.parse_unified_diff(diff) == [("x.md", 4, "one"), ("x.md", 5, "two"), ("x.md", 11, "new")]


def test_dash_hits():
    rows = [("a.md", 1, f"x {EM} y"), ("a.md", 2, "range 2" + chr(0x2013) + "4"), ("a.md", 3, chr(0x2015) * 2)]
    assert [n for _, n, _ in rc.dash_hits(rows, CFG["dash_chars"])] == [1, 3]


def test_mainland_hits_uses_kit_table():
    zt = load_tool("zh-tw/zh_tw_terms.py")
    terms, allow = zt.load()
    term = next(t for t in terms if [x.cn for _, x in zt.find(f"本研究的{t.cn}很重要。", terms, allow)] == [t.cn])
    rows = [("a.md", 1, f"本研究的{term.cn}很重要。"), ("b.md", 2, "本研究以訪談蒐集資料。"),
            ("c.md", 3, "english only")]
    assert rc.mainland_hits(rows) == [("a.md", 1, term.cn, term.tw)]
    assert rc.mainland_hits(rows, exclude={"a.md"}) == []


@pytest.mark.parametrize("line,names", [
    ("mail " + "someone" + "@" + "lab.edu.tw", [EMAIL]),
    ("placeholder you" + "@" + "example.org", []),
    ("clone git" + "@" + "github.com:org/repo.git", []),
    ("path " + HOME_DIR, [HOME]),
    ("我在" + "NT" + "UB任教", [INST_A]),
    ("清" + "大的研究", [INST_B]),
    ("釐清大綱", []),
    ("CONTENT" + "UBE", []),
    ("site course." + "interaction" + ".tw/x", [SITE]),
    ("創意科技" + "產品設計系", [DEPT]),
])
def test_privacy_line_hits(line, names):
    assert [n for n, _ in rc.privacy_line_hits(line, CFG)] == names


def test_privacy_exemption_only_in_exempt_files():
    page = "https://course." + "interaction" + ".tw/research-writing-kit/"
    assert rc.privacy_line_hits(page, CFG, exempt=True) == []
    assert rc.privacy_line_hits(page, CFG, exempt=False)
    other = "https://" + "interaction" + ".tw/elsewhere"
    assert rc.privacy_line_hits(other, CFG, exempt=True)


def _git(cwd, *args):
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.org", *args],
                   cwd=cwd, check=True, capture_output=True)


def test_added_lines_and_privacy_in_scratch_repo(tmp_path):
    _git(tmp_path, "init", "-q", "-b", "main")
    (tmp_path / "a.md").write_text(f"old {EM} line\n", encoding="utf-8")
    _git(tmp_path, "add", ".")
    _git(tmp_path, "commit", "-q", "-m", "base")
    _git(tmp_path, "checkout", "-q", "-b", "feature")
    (tmp_path / "a.md").write_text(f"old {EM} line\nnew {EM} line\n", encoding="utf-8")
    _git(tmp_path, "commit", "-qam", "change")
    (tmp_path / "new.md").write_text("path " + HOME_DIR + "\n", encoding="utf-8")
    rows = rc.added_lines("main", tmp_path)
    assert ("a.md", 2, f"new {EM} line") in rows and ("new.md", 1, "path " + HOME_DIR) in rows
    assert all(t != f"old {EM} line" for _, _, t in rows), "pre-existing lines are not counted"
    bad, _ = rc.check_dashes(rows, CFG)
    assert bad == [f"a.md:2: new {EM} line"]
    bad, _ = rc.check_privacy(CFG, tmp_path)
    assert bad == [f"new.md:1: {HOME}: " + HOME_DIR.rsplit("/", 1)[0]]


def test_cli_runs_fixture_and_frontmatter_checks():
    r = run_tool("dev/release_check.py", "--only", "1", "2")
    assert r.returncode == 0, r.stdout
    assert "[PASS] 1" in r.stdout and "[PASS] 2" in r.stdout


def test_cli_bad_base_is_a_failure_not_a_pass():
    r = run_tool("dev/release_check.py", "--only", "3", "--base", "no-such-ref-xyz")
    assert r.returncode == 1 and "check crashed" in r.stdout


def test_run_on_real_repo_reports_every_selected_check():
    res = rc.run([1, 5], "HEAD", CFG, ROOT)
    assert [k for k, *_ in res] == [1, 5]
