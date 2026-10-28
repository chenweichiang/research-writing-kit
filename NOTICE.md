# 使用須知 · NOTICE

English version below.

本專案由 Chenwei Chiang（江振維）整理並公開分享：一套用 AI 協助寫研究論文與計畫提案的
方法，加一個小工具箱。公開的目的是讓研究者與學生拿去用、改成自己的版本。

## 你可以

- 檢視、clone、下載、在自己的電腦上安裝與改寫本 repo 的方法文件、skill 範本與工具，
  用於你自己的研究、教學與寫作。
- 把它介紹給別人，直接給 GitHub 網址即可，不必再轉傳檔案。

## 你自己產出的東西是你的

用這套方法與工具，為你自己的論文／提案生成的稿件、骨架、聲音檔、客製 skill，
那些都是你的，不受本須知限制。本須知只約束「再散布這個 repo 本身」與第三方資料。

## 授權（兩種內容、兩種授權）

| 內容 | 授權 | 全文 |
|------|------|------|
| 程式碼：`tools/` 下的 `.py`／`.sh`／`.lua`、規則與設定模板 | MIT | [`LICENSE`](LICENSE) |
| 方法與文件：`method/`、`skills/`、`agents/`、`templates/`、`setup/`、`examples/`、`README.md`、`CLAUDE.md` | CC BY 4.0（姓名標示） | [`LICENSE-DOCS`](LICENSE-DOCS) |
| 第三方詞表：`data/academic-vocab/` | 各清單原授權 | 見下〈第三方資料〉 |
| 台灣用語詞表：`tools/zh-tw/zh_tw_terms.tsv` | MIT（部分詞條取自兩個 MIT 專案） | 見下〈第三方資料〉 |
| 英文 LLM 趨同詞表：`tools/en/en_slop_terms.tsv` | MIT（改作自 slop-forensics） | 見下〈第三方資料〉 |

白話：程式可自由使用、修改與商業使用，保留版權聲明即可；方法文件也可以改寫、翻譯、拿去教、
拿去做自己的版本，唯一條件是標示出處（作者 Chenwei Chiang 與 repo 網址），改寫版請註明改自本專案。

## 引用與致謝

在論文、教材或衍生工具裡用到本方法時，請註明出處，例如：

> Chiang, C. (2026). *Research Writing Kit* (v1.11.2) [Method and toolkit].
> https://github.com/chenweichiang/research-writing-kit

機器可讀的引用資訊在 [`CITATION.cff`](CITATION.cff)。

## 第三方資料

以下資料非本專案原創，各有自己的授權，對所有人都有效。

### 學術詞表（`data/academic-vocab/`）

- AWL（Academic Word List, Coxhead 2000）：CC BY-NC-ND 3.0，需標示出處、限非商業、
  不得改作。因為 ND 條款，本 repo 不隨附 AWL：你執行 `tools/vocab/fetch_awl.py` 從
  Victoria University of Wellington 官方頁面下載並在自己電腦上轉成 TSV（該檔已列入 `.gitignore`，
  不會被提交）。引用請寫 Coxhead (2000)。
- AVL（Academic Vocabulary List, Gardner & Davies 2014）與 ACL（Academic Collocation List,
  Ackermann & Chen 2013）：研究／教育用途免費，使用請標示出處（見 `data/academic-vocab/README.md`）。

這三份詞表不在 MIT／CC BY 的範圍內。商業用途、或要把詞表另行散布時，請自行確認各清單的授權條款；本專案不代為授權。

### 台灣用語詞表（`tools/zh-tw/zh_tw_terms.tsv`）

部分詞條取自兩個 MIT 授權專案，依 MIT 條款保留其版權聲明（每列 `source` 欄註明出處，檔頭列出上游版本）：

- zhtw-mcp（sysprog21/zhtw-mcp，`assets/ruleset.json`）：MIT License，Copyright (c) 2026 National
  Cheng Kung University, Taiwan。其兩岸詞彙資料源自 OpenCC（Apache-2.0）。
- speak-human-tw（Raymondhou0917/speak-human-tw，`references/taiwan-localization.md`）：MIT License，
  Copyright (c) 2026 Raymond Hou。

### 英文 LLM 趨同詞表（`tools/en/en_slop_terms.tsv`）

改作自 slop-forensics（sam-paech/slop-forensics，essays 領域詞表）：MIT License，
Copyright (c) 2025 Sam Paech。本專案只保留在已發表 HCI 論文裡少見的詞條，並附上參照頻率欄；依 MIT 條款保留其版權聲明。

