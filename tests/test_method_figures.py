"""tools/method (method_decision_check, analysis_plan_check, tea_second_opinion)
and tools/figures/figure_a11y."""
import json

import pytest

from conftest import ROOT, run_tool

EN_TEMPLATE = ROOT / "templates/method-decision.template.md"


def test_method_decision_selftest():
    r = run_tool("method/method_decision_check.py", "--selftest")
    assert r.returncode == 0 and "all cases passed" in r.stdout


def test_method_decision_blank_template_fails():
    r = run_tool("method/method_decision_check.py", EN_TEMPLATE)
    assert r.returncode == 1 and "missing" in r.stdout


def test_method_decision_filled_example_passes(tmp_path):
    import sys
    sys.path.insert(0, str(ROOT / "tools/method"))
    import method_decision_check as mdc
    for lang in ("en", "zh"):
        f = tmp_path / f"md-{lang}.md"
        f.write_text(mdc._filled_example(lang), encoding="utf-8")
        r = run_tool("method/method_decision_check.py", f)
        assert r.returncode == 0, r.stdout
    assert run_tool("method/method_decision_check.py", tmp_path / "none.md").returncode == 2


def test_analysis_plan_selftest_and_template():
    r = run_tool("method/analysis_plan_check.py", "--selftest")
    assert r.returncode == 0, r.stdout
    r = run_tool("method/analysis_plan_check.py", ROOT / "templates/analysis-plan.template.md")
    assert r.returncode == 1 and "missing" in r.stdout


def test_tea_second_opinion_example_and_missing_tea(tmp_path):
    r = run_tool("method/tea_second_opinion.py", "--example")
    assert r.returncode == 0
    spec = json.loads(r.stdout)
    assert spec["design"]["study type"] == "experiment"
    assert run_tool("method/tea_second_opinion.py").returncode == 2
    try:
        import tea  # noqa: F401
    except ImportError:
        (tmp_path / "spec.json").write_text(r.stdout, encoding="utf-8")
        (tmp_path / "d.csv").write_text("id,cond,score\n1,A,3\n", encoding="utf-8")
        r = run_tool("method/tea_second_opinion.py", "--csv", tmp_path / "d.csv",
                     "--spec", tmp_path / "spec.json")
        assert r.returncode == 1 and "tea is not installed" in r.stderr


def _image(path, colors):
    np = pytest.importorskip("numpy")
    Image = pytest.importorskip("PIL.Image")
    arr = np.zeros((60, 60 * len(colors), 3), dtype=np.uint8)
    for i, c in enumerate(colors):
        arr[:, i * 60:(i + 1) * 60] = c
    Image.fromarray(arr).save(path)
    return path


def test_figure_a11y_red_green_collapses(tmp_path):
    f = _image(tmp_path / "rg.png", [(200, 60, 40), (90, 130, 40)])
    r = run_tool("figures/figure_a11y.py", "--no-render", f)
    assert r.returncode == 1, r.stdout + r.stderr
    assert "collapse under deutan" in r.stdout
    assert not (tmp_path / "rg_a11y").exists()


def test_figure_a11y_distinct_colours_pass_and_render(tmp_path):
    f = _image(tmp_path / "ok.png", [(0, 0, 0), (255, 200, 0)])
    r = run_tool("figures/figure_a11y.py", f)
    assert r.returncode == 0, r.stdout + r.stderr
    names = {p.name for p in (tmp_path / "ok_a11y").iterdir()}
    assert names == {"protan.png", "deutan.png", "tritan.png", "grayscale.png"}
