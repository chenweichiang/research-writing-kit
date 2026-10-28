#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["numpy"]
# ///
"""coding_pack.py: a second-coder pack for qualitative coding. Question CSVs plus a codebook
become one offline HTML page; the coder's export becomes the project's 0/1 coding tables;
Cohen's kappa scores the agreement.

Why it exists: when a study needs a second coder, each project tends to hand-roll its own
web page or spreadsheet, and coders who are not methods specialists give up on a code table
that is hard to fill in. This tool fixes the flow: the coder opens ONE html file, ticks the
codes for one response at a time (number keys work), and exports a CSV; the author then
turns that export back into the project's own 0/1 coding tables and scores the agreement.

Usage:
  coding_pack.py build --codebook codebook.md --csv q1.csv [--csv q2.csv ...] --id-col pid --text-col response \\
                       --coder "Coder B" --out pack.html [--title TITLE] [--ui en|zh-TW] [--allow-tracked]
  coding_pack.py import export.csv --into FOLDER [--blank-glob '*_BLANK_*.csv'] [--id-col pid] [--text-col response] [--force]
  coding_pack.py score A_DONE.csv B_DONE.csv [--pair C D ...] --id-col pid --text-col response \\
                       --threshold 0.61 --low-prev 0.10 [--seed 20261025] [--boot 2000] [--out-dir DIR]
  coding_pack.py --selftest

Codebook format (Markdown): a `## General rules` section first (shown to the coder; inline
markup such as bold and backticks is stripped; the Chinese heading `## 總則` also works),
then one section per question, `## Question 1: the question text` (the label is split from
the text at the first colon, ASCII or full-width), holding one table
`| Code | Definition | Boundary (what does not count) |`. A code name may carry a bracketed
suffix such as `L_sound (new)`; it is removed before names are matched against the CSV
columns. The question sections map to the `--csv` files in order. A code whose name ends in
"other" (or the Chinese 其他) means "none of the above": it is 1 only when every other code
is 0 (mutually exclusive with them).

Each question CSV is a "BLANK" file: an id column, a response-text column, and one empty
column per code. The page shows the response text; the export never contains it.

Export file (long table, UTF-8 with BOM): `pack_hash,coder,question,pid,code,value`
  question = file name of that question's BLANK CSV; code = the CSV column name (prefix such
  as L_ included); value = 0 or 1. The response text is not included.

Pack hash = sha256 over each question's (file name, code list, (pid, response text) sorted
by pid). build writes it into the HTML; import recomputes it from the BLANK files and
refuses to continue if it differs, so an export cannot be paired with edited or different
questions.

import keeps the BLANK file as it is (pid, response text and code-column order unchanged),
replaces only the code columns with 0/1, and names the output by replacing the first
"BLANK" in the file name with "DONE". An existing DONE file is never overwritten unless
--force is given.

score compares two coders' DONE files code by code: Cohen's kappa, percent agreement, PABAK,
prevalence counts, a bootstrap 95% CI (resampling responses), and flags: below the kappa
threshold, or low prevalence (kappa is not interpreted there; only agreement and counts are
reported). A pooled kappa over all questions and codes is added. Fix the threshold and the
low-prevalence rule BEFORE seeing the data, and report the kappa from before the coders
discuss their disagreements.

HTML page language: English by default; `--ui zh-TW` gives the Traditional Chinese (Taiwan)
interface. All interface strings live in the UI dict, one entry per language.

Exit codes: 0 success; 2 invalid input (mismatch, missing values, hash mismatch, rule
violation, missing dependency); 3 privacy gate refused the output path; 4 a DONE file
already exists.

Privacy: the HTML contains participants' answers. Open it locally or hand it to the coder
directly; never post it on a public page and never upload it to a cloud AI service. The
author side needs only counts, the hash and kappa numbers; score prints only code names,
numbers and pids, never response text. build refuses to write the page inside a git
repository unless the path is ignored (or --allow-tracked is given), because a committed
page stays in history for good.

Dependencies: Python 3.9+; numpy for score (pip install numpy). build and import need only
the standard library.
"""
import argparse
import csv
import fnmatch
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

try:
    import numpy as np
except ImportError:  # score and selftest report this with an install hint
    np = None

NAN = float("nan")
PRIVACY_MSG = ("note: this file contains participants' answers. Keep it local or hand it directly to the "
               "coder; do not put it on a public page or upload it to a cloud AI service.")
PRE_MSG = ("reminder: the threshold and the low-prevalence rule must be fixed before seeing the data; "
           "the kappa from before discussion is the one to report.")
RULES_HEADINGS = ("總則", "general rules", "rules", "instructions", "guidelines")
CODE_HEADER_CELLS = ("碼", "code")


class Fail(Exception):
    def __init__(self, msg, code=2):
        super().__init__(msg)
        self.code = code


def need_numpy():
    if np is None:
        raise Fail("score needs numpy. Install it with: pip install numpy")


