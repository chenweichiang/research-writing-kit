#!/usr/bin/env python3
"""md_prose.py — extract the *actual prose* from a markdown / TeX / Quarto draft.

🔴 **Why this exists** (learned the hard way, six separate times):
Style diagnostics measure **punctuation density and sentence length**, so any
**layout syntax** that leaks in corrupts the numbers directly. Measured cases:

  · `text.count("---")` counts YAML frontmatter and table separator rows
    (`| :--- | :---: |` — six columns counted as six dashes) as em-dashes.
    Real em-dashes: 56. Reported: 73 (+30%).
  · `<!-- internal note -->` never reaches the submitted paper, yet contributed
    8 semicolons and 10 colons.
  · Semicolons inside pandoc multi-key citations `[@a; @b]` are syntax, not style.
  · Table rows get glued onto neighbouring sentences, and `**Bold head.**` /
    `## Heading` / `![Figure]` defeat the "next char must be uppercase" sentence
    splitter — two or three sentences merge into one. **Mean sentence length was
    inflated by 50%** (35.99 → 23.97 words; percentile 97th → 36th).

Both the English and the Chinese diagnostic need the *same* rules, so they live
here. Change a rule once, here.

⚠️ Scope: this module only strips what is not prose. It makes **no language
   judgement**. Citation keys become a `[CITES]` placeholder rather than being
   deleted, so sentence structure does not collapse.
"""
import re

__all__ = ["strip_markup", "mask_nonprose"]


def mask_nonprose(txt: str) -> str:
    """把「不進交付版」的內容換成等長空白,**保留行數與行內位移**。

    給**逐行報行號**的工具用(`zh_localize` / `zh_term_check` / `voice_lint`):
    直接刪除會讓行號全錯,所以只遮不刪。

    遮的:HTML 註解、code fence。
    🔴 **不遮表格與標題** —— 那是讀者真的看得到的交付文字,術語與在地化必須查。
       (文風指標才要剝表格,走 `strip_markup(drop_tables=True)`。)

    2026-08-23 實測動機:註解裡示範用的「軟件/用戶/數據庫」被 zh_localize 當成真的陸用語;
    `voice_lint` 把 `<!--` `-->` 兩個註解符號本身的 `--` 當成破折號報了 4 次。
    """
    def blank(m):
        return "".join("\n" if c == "\n" else " " for c in m.group(0))
    txt = re.sub(r"<!--.*?-->", blank, txt, flags=re.S)
    txt = re.sub(r"```.*?```", blank, txt, flags=re.S)
    return txt


def strip_markup(txt: str, *, tex: bool = False, drop_tables: bool = True,
                 drop_headings: bool = True, cite_placeholder: str = "[CITES]") -> str:
    """回傳只剩散文的文字。各步驟為何存在見模組 docstring。"""
    if tex:
        txt = re.sub(r"(?m)%.*$", "", txt)
        txt = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^}]*\})?", " ", txt)

    # ① HTML 註解:交付版看不到它,算它的標點是純灌水
    txt = re.sub(r"<!--.*?-->", " ", txt, flags=re.S)
    # ② 程式碼區塊
    txt = re.sub(r"```.*?```", " ", txt, flags=re.S)
    # ③ YAML frontmatter(檔首 --- … ---)
    txt = re.sub(r"\A\s*---\n.*?\n---\s*\n", "\n", txt, flags=re.S)
    # ④ pandoc 多鍵引用 [@a; @b] → 佔位(分號是語法不是文風)
    if cite_placeholder is not None:
        txt = re.sub(r"\[(?:-?@[^\];]+)(?:\s*;\s*-?@[^\];]+)+\]", cite_placeholder, txt)
    # ⑤ 圖片與連結(連結保留文字,圖片整個丟)
    txt = re.sub(r"!\[[^\]]*\]\([^)]*\)(\{[^}]*\})?", " ", txt)
    txt = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", txt)
    # ⑥ 待補標記
    txt = re.sub(r"【[^】]*】", " ", txt)

    lines = txt.split("\n")
    if drop_tables:      # 表格整列(分隔列與內容列都不是散文)
        lines = [l for l in lines if not l.lstrip().startswith("|")]
    if drop_headings:    # 標題行:留著會讓「下一字大寫」的斷句規則黏住句子
        lines = [l for l in lines if not l.lstrip().startswith("#")]
    # 水平分隔線
    lines = [l for l in lines if not re.fullmatch(r"\s*([-*_])\1{2,}\s*", l)]
    txt = "\n".join(lines)

    # ⑦ 強調標記:`**Bold head.**` 的 `*` 不是大寫字母 → 斷句失效
    txt = re.sub(r"\*\*|\*|__|(?<=\s)_(?=\w)|(?<=\w)_(?=\s)", "", txt)
    return txt


if __name__ == "__main__":                      # 自測:雜訊不該改變散文內容
    base = "這是一段中文正文。它有一個分號；還有一個破折號——就這樣。"
    noisy = ("---\ntitle: t\n---\n" + base +
             "\n<!-- 註解；破折號——甲、乙、丙 -->\n| a | b |\n| :--- | ---: |\n| 甲；乙 | c——d |\n## 標題：測\n")
    a, b = strip_markup(base), strip_markup(noisy)
    same = a.strip() == b.strip()
    print(("✅" if same else "🔴") + " 差分自測:加入註解/表格/frontmatter/標題後,散文"
          + ("一致" if same else f"不一致\n  base ={a.strip()!r}\n  noisy={b.strip()!r}"))
