"""tools/collab/source_trace and tools/versioning/version_check."""
import shutil
import subprocess

import pytest

from conftest import load_tool, run_tool

st = load_tool("collab/source_trace.py")

ORIG = """# 研究方法
本研究邀請 12 位高齡者參與遊戲化課程。課程共進行四週，每週一次。
課後以半結構訪談蒐集參與者的使用經驗。
"""
REPLY = "回覆：訪談逐字稿由第一作者整理，共約六小時。\n"
DRAFT = """# 研究方法
本研究邀請 12 位高齡者參與為期四週的遊戲化課程，每週進行一次。
課後以半結構訪談蒐集參與者的使用經驗。
訪談逐字稿由第一作者整理，共約六小時。
另以 SUS 量表進行前後測，信度 Cronbach's α 為 .87。
這樣的安排讓課程更貼近長者的日常。
共回收 15 份有效問卷。
以下依序說明三個部分的內容。
"""


@pytest.fixture
def files(tmp_path):
    out = {}
    for name, body in (("orig", ORIG), ("reply", REPLY), ("draft", DRAFT)):
        p = tmp_path / f"{name}.md"
        p.write_text(body, encoding="utf-8")
        out[name] = p
    return out


def trace_rows(draft, origs):
    src = []
    for p in origs:
        src += [(str(p), ln, s) for ln, s in st.sentences(st.read_any(str(p)))]
    allsrc = "\n".join(st.read_any(str(p)) for p in origs)
    return {r["line"]: r for r in st.trace(st.sentences(st.read_any(str(draft))), st.build_index(src), allsrc)}


# ---- source_trace ----

def test_fabricated_method_is_red(files):
    r = trace_rows(files["draft"], [files["orig"], files["reply"]])
    assert r[5]["flag"] == "🔴"          # a scale and a reliability figure the original never had


def test_reply_counts_as_source(files):
    r = trace_rows(files["draft"], [files["orig"], files["reply"]])
    assert r[4]["status"] == "traced"
    r2 = trace_rows(files["draft"], [files["orig"]])
    assert r2[4]["status"] != "traced"


def test_merged_sentence_traced(files):
    r = trace_rows(files["draft"], [files["orig"], files["reply"]])
    assert r[2]["status"] in ("traced", "rewritten")   # two sentences merged into one still trace back
    assert r[2]["flag"] == ""


def test_number_not_in_source_is_red_even_if_similar(files):
    r = trace_rows(files["draft"], [files["orig"], files["reply"]])
    assert r[7]["flag"] == "🔴"
    assert "15" in r[7]["lost_nums"]


def test_unsourced_claim_about_course_is_red(files):
    # no number and no method word, but a site fact (the supervisor is gone, a design assumption)
    r = trace_rows(files["draft"], [files["orig"], files["reply"]])
    assert r[6]["flag"] == "🔴"


def test_unsourced_english_site_fact_is_red(tmp_path):
    # English drafts: an untraced sentence about the course or its students is a site fact, not a connective
    orig = tmp_path / "orig.md"
    orig.write_text("# Method\n\nTwelve older adults joined a four-week game-based course.\n", encoding="utf-8")
    draft = tmp_path / "draft.md"
    draft.write_text("# Method\n\nTwelve older adults joined a four-week game-based course.\n"
                     "The industry mentor had already left the course by then.\n"
                     "The sections below follow in turn.\n", encoding="utf-8")
    r = trace_rows(draft, [orig])
    assert r[4]["flag"] == "🔴", r[4]
    assert r[5]["flag"] == "🟡", r[5]


def test_connective_is_yellow(files):
    r = trace_rows(files["draft"], [files["orig"], files["reply"]])
    assert r[8]["flag"] == "🟡"


