"""--help on the hand-parsed CLIs prints the module docstring and exits 0."""
import pytest
from conftest import run_tool

TOOLS = [
    "zh-tw/zh_ai_style.py",
    "zh-tw/voice_lint.py",
    "zh-tw/zh_gloss_scan.py",
    "zh-tw/zh_localize.py",
    "submit/wordcount_approx.py",
]


@pytest.mark.parametrize("rel", TOOLS)
@pytest.mark.parametrize("flag", ["--help", "-h"])
def test_help_prints_docstring(rel, flag):
    r = run_tool(rel, flag)
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip()