## 問題與回饋

有任何使用上的問題，歡迎在 GitHub 開 issue；想貢獻改動請先讀 [`CONTRIBUTING.md`](CONTRIBUTING.md)。

---

# Notice (English)

This project is compiled and shared by Chenwei Chiang (江振維): a method for writing research
papers and grant proposals with an AI, plus a small toolbox. It is published so that researchers
and students can use it and make their own versions.

## What you may do

- View, clone, download, install and adapt the method documents, skill templates and tools in
  this repository on your own computer, for your own research, teaching and writing.
- Recommend it to others by giving them the GitHub URL; there is no need to forward the files.

## What you produce is yours

Manuscripts, skeletons, voice profiles and customized skills that you generate for your own
papers or proposals with this method and these tools are yours and are not covered by this
notice. This notice only concerns redistribution of the repository itself and the third-party
data it contains.

## Licences (two kinds of content, two licences)

| Content | Licence | Full text |
|---------|---------|-----------|
| Code: `.py`, `.sh` and `.lua` files under `tools/`, rule and settings templates | MIT | [`LICENSE`](LICENSE) |
| Method and documents: `method/`, `skills/`, `agents/`, `templates/`, `setup/`, `examples/`, `README.md`, `CLAUDE.md` | CC BY 4.0 (attribution) | [`LICENSE-DOCS`](LICENSE-DOCS) |
| Third-party word lists: `data/academic-vocab/` | Each list's own licence | see "Third-party data" below |
| Taiwan-Mandarin term table: `tools/zh-tw/zh_tw_terms.tsv` | MIT (some entries come from two MIT projects) | see "Third-party data" below |
| English LLM convergence-word list: `tools/en/en_slop_terms.tsv` | MIT (adapted from slop-forensics) | see "Third-party data" below |

In plain words: the code is free to use, modify and sell as long as the copyright notice is kept;
the method documents may be rewritten, translated, taught and turned into your own version, with
attribution (the author Chenwei Chiang and the repository URL) as the only condition. Please note
in a derived version that it is adapted from this project.

## Citation

When you use this method in a paper, teaching material or a derived tool, please cite it, for example:

> Chiang, C. (2026). *Research Writing Kit* (v1.11.2) [Method and toolkit].
> https://github.com/chenweichiang/research-writing-kit

Machine-readable citation metadata is in [`CITATION.cff`](CITATION.cff).

## Third-party data

The following data is not original to this project. Each item carries its own licence, which applies to everyone.

### Academic word lists (`data/academic-vocab/`)

- AWL (Academic Word List, Coxhead 2000): CC BY-NC-ND 3.0, attribution required, non-commercial,
  no derivatives. Because of the ND term the AWL is not shipped with this repository: run
  `tools/vocab/fetch_awl.py` to download it from the Victoria University of Wellington pages and
  convert it to TSV on your own computer (the file is listed in `.gitignore` and is never committed).
  Cite it as Coxhead (2000).
- AVL (Academic Vocabulary List, Gardner & Davies 2014) and ACL (Academic Collocation List,
  Ackermann & Chen 2013): free for research and educational use, with attribution (see
  `data/academic-vocab/README.md`).

None of these three lists is covered by the MIT or CC BY licence above. For commercial use, or to
redistribute a list on its own, check each list's own terms; this project cannot grant that permission.

### Taiwan-Mandarin term table (`tools/zh-tw/zh_tw_terms.tsv`)

Some entries come from two MIT-licensed projects and keep their copyright notices under the MIT
terms (the `source` column of each row names the origin; the file header lists the upstream versions):

- zhtw-mcp (sysprog21/zhtw-mcp, `assets/ruleset.json`): MIT License, Copyright (c) 2026 National
  Cheng Kung University, Taiwan. Its cross-strait vocabulary data derives from OpenCC (Apache-2.0).
- speak-human-tw (Raymondhou0917/speak-human-tw, `references/taiwan-localization.md`): MIT License,
  Copyright (c) 2026 Raymond Hou.

### English LLM convergence-word list (`tools/en/en_slop_terms.tsv`)

Adapted from slop-forensics (sam-paech/slop-forensics, the essays-domain list): MIT License,
Copyright (c) 2025 Sam Paech. This project keeps only the terms that are rare in published HCI
papers and adds a reference-frequency column; the copyright notice is kept under the MIT terms.

## Questions and feedback

For questions about use, open an issue on GitHub. To contribute a change, read
[`CONTRIBUTING.md`](CONTRIBUTING.md) first.