# ------------------------------------------------------------ UI strings (one dict per language)
# {name} placeholders are filled in by the page script.
UI = {
    "en": {
        "lang": "en",
        "default_title": "Second-coder coding",
        "intro": "Coder: {coder}. {items} responses in {qs} questions. Progress is saved in this browser "
                 "automatically; reloading the page will not lose it.",
        "rules": "General rules",
        "col_code": "Code",
        "col_def": "Definition and boundary",
        "not_counted": "Does not count: ",
        "start": "Start",
        "resume": "Continue ({done} done)",
        "progress": "Item {pos} of {total}",
        "prompt": "Which of these apply to this response? (tick all that apply)",
        "need_other": "If none apply, tick \"{other}\"",
        "need_one": "Tick at least one; if none apply, press \"None apply\".",
        "prev": "Previous",
        "next": "Next (Enter)",
        "finish": "Finish",
        "none_fit": "None apply",
        "none_ok": "Confirmed: none apply (all 0).",
        "done_title": "All items reviewed",
        "done_ok": "All {total} items are done. Press the button below to export, then send the downloaded "
                   "CSV file back to the researcher.",
        "done_left": "{left} items are not done yet. You can export once every item is done.",
        "export": "Export CSV",
        "back_first": "Back to the first unfinished item",
        "back_last": "Back to the last item",
        "export_note": "The export contains the codes only, not the response text.",
        "hash": "Pack hash ",
    },
    "zh-TW": {
        "lang": "zh-Hant",
        "default_title": "第二編碼者判讀",
        "intro": "判讀者：{coder}　共 {items} 則、{qs} 題。進度自動存在這個瀏覽器，重新整理不會掉。",
        "rules": "總則",
        "col_code": "碼",
        "col_def": "定義與邊界",
        "not_counted": "不算：",
        "start": "開始",
        "resume": "繼續（已完成 {done} 則）",
        "progress": "第 {pos} 則／共 {total} 則",
        "prompt": "這則回答符合哪些？（可複選）",
        "need_other": "都不符合請勾「{other}」",
        "need_one": "請至少勾一項；若都不符合，請按「都不符合」。",
        "prev": "上一則",
        "next": "下一則（Enter）",
        "finish": "完成",
        "none_fit": "都不符合",
        "none_ok": "已確認：這則都不符合（全 0）。",
        "done_title": "全部看完了",
        "done_ok": "共 {total} 則都已完成。按下面的按鈕匯出，把下載的 CSV 檔交回給研究者。",
        "done_left": "還有 {left} 則沒完成，完成後才能匯出。",
        "export": "匯出 CSV",
        "back_first": "回到第一則未完成",
        "back_last": "回到最後一則",
        "export_note": "匯出檔只有編碼結果，不含回答原文。",
        "hash": "包雜湊 ",
    },
}


# ------------------------------------------------------------ codebook

def strip_suffix(name):
    """Drop a trailing bracketed suffix and wrapping marks: `L_sound (new)` -> `L_sound`."""
    name = name.strip().strip("`*").strip()
    return re.sub(r"\s*[（(][^）)]*[）)]\s*$", "", name).strip()


def display_name(code):
    """Plain display name: drop an English prefix such as L_ or T_."""
    return re.sub(r"^[A-Za-z]+_", "", code)


def is_other(name):
    """True for the exclusive 'none of the above' code: name ends in 'other' or 其他."""
    return name.endswith("其他") or re.search(r"(?:^|[_\s])other$", name, re.I) is not None


def plain_md(s):
    """The page does not render markdown: strip inline marks (bold, italics, code, links); keep
    line breaks and numbering."""
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"(\*\*|__)(.+?)\1", r"\2", s)
    s = re.sub(r"`([^`]*)`", r"\1", s)
    s = re.sub(r"(?<![*\w])\*(?=\S)([^*\n]+?)(?<=\S)\*(?!\*)", r"\1", s)
    return s


def split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.replace("\\|", "|").strip() for c in re.split(r"(?<!\\)\|", s)]


def parse_codebook(text):
    """Return (rules text, [question dict]); question = label, text, heading, codes[{raw,name,definition,boundary}]."""
    sections, cur = [], None
    for line in text.splitlines():
        m = re.match(r"^##\s+(.*\S)\s*$", line)
        if m and not line.startswith("###"):
            cur = {"heading": m.group(1), "lines": []}
            sections.append(cur)
        elif cur is not None:
            cur["lines"].append(line)
    rules, questions = "", []
    for sec in sections:
        if sec["heading"].lower().startswith(RULES_HEADINGS):
            rules = plain_md("\n".join(sec["lines"]).strip())
            continue
        codes = []
        for line in sec["lines"]:
            if not line.strip().startswith("|"):
                continue
            cells = split_row(line)
            if all(re.fullmatch(r":?-{2,}:?", c) or c == "" for c in cells):
                continue
            if cells[0].strip("*` ").lower() in CODE_HEADER_CELLS:
                continue
            codes.append({
                "raw": cells[0],
                "name": strip_suffix(cells[0]),
                "definition": plain_md(cells[1]) if len(cells) > 1 else "",
                "boundary": plain_md(cells[2]) if len(cells) > 2 else "",
            })
        if not codes:
            continue
        parts = re.split(r"[：:]", sec["heading"], maxsplit=1)
        label = parts[0].strip()
        qtext = parts[1].strip() if len(parts) > 1 else ""
        names = [c["name"] for c in codes]
        dup = sorted({n for n in names if names.count(n) > 1})
        if dup:
            raise Fail(f"codebook section \"{sec['heading']}\" has duplicate codes: {', '.join(dup)}")
        questions.append({"heading": sec["heading"], "label": label, "text": qtext, "codes": codes})
    if not questions:
        raise Fail("no question section found in the codebook (need `## Question 1: ...` followed by a code table)")
    return rules, questions


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    if not rows:
        raise Fail(f"{path} is empty")
    return rows[0], rows[1:]


