#!/usr/bin/env python3
"""polish_check.py: checks a native-polish change list before any of it touches the
draft. Applies the edits to an in-memory copy and verifies invariants, forbidden forms,
sentence length and register direction. Chinese and English. Local, no upload.

Why this exists: in the native-polish step (co-author Phase 5.5) the editor subagent
returns a change list and never edits the draft; the main session adjudicates each item.
This script is the mechanical half of that review, so a numeric slip, a changed
citation or a feature pushed out of the field's range is caught by a rule instead of by
someone's eyes on item 140 of 200.

Change-list format (a comment line above each tuple gives the category and a reason):
  E = [("original string, verbatim and unique in the draft", "replacement"), ...]
A .py file is read with ast.literal_eval (never executed). A .json file holding
[["original", "replacement"], ...] also works.

Blocks (exit 1):
  - the original string is not unique, falls outside --lines, overlaps another edit, or
    spans a line break; the edit touches a table row, heading, image line or caption;
  - the multiset of numbers, citations, comments, quoted text, math, LaTeX commands,
    (Chinese drafts) Latin words, or --lock terms changes;
  - the text grows by more than --grow-budget (Han characters for zh, words for en;
    default 0; --allow-grow lifts the limit);
  - a forbidden form increases (contrast frames, stock metadiscourse, dashes, and for zh
    sentence-initial 然而 and mainland-Mandarin terms from tools/zh-tw/zh_tw_terms.tsv;
    add your own with --forbid-file);
  - more sentences exceed the length limit (--max-len; 120 Han characters or 45 words);
  - register direction (when a corpus is given and the draft is long enough, 1000 Han
    characters or 800 words): a feature that was high rises, one that was low falls, or
    one inside the band is pushed out. See tools/register/register_profile.py.
Report only: translationese indicators (zh), nominalization and passive counts (en), mean
sentence length, stance counts that changed, and features that moved back into the band.
The semicolon is not blocked: Taiwan journal papers use it routinely. Whether YOUR letters
use it is a voice question for voice_lint, not a register question for a paper.

--apply writes the edits back only when every check passes. Use it after adjudication,
with the change list trimmed to the items you accepted.

Usage:
  polish_check.py --draft <draft> --edits e_A.py[,e_B.py] --lang zh|en [--lines 49-58,69-104]
                  [--corpus <dir> --venue <folder>] [--biber-python <py>] [--no-biber] [--no-register]
                  [--lock "term one,term two"] [--lock-file terms.txt] [--forbid-file forbid.json]
                  [--grow-budget N | --allow-grow] [--max-len N] [--apply]
  polish_check.py --selftest     # synthetic text and a synthetic corpus in a temp dir
"""
import argparse
import ast
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
for sub in ("zh-tw", "en", "common"):
    sys.path.insert(0, str(HERE.parent / sub))
sys.path.insert(0, str(HERE))

DASH = chr(0x2014)

# ---------- invariants ----------
RX_NUM = r"\d[\d,]*(?:\.\d+)?%?|\.\d+"
RX_HTML_COMMENT = r"<!--.*?-->"
RX_TEX_COMMENT = r"(?<!\\)%[^\n]*"
RX_CITE = (r"\\cite[a-zA-Z]*\*?(?:\[[^\]]*\])*\{[^}]*\}"            # LaTeX \cite{...}
           r"|\[@[^\]]+\]|(?<![\w.])@[A-Za-z][\w:-]*"               # Pandoc [@key], @key
           r"|（[^（）]*?\d{4}[^（）]*?）|\([^()]*?\d{4}[a-z]?[^()]*?\)")  # author-year brackets
RX_QUOTE_ZH = r"「[^」]*」|《[^》]*》|〈[^〉]*〉"
RX_QUOTE_EN = r"“[^”]*”|``.*?''|\"[^\"\n]*\""
RX_MATH = r"\$[^$\n]+\$|\\\(.*?\\\)"
RX_TEXCMD = r"\\[a-zA-Z]+"
RX_LATIN = r"[A-Za-z][A-Za-z\-üöéåä′']*"

