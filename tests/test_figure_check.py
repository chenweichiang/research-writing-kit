"""tools/figures/figure_check: offline regression tests on synthetic PDFs.

Each case pins one false positive or false negative met while calibrating the tool on real
manuscripts (the reason is in the docstring of the matching function in figure_check.py).
"""
import os

import pytest

from conftest import load_tool

fitz = pytest.importorskip("pymupdf")
fc = load_tool("figures/figure_check.py")

LINE = "The quick brown fox jumps over the lazy dog while the band plays on and on, "
X0 = 72


def body_line():
    s = LINE
    while fitz.get_text_length(s + "x", fontsize=11) < 440:
        s += "x"
    return s


def new_doc(extra_lines=()):
    """One A4 page: 25 equal-width body lines (column about 72 to 512 pt) plus the caller's extra lines."""
    d = fitz.open()
    p = d.new_page(width=595, height=842)
    s = body_line()
    y = 480
    for _ in range(25):
        p.insert_text((X0, y), s, fontsize=11)
        y += 14
    for (x, yy, t, size) in extra_lines:
        p.insert_text((x, yy), t, fontsize=size)
    return d, p


def solid_pixmap(w, h, border=0):
    pix = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, w, h), False)
    pix.clear_with(255)
    pix.set_rect(fitz.IRect(border, 0, w - border, h), (40, 40, 40))
    return pix


def run_check(d, tmp_path):
    path = os.path.join(str(tmp_path), "t.pdf")
    d.save(path)
    return fc.check(path)


def test_caption_vs_prose():
    yes = ["表 3 引導式後設論述的六個中文構式", "表 3 中文構式", "圖 1：示意", "表 2-1　核心名詞",
           "Figure 1. The record", "Table 2 Summary of results", "Fig. 3"]
    no = ["表 5 因此不是對合理定義空間的抽樣", "圖 3 是作者繪製", "表 2 和表 3 的差異", "Table 1 lists the corpora",
          "表 4 顯示六條構式。"]
    for t in yes:
        assert fc.caption(t) is not None, t
    for t in no:
        assert fc.caption(t) is None, t


def test_expand_nums():
    assert fc.expand_nums("1, 2, and 5") == ["1", "2", "5"]
    assert fc.expand_nums("2–4") == ["2", "3", "4"]


def test_appendix_table_is_not_a_reference():
    assert fc.REF.search("附錄表 3 刺激材料") is None


def test_reference_split_across_lines_and_missing_caption(tmp_path):
    d, p = new_doc([(X0, 100, "as shown in the panel (Figure", 11), (X0, 114, "1) and in Figure 2 below.", 11),
                    (X0, 330, "Figure 1. A test image", 9)])
    p.insert_image(fitz.Rect(X0, 150, X0 + 300, 320), pixmap=solid_pixmap(600, 340))
    red, warn, _ = run_check(d, tmp_path)
    assert any("text mentions Figure 2" in x for x in red), red
    # "(Figure" / "1)" split across a line break must still count as a reference
    assert not any("Figure 1 has a caption but is never referenced" in x for x in warn), warn


def test_wider_than_column_is_warning_off_page_is_red(tmp_path):
    d, p = new_doc([(X0, 330, "Figure 1. Wide", 9), (X0, 120, "See Figure 1.", 11)])
    p.insert_image(fitz.Rect(X0 - 20, 150, 530, 320), pixmap=solid_pixmap(600, 200))
    red, warn, _ = run_check(d, tmp_path)
    assert not red, red
    assert any("beyond the text column" in x for x in warn), warn
    d, p = new_doc([(X0, 330, "Figure 1. Off page", 9), (X0, 120, "See Figure 1.", 11)])
    p.insert_image(fitz.Rect(X0, 150, 600, 320), pixmap=solid_pixmap(600, 200))
    red, warn, _ = run_check(d, tmp_path)
    assert any("runs off the page" in x for x in red), red


