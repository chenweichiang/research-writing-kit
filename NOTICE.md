# 使用須知 · NOTICE

本專案由 Chiang Chenwei（江振維）整理並公開分享：一套用 AI 協助寫研究論文與計畫提案的
**方法**，加一個小工具箱。公開的目的是讓研究者與學生拿去用、改成自己的版本。

## 你可以

- 檢視、clone、下載、在自己的電腦上安裝與改寫本 repo 的方法文件、skill 範本與工具，
  用於你自己的研究、教學與寫作。
- 把它介紹給別人——直接給 GitHub 網址即可，不必再轉傳檔案。

## 你自己產出的東西是你的

用這套方法與工具，為你自己的論文／提案生成的稿件、骨架、聲音檔、客製 skill——
**那些都是你的**，不受本須知限制。本須知只約束「再散布這個 repo 本身」與第三方資料。

## 授權（兩種內容、兩種授權）

| 內容 | 授權 | 全文 |
|------|------|------|
| **程式碼**：`tools/` 下的 `.py`／`.sh`／`.lua`、規則與設定模板 | **MIT** | [`LICENSE`](LICENSE) |
| **方法與文件**：`method/`、`skills/`、`agents/`、`templates/`、`setup/`、`examples/`、`README.md`、`CLAUDE.md` | **CC BY 4.0**（姓名標示） | [`LICENSE-DOCS`](LICENSE-DOCS) |
| **第三方詞表**：`data/academic-vocab/` | 各清單原授權（見下） | — |

白話：程式隨便用、隨便改、可商用，保留版權聲明即可；方法文件也可以改寫、翻譯、拿去教、
拿去做自己的版本，**唯一條件是標示出處**（作者 Chiang Chenwei 與 repo 網址），改寫版請註明改自本專案。

## 引用與致謝

在論文、教材或衍生工具裡用到本方法時，請註明出處，例如：

> Chiang, C. (2026). *Research Writing Kit* (v1.3.0) [Method and toolkit].
> https://github.com/chenweichiang/research-writing-kit

## 第三方資料的授權（對所有人都有效）

`data/academic-vocab/` 收錄的學術詞表為第三方資料，非本專案原創，各有自己的授權：

- **AWL**（Academic Word List, Coxhead 2000）：**CC BY-NC-ND 3.0**——需標示出處、限非商業、
  不得改作。因為 ND 條款，**本 repo 不隨包附上 AWL**：你執行 `tools/vocab/fetch_awl.py` 從
  Victoria University of Wellington 官方頁面下載並在自己電腦上轉成 TSV（該檔已列入 .gitignore，
  不會被提交）。引用請寫 Coxhead (2000)。
- **AVL**（Academic Vocabulary List, Gardner & Davies 2014）與 **ACL**（Academic Collocation List,
  Ackermann & Chen 2013）：研究／教育用途免費，使用請標示出處（見 `data/academic-vocab/README.md`）。

**這三份詞表不在 MIT／CC BY 的範圍內**。商業用途、或要把詞表另行散布時，請自行確認各清單的授權條款；本專案不代為授權。

---

有任何使用上的問題，歡迎在 GitHub 開 issue。