# ---------- forms that may not increase ----------
ZH_FORBID = {
    "contrast frames (並非/而非/而不是/不是…而是/不在於…而在於/與其…不如)":
        r"並非|而非|而不是|不是[^。]{0,30}而是|不在於[^。]{0,30}而在於|與其[^。]{0,30}不如",
    "stock metadiscourse (不僅/綜上所述/總而言之/值得注意/由此可見/換言之/亦即/也就是說/首先/其次/脈絡下/研究顯示)":
        r"不僅|綜上所述|總而言之|值得注意|由此可見|換言之|亦即|也就是說|首先|其次|脈絡下|有研究指出|研究顯示",
    "dashes": DASH + DASH + "|" + DASH,
    "然而 starting a sentence": r"(?:^|[。！？\n])\s*然而",
    "redundant 此一/這一類 pointing": r"此一|這一類|這一場|這一種|這一項",
    "self-congratulatory verdicts": r"恰恰是|恰切合|之所在|價值所在|真正的[^，。]{0,8}(?:在於|重量|價值)",
    "colloquial words (當成/看作/看成/好像/沒辦法)": r"當成|看作|看成|好像|沒辦法",
}
EN_FORBID = {
    "contrast (not…but / , not / rather than / instead of / not only / not merely / less about…than)":
        r"\bnot\b[^.;]{0,60}\bbut\b|,\s*not\s|\brather than\b|\binstead of\b|\bnot only\b|\bnot merely\b"
        r"|\bless about\b[^.]{0,60}\bthan\b",
    "dashes": DASH + r"|(?<!-)---(?!-)",
    "opener cliches (in the era of / paradigm shift / has emerged as / the advent of / rapidly evolving)":
        r"(?i)\bin the era of\b|\bparadigm shift\b|\bhas emerged as\b|\bthe advent of\b|\brapidly evolving\b",
    "overclaim (never / the only / unprecedented / prove / clearly / obviously / fundamentally)":
        r"(?i)\bnever\b|\bthe only\b|\bunprecedented\b|\bprove[sdn]?\b|\bclearly\b|\bobviously\b"
        r"|\bfundamentally\b",
    "LLM-convergent words (delve / intricate / pivotal / multifaceted / underscore / tapestry / "
    "meticulous / paramount / foster / crucial)":
        r"(?i)\bdelv\w*|\bintricate\w*|\bpivotal\b|\bmultifaceted\b|\bunderscor\w*|\btapestr\w*"
        r"|\bmeticulous\w*|\bparamount\b|\bfoster\w*|\bcrucial\w*",
    "self-described honesty (to be honest / candid / transparently)":
        r"(?i)\bto be honest\b|\bcandid\w*|\btransparently\b",
}

TEX = False   # only a LaTeX draft has % comments; in Markdown "1.1%" is a number, not a comment


def strip_comments(t):
    t = re.sub(RX_HTML_COMMENT, "", t, flags=re.S)
    return re.sub(RX_TEX_COMMENT, "", t) if TEX else t


def han(t):
    return len(re.findall(r"[一-鿿]", strip_comments(t)))


def words(t):
    return len(re.findall(r"[A-Za-z]+(?:['’-][A-Za-z]+)*", strip_comments(t)))


def no_quotes(t, lang):
    return re.sub(RX_QUOTE_ZH if lang == "zh" else RX_QUOTE_EN, "", strip_comments(t))