def test_rewrite_smuggling_method_is_red(tmp_path):
    # a reworded sentence that carries in an analysis procedure that was never carried out
    o = tmp_path / "o.md"
    o.write_text("另系統性整理教師於課程實施歷程中的教學紀錄與反思，作為回答研究問題三的依據。\n", encoding="utf-8")
    d = tmp_path / "d.md"
    d.write_text("質性資料方面，本研究系統性整理教師於課程實施歷程中的教學紀錄與反思，"
                 "依「原先的教學假設、現場發生的落差、後續調整」三個面向歸納，作為回答研究問題三的依據。\n",
                 encoding="utf-8")
    src = [(str(o), ln, x) for ln, x in st.sentences(st.read_any(str(o)))]
    row = st.trace(st.sentences(st.read_any(str(d))), st.build_index(src), st.read_any(str(o)))[0]
    assert row["status"] == "rewritten"
    assert row["flag"] == "🔴"
    assert "三個面向歸納" in row["novel"]


def test_gate_exit_code(files, tmp_path):
    r = run_tool("collab/source_trace.py", "--orig", files["orig"], files["reply"], "--draft", files["draft"],
                 "--gate", "--report", tmp_path / "r.md")
    assert r.returncode == 1, r.stdout + r.stderr
    assert "🔴 3" in r.stdout
    assert (tmp_path / "r.md").read_text(encoding="utf-8").startswith("# Source trace report")
    # without --gate the same input exits 0
    r = run_tool("collab/source_trace.py", "--orig", files["orig"], files["reply"], "--draft", files["draft"])
    assert r.returncode == 0 and "Must resolve" in r.stdout


def test_citation_list_not_split():
    parts = st.split_line("如焦點團體法（周雅容，1997；Masadeh, 2012）與情境故事法（唐玄輝、林穎謙，2011）等。")
    assert len(parts) == 1      # a semicolon inside brackets must not cut the sentence, or the year leaves its citation


def test_new_literature_is_orange_not_red(files, tmp_path):
    d = tmp_path / "lit.md"
    d.write_text("Sailer與Homner（2020）的後設分析發現遊戲化對認知學習成果有小幅正向效果（g = .49）。\n"
                 "本研究實驗組 30 人的效果量為 .87，高於前述研究。\n", encoding="utf-8")
    src = [(str(files["orig"]), ln, x) for ln, x in st.sentences(st.read_any(str(files["orig"])))]
    rows = st.trace(st.sentences(st.read_any(str(d))), st.build_index(src), ORIG)
    assert rows[0]["flag"] == "🟠"       # about other people's work: verify the citation instead
    assert rows[1]["flag"] == "🔴"       # a number about the study with no source


def test_english_words_and_threshold():
    src = [("o.md", 1, "We interviewed twelve older adults about their experience of the game.")]
    rows = st.trace([(1, "We interviewed twelve older adults about their experience of the game.")],
                    st.build_index(src), src[0][2])
    assert rows[0]["status"] == "traced" and rows[0]["flag"] == ""
    rows = st.trace([(1, "A survey of 48 clinicians confirmed the pattern.")], st.build_index(src), src[0][2])
    assert rows[0]["status"] == "untraced" and rows[0]["flag"] == "🔴"


def test_docx_input(tmp_path):
    docx = pytest.importorskip("docx")
    d = docx.Document()
    for line in DRAFT.split("\n"):
        d.add_paragraph(line)
    p = tmp_path / "draft.docx"
    d.save(str(p))
    assert "SUS 量表" in st.read_any(str(p))


# ---- version_check ----

def sh(cwd, *cmd):
    subprocess.run(list(cmd), cwd=cwd, check=True, capture_output=True)


def make_project(root, folder="latest"):
    (root / "VERSION").write_text("1.2.0\n", encoding="utf-8")
    (root / "CHANGELOG.md").write_text(
        "# Changelog\n\n## 1.2.0 (2026-10-04) rewrite section 4\n- x\n\n## 1.1.0 (2026-10-01)\n", encoding="utf-8")
    (root / folder).mkdir()
    (root / folder / "paper_v1.2.0.docx").write_bytes(b"x")
    sh(root, "git", "init", "-q")
    sh(root, "git", "add", "-A")
    sh(root, "git", "-c", "user.email=t@example.org", "-c", "user.name=t", "commit", "-qm", "init")
    return root


needs_git = pytest.mark.skipif(shutil.which("git") is None, reason="git not installed")


def vcheck(root, *extra):
    return run_tool("versioning/version_check.py", root, *extra)


