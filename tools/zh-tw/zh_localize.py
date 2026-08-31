#!/usr/bin/env python3
"""Taiwan-Mandarin localization check — mainland-vs-Taiwan term list + 台/臺
consistency + a false-positive whitelist. Local-only, never uploads. Report-only.

Why not OpenCC: OpenCC's s2twp over-corrects text that is *already* Traditional
(it "fixes" 文件→檔案, 參考→引…), so the noise drowns the signal. This tool uses a
precise mainland-term table + a 台/臺 check with a whitelist, and only reports real
hits — you decide each one by hand.

No dependencies (Python 3 standard library only).

Usage:
    python3 zh_localize.py <file.md|.txt|.tex>     # or pipe via stdin
"""
import re
import sys
import sys as _sys, pathlib as _pl
_sys.path.insert(0, str(_pl.Path(__file__).resolve().parent.parent / "common"))
from md_prose import mask_nonprose
from pathlib import Path

# ── Mainland terms (Traditional script, but mainland usage). A value in
#    parentheses = context-sensitive, judge case by case. Extend freely. ──
TERMS = {
    "反饋": "回饋", "落地": "實施(指 implement;landing page 之落地頁→到達頁)", "錨定": "參照(anchoring 直譯腔,如錨定樣本→參照樣本;心理學術語「錨定效應」為例外)", "視頻": "影片", "音頻": "音訊", "屏幕": "螢幕", "默認": "預設",
    "接口": "介面", "服務器": "伺服器", "用戶": "使用者", "內存": "記憶體",
    "信息": "資訊", "信號": "訊號", "數據庫": "資料庫", "代碼": "程式碼",
    "編程": "程式設計", "調試": "除錯", "緩存": "快取", "帶寬": "頻寬",
    "硬盤": "硬碟", "激光": "雷射", "矢量": "向量", "概率": "機率",
    "軟件": "軟體", "硬件": "硬體", "鼠標": "滑鼠", "光標": "游標",
    "智能": "智慧(AI context)", "卸載": "解除安裝(software context)",
    "網絡": "網路(concrete-network context)",
    "視屏": "螢幕／影片", "缺省": "預設", "字符": "字元", "比特": "位元",
    "默認值": "預設值", "數據": "資料(numeric context may keep 數據)",
}

# ── Whitelist: fragments containing these strings are NOT reported
#    (correct Taiwan terms / brand names / established academic renderings).
#    🔧 CUSTOMIZE: add your own institution/brand names that use 台 officially. ──
WHITELIST = (
    # established academic renderings / correct Taiwan usage (avoid false hits)
    "演算法", "演算", "數據庫",
    # generic academic terms whose 智能/卸載 are NOT the mainland software senses
    "認知卸載", "智能障礙",
    # generic Taiwan "item/procedure" (not project/program)
    "評分項目", "申請程序", "程序正義", "送審程序",
    # brand / institution names that officially use 台 (add your own here)
    "台電", "台新", "台灣電力", "台積電", "台塑", "台達", "台泥", "台肥", "台糖",
)


def _mask(line: str) -> str:
    for w in WHITELIST:
        line = line.replace(w, "□" * len(w))
    return line


def check_terms(text: str):
    hits = []
    for i, line in enumerate(text.split("\n"), 1):
        masked = _mask(line)
        for cn, tw in TERMS.items():
            for m in re.finditer(re.escape(cn), masked):
                ctx = line[max(0, m.start() - 8): m.start() + len(cn) + 8]
                hits.append((i, cn, tw, ctx))
    return hits


def check_tai(text: str):
    """台→臺 consistency (formal documents prefer 臺; brand names already masked)."""
    hits = []
    for i, line in enumerate(text.split("\n"), 1):
        masked = _mask(line)
        for m in re.finditer("台", masked):
            ctx = line[max(0, m.start() - 6): m.start() + 7]
            hits.append((i, ctx))
    return hits


def report(text: str) -> str:
    L = ["=== 1. Mainland terms (context-sensitive, judge each) ==="]
    th = check_terms(text)
    if not th:
        L.append("  OK — no hits.")
    else:
        for i, cn, tw, ctx in th:
            L.append(f"  L{i}  「{cn}」→{tw}   …{ctx}…")

    L.append("\n=== 2. 台→臺 (formal docs prefer 臺; brand names auto-excluded) ===")
    ta = check_tai(text)
    if not ta:
        L.append("  OK — no non-brand 台.")
    else:
        for i, ctx in ta[:40]:
            L.append(f"  L{i}  台→臺   …{ctx}…")
        if len(ta) > 40:
            L.append(f"  … {len(ta)} total, first 40 shown.")
    L.append(f"\nSummary: {len(th)} mainland-term hits, {len(ta)} 台→臺. "
             "Report-only; judge each by hand.")
    return "\n".join(L)


def main():
    if any(a in ("-h", "--help") for a in sys.argv[1:]):
        print(__doc__.strip() if __doc__ else "usage: see the header of this file")
        return
    arg = sys.argv[1] if len(sys.argv) > 1 else "-"
    text = sys.stdin.read() if arg == "-" else \
        Path(arg).expanduser().read_text(encoding="utf-8", errors="ignore")
    # 🔴 Mask HTML comments and code fences: internal notes never reach the
    #    submitted paper, so flagging terms inside them is a false alarm.
    #    MASK rather than delete — this tool reports line numbers, and deleting
    #    lines would shift every one of them.
    #    ⚠️ Deliberately does NOT mask tables and headings: readers see that text,
    #    so its terminology must still be checked.
    text = mask_nonprose(text)
    print(report(text))


if __name__ == "__main__":
    main()