def load_question_csv(path, id_col, text_col):
    header, body = read_csv(path)
    for need in (id_col, text_col):
        if need not in header:
            raise Fail(f"{os.path.basename(path)} lacks column \"{need}\" (actual columns: {', '.join(header)})")
    ii, ti = header.index(id_col), header.index(text_col)
    codes = [h for i, h in enumerate(header) if i not in (ii, ti)]
    rows, seen = [], set()
    for r in body:
        if not r or all(not c.strip() for c in r):
            continue
        r = r + [""] * (len(header) - len(r))
        pid = r[ii].strip()
        if pid in seen:
            raise Fail(f"duplicate pid in {os.path.basename(path)}: {pid}")
        seen.add(pid)
        rows.append((pid, r[ti]))
    return {"file": os.path.basename(path), "codes": codes, "rows": rows}


def pack_hash(questions):
    """questions: [{file, codes, rows[(pid, text)]}]; independent of question order and row order."""
    canon = [
        {"q": q["file"], "codes": list(q["codes"]), "rows": sorted([list(r) for r in q["rows"]])}
        for q in sorted(questions, key=lambda q: q["file"])
    ]
    blob = json.dumps(canon, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


# ------------------------------------------------------------ privacy gate

def privacy_gate(out, allow_tracked):
    out = os.path.abspath(out)
    d = os.path.dirname(out)
    while d and not os.path.isdir(d):
        d = os.path.dirname(d)
    try:
        r = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    except OSError:
        return  # git is not installed
    if r.returncode != 0:
        return  # not inside a git repository
    ig = subprocess.run(["git", "-C", d, "check-ignore", "-q", out], capture_output=True, text=True)
    if ig.returncode == 0:
        return
    if allow_tracked:
        print("warning: the output path is inside a git repository and not ignored "
              "(allowed by --allow-tracked).", file=sys.stderr)
        return
    raise Fail(f"refusing to write {out}: it is inside a git repository ({r.stdout.strip()}) and not ignored, "
               "and the HTML contains participants' answers, which would stay in history once committed. "
               "Add the path to .gitignore, or pass --allow-tracked if you accept the risk.", 3)


# ------------------------------------------------------------ build

HTML_TEMPLATE = r"""<!doctype html>
<html lang="__LANG__">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
:root{--bg:#faf9f6;--fg:#222;--mute:#6b6b6b;--line:#d8d4cc;--acc:#1f5f8b;--accbg:#e8f1f8;--warn:#a33}
@media (prefers-color-scheme:dark){:root{--bg:#1c1c1e;--fg:#e8e6e1;--mute:#a09d96;--line:#3a3a3c;--acc:#7db7e0;--accbg:#22333f;--warn:#e88}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:17px/1.7 -apple-system,"Helvetica Neue","PingFang TC","Noto Sans TC",sans-serif}
main{max-width:760px;margin:0 auto;padding:20px 16px 90px}
h1{font-size:1.4em;margin:.4em 0}h2{font-size:1.15em;margin:1.6em 0 .4em}
.rules,.answer{white-space:pre-wrap;border:1px solid var(--line);border-radius:8px;padding:12px 14px}
.answer{font-size:1.1em;background:var(--accbg)}
.qtext{color:var(--mute);margin:.2em 0 .6em}
table{border-collapse:collapse;width:100%;font-size:.92em}td,th{border-bottom:1px solid var(--line);padding:6px 8px;vertical-align:top;text-align:left}
small,.small{color:var(--mute);font-size:.82em;display:block;line-height:1.5}
label.opt{display:flex;gap:10px;align-items:flex-start;border:1px solid var(--line);border-radius:8px;padding:10px 12px;margin:8px 0;cursor:pointer}
label.opt.on{border-color:var(--acc);background:var(--accbg)}
label.opt input{width:22px;height:22px;margin-top:4px;flex:none}
.key{display:inline-block;min-width:1.4em;color:var(--acc);font-weight:bold}
button{font:inherit;padding:9px 18px;border-radius:8px;border:1px solid var(--acc);background:var(--acc);color:#fff;cursor:pointer;margin:4px 6px 4px 0}
button.ghost{background:transparent;color:var(--acc)}button:disabled{opacity:.4;cursor:not-allowed}
.bar{height:6px;background:var(--line);border-radius:3px;margin:6px 0 14px}.bar>div{height:100%;background:var(--acc);border-radius:3px}
.msg{color:var(--warn);min-height:1.6em}
#hash{position:fixed;right:8px;bottom:6px;font:11px monospace;color:var(--mute)}
</style>
</head>
<body>
<main id="app"></main>
<div id="hash"></div>
<script type="application/json" id="pack-data">__DATA__</script>
<script>
(function(){
"use strict";
var D=JSON.parse(document.getElementById("pack-data").textContent);
var U=D.ui;
function T(key,vars){var s=U[key];Object.keys(vars||{}).forEach(function(k){s=s.split("{"+k+"}").join(String(vars[k]));});return s;}
var KEY="codingpack:"+D.hash+":"+D.coder;
var items=[];
D.questions.forEach(function(q,qi){q.rows.forEach(function(r,ri){items.push({qi:qi,ri:ri});});});
var state={ans:{},pos:-1};
try{var s=localStorage.getItem(KEY);if(s){var o=JSON.parse(s);if(o&&o.ans){state=o;}}}catch(e){}
function save(){try{localStorage.setItem(KEY,JSON.stringify(state));}catch(e){}}
function ak(it){return it.qi+":"+it.ri;}
function getAns(it){var k=ak(it);if(!state.ans[k]){state.ans[k]={v:D.questions[it.qi].codes.map(function(){return 0;}),empty:false};}return state.ans[k];}
function sum(a){return a.v.reduce(function(x,y){return x+y;},0);}
function isDone(it){var a=state.ans[ak(it)];return !!a&&(sum(a)>0||a.empty);}
function doneCount(){return items.filter(isDone).length;}
var app=document.getElementById("app");
document.getElementById("hash").textContent=U.hash+D.hash.slice(0,12);
var msg="";
function h(tag,attrs,kids){var e=document.createElement(tag);
  if(attrs){Object.keys(attrs).forEach(function(k){if(k==="class")e.className=attrs[k];else if(k.slice(0,2)==="on")e.addEventListener(k.slice(2),attrs[k]);else e.setAttribute(k,attrs[k]);});}
  (kids||[]).forEach(function(c){e.appendChild(typeof c==="string"?document.createTextNode(c):c);});return e;}
function small(t){return h("small",null,[t]);}
function go(p){state.pos=p;msg="";save();render();window.scrollTo(0,0);}
function firstUndone(){for(var i=0;i<items.length;i++){if(!isDone(items[i]))return i;}return items.length;}
function toggle(it,ci){var q=D.questions[it.qi],a=getAns(it);
  if(a.v[ci]){a.v[ci]=0;}else{a.v[ci]=1;
    if(ci===q.other){a.v=a.v.map(function(x,i){return i===ci?1:0;});}
    else if(q.other>=0){a.v[q.other]=0;}}
  a.empty=false;msg="";save();render();}
function next(){var it=items[state.pos],q=D.questions[it.qi],a=getAns(it);
  if(sum(a)===0&&!a.empty){msg=q.other>=0?T("need_other",{other:q.codes[q.other].label}):T("need_one");render();return;}
  go(state.pos+1);}
function noneFit(){var it=items[state.pos],a=getAns(it);a.v=a.v.map(function(){return 0;});a.empty=true;go(state.pos+1);}
function renderIntro(){
  var kids=[h("h1",null,[D.title]),small(T("intro",{coder:D.coder,items:items.length,qs:D.questions.length})),
    h("h2",null,[U.rules]),h("div",{class:"rules"},[D.rules])];
  D.questions.forEach(function(q){
    kids.push(h("h2",null,[q.label+(q.text?": ":"")+q.text]));
    var t=h("table");t.appendChild(h("tr",null,[h("th",null,[U.col_code]),h("th",null,[U.col_def])]));
    q.codes.forEach(function(c){var td=h("td");td.appendChild(document.createTextNode(c.definition||""));
      if(c.boundary){td.appendChild(small(U.not_counted+c.boundary));}
      t.appendChild(h("tr",null,[h("td",null,[c.label]),td]));});
    kids.push(t);});
  var d=doneCount();
  kids.push(h("p",null,[h("button",{onclick:function(){go(firstUndone());}},[d>0?T("resume",{done:d}):U.start])]));
  return kids;}
function renderItem(){
  var it=items[state.pos],q=D.questions[it.qi],row=q.rows[it.ri],a=getAns(it);
  var kids=[h("div",{class:"bar"},[h("div",{style:"width:"+Math.round(100*state.pos/items.length)+"%"})]),
    small(T("progress",{pos:state.pos+1,total:items.length})+"  "+q.label),
    h("div",{class:"qtext"},[q.text]),h("div",{class:"answer"},[row.text]),
    h("h2",null,[U.prompt])];
  q.codes.forEach(function(c,ci){
    var cb=h("input",{type:"checkbox"});cb.checked=!!a.v[ci];cb.addEventListener("change",function(){toggle(it,ci);});
    var body=h("div",null,[(ci<9?h("span",{class:"key"},[String(ci+1)+" "]):""),c.label]);
    if(c.definition)body.appendChild(small(c.definition));
    if(c.boundary)body.appendChild(small(U.not_counted+c.boundary));
    kids.push(h("label",{class:"opt"+(a.v[ci]?" on":"")},[cb,body]));});
  kids.push(h("div",{class:"msg"},[msg]));
  var nav=[h("button",{class:"ghost",onclick:function(){go(state.pos-1);}},[U.prev]),
    h("button",{onclick:next},[state.pos===items.length-1?U.finish:U.next])];
  if(q.other<0&&sum(a)===0){nav.push(h("button",{class:"ghost",onclick:noneFit},[U.none_fit]));}
  kids.push(h("div",null,nav));
  if(a.empty&&sum(a)===0)kids.push(small(U.none_ok));
  return kids;}
function csvEsc(v){v=String(v);return /[",\n\r]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v;}
function exportCsv(){
  var lines=["pack_hash,coder,question,pid,code,value"];
  items.forEach(function(it){var q=D.questions[it.qi],row=q.rows[it.ri],a=getAns(it);
    q.codes.forEach(function(c,ci){lines.push([D.hash,D.coder,q.file,row.pid,c.name,a.v[ci]].map(csvEsc).join(","));});});
  var blob=new Blob(["﻿"+lines.join("\r\n")+"\r\n"],{type:"text/csv;charset=utf-8"});
  var url=URL.createObjectURL(blob),a=document.createElement("a");
  a.href=url;a.download="coding_export_"+D.coder.replace(/[^\w\-]+/g,"_")+"_"+D.hash.slice(0,12)+".csv";document.body.appendChild(a);a.click();
  setTimeout(function(){URL.revokeObjectURL(url);a.remove();},500);}
function renderFinish(){
  var left=items.length-doneCount();
  var kids=[h("h1",null,[U.done_title]),h("p",null,[left===0?T("done_ok",{total:items.length}):T("done_left",{left:left})])];
  var b=h("button",{onclick:exportCsv},[U.export]);if(left>0)b.disabled=true;
  kids.push(h("p",null,[b,h("button",{class:"ghost",onclick:function(){go(left>0?firstUndone():items.length-1);}},[left>0?U.back_first:U.back_last])]));
  kids.push(small(U.export_note));
  return kids;}
function render(){
  var kids=state.pos<0?renderIntro():(state.pos>=items.length?renderFinish():renderItem());
  app.textContent="";kids.forEach(function(k){app.appendChild(k);});}
document.addEventListener("keydown",function(e){
  if(state.pos<0||state.pos>=items.length)return;
  if(e.key==="Enter"){e.preventDefault();if(document.activeElement&&document.activeElement.blur)document.activeElement.blur();next();return;}
  if(/^[1-9]$/.test(e.key)){var it=items[state.pos],q=D.questions[it.qi],ci=parseInt(e.key,10)-1;
    if(ci<q.codes.length){e.preventDefault();toggle(it,ci);}}});
if(state.pos>items.length)state.pos=-1;
render();
})();
</script>
</body>
</html>
"""


def cmd_build(a):
    if a.ui not in UI:
        raise Fail(f"--ui must be one of: {', '.join(UI)}")
    ui = UI[a.ui]
    with open(a.codebook, encoding="utf-8") as f:
        rules, qs = parse_codebook(f.read())
    if len(qs) != len(a.csv):
        raise Fail(f"the codebook has {len(qs)} question sections but {len(a.csv)} --csv files were given "
                   "(they must correspond one to one, in order)")
    loaded = []
    errs = []
    for q, path in zip(qs, a.csv):
        data = load_question_csv(path, a.id_col, a.text_col)
        cb = [c["name"] for c in q["codes"]]
        miss = [c for c in cb if c not in data["codes"]]
        extra = [c for c in data["codes"] if c not in cb]
        if miss or extra:
            errs.append(f"\"{q['heading']}\" vs {data['file']}: only in codebook {miss or 'none'}; "
                        f"only in CSV {extra or 'none'}")
        loaded.append(data)
    names = [d["file"] for d in loaded]
    if len(set(names)) != len(names):
        errs.append("two --csv files share a file name (the export identifies questions by file name, so they must differ)")
    if errs:
        raise Fail("code columns do not match:\n  " + "\n  ".join(errs))
    privacy_gate(a.out, a.allow_tracked)
    h = pack_hash(loaded)
    def by_name(q):
        return {c["name"]: c for c in q["codes"]}

    questions = []
    for q, d in zip(qs, loaded):
        cm = by_name(q)
        codes = [{"name": n, "label": display_name(n), "definition": cm[n]["definition"], "boundary": cm[n]["boundary"]}
                 for n in d["codes"]]
        other = next((i for i, c in enumerate(codes) if is_other(c["name"])), -1)
        questions.append({"file": d["file"], "label": q["label"], "text": q["text"], "codes": codes, "other": other,
                          "rows": [{"pid": p, "text": t} for p, t in d["rows"]]})
    title = a.title or ui["default_title"]
    data = {"hash": h, "coder": a.coder, "title": title, "rules": rules, "ui": ui, "questions": questions}
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/").replace("<!--", "<\\!--")
    page = (HTML_TEMPLATE.replace("__LANG__", ui["lang"]).replace("__TITLE__", html.escape(title))
            .replace("__DATA__", blob))
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(page)
    n = sum(len(d["rows"]) for d in loaded)
    print(f"wrote {a.out}: {len(qs)} questions, {n} responses; pack hash {h[:12]}")
    print(PRIVACY_MSG, file=sys.stderr)
    return 0


# ------------------------------------------------------------ import

def cmd_import(a):
    header, body = read_csv(a.export)
    want = ["pack_hash", "coder", "question", "pid", "code", "value"]
    if header != want:
        raise Fail(f"the export file's columns should be {','.join(want)}; actual: {','.join(header)}")
    recs = [r for r in body if r and any(c.strip() for c in r)]
    hashes = {r[0] for r in recs}
    coders = {r[1] for r in recs}
    if len(hashes) != 1 or len(coders) != 1:
        raise Fail(f"the export should hold one pack hash and one coder; found {len(hashes)} hashes and {len(coders)} coders")
    exp_hash, coder = hashes.pop(), coders.pop()
    if not os.path.isdir(a.into):
        raise Fail(f"--into must be the folder holding the BLANK files; {a.into} does not exist")
    blanks = sorted(f for f in os.listdir(a.into)
                    if fnmatch.fnmatch(f, a.blank_glob) and coder in f)
    if not blanks:
        raise Fail(f"no BLANK file in {a.into} matches {a.blank_glob} with the coder name \"{coder}\" in its file name")
    loaded = [load_question_csv(os.path.join(a.into, f), a.id_col, a.text_col) for f in blanks]
    if pack_hash(loaded) != exp_hash:
        raise Fail(f"pack hash mismatch: export {exp_hash[:12]}, recomputed from the BLANK files {pack_hash(loaded)[:12]} "
                   "(a BLANK file was edited, or this export belongs to a different set of questions)")
    errs = []
    by_q = {}
    for r in recs:
        by_q.setdefault(r[2], []).append(r)
    for q in by_q:
        if q not in blanks:
            errs.append(f"the export has an unknown question: {q}")
    results = {}
    for d in loaded:
        f = d["file"]
        got = {}
        for _, _, _, pid, code, val in by_q.get(f, []):
            if code not in d["codes"]:
                errs.append(f"{f}: unknown code {code}")
                continue
            if val not in ("0", "1"):
                errs.append(f"{f}: pid {pid} code {code} has value \"{val}\", not 0/1")
                continue
            if (pid, code) in got:
                errs.append(f"{f}: pid {pid} code {code} appears twice")
                continue
            got[(pid, code)] = int(val)
        if f not in by_q:
            errs.append(f"{f}: the export has no rows for this question")
        for pid, _ in d["rows"]:
            for c in d["codes"]:
                if (pid, c) not in got:
                    errs.append(f"{f}: pid {pid} is missing code {c}")
        other = next((c for c in d["codes"] if is_other(c)), None)
        if other:
            for pid, _ in d["rows"]:
                vals = {c: got.get((pid, c)) for c in d["codes"]}
                if None in vals.values():
                    continue
                rest = sum(v for c, v in vals.items() if c != other)
                if vals[other] == 1 and rest > 0:
                    errs.append(f"{f}: pid {pid} \"{other}\" and another code are both 1 (they are mutually exclusive)")
                elif vals[other] == 0 and rest == 0:
                    errs.append(f"{f}: pid {pid} is all 0 but \"{other}\" is 0 (none-apply must be coded as {other})")
        results[f] = got
    if errs:
        more = f"\n  ... and {len(errs) - 20} more" if len(errs) > 20 else ""
        raise Fail(f"import validation failed ({len(errs)} problems):\n  " + "\n  ".join(errs[:20]) + more)
    outs = {f: os.path.join(a.into, f.replace("BLANK", "DONE", 1)) for f in blanks}
    exist = [p for p in outs.values() if os.path.exists(p)]
    if exist and not a.force:
        raise Fail("these DONE files already exist; refusing to overwrite (use --force to overwrite):\n  "
                   + "\n  ".join(exist), 4)
    for f, d in zip(blanks, loaded):
        header_b, body_b = read_csv(os.path.join(a.into, f))
        ii = header_b.index(a.id_col)
        ci = {c: header_b.index(c) for c in d["codes"]}
        with open(outs[f], "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(header_b)
            for r in body_b:
                if not r or all(not c.strip() for c in r):
                    continue
                r = r + [""] * (len(header_b) - len(r))
                pid = r[ii].strip()
                for c, i in ci.items():
                    r[i] = str(results[f][(pid, c)])
                w.writerow(r)
        print(f"wrote {outs[f]}")
    print(f"import complete: {len(blanks)} questions, coder \"{coder}\", pack hash {exp_hash[:12]}")
    return 0


# ------------------------------------------------------------ score

def counts_matrix(a, b):
    """Per-response (n11, n10, n01, n00) counts."""
    need_numpy()
    a, b = np.asarray(a, int), np.asarray(b, int)
    return np.stack([(a & b), (a & (1 - b)), ((1 - a) & b), ((1 - a) & (1 - b))], axis=-1)


def kappa_from_counts(c):
    c = np.asarray(c, float)
    n = c.sum(-1)
    po = (c[..., 0] + c[..., 3]) / n
    pa = (c[..., 0] + c[..., 1]) / n
    pb = (c[..., 0] + c[..., 2]) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    with np.errstate(divide="ignore", invalid="ignore"):
        k = (po - pe) / (1 - pe)
    return np.where(np.isclose(1 - pe, 0), np.nan, k)


def point_kappa(a, b):
    """Cohen's kappa for two binary raters; NaN when both use one single value (chance agreement = 1)."""
    need_numpy()
    a, b = np.asarray(a, int), np.asarray(b, int)
    if len(set(a.tolist()) | set(b.tolist())) < 2 or a.size == 0:
        return NAN
    return float(kappa_from_counts(counts_matrix(a, b).sum(axis=0)))


def bootstrap_ci(per_resp_counts, boot, rng):
    """Resample responses; per_resp_counts has shape (N, 4). Degenerate resamples count as NaN and are skipped."""
    n = per_resp_counts.shape[0]
    if n == 0 or boot <= 0:
        return NAN, NAN
    idx = rng.integers(0, n, size=(boot, n))
    ks = kappa_from_counts(per_resp_counts[idx].sum(axis=1))
    ks = ks[~np.isnan(ks)]
    if ks.size == 0:
        return NAN, NAN
    return float(np.percentile(ks, 2.5)), float(np.percentile(ks, 97.5))


def fmt(x, nd=3):
    return "NaN" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.{nd}f}"


def load_done(path, id_col, text_col):
    header, body = read_csv(path)
    if id_col not in header:
        raise Fail(f"{os.path.basename(path)} lacks column \"{id_col}\"")
    ii = header.index(id_col)
    ti = header.index(text_col) if text_col in header else None
    codes = [h for i, h in enumerate(header) if i not in (ii, ti)]
    data, texts = {}, {}
    for r in body:
        if not r or all(not c.strip() for c in r):
            continue
        r = r + [""] * (len(header) - len(r))
        pid = r[ii].strip()
        vals = []
        for c in codes:
            v = r[header.index(c)].strip()
            if v not in ("0", "1"):
                raise Fail(f"{os.path.basename(path)}: pid {pid} code {c} has value \"{v}\", not 0/1 (is the file completely filled in?)")
            vals.append(int(v))
        data[pid] = vals
        if ti is not None:
            texts[pid] = r[ti]
    return codes, data, texts


FLAG_LOW = "low prevalence: kappa not interpreted, agreement and counts only"
FLAG_OK, FLAG_BELOW, FLAG_SINGLE = "meets threshold", "below threshold", "single value"


def cmd_score(a):
    need_numpy()
    pairs = [(a.a, a.b)] + [tuple(p) for p in (a.pair or [])]
    print(PRE_MSG)
    rng = np.random.default_rng(a.seed)
    rows, all_a, all_b, all_counts = [], [], [], []
    for pa, pb in pairs:
        ca, da, ta = load_done(pa, a.id_col, a.text_col)
        cb, db, tb = load_done(pb, a.id_col, a.text_col)
        qname = re.sub(r"[^\w\-一-鿿]+", "_", os.path.splitext(os.path.basename(pa))[0])
        if ca != cb:
            raise Fail(f"{qname}: the code columns differ: only in A {[c for c in ca if c not in cb]}; "
                       f"only in B {[c for c in cb if c not in ca]}")
        if set(da) != set(db):
            raise Fail(f"{qname}: the pids differ: only in A {sorted(set(da) - set(db))[:10]}; "
                       f"only in B {sorted(set(db) - set(da))[:10]}")
        bad = [p for p in da if p in ta and p in tb and ta[p] != tb[p]]
        if bad:
            raise Fail(f"{qname}: pids whose response text differs between the two files: {bad[:10]}")
        pids = sorted(da)
        A = np.array([da[p] for p in pids], int)
        B = np.array([db[p] for p in pids], int)
        n = len(pids)
        print(f"\n[{qname}] N={n}")
        dis = []
        for j, code in enumerate(ca):
            x, y = A[:, j], B[:, j]
            k = point_kappa(x, y)
            lo, hi = bootstrap_ci(counts_matrix(x, y), a.boot, rng)
            agree = float((x == y).mean())
            pabak = 2 * agree - 1
            na, nb = int(x.sum()), int(y.sum())
            note = ""
            if (na + nb) / 2 < a.low_prev * n:
                flag = FLAG_LOW
            elif np.isnan(k):
                flag, note = FLAG_SINGLE, "both coders used a single value on this code, so kappa cannot be computed"
            else:
                flag = FLAG_OK if k >= a.threshold else FLAG_BELOW
            if np.isnan(k) and not note:
                note = "single value, kappa recorded as NaN"
            rows.append({"question": qname, "code": code, "N": n, "kappa": fmt(k), "ci_low": fmt(lo),
                         "ci_high": fmt(hi), "pct_agree": fmt(agree * 100, 1), "pabak": fmt(pabak),
                         "a_checked": na, "b_checked": nb, "flag": flag, "note": note})
            print(f"  {code}: kappa={fmt(k)} [{fmt(lo)}, {fmt(hi)}] agree={fmt(agree * 100, 1)}% PABAK={fmt(pabak)} "
                  f"checked A={na}/B={nb}  {flag}{(' (' + note + ')') if note else ''}")
            for i in np.nonzero(x != y)[0]:
                dis.append([pids[i], code, int(x[i]), int(y[i]), "", ""])
        all_a.append(A.reshape(-1))
        all_b.append(B.reshape(-1))
        all_counts.append(counts_matrix(A, B).sum(axis=1))  # (N, 4): per response, summed over codes
        if a.out_dir:
            os.makedirs(a.out_dir, exist_ok=True)
            p = os.path.join(a.out_dir, f"disagreements_{qname}.csv")
            with open(p, "w", encoding="utf-8-sig", newline="") as fh:
                w = csv.writer(fh)
                w.writerow(["pid", "code", "A", "B", "consensus", "reason"])
                w.writerows(dis)
        print(f"  {len(dis)} disagreeing cells; pids involved: {sorted({d[0] for d in dis})[:30]}")
    fa, fb = np.concatenate(all_a), np.concatenate(all_b)
    pooled = np.concatenate(all_counts, axis=0)
    k = point_kappa(fa, fb)
    lo, hi = bootstrap_ci(pooled, a.boot, rng)
    agree = float((fa == fb).mean())
    rows.append({"question": "pooled", "code": "all", "N": len(fa), "kappa": fmt(k), "ci_low": fmt(lo),
                 "ci_high": fmt(hi), "pct_agree": fmt(agree * 100, 1), "pabak": fmt(2 * agree - 1),
                 "a_checked": int(fa.sum()), "b_checked": int(fb.sum()), "flag": "",
                 "note": "every response x code cell of every question pooled into one 2x2 table"})
    print(f"\n[pooled] cells={len(fa)} kappa={fmt(k)} [{fmt(lo)}, {fmt(hi)}] agree={fmt(agree * 100, 1)}% "
          f"PABAK={fmt(2 * agree - 1)}")
    if a.out_dir:
        p = os.path.join(a.out_dir, "kappa_summary.csv")
        with open(p, "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
        print(f"wrote {p}")
    return 0


# ------------------------------------------------------------ selftest

def selftest():
    need_numpy()
    import random
    tmp = tempfile.mkdtemp(prefix="coding_pack_selftest_")
    try:
        cb = os.path.join(tmp, "codebook.md")
        with open(cb, "w", encoding="utf-8") as f:
            f.write("# Codebook\n\n## General rules\n1. Several codes may apply.\n2. Use Other only when none apply.\n\n"
                    "## Question 1: What did you learn?\n\n| Code | Definition | Boundary (what does not count) |\n|---|---|---|\n"
                    "| L_teamwork | mentions working together | individual work only |\n"
                    "| L_sound (new) | mentions sound | not music |\n| L_other | none of the above | |\n\n"
                    "## Question 2: Any other thoughts?\n\n| Code | Definition | Boundary |\n|---|---|---|\n"
                    "| T_fun | found it enjoyable | |\n| T_hard | found it hard | |\n")
        rnd = random.Random(7)
        csvs = []
        specs = [("q1_learned", ["L_teamwork", "L_sound", "L_other"]), ("q2_idea", ["T_fun", "T_hard"])]
        for name, codes in specs:
            p = os.path.join(tmp, f"coderB_Second_BLANK_{name}.csv")
            with open(p, "w", encoding="utf-8-sig", newline="") as f:
                w = csv.writer(f)
                w.writerow(["pid", "response"] + codes)
                for i in range(30):
                    w.writerow([f"P{i:02d}", f"fake answer {name} {i}", *[""] * len(codes)])
            csvs.append(p)
        out = os.path.join(tmp, "pack.html")
        argv = ["build", "--codebook", cb, "--out", out, "--coder", "Second", "--allow-tracked"]
        for p in csvs:
            argv += ["--csv", p]
        if main(argv) != 0:
            raise Fail("selftest: build failed")
        with open(out, encoding="utf-8") as fh:
            page = fh.read()
        h = re.search(r'"hash": "([0-9a-f]{64})"', page).group(1)
        exp_rows, a_rows = [["pack_hash", "coder", "question", "pid", "code", "value"]], {}
        for (name, codes), p in zip(specs, csvs):
            for i in range(30):
                other = is_other(codes[-1])
                v = [0] * len(codes)
                if other and rnd.random() < 0.25:
                    v[-1] = 1
                else:
                    k = rnd.randrange(len(codes) - (1 if other else 0))
                    v[k] = 1
                    if rnd.random() < 0.3 and len(codes) - (1 if other else 0) > 1:
                        v[(k + 1) % (len(codes) - (1 if other else 0))] = 1
                a_rows[(name, i)] = list(v)
                bv = list(v)
                if i % 7 == 0 and not other:
                    bv[0] ^= 1
                    if sum(bv) == 0:
                        bv[0] = 1
                for c, x in zip(codes, bv):
                    exp_rows.append([h, "Second", os.path.basename(p), f"P{i:02d}", c, str(x)])
        ex = os.path.join(tmp, "export.csv")
        with open(ex, "w", encoding="utf-8-sig", newline="") as f:
            csv.writer(f).writerows(exp_rows)
        if main(["import", ex, "--into", tmp]) != 0:
            raise Fail("selftest: import failed")
        a_files = []
        for (name, codes), p in zip(specs, csvs):
            ap = os.path.join(tmp, f"coderA_DONE_{name}.csv")
            with open(ap, "w", encoding="utf-8-sig", newline="") as f:
                w = csv.writer(f)
                w.writerow(["pid", "response"] + codes)
                for i in range(30):
                    w.writerow([f"P{i:02d}", f"fake answer {name} {i}"] + a_rows[(name, i)])
            a_files.append(ap)
        b_done = [p.replace("BLANK", "DONE", 1) for p in csvs]
        sc = ["score", a_files[0], b_done[0], "--pair", a_files[1], b_done[1], "--out-dir", os.path.join(tmp, "out"),
              "--boot", "200"]
        if main(sc) != 0:
            raise Fail("selftest: score failed")
        if not os.path.exists(os.path.join(tmp, "out", "kappa_summary.csv")):
            raise Fail("selftest: kappa_summary.csv was not written")
        if shutil.which("node"):
            js = re.search(r"<script>\n(.*?)</script>", page, re.S).group(1)
            jp = os.path.join(tmp, "x.js")
            with open(jp, "w", encoding="utf-8") as fh:
                fh.write(js)
            r = subprocess.run(["node", "--check", jp], capture_output=True, text=True)
            if r.returncode != 0:
                raise Fail("selftest: syntax error in the embedded JavaScript\n" + r.stderr)
        print("selftest passed")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ------------------------------------------------------------ entry point

def build_parser():
    ap = argparse.ArgumentParser(description="second-coder pack for qualitative coding: build / import / score")
    ap.add_argument("--selftest", action="store_true", help="run build -> import -> score on built-in fake data")
    sub = ap.add_subparsers(dest="cmd")
    b = sub.add_parser("build", help="codebook + question CSVs -> one offline HTML page")
    b.add_argument("--codebook", required=True)
    b.add_argument("--csv", action="append", required=True,
                   help="one per question, in the order of the codebook's question sections")
    b.add_argument("--id-col", default="pid")
    b.add_argument("--text-col", default="response")
    b.add_argument("--coder", required=True)
    b.add_argument("--out", required=True)
    b.add_argument("--title", default="")
    b.add_argument("--ui", default="en", choices=sorted(UI), help="language of the coder's page (default en)")
    b.add_argument("--allow-tracked", action="store_true",
                   help="allow writing to a git path that .gitignore does not ignore")
    i = sub.add_parser("import", help="export file -> 0/1 DONE coding tables")
    i.add_argument("export")
    i.add_argument("--into", required=True)
    i.add_argument("--blank-glob", default="*_BLANK_*.csv")
    i.add_argument("--id-col", default="pid")
    i.add_argument("--text-col", default="response")
    i.add_argument("--force", action="store_true")
    s = sub.add_parser("score", help="Cohen's kappa for two coders")
    s.add_argument("a")
    s.add_argument("b")
    s.add_argument("--pair", nargs=2, action="append", metavar=("A", "B"),
                   help="file pair for another question (repeatable)")
    s.add_argument("--id-col", default="pid")
    s.add_argument("--text-col", default="response")
    s.add_argument("--threshold", type=float, default=0.61)
    s.add_argument("--low-prev", type=float, default=0.10)
    s.add_argument("--seed", type=int, default=20261025)
    s.add_argument("--boot", type=int, default=2000)
    s.add_argument("--out-dir", default="")
    return ap


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError, OSError):
            pass
    ap = build_parser()
    a = ap.parse_args(argv)
    try:
        if a.selftest:
            return selftest()
        if a.cmd == "build":
            return cmd_build(a)
        if a.cmd == "import":
            return cmd_import(a)
        if a.cmd == "score":
            return cmd_score(a)
        ap.print_help()
        return 2
    except Fail as e:
        print(f"error: {e}", file=sys.stderr)
        return e.code
    except OSError as e:
        print(f"error: could not read or write a file: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