def invariants(t, lang, locks):
    body = strip_comments(t)
    out = {
        "numbers": Counter(re.findall(RX_NUM, body)),
        "comments": Counter(re.findall(RX_HTML_COMMENT, t, flags=re.S)
                            + (re.findall(RX_TEX_COMMENT, t) if TEX else [])),
        "citations": Counter(re.findall(RX_CITE, body)),
        "quoted text and titles": Counter(re.findall(RX_QUOTE_ZH if lang == "zh" else RX_QUOTE_EN, body)),
        "math": Counter(re.findall(RX_MATH, body)),
        "LaTeX commands": Counter(re.findall(RX_TEXCMD, body)),
    }
    if lang == "zh":
        out["Latin words"] = Counter(re.findall(RX_LATIN, body))
    if locks:
        out["locked terms"] = Counter({k: body.count(k) for k in locks})
    return out


def mainland_terms(t):
    """Mainland-Mandarin terms from the kit's term table (flag and fix entries)."""
    try:
        import zh_tw_terms as T
    except ImportError:
        return None
    return len(T.find(t))


def sentences(t, lang):
    t = strip_comments(t)
    body = "\n".join(l for l in t.split("\n")
                     if l.strip() and not l.lstrip().startswith(("|", "#", "!", ":::", "\\begin", "\\end")))
    if lang == "zh":
        return [x for x in re.split(r"(?<=[。！？])", body) if re.search(r"[一-鿿]", x)]
    return [x for x in re.split(r"(?<=[.!?])\s+(?=[A-Z])", body) if re.search(r"[A-Za-z]{3}", x)]


def slen(s, lang):
    return han(s) if lang == "zh" else words(s)


def indicators(t, lang):
    body = no_quotes(t, lang)
    if lang == "zh":
        k = max(1, han(body)) / 1000
        P = {"的 per 1k": r"的", "被": r"被", "進行/加以/予以": r"進行|加以|予以",
             "對於/關於/作為": r"對於|關於|作為", "一個/一種/一項": r"一個|一種|一項", "其/它": r"其|它"}
    else:
        k = max(1, words(body)) / 1000
        P = {"-tion/-ment nominalizations per 1k": r"\b\w{4,}(?:tion|tions|ment|ments)\b",
             "be + -ed passive": r"\b(?:is|are|was|were|be|been|being)\s+\w+ed\b",
             "it is … that": r"(?i)\bit is\b[^.]{0,40}\bthat\b",
             "there is/are": r"(?i)\bthere (?:is|are)\b"}
    return {x: (len(re.findall(v, body)) / k if "per 1k" in x else len(re.findall(v, body)))
            for x, v in P.items()}


def _pairs(value, src):
    out = []
    for item in value:
        if not (isinstance(item, (list, tuple)) and len(item) == 2
                and all(isinstance(x, str) for x in item)):
            sys.exit(f"{src}: every edit must be a pair of strings (original, replacement)")
        out.append((item[0], item[1]))
    return out


def load_edits(paths):
    """Read change lists without executing them: `E = [...]` in a .py file, or a JSON list."""
    E = []
    for f in (p.strip() for p in paths.split(",") if p.strip()):
        text = Path(f).expanduser().read_text(encoding="utf-8")
        if f.endswith(".json"):
            E += _pairs(json.loads(text), f)
            continue
        try:
            tree = ast.parse(text, filename=f)
        except SyntaxError as e:
            sys.exit(f"{f}: not valid Python ({e})")
        node = next((n.value for n in tree.body if isinstance(n, ast.Assign)
                     and any(isinstance(t, ast.Name) and t.id == "E" for t in n.targets)), None)
        if node is None:
            sys.exit(f"{f}: no `E = [...]` assignment found")
        try:
            E += _pairs(ast.literal_eval(node), f)
        except ValueError:
            sys.exit(f"{f}: `E` must be a literal list of string pairs (no code, no variables)")
    return E


def load_forbid(path):
    if not path:
        return {}
    cfg = json.loads(Path(path).expanduser().read_text(encoding="utf-8"))
    return {k: v for k, v in cfg.items() if not k.startswith("_")}


def parse_ranges(s, nlines):
    if not s:
        return [(1, nlines)]
    out = []
    for part in s.split(","):
        a, _, b = part.partition("-")
        out.append((int(a), int(b or a)))
    return out