def test_white_margin_inside_image_is_not_overflow(tmp_path):
    d, p = new_doc([(X0, 330, "Figure 1. Photo with white margin", 9), (X0, 120, "See Figure 1.", 11)])
    # frame 52-532 (20 pt wider than the column), 25 px white margin each side (about 20 pt): the ink sits inside the column
    p.insert_image(fitz.Rect(X0 - 20, 150, 532, 320), pixmap=solid_pixmap(600, 200, border=25))
    red, warn, _ = run_check(d, tmp_path)
    assert not any("beyond the text column" in x or "runs off" in x for x in red + warn), red + warn


def test_clipped_vector_pattern_is_not_overflow(tmp_path):
    d, p = new_doc([(X0, 330, "Figure 1. Hatched bars", 9), (X0, 120, "See Figure 1.", 11)])
    sh = p.new_shape()
    for i in range(10):     # one path per bar (matplotlib and Typst both write it this way; ten bars in one path would not count as a figure)
        sh.draw_rect(fitz.Rect(X0 + 10 + 30 * i, 200, X0 + 30 + 30 * i, 300))
        sh.finish(color=(0, 0, 0), fill=(0.5, 0.5, 0.5))
    sh.commit()
    # hatch pattern tile: its frame spans 0-595 (past the page), but it is clipped to 150-400 (the matplotlib hatch case)
    xref = p.get_contents()[-1]
    d.update_stream(xref, d.xref_stream(xref) + b"\nq 150 542 250 100 re W n 1 0 0 rg 0 542 595 100 re f Q\n")
    red, warn, _ = run_check(d, tmp_path)
    assert not any("beyond the text column" in x or "runs off" in x or "no figure was found" in x
                   for x in red + warn), red + warn


def test_tiny_text_inside_vector_figure(tmp_path):
    d, p = new_doc([(X0, 330, "Figure 1. Shrunk chart", 9), (X0, 120, "See Figure 1.", 11),
                    (X0 + 40, 250, "axis label", 3.5)])
    sh = p.new_shape()
    for i in range(10):
        sh.draw_line((X0 + 10, 200 + 10 * i), (X0 + 300, 200 + 10 * i))
        sh.finish(color=(0, 0, 0))
    sh.draw_rect(fitz.Rect(X0 + 5, 195, X0 + 305, 300))
    sh.finish(color=(0, 0, 0))
    sh.commit()
    red, _, _ = run_check(d, tmp_path)
    assert any("smallest font" in x for x in red), red


def test_shrunk_raster_chart(tmp_path):
    # a 3300 px wide white-background chart shrunk to 180 pt (about 1300 dpi equivalent), 40% of the column width
    d, p = new_doc([(X0, 330, "Figure 1. Shrunk raster chart", 9), (X0, 120, "See Figure 1.", 11)])
    pix = fitz.Pixmap(fitz.csRGB, fitz.IRect(0, 0, 3300, 1900), False)
    pix.clear_with(255)
    pix.set_rect(fitz.IRect(300, 900, 3000, 960), (0, 0, 0))
    p.insert_image(fitz.Rect(X0 + 130, 150, X0 + 310, 254), pixmap=pix)
    red, _, _ = run_check(d, tmp_path)
    assert any("dpi equivalent" in x and "of the column width" in x for x in red), red
    # a dark photo shrunk the same way does not count: high-dpi photos are common and hold no text
    d, p = new_doc([(X0, 330, "Figure 1. Photo", 9), (X0, 120, "See Figure 1.", 11)])
    p.insert_image(fitz.Rect(X0 + 130, 150, X0 + 310, 254), pixmap=solid_pixmap(3300, 1900))
    red, warn, _ = run_check(d, tmp_path)
    assert not any("dpi equivalent" in x for x in red + warn), red + warn


def test_numbering_gap(tmp_path):
    d, p = new_doc([(X0, 330, "Figure 1. One", 9), (X0, 120, "See Figure 1 and Figure 3.", 11),
                    (X0, 470, "Figure 3. Three", 9)])
    p.insert_image(fitz.Rect(X0, 150, X0 + 300, 320), pixmap=solid_pixmap(300, 170))
    p.insert_image(fitz.Rect(X0, 340, X0 + 300, 460), pixmap=solid_pixmap(300, 120))
    red, _, _ = run_check(d, tmp_path)
    assert any("numbering gap: missing 2" in x for x in red), red
