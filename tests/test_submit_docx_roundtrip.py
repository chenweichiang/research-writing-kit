"""Tests for tools/submit/docx_roundtrip.py, wordcount_approx.py and word_count.sh.
Needs pandoc for the round-trip cases (skipped when missing). word_count.sh drives Word
and is not run here; only its syntax and the fallback path are checked."""
import shutil
import subprocess

import pytest

from conftest import ROOT, load_tool, run_tool

MD = """---
title: Test manuscript
---

# Introduction

本研究探討互動裝置如何影響觀眾行為[@chen2024]。第二句說明方法。This is an English sentence about design. Another one follows here!

# Method

我們招募了二十位參與者，進行為期兩週的觀察；結果顯示明顯差異。
"""

needs_pandoc = pytest.mark.skipif(shutil.which("pandoc") is None, reason="needs pandoc")


@pytest.fixture
def built(tmp_path):
    md = tmp_path / "a.md"
    md.write_text(MD, encoding="utf-8")
    docx = tmp_path / "a.docx"
    subprocess.run(["pandoc", str(md), "-o", str(docx)], check=True)
    return tmp_path, md, docx


def pandoc_build(d, name, text):
    md = d / (name + ".md")
    out = d / (name + ".docx")
    md.write_text(text, encoding="utf-8")
    subprocess.run(["pandoc", str(md), "-o", str(out)], check=True)
    return md, out


def rt(*args):
    return run_tool("submit/docx_roundtrip.py", *args)


@needs_pandoc
def test_clean_roundtrip(built):
    _, md, docx = built
    r = rt(md, docx)
    assert r.returncode in (0, 1)
    # a docx built without citeproc keeps "[@chen2024]": a leftover, not a differing sentence
    assert "missing 0, extra 0" in r.stdout


@needs_pandoc
def test_clean_without_cite(built):
    d = built[0]
    md2, docx2 = pandoc_build(d, "b", MD.replace("[@chen2024]", ""))
    r = rt(md2, docx2)
    assert r.returncode == 0, r.stdout
    assert r.stdout.strip().endswith("missing 0, extra 0, leftovers 0")


@needs_pandoc
def test_detects_residue_and_missing(built):
    d = built[0]
    base = MD.replace("[@chen2024]", "")
    _, docx2 = pandoc_build(d, "c", base + "\n[[Author check: sample size here]] 另外 TODO 補圖 ?? 。\n")
    clean = d / "clean.md"
    clean.write_text(base.replace("第二句說明方法。", "")
                     + "\n一段只在源檔的獨有句子，用來驗證缺句偵測。\n", encoding="utf-8")
    r = rt(clean, docx2)
    assert r.returncode == 1
    for s in ("[[Author check", "TODO", "??", "只在源檔的獨有句子", "第二句說明方法"):
        assert s in r.stdout


@needs_pandoc
def test_fuzzy_ignores_small_punct_diff(built):
    d = built[0]
    md2 = d / "d.md"
    md2.write_text("這是一個用來測試模糊比對的比較長的句子，內容完全相同。\n", encoding="utf-8")
    _, out = pandoc_build(d, "e", "這是一個用來測試模糊比對的比較長的句子，內容完全相同！\n")
    assert "missing 0, extra 0" in rt(md2, out).stdout


@needs_pandoc
def test_json_and_read_error(built):
    _, md, docx = built
    r = rt(md, docx, "--json")
    assert '"summary"' in r.stdout
    assert rt(md, "/nonexistent.docx").returncode == 2


@needs_pandoc
def test_consecutive_empty_paragraphs(built):
    pd = pytest.importorskip("docx")
    d = built[0]
    doc = pd.Document()
    for t in ("前文一句話在這裡。", "", "", "後文一句話在這裡。"):
        doc.add_paragraph(t)
    p = d / "empty.docx"
    doc.save(str(p))
    src = d / "s.md"
    src.write_text("前文一句話在這裡。\n\n後文一句話在這裡。\n", encoding="utf-8")
    r = rt(src, p)
    assert r.returncode == 1
    assert "consecutive empty paragraphs" in r.stdout


def test_approx_count():
    wa = load_tool("submit/wordcount_approx.py")
    c = wa.approx_count("這是中文 and English words 123 test-case.")
    assert c["cjk"] == 4
    assert c["latin"] == 5   # and English words 123 test-case
    assert c["words"] == 9
    assert wa.approx_count("")["words"] == 0
    assert "APPROXIMATE" in wa.format_line(c)


def test_approx_cli_on_text_file(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text("one two three 四五六", encoding="utf-8")
    r = run_tool("submit/wordcount_approx.py", f)
    assert r.returncode == 0
    assert "Approximate word count 6" in r.stdout


def test_word_count_sh_syntax_and_args(tmp_path):
    sh = ROOT / "tools" / "submit" / "word_count.sh"
    assert subprocess.run(["bash", "-n", str(sh)], capture_output=True, text=True).returncode == 0
    r = run_tool("submit/word_count.sh", tmp_path / "missing.docx")
    assert r.returncode == 2
    assert "usage" in r.stderr