def check(text, E, lang, ranges=None, locks=(), allow_grow=False, max_len=None, grow_budget=0,
          register=False, corpus=None, venue=None, biber_python=None, biber=True, extra_forbid=None):
    """(ok, report lines, text after the edits). Writes nothing."""
    global TEX
    TEX = bool(re.search(r"\\documentclass|\\begin\{document\}", text))
    rep, ok = [], True
    lines = text.split("\n")
    starts = [0]
    for l in lines:
        starts.append(starts[-1] + len(l) + 1)
    spans = [(starts[a - 1], starts[min(b, len(lines))]) for a, b in parse_ranges(ranges, len(lines))]
    max_len = max_len or (120 if lang == "zh" else 45)

    seen = []
    for o, n in E:
        c = text.count(o)
        if c != 1:
            rep.append(f"FAIL original occurs {c} times (must be exactly 1): {o[:50]}")
            ok = False
            continue
        i = text.index(o)
        if not any(a <= i and i + len(o) <= b for a, b in spans):
            rep.append(f"FAIL original is outside the given line range: {o[:50]}")
            ok = False
        for j, span in seen:
            if not (i + len(o) <= j or j + span <= i):
                rep.append(f"FAIL overlaps another edit: {o[:50]}")
                ok = False
        seen.append((i, len(o)))
        if "\n" in o or "\n" in n:
            rep.append(f"FAIL spans or adds a line break (paragraph structure stays): {o[:50]}")
            ok = False
        line = lines[text.count("\n", 0, i)]
        if line.lstrip().startswith("|") or o.count("|") != n.count("|"):
            rep.append(f"FAIL table rows are not edited: {o[:50]}")
            ok = False
        if line.lstrip().startswith(("#", "![")) or re.search(r"\\(?:sub)*section\*?\{|\\caption\{", o):
            rep.append(f"FAIL headings, image lines and captions are outside polish: {o[:50]}")
            ok = False
    if not ok:
        return False, rep, text

    after = text
    for o, n in E:
        after = after.replace(o, n, 1)
    # Lengths change once edits apply, so invariants and indicators compare the whole text;
    # the line range only limits where edits may sit.
    inv_b, inv_a = invariants(text, lang, locks), invariants(after, lang, locks)
    for name, x in inv_b.items():
        y = inv_a[name]
        if x == y:
            rep.append(f"ok   {name} unchanged")
        else:
            rep.append(f"FAIL {name} changed: removed {dict(x - y)} added {dict(y - x)}")
            ok = False

    b, a, unit = (han(text), han(after), "Han chars") if lang == "zh" else (words(text), words(after), "words")
    budget = None if allow_grow else (grow_budget or 0)
    grow_bad = budget is not None and a - b > budget
    rule = "no limit" if budget is None else ("may not grow" if budget == 0 else f"budget +{budget}")
    rep.append(f"{'FAIL' if grow_bad else 'ok  '} {unit} {b} -> {a} ({a - b:+d}; {rule})")
    ok &= not grow_bad

    forbid = dict(ZH_FORBID if lang == "zh" else EN_FORBID)
    forbid.update(extra_forbid or {})
    nb, na = no_quotes(text, lang), no_quotes(after, lang)
    for k, v in forbid.items():
        cb, ca = len(re.findall(v, nb, flags=re.M)), len(re.findall(v, na, flags=re.M))
        ok &= not ca > cb
        rep.append(f"{'FAIL' if ca > cb else 'ok  '} {k} {cb} -> {ca}")
    if lang == "zh":
        mb, ma = mainland_terms(nb), mainland_terms(na)
        if mb is not None:
            ok &= not ma > mb
            rep.append(f"{'FAIL' if ma > mb else 'ok  '} mainland-Mandarin terms (zh_tw_terms.tsv) {mb} -> {ma}")

    ib, ia = indicators(text, lang), indicators(after, lang)
    fmt = lambda x, v: f"{v:.1f}" if "per 1k" in x else f"{v}"
    rep.append("indicators (report only): " + "; ".join(f"{x} {fmt(x, ib[x])}->{fmt(x, ia[x])}" for x in ib))

    sb, sa = sentences(text, lang), sentences(after, lang)
    lb, la = [slen(s, lang) for s in sb], [slen(s, lang) for s in sa]
    longb, longa = sum(1 for x in lb if x > max_len), sum(1 for x in la if x > max_len)
    mb_, ma_ = sum(lb) / max(1, len(lb)), sum(la) / max(1, len(la))
    rep.append(f"sentences {len(sb)} -> {len(sa)}; mean length {mb_:.1f} -> {ma_:.1f}; "
               f"over {max_len} {unit}: {longb} -> {longa}")
    if longa > longb:
        ok = False
        rep.append(f"FAIL more sentences over {max_len} {unit}")
    if lang == "zh" and ma_ < mb_:
        rep.append("note mean sentence length fell. Taiwan journal sentences run longer than machine "
                   "rewrites; every split needs a reason")

    if register:
        import register_profile as R
        pb = R.measure(text, lang, corpus, venue, biber_python, biber, TEX)
        pa = R.measure(after, lang, corpus, venue, biber_python, biber, TEX) if pb else None
        if pb and pa:
            bad, notes = R.compare(pb, pa)
            rep.append(f"register direction (baseline = {pb['venue']}, {pb['n_docs']} papers; "
                       "whole draft before -> after):")
            rep += [f"FAIL {x}" for x in bad] or ["ok   no feature moved away from the band"]
            rep += [f"     {x}" for x in notes]
            ok &= not bad
        else:
            rep.append("(register direction not checked: no corpus, too few papers, or the draft is too short)")
    rep.append(f"edits: {len(E)}")
    return ok, rep, after


