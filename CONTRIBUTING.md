# Contributing

Issues and pull requests are welcome, in Traditional Chinese or English.

## Reporting a problem

Open an issue with the command you ran, what you expected, what happened (the full error if there is one), your operating system and Python version, and whether you set the kit up in lite or full mode. For a wrong result from a checking tool, a short text that reproduces it helps more than a description.

## Term table (Taiwan Mandarin)

`tools/zh-tw/zh_tw_terms.tsv` decides what `zh_localize.py` flags. To add, remove or narrow a term, open an issue with the term, the context where it goes wrong, and a source such as the National Academy for Educational Research term database (樂詞網) or usage counts from published Taiwanese papers. The table is synchronised from the maintainer's copy, so changes are applied there rather than merged directly into the file.

## Pull requests

Keep each pull request to one change. Before opening it, run the tests and the release check:

```bash
python -m pip install pytest pyyaml numpy pillow
python -m pytest tests -q
python tools/dev/release_check.py --base origin/main
```

CI runs both on every pull request. The release check rejects em dashes and mainland-Mandarin terms in added lines, e-mail addresses and home-directory paths anywhere, and skill or agent files whose frontmatter does not parse.

Conventions:

- Tools use the Python standard library where they can. A new dependency belongs in the tool's own docstring and in `setup/TOOLS.md`, with what happens when it is missing.
- The core (`method/`, `skills/`, `agents/`, `templates/`) stays language-neutral. Anything specific to Traditional Chinese or Taiwan goes under `setup/addons/zh-tw/` or `tools/zh-tw/`.
- New tools need a test in `tests/` and a row in the tool tables of both `README.md` and `README.en.md`.
- Changes to the method go in `CHANGELOG.md` as well, in both languages.

---

# 參與貢獻

歡迎用繁體中文或英文開 issue、送 pull request。

## 回報問題

開 issue 時請附上執行的指令、預期結果、實際結果（有錯誤訊息請貼完整）、作業系統與 Python 版本，以及安裝時選的是 lite 還是 full 模式。檢查工具判錯時，一小段能重現的文字比描述更有用。

## 台灣用語詞表

`tools/zh-tw/zh_tw_terms.tsv` 決定 `zh_localize.py` 會標出哪些詞。要新增、刪除或限縮詞條，請開 issue，寫明詞彙、在什麼脈絡下判錯，並附出處，例如國家教育研究院樂詞網，或台灣已發表論文的使用次數。詞表由維護者的版本同步過來，修改會在那邊套用，不直接合併進這個檔。

## Pull request

一個 pull request 只做一件事。送出前請跑測試與發版檢查：

```bash
python -m pip install pytest pyyaml numpy pillow
python -m pytest tests -q
python tools/dev/release_check.py --base origin/main
```

CI 在每個 pull request 都會跑這兩項。發版檢查會擋：新增行裡的長破折號與大陸用語、任何位置的電子郵件地址與家目錄路徑，以及 frontmatter 解析不了的 skill 與 agent 檔。

慣例：

- 工具盡量只用 Python 標準函式庫。新增的相依套件要寫在該工具的 docstring 與 `setup/TOOLS.md`，並說明沒裝時會怎樣。
- 核心（`method/`、`skills/`、`agents/`、`templates/`）維持語言中立，繁體中文或台灣專屬的內容放 `setup/addons/zh-tw/` 或 `tools/zh-tw/`。
- 新工具要在 `tests/` 加測試，並在 `README.md` 與 `README.en.md` 的工具表各加一列。
- 方法有改動時，`CHANGELOG.md` 中英文都要寫。