@needs_git
def test_clean_project_passes(tmp_path):
    r = vcheck(make_project(tmp_path))
    assert r.returncode == 0, r.stdout


@needs_git
def test_changelog_behind_version(tmp_path):
    root = make_project(tmp_path)
    (root / "VERSION").write_text("1.3.0\n", encoding="utf-8")
    (root / "latest" / "paper_v1.2.0.docx").rename(root / "latest" / "paper_v1.3.0.docx")
    r = vcheck(root)
    assert r.returncode == 1
    assert "write the CHANGELOG first" in r.stdout


@needs_git
def test_mixed_versions_in_latest(tmp_path):
    root = make_project(tmp_path)
    (root / "latest" / "paper_v1.1.0.pdf").write_bytes(b"x")
    r = vcheck(root)
    assert r.returncode == 1
    assert "mixes in other versions: 1.1.0" in r.stdout


@needs_git
def test_tag_reused_after_change(tmp_path):
    root = make_project(tmp_path)
    sh(root, "git", "tag", "v1.2.0")
    with open(root / "CHANGELOG.md", "a", encoding="utf-8") as f:
        f.write("\nan extra line\n")
    r = vcheck(root)
    assert r.returncode == 1
    assert "is tagged" in r.stdout


@needs_git
def test_legacy_two_part_is_warning(tmp_path):
    root = make_project(tmp_path)
    (root / "VERSION").write_text("1.5\n", encoding="utf-8")
    r = vcheck(root)
    assert "two-part convention" in r.stdout


@needs_git
def test_chinese_delivery_folder_names(tmp_path):
    root = make_project(tmp_path, folder="最新交付")
    r = vcheck(root)
    assert r.returncode == 0, r.stdout
    assert "最新交付 has only 1.2.0" in r.stdout
    (root / "最新交付" / "稿_v1.1.0.pdf").write_bytes(b"x")
    r = vcheck(root)
    assert r.returncode == 1
    assert "mixes in other versions: 1.1.0" in r.stdout
    assert "move old ones to 版本/" in r.stdout


@needs_git
def test_submission_text_must_not_carry_version(tmp_path):
    root = make_project(tmp_path)
    bad = root / "submission.txt"
    bad.write_text("Abstract  draft v1.2.0 of the manuscript", encoding="utf-8")
    r = vcheck(root, "--submission", bad)
    assert r.returncode == 1
    assert "shows a version or a review-copy marker" in r.stdout
    zh = root / "submission_zh.txt"
    zh.write_text("審閱稿 頁尾", encoding="utf-8")
    assert vcheck(root, "--submission", zh).returncode == 1   # the Chinese footer word is caught too
    good = root / "submission2.txt"
    good.write_text("Abstract of the manuscript, 2026.", encoding="utf-8")
    assert vcheck(root, "--submission", good).returncode == 0


def minimal_pdf(text):
    """A one-page PDF with a single text line, built by hand (no PDF library needed)."""
    stream = f"BT /F1 12 Tf 50 700 Td ({text}) Tj ET"
    objs = ["<< /Type /Catalog /Pages 2 0 R >>",
            "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R "
            "/Resources << /Font << /F1 5 0 R >> >> >>",
            f"<< /Length {len(stream)} >>\nstream\n{stream}\nendstream",
            "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    out, offs = "%PDF-1.4\n", []
    for i, o in enumerate(objs, 1):
        offs.append(len(out))
        out += f"{i} 0 obj\n{o}\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n"
    out += "".join(f"{o:010d} 00000 n \n" for o in offs)
    out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n"
    return out.encode("latin-1")


@needs_git
@pytest.mark.skipif(shutil.which("pdftotext") is None, reason="needs pdftotext")
def test_submission_pdf_body_must_not_carry_version(tmp_path):
    root = make_project(tmp_path)
    p = root / "sub.pdf"
    p.write_bytes(minimal_pdf("Abstract  draft v1.2.0 of the manuscript"))
    r = vcheck(root, "--submission", p)
    assert r.returncode == 1 and "shows a version" in r.stdout
    q = root / "sub2.pdf"
    q.write_bytes(minimal_pdf("Abstract of the manuscript, 2026."))
    assert vcheck(root, "--submission", q).returncode == 0