def selftest():
    zh = ("# 標題\n\n本研究對樣本進行比較，共 72 則（Wang, 2020）。「原句」不動，受試者作為對象。\n"
          "| 表 | 1 |\n\n情境感知指標是本研究的術語。\n")
    en = ("# Title\n\nWe conducted a comparison of 72 cases \\cite{wang2020}. The result is \"quoted\".\n"
          "Participants were recruited in 2024 (Lee, 2021).\n")
    cases = [
        ("zh: removing a light verb passes", zh, "zh", [("本研究對樣本進行比較", "本研究比較樣本")], True),
        ("zh: a changed number is blocked", zh, "zh", [("共 72 則", "共 70 則")], False),
        ("zh: a changed citation is blocked", zh, "zh", [("（Wang, 2020）", "（Wang, 2021）")], False),
        ("zh: growth beyond the budget is blocked", zh, "zh",
         [("本研究對樣本進行比較", "本研究針對所有的樣本進行了詳細比較")], False),
        ("zh: a new contrast frame is blocked", zh, "zh", [("本研究對樣本進行比較", "本研究比較樣本而非")], False),
        ("zh: an edited table row is blocked", zh, "zh", [("| 表 | 1 |", "| 表格 | 1 |")], False),
        ("zh: an edited locked term is blocked", zh, "zh", [("情境感知指標是", "情境指標是")], False),
        ("zh: a non-unique original is blocked", zh, "zh", [("本", "此")], False),
        ("zh: a prose semicolon is allowed", zh, "zh", [("「原句」不動，受試者", "「原句」不動；受試者")], True),
        ("zh: sentence-initial 然而 is blocked", zh, "zh",
         [("情境感知指標是本研究的術語", "然而情境感知指標是本研究術語")], False),
        ("zh markdown: text after a percentage is editable (not a comment)",
         "樣本約占 3.5%，比例是略微偏低。\n", "zh", [("比例是略微偏低", "比例為略微偏低")], True),
        ("en: de-nominalizing passes", en, "en",
         [("We conducted a comparison of 72 cases", "We compared 72 cases")], True),
        ("en: a changed citation key is blocked", en, "en", [("\\cite{wang2020}", "\\cite{wang2021}")], False),
        ("en: a new 'rather than' is blocked", en, "en",
         [("We conducted a comparison of 72 cases", "We compared 72 cases rather than")], False),
        ("en: changed quoted text is blocked", en, "en", [("\"quoted\"", "\"cited\"")], False),
        ("en: word growth is blocked", en, "en",
         [("Participants were recruited", "Participants were carefully and deliberately recruited")], False),
        ("en LaTeX: an edited % comment is blocked",
         "\\documentclass{article}\nWe compared cases. % keep this note\n", "en",
         [("% keep this note", "% changed")], False),
    ]
    good = True
    for name, text, lang, E, want in cases:
        got, rep, _ = check(text, E, lang, locks=["情境感知指標"] if lang == "zh" else [])
        good &= got == want
        print(f"{'PASS' if got == want else 'FAIL'} {name} (expected {'pass' if want else 'block'}, "
              f"got {'pass' if got else 'block'})")
        if got != want:
            print("   " + "\n   ".join(rep))
    # A mainland term taken from the kit's own table, so this file never spells one out.
    import zh_tw_terms as T
    terms, _ = T.load()
    term = next(x.cn for x in terms if x.mode == "fix" and not x.skip and not x.need)
    t = not check(zh, [("受試者作為對象", "受試者作為" + term)], "zh", allow_grow=True)[0]
    good &= t
    print(f"{'PASS' if t else 'FAIL'} zh: a new mainland term is blocked")
    g = lambda b: check(zh, [("本研究對樣本進行比較", "本研究針對所有樣本進行比較")], "zh", grow_budget=b)[0]
    t = (not g(0)) and (not g(2)) and g(4)
    good &= t
    print(f"{'PASS' if t else 'FAIL'} --grow-budget: net +4 chars, budget 0 and 2 block, 4 passes")
    t = check(zh, [("受試者作為對象", "受試者作為對象")], "zh", extra_forbid={"作為 (test)": "作為"})[0]
    t2 = not check(zh, [("受試者作為對象", "受試者作為對象，作為樣本")], "zh", allow_grow=True,
                   extra_forbid={"作為 (test)": "作為"})[0]
    good &= t and t2
    print(f"{'PASS' if t and t2 else 'FAIL'} --forbid-file forms may not increase")

    import zh_register as Z
    with tempfile.TemporaryDirectory() as d:
        corpus = Z.synthetic_corpus(Path(d) / "zh")
        head = "開場先交代本文以訪談補充的理由。"
        body = head + ("本文以問卷蒐集資料，並分析受訪者的回饋。本文討論設計意義，也整理後續方向。" * 30 + "\n") * 2
        worse = check(body, [(head, "開場先交代本文以本文訪談補充的理由。")], "zh",
                      grow_budget=10, register=True, corpus=corpus, venue="JX")
        better = check(body, [(head, "開場先交代本研究以訪談補充的理由。")], "zh",
                       grow_budget=10, register=True, corpus=corpus, venue="JX")
        t = (not worse[0]) and any("本文" in x and "may not increase" in x for x in worse[1]) and better[0]
        good &= t
        print(f"{'PASS' if t else 'FAIL'} register direction: more of an already-high 本文 is blocked, "
              "switching it to 本研究 passes (synthetic corpus)")

        draft, bad, fine = (os.path.join(d, x) for x in ("d.md", "bad.py", "ok.json"))
        Path(draft).write_text(zh, encoding="utf-8")
        Path(bad).write_text('# number: deliberate error\nE = [("共 72 則", "共 70 則")]\n', encoding="utf-8")
        Path(fine).write_text(json.dumps([["本研究對樣本進行比較", "本研究比較樣本"]], ensure_ascii=False),
                              encoding="utf-8")
        run = lambda e: subprocess.run([sys.executable, __file__, "--draft", draft, "--edits", e,
                                        "--lang", "zh", "--apply"], capture_output=True, text=True).returncode
        rc_bad = run(bad)
        kept = Path(draft).read_text(encoding="utf-8") == zh
        rc_ok = run(fine)
        applied = "本研究比較樣本" in Path(draft).read_text(encoding="utf-8")
        t = rc_bad == 1 and kept and rc_ok == 0 and applied
        good &= t
        print(f"{'PASS' if t else 'FAIL'} --apply: a failing list leaves the draft alone, a passing one writes it")

        evil = os.path.join(d, "evil.py")
        Path(evil).write_text('import os\nE = [(os.getcwd(), "x")]\n', encoding="utf-8")
        r = subprocess.run([sys.executable, __file__, "--draft", draft, "--edits", evil, "--lang", "zh"],
                           capture_output=True, text=True)
        t = r.returncode != 0 and "literal" in r.stderr
        good &= t
        print(f"{'PASS' if t else 'FAIL'} an edits file with code in it is refused, not executed")
    print("\nselftest: all passed" if good else "\nselftest: FAILED, do not trust this checker")
    return 0 if good else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--draft")
    ap.add_argument("--edits", help="change-list file(s), comma-separated (give all of them to check "
                                    "several editors' lists together)")
    ap.add_argument("--lang", choices=["zh", "en"])
    ap.add_argument("--lines", help="edits may only sit in these line ranges, e.g. 49-58,69-104")
    ap.add_argument("--lock", default="", help="terms that must not change, comma-separated")
    ap.add_argument("--lock-file", help="terms that must not change, one per line")
    ap.add_argument("--forbid-file", help="JSON {label: regex} of extra forms that may not increase")
    ap.add_argument("--allow-grow", action="store_true", help="no limit on text growth")
    ap.add_argument("--grow-budget", type=int, default=0,
                    help="net Han characters (zh) or words (en) all edits together may add. Merging "
                         "sentences and restoring 進行/透過 add characters; keep it small when the "
                         "venue's length limit is tight")
    ap.add_argument("--corpus", help="register baseline corpus (default: $ZH_CORPUS_DIR for zh, "
                                     "$CORPUS_DIR for en); without one the register check is skipped")
    ap.add_argument("--venue", help="register baseline venue folder")
    ap.add_argument("--biber-python", help="python of the Biber environment (default: $BIBER_PYTHON)")
    ap.add_argument("--no-register", action="store_true", help="skip the register direction check")
    ap.add_argument("--no-biber", action="store_true", help="English: skip the Biber grammar layer")
    ap.add_argument("--max-len", type=int, help="sentence length limit (default 120 Han chars / 45 words)")
    ap.add_argument("--apply", action="store_true", help="write the edits back only if everything passes")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.draft and a.edits and a.lang):
        ap.error("needs --draft, --edits and --lang (or --selftest)")
    locks = [x.strip() for x in a.lock.split(",") if x.strip()]
    if a.lock_file:
        locks += [l.strip() for l in Path(a.lock_file).expanduser().read_text(encoding="utf-8").splitlines()
                  if l.strip() and not l.startswith("#")]
    corpus = a.corpus or os.environ.get("ZH_CORPUS_DIR" if a.lang == "zh" else "CORPUS_DIR")
    text = Path(a.draft).read_text(encoding="utf-8")
    ok, rep, after = check(text, load_edits(a.edits), a.lang, a.lines, locks, a.allow_grow, a.max_len,
                           a.grow_budget, bool(corpus) and not a.no_register, corpus, a.venue,
                           a.biber_python, not a.no_biber, load_forbid(a.forbid_file))
    print("\n".join(rep))
    print("overall:", "PASS" if ok else "FAIL, fix and rerun")
    if a.apply:
        if ok:
            Path(a.draft).write_text(after, encoding="utf-8")
            print(f"written back to {a.draft}")
        else:
            print("not passed; the draft was not changed")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
