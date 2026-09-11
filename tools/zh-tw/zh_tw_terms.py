#!/usr/bin/env python3
"""台灣慣用語詞表：讀取與比對（零依賴，只用 Python 標準庫）。
Taiwan-Mandarin term table: loader and matcher (standard library only).

SSoT＝~/Developer/server/services/research-mcp/zh_tw_terms.tsv 與本檔。
research-writing-kit、deck-template、deck-local 裡的同名檔是同步副本，由
server/scripts/dev/sync_zh_tw_terms.py 覆寫：改詞表只改 server 那份，改完跑同步。
Copies in other repos are overwritten by that sync script; edit the server copy only.

TSV 欄位（tab 分隔，# 開頭為註解）：cn  tw  mode  skip_near  need_near  note  source
  mode       fix＝無歧義，可自動替換（delegate.py 對模型輸出用）；flag＝要看脈絡，只提示；
             allow＝白名單片段（台灣正確詞、既定學術譯名、官方用「台」的專名），比對前先遮掉
  skip_near  命中處前後 WIN 字內出現任一詞（| 分隔）就不報，例：數據 遇到「統計」
  need_near  命中處前後 WIN 字內至少出現一詞才報，例：數組 要有「陣列／索引」
"""
import re
from pathlib import Path
from typing import NamedTuple

TSV = Path(__file__).with_name("zh_tw_terms.tsv")
WIN = 10


class Term(NamedTuple):
    cn: str
    tw: str
    mode: str
    skip: tuple
    need: tuple
    note: str
    source: str


def load(path=None):
    """回傳 (terms, allow)；兩者都依長度由長到短排好。"""
    terms, allow = [], []
    for raw in Path(path or TSV).read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.startswith("#"):
            continue
        cn, tw, mode, skip, need, note, source = (c.strip() for c in (raw.split("\t") + [""] * 7)[:7])
        if cn == "cn":  # 表頭
            continue
        if mode == "allow":
            allow.append(cn)
        elif mode in ("fix", "flag"):
            terms.append(Term(cn, tw, mode, tuple(w for w in skip.split("|") if w),
                              tuple(w for w in need.split("|") if w), note, source))
        else:
            raise ValueError(f"zh_tw_terms.tsv: unknown mode {mode!r} ({cn})")
    terms.sort(key=lambda t: -len(t.cn))
    return terms, tuple(sorted(allow, key=len, reverse=True))


def mask(text, allow):
    """白名單片段換成等長的□，位置不變（行號與上下文照舊可算）。"""
    for a in allow:
        text = text.replace(a, "□" * len(a))
    return text


def _matches(text, terms, allow):
    if not terms:
        return
    masked = mask(text, allow)
    by_cn = {t.cn: t for t in terms}
    rx = re.compile("|".join(re.escape(t.cn) for t in sorted(terms, key=lambda t: -len(t.cn))))
    for m in rx.finditer(masked):
        t = by_cn[m.group()]
        win = masked[max(0, m.start() - WIN): m.end() + WIN]
        if t.skip and any(w in win for w in t.skip):
            continue
        if t.need and not any(w in win for w in t.need):
            continue
        yield m.start(), m.end(), t


def find(text, terms=None, allow=None):
    """回傳 [(起點, Term), …]；同一處只報最長的詞。"""
    if terms is None:
        terms, allow = load()
    return [(s, t) for s, _, t in _matches(text, terms, allow or ())]


def fix(text, terms=None, allow=None):
    """只替換 mode=fix 的詞；回傳 (新文字, ["視頻→影片", …])。"""
    if terms is None:
        terms, allow = load()
    out, done, last = [], [], 0
    for s, e, t in _matches(text, [t for t in terms if t.mode == "fix"], allow or ()):
        out += [text[last:s], t.tw]
        last = e
        done.append(f"{t.cn}→{t.tw}")
    out.append(text[last:])
    return "".join(out), sorted(set(done))
