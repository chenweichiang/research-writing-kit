# 研究寫作套件 · Research Writing Kit

**版本 `v1.3.0`**（2026-08）· 專案頁：<https://course.interaction.tw/research-writing-kit/>

**English → [README.en.md](README.en.md)**

> 一套用 AI 協助寫**研究論文與計畫提案**的方法，而且它會**自己安裝、自己客製**。
> 你不用懂 AI、不用會設定。把資料夾交給你的 Claude，它會問你幾個問題，再幫你把
> 適合你的工具建好。

**English tl;dr:** A method for AI-assisted academic writing that installs and
customizes itself. Open this folder in Claude Code and say *"Read CLAUDE.md and set
me up."* Your Claude interviews you, then generates writing skills tailored to your
field, language, and voice. See `CLAUDE.md` (the installer) and `method/` (the method).

---

## 這是什麼

這不是那種「寫好給你貼上去」的模板。它是一套**方法**，加一個會自我安裝的小工具箱。幾個原則：

- **你擁有想法與論證，AI 負責跑腿**：找文獻、查證引用、架論證骨架、寫成稿、還自己檢查。
- **先架骨架再寫字**：不從空白頁硬擠出稿（那種硬擠就是「AI 味」的來源），先把論證結構立好，再照著它寫成文字。
- **絕不編造引用**：每一條文獻都真的抓下來、確認方向對。查不到就標「未驗證」，不假裝。
- **像你的聲音**：用你的母語寫時，對齊你自己的文風，不磨成通用 AI 腔。
- **誠實內建**：效果量＋信賴區間（不只 p 值）、資料留在你電腦、交稿前去 AI 味、乾淨二審。

---

## 怎麼用

這套方法最終在**你自己電腦的 Claude Code** 上跑，這樣資料才留在本機、工具才跑得動。
依你現在手上有什麼，選一條路開始：

### 情況 A ｜ 你電腦上已經有 Claude Code

1. **拿到這個資料夾**：這是公開 repo，不用登入。有 git 的話
   `git clone https://github.com/chenweichiang/research-writing-kit.git`；
   不想裝 git 也可以在 GitHub 頁面按綠色 **Code → Download ZIP** 解壓，只是之後沒辦法
   `git pull` 一鍵更新。放哪裡都行。
2. **在資料夾裡打開 Claude Code**：開終端機，`cd` 進到這個資料夾，輸入 `claude`。
3. **貼這一句話**：
   > **「讀 CLAUDE.md，幫我設定。」**（英文：`Read CLAUDE.md and set me up.`）

### 情況 B ｜ 你現在在 claude.ai 網頁版，還沒有 Claude Code

把這個 repo 連給網頁版的 Claude（用 GitHub 連接器），跟它說 **「讀 CLAUDE.md，幫我設定」**。
它就會**一步步帶你把 Claude Code 裝到你電腦，再把資料夾搬過去**（細節見
[`setup/WEB.md`](setup/WEB.md)）。裝好後回到上面**情況 A 的第 2 步**。

> ⚠️ Claude Code 需要**付費的 Claude 方案**（Pro／Max／Team，或 API 計費）。**免費的
> claude.ai 帳號不能用**。網頁版的 Claude 會在動手裝之前先提醒你這件事。

---

### 設定好之後，你的 Claude 會做這三件事
1. **問你幾個問題**：你寫什麼、用什麼語言、想投哪、有沒有自己的舊稿可以讓它學你的文風。
2. **幫你生出專屬工具**：照你的答案，把「協作寫作」「投稿前檢查」等 skill 客製好、裝進你的
   Claude。
3. **教你實際會用到的幾句話**，然後你就可以開始了。

### 之後每天怎麼用
在放論文的資料夾裡開 Claude Code，用平常講話的方式說要做什麼（你也可以直接打 `/skill名`）：

| 你打這句 | Claude 幫你做 | 對應的 skill／工具 |
|----------|---------------|-------------------|
| **「幫我寫這篇論文／提案」** | 協作寫作：找文獻、架論證骨架、寫成稿、自己檢查 | `/co-author` |
| **「幫我檢查這篇再投」** | 投稿前的品質與格式檢查（五層） | `/paper-review` |
| **「幫我把這些引用的 PDF 收齊」** | 收集並查證參考文獻 | `/fetch-refs` |
| **「這些引用真的撐得住我寫的話嗎？」** | 逐句對照 PDF 原文判定引用方向、DOI 權威查驗 | `/verify-citations`（＋`citation-skeptic` 二審） |
| **「誰引用了這篇？有沒有我漏掉的後續研究」** | 引用滾雪球：從一篇（或整份書目）長出該讀而未讀的文獻清單 | `/fetch-refs` → `tools/refs/snowball.py` |
| **「審稿意見回來了，幫我回」** | 逐點回應：拆解意見→逐點裁定→修訂對照→回應信→交付前完整性驗證 | `/rebuttal` → `tools/rebuttal/check_response.py` |
| **「我這篇短文要擴寫成期刊全文」** | 逆向盤點入線，並盤點文字回收與揭露措辭（擴寫本質上就是重用） | `/co-author` Phase 0.5 |
| **「我要再投一個地方，可以吧？」** | 查投稿狀態表，確認同一份稿件沒有同時在別處審查中 | `tools/submissions/check_submissions.py` |
| **「這張圖印成黑白會不會看不懂？」** | 圖表色覺可及性：色盲模擬＋灰階對比，並產生模擬圖給你看 | `/paper-review` → `tools/figures/figure_a11y.py` |
| **「別再犯同樣的錯」「改 A 又弄壞 B」** | 文件回歸：把抓到的錯寫成一條常駐檢查，改完全庫重掃，復發就擋下 | `/doc-regress` → `tools/regress/regress.py` |
| **「有沒有哪篇被撤稿了？」** | 撤稿掃描：整份書目對 Crossref＋OpenAlex 查撤稿，每次交付前重跑 | `tools/refs/retraction_scan.py` |
| **「這句沒掛引用，站得住嗎？」** | 無引用宣稱掃描：找出沒有引用的量化／因果／最高級句子，逐筆補引用、指出自家資料、或降級措辭 | `tools/claims/uncited_claims_scan.py` |
| **「稿裡的數字跟分析結果對得上嗎？」** | 數字帳本勾稽：每個數字回溯到產生它的運算；改數字先更帳本再改稿，回歸檢查擋舊值復發 | `/doc-regress` §3.5 |
| **「把這篇排成投稿 PDF」「中文 PDF」** | 依場域模板排版；第二語言稿連同回譯稿成對交付 | `/build-pdf` |
| **「投出去之前還缺哪些聲明？」** | 投稿聲明六件套：AI 使用揭露／研究倫理／資料可得性／作者貢獻／利益衝突／預註冊 | `/co-author` Phase 6-2a、`/paper-review` 第 7 項 |

> 預設走**最簡單的模式**：只要 Claude ＋ 網路，什麼都不用安裝。之後真的需要更強的工具
> （本機統計、文獻庫、語言檢查）再一次加一個就好。

---

## 隱私

- 這個 repo 裡只有**方法與工具**，沒有任何人的稿件或資料。

## 授權

- **程式碼**（`tools/`）：MIT——隨便用、隨便改、可商用，保留版權聲明即可（[`LICENSE`](LICENSE)）。
- **方法與文件**（`method/`、`skills/`、`agents/`、`templates/`、`setup/`、README）：CC BY 4.0——可改寫、翻譯、教學、做自己的版本，**唯一條件是標示出處**（[`LICENSE-DOCS`](LICENSE-DOCS)）。
- **第三方詞表**（`data/academic-vocab/`）：隨包的 AVL、ACL 為研究／教學免費使用、需標示出處；AWL 是 CC BY-NC-ND（不得改作），**不隨包**，由你用 `tools/vocab/fetch_awl.py` 自行抓取到本機。都不在上面兩種授權範圍內。
- 引用格式與細則見 [`NOTICE.md`](NOTICE.md)。
- 方法本身要求：**未發表的稿件與研究原始資料永遠留在你自己的電腦**，不上傳雲端、不丟公開的
  AI 偵測器。你生成的個人設定（文風檔、投稿筆記、骨架）也不會被這個 repo 收走
  （見 `.gitignore`）。

---

## 資料夾裡有什麼（完整清單）

| 位置 | 內容 |
|------|------|
| `CLAUDE.md` | **安裝器**：你的 Claude 讀這個來訪談你、生成你的專屬設定。 |
| `NOTICE.md` | 分享條件與第三方資料授權。 |
| `method/` | **方法本體**四份：`PHILOSOPHY.md`（心法）、`IRON-RULES.md`（鐵則）、`WORKFLOW.md`（八個 Phase 的完整流程）、`ARGUMENTATION.md`（論證工法，內部診斷用）。 |
| `skills/` | 七個 skill 範本（見下表）。 |
| `agents/` | 兩個 subagent 範本（見下表）。 |
| `tools/` | 十六支本機腳本＋輔助檔＋模板（見下表），說明在 `tools/README.md`。 |
| `templates/` | 四份空白檔：`VOICE_PROFILE.template.md`（文風檔）、`venue-notes.template.md`（投稿場域筆記）、`skeleton.template.md`（論證骨架）、`voice_rules.template.json`（聲音硬規則）。 |
| `data/academic-vocab/` | 開放學術詞表：隨包兩份（`avl_core_words.tsv`、`acl_collocations.tsv`），第三份 `awl_families.tsv` 由 `tools/vocab/fetch_awl.py` 在你電腦上產生（授權不允許隨包）。投稿前檢查的用字層拿來當錨點，不是自動替換；授權見 `NOTICE.md`。 |
| `examples/skeleton.example.md` | 一份填好的骨架範例，讓 Claude 有具體參照。 |
| `setup/` | `LITE.md`（零安裝模式）、`TOOLS.md`（選配工具與降級對照）、`INTERVIEW.md`（面談問法）、`WEB.md`（從 claude.ai 網頁版上手）、`addons/zh-tw/README.md`（繁中在地化包）。 |

### 七個 skill

安裝後，用講的或直接打 `/名稱` 都會觸發。

| skill | 做什麼 | 會用到的工具 |
|-------|--------|--------------|
| `co-author` | 從無到有的協作寫作（論文與提案）：骨架→查證→寫稿→交付前關卡；也走既有稿改寫、轉投、擴寫 | 交付前掃描三支（撤稿／無引用宣稱／回歸）、`check_submissions.py`、兩個 subagent |
| `paper-review` | 投稿前五層檢查：機械層→用字→語言→邏輯與審稿視角→交付完整性；只檢查不改稿 | 中文三支、`lt_check.sh`、`ai_style_diag.py`、`figure_a11y.py`、`uncited_claims_scan.py`、（選配）R `statcheck`＋`scrutiny` |
| `fetch-refs` | 把書目的 PDF 收齊、逐篇確認內容真的相符、歸檔＋清單；含引用滾雪球 | `snowball.py`、線上 API |
| `verify-citations` | 逐句對照 PDF 判定引用是否被原文支撐、方向對不對；DOI 權威查驗；撤稿掃描 | `retraction_scan.py`、`citation-skeptic` 二審、（選配）MinerU |
| `rebuttal` | 審稿回應：拆點→裁定→落實修訂→回應信→完整性驗證 | `check_response.py`＋三份模板、`de-cadencing-scholar`、（選配）`latexdiff` |
| `doc-regress` | 抓到一次錯就寫成常駐檢查；數字帳本；死規則健檢 | `regress.py`、`dead_rule_check.py`＋兩份模板 |
| `build-pdf` | 依場域模板排版成 PDF；第二語言稿連同回譯稿成對交付；繁中用 Typst 配方 | Typst 或 Quarto／LaTeX |

### 兩個 subagent

| agent | 做什麼 | 何時派 |
|-------|--------|--------|
| `de-cadencing-scholar` | 母語學者視角挑掉英文稿「一看就是 AI 潤過」的節奏痕跡並改寫 | 英文稿交付前；審稿回應信交付前 |
| `citation-skeptic` | 對被標記「引用可能有問題」的判定做校準二審：預設引用正確，只有 PDF 逐字直接矛盾才維持指控 | `verify-citations` 有 flag 時 |

### 隨包工具（`tools/`，全部）

| 檔案 | 用途 | 額外要裝什麼 |
|------|------|--------------|
| `common/md_prose.py` | 共用模組：把 markdown／LaTeX 版面語法（frontmatter、表格、註解、code）剝掉只留散文，四支文風工具都靠它；不直接執行 | — |
| `zh-tw/zh_localize.py` | 陸用語→台灣用語、台／臺一致性（只報不改） | 不用 |
| `zh-tw/zh_ai_style.py` | 中文 AI 句法指紋：破折號、三連並列、趨同詞、句長節奏；可對照你自己的親筆語料 | 不用 |
| `zh-tw/voice_lint.py` | 你自己的聲音硬規則（吃 `voice_rules.json`），交稿前守門，不乾淨不放行 | 不用 |
| `en/lt_check.sh` | 英文文法＋美英拼字一致性（離線 LanguageTool）；有 n-gram 資料會自動加掛易混詞偵測 | `brew install languagetool pandoc` |
| `en/lt_strip_noprose.lua` | `lt_check.sh` 用的 pandoc 濾鏡，剝掉非散文再送檢；不直接執行 | （隨 pandoc） |
| `en/ai_style_diag.py` | 英文 AI 指紋：對照你領域已發表論文語料的百分位；自動排除自家草稿與模板檔以免污染基線 | 自備語料；讀 PDF 需 `pdftotext`（`brew install poppler`） |
| `figures/figure_a11y.py` | 圖表色覺可及性：三種色盲模擬＋灰階對比，寫出模擬圖供目檢 | `pip install numpy pillow`（PDF 另需 `pymupdf`） |
| `refs/snowball.py` | 引用滾雪球：誰引用了這篇／這篇引了誰／相近研究，多種子聚合排序 | 不用（需網路） |
| `refs/retraction_scan.py` | 撤稿掃描：`.bib` 或 DOI 清單對 Crossref 更新關係＋OpenAlex `is_retracted` 雙源查核；無 DOI 條目另列不算已掃 | 不用（需網路） |
| `claims/uncited_claims_scan.py` | 沒掛引用的量化／因果／最高級宣稱（`.md`／`.tex`／`.qmd`，中英通吃）；逐筆裁決後可加豁免註記 | 不用 |
| `regress/regress.py` | 文件回歸：照專案的 `regress.json` 掃全庫；內建懸空引用、個資、待辦、舊值復發、歸屬缺漏等規則，專案自訂規則用 `--extra my_rules.py` | 不用 |
| `regress/dead_rule_check.py` | 規則健檢：哪條規則已永遠不會觸發（錨點文字改掉了） | 不用 |
| `regress/rules.template.json`、`regress/numbers-ledger.template.md` | 回歸規則設定檔與數字帳本的空白模板 | — |
| `rebuttal/check_response.py` | 回應信完整性：每點都答了嗎／說要改的真的改了嗎／不接受的有沒有依據 | 不用 |
| `rebuttal/points.template.tsv`、`revisions.template.tsv`、`response-letter.template.md` | 審稿意見拆點表、修訂對照表、回應信模板 | — |
| `submissions/check_submissions.py` | 一稿多投防護＋投稿狀態總覽（同一份稿件不得同時在兩處審查） | 不用 |
| `submissions/SUBMISSIONS.template.tsv` | 投稿狀態表模板 | — |
| `vocab/fetch_awl.py` | 從 Victoria University of Wellington 官方頁面抓 Coxhead 的 AWL 詞表，轉成 `data/academic-vocab/awl_families.tsv`（AWL 授權不得改作，所以 kit 不隨包、請你自己抓；跑一次即可） | 不用（需網路） |

---

## 安裝後，你的電腦上會多出什麼

安裝器（`CLAUDE.md`）會問你「只給這篇，還是全部」，然後：

| 東西 | 放哪 | 說明 |
|------|------|------|
| 七個 skill | `~/.claude/skills/<名稱>/SKILL.md`（全域）或你論文資料夾的 `.claude/skills/`（單一專案） | **照你的答案改寫過**，不是原檔複製；領域、語言、場域、模式都填進去了 |
| 兩個 subagent | `~/.claude/agents/` 或專案 `.claude/agents/` | 寫英文或要查引用的人才裝 |
| 你的 `CLAUDE.md` 多一段 | `~/.claude/CLAUDE.md` 或專案 `CLAUDE.md` | 記你的領域、語言、場域、模式（lite／full）、文風檔位置，以及 **kit 的路徑（`KIT PATH`）**——全機只記這一處，搬 kit 只改這一行 |
| `voice-samples/` | 你的專案或家目錄 | **只放你親筆寫的文章**（給了舊稿才有）；文風工具的 `--authored` 指這裡，絕不指向混有 AI 稿的資料夾 |
| `VOICE_PROFILE.md`、`voice_rules.json` | 同上 | 從你的舊稿抽出的文風描述與硬規則；`voice_lint.py` 吃後者 |

沒安裝的選配工具，生成的 skill 會寫成「若已安裝才用」，不會假裝它存在。

---

## 跑起來後，你的論文專案裡會長出的檔案

這些都是**你的**檔案（在你的論文資料夾，不在這個 repo），建議連同稿子一起版控。

| 檔案 | 誰建的 | 用途 |
|------|--------|------|
| `skeleton.md` | `co-author` | 論證骨架＝唯一權威；每個 Phase 結束回寫 `## Progress`，新 session 先讀它 |
| `venue-notes.md` | `co-author` | 目標場域當年度的格式、字數、審查慣例、AI 揭露政策、預印本政策 |
| `search-log.md` | `co-author` | 檢索留痕：用了哪些資料庫、查詢字串、日期、納入排除——審稿人問「為何漏了 X」時要答得出來 |
| `ADJUDICATED.md` | `co-author`／`paper-review`／`doc-regress` | 已裁定事項：「看起來錯、查過、其實對」的清單，之後的檢查不重問 |
| 文獻 PDF 資料夾＋清單檔 | `fetch-refs` | 依 `NN [作者 年] 標題.pdf` 命名；清單記找到什麼、沒找到什麼、驗證層級（verified／LOW-CONFIDENCE）、自署著作標記 |
| `snowball.csv` | `snowball.py` | 滾雪球結果（可自訂檔名） |
| `regress.json`、`my_rules.py`（選） | `doc-regress` | 回歸規則設定與專案自訂規則；隨稿版控 |
| 數字帳本（照 `numbers-ledger.template.md`） | `doc-regress`／`co-author` Phase 3 | 稿中每個數字回溯到產生它的運算；重跑分析→先更帳本→再改稿 |
| `rebuttal/points.tsv`、`rebuttal/revisions.tsv`、`rebuttal/response-letter.md` | `rebuttal` | 意見拆點、修訂對照、回應信 |
| `<圖檔名>_a11y/`（`protan.png`、`deutan.png`、`tritan.png`、`grayscale.png`） | `figure_a11y.py` | 色盲與灰階模擬圖，**一定要開來看**，數字只是證據不是判決 |
| 撤稿／無引用宣稱掃描的 JSON 報告（選） | `retraction_scan.py --out`、`uncited_claims_scan.py --json` | 給 CI 或留檔用；平常看終端輸出即可 |
| 回譯稿＋兩份 PDF | `co-author`／`build-pdf` | 第二語言稿的簽核入口：原稿 PDF 與回譯 PDF 成對交付 |
| `SUBMISSIONS.tsv` | `check_submissions.py` | **放在所有論文專案之上一層**（一份台帳管全部；`SUBMISSIONS_TSV` 環境變數指向它）；一稿多投在單一專案資料夾裡看不出來 |

> 這個 repo 的 `.gitignore` 排除 `VOICE_PROFILE.md`／`venue-notes.md`／`skeleton.md`，是為了**不讓任何人的個人設定回流到 kit**；在你自己的論文專案裡，這些檔案該跟著稿子一起版控。

---

## 會用到哪些外部程式與服務（完整對照）

> 一句話版本：**只要 Claude Code 就能開始**。其他都是「有了更好」，而且 Claude 會在
> 你真的需要時才建議裝，一次一個。

### 一定需要的

| 工具 | 用途 | 怎麼取得 |
|------|------|----------|
| **Claude Code** | 整套方法的執行者：訪談你、找文獻、架骨架、寫稿、自我檢查 | [claude.com/claude-code](https://claude.com/claude-code)（需付費 Claude 方案：Pro／Max／Team 或 API 計費） |
| **Python 3** | 跑隨包附的本機檢查工具 | macOS 要先裝 Xcode Command Line Tools（`xcode-select --install`）或 `brew install python`；Linux 多數發行版內建；Windows 到 python.org 抓安裝檔 |
| **git** | 下載與更新這個 repo（`git clone` / `git pull`） | macOS 裝 Xcode Command Line Tools 就有；或用 GitHub 頁面的 Download ZIP（之後無法一鍵更新） |

### 選配的本機程式（哪個功能用到、怎麼裝）

| 程式 | 哪裡用到 | 怎麼裝 |
|------|----------|--------|
| **LanguageTool**＋**pandoc** | `lt_check.sh` 英文文法（`paper-review` 第 3 層） | `brew install languagetool pandoc`；n-gram 資料選配，放到 `$LT_NGRAMS` |
| **poppler**（`pdftotext`） | `ai_style_diag.py` 讀 PDF、`verify-citations` 讀文獻 PDF | `brew install poppler` |
| **numpy**、**Pillow**（＋**pymupdf**） | `figure_a11y.py` | `pip install numpy pillow`（PDF 圖另加 `pymupdf`） |
| **MinerU** | 掃描檔／中文 PDF 抽成乾淨文字（`verify-citations`） | `uv tool install mineru` |
| **R**＋`statcheck`、`scrutiny` | `paper-review` 第 1 層重算 p 值、GRIM 查平均數可能性（沒裝就退回手算） | 裝 R 後 `install.packages(c("statcheck","scrutiny"))` |
| **R**＋`DeclareDesign` | `co-author` Phase 3.5 設計診斷（看 coverage 不只看 power） | `install.packages("DeclareDesign")` |
| **R** 或 **Python** 統計 | 本機統計分析：混合模型（`lme4`／`afex`）、序數 Likert（`ordinal::clmm`）、事後比較與效果量；分流規則見 `setup/TOOLS.md` | 資料全程留在你電腦；數值雷區見 `setup/TOOLS.md` |
| **R** 貝氏三路 | 公式寫得出的階層模型→`brms`；「無差異」結論要 BF01→`BayesFactor`；**離散潛在變數／混合模型／自訂 sampler／JAGS 舊模型移植→`nimble`**（BUGS 語法，Stan 寫不出離散參數）；三者都要報先驗與收斂診斷 | `install.packages(c("brms","BayesFactor","nimble"))`；`brms` 另需 CmdStan 或 rstan |
| **Harper** | 英文毫秒級第一遍文法（存檔就報；LanguageTool 仍是主力） | 編輯器外掛或 CLI，離線 |
| **autocorrect** | 中文全半形、盤古空格自動整理 | `brew install autocorrect` |
| **Typst** 或 **Quarto**／**LaTeX** | `build-pdf` 排版；繁中走 Typst 配方（`setup/addons/zh-tw/`） | 依場域官方模板選；`latexdiff` 給 `rebuttal` 做修訂對照 |
| **Jupyter** | 可重跑的分析筆記本 | `pip install jupyterlab` |
| 機構圖書館 **VPN** | 付費牆內的文獻全文（`fetch-refs`） | 依你的機構 |
| 本機 **RAG** | 自己文獻庫的語意檢索（哪篇、哪頁） | `setup/TOOLS.md` 給方向，不給實作 |

### Claude 與工具會連的線上服務（免費、不用裝、不用註冊）

| 服務 | 哪裡用到 | 送出什麼 |
|------|----------|----------|
| **Crossref** | `retraction_scan.py`（撤稿更新關係）、`verify-citations` DOI／書目查驗 | 只送 DOI |
| **OpenAlex** | `retraction_scan.py`（`is_retracted`）、`snowball.py`、無 DOI 條目的標題補查 | DOI 或標題 |
| **Semantic Scholar** | `snowball.py` 後備線、引用補查 | DOI 或標題 |
| **Unpaywall**、**arXiv** | `fetch-refs` 抓開放取用的 PDF | DOI |

**稿件內容從不送出**——線上服務只拿到 DOI、標題、作者這類書目資料；未發表稿件與研究原始資料永遠留在你的電腦。

### 刻意不收的環節

原作者的工具鏈還有幾個環節存在，但**不出貨**——不是忘了，是它們超出「論文與提案」的範圍，或綁死在某台機器上：

- **present-video**（發表影片一條龍：TTS 克隆本人聲音／Whisper 聽寫驗證／本機生圖）：超出論文與提案的範圍，且每一段都要自架模型。
- **paper-healthcheck**：檢查的是作者**本機工具鏈本身**有沒有斷、有沒有新版，不是檢查稿件；你的工具鏈長什麼樣它不知道。
- **contradiction_scan／backfill_from_lit**（庫裡有沒有人反駁我／缺的 PDF 先從本機補）：需要本機文獻全文索引與本機 LLM 做極性判斷；`setup/TOOLS.md` 只給方向，不給實作。
- **zh_term_check**（整篇術語譯名對照樂詞網）：需要樂詞網資料庫，得自己下載建庫（bring your own）；單詞查詢請你的 Claude 上網查即可。

---

## 給進階使用者
所有 skill 都是純 Markdown 的 `SKILL.md`，Claude Code 會自動辨識。想手動掛成全域 skill，
把 `skills/<name>/` 複製或 symlink 到 `~/.claude/skills/` 即可；`agents/` 的兩個 subagent
範本同理，掛到 `~/.claude/agents/`（或專案的 `.claude/agents/`）。但還是建議讓 `CLAUDE.md`
的安裝流程幫你客製，不要照抄原版。

兩個原則：**乾淨二審只給檔案路徑**（不餵主對話的寫稿史，否則盲點共享）；**終審與引用二審是判斷活，
用你的主力模型，別為省錢降級**。機械層的掃描（撤稿、無引用宣稱、回歸）不需要模型，直接跑腳本。

---

## 版本紀錄

- **v1.3.0**（2026-08-25）：**補上交付前最容易漏、事後最難救的幾道關卡。** 新增第七個 skill
  `doc-regress`（抓到一次錯就寫成一條常駐檢查，改 A 不再弄壞 B；規則隨稿版控，含數字帳本模板
  `tools/regress/numbers-ledger.template.md` 與 `regress.py`／`dead_rule_check.py`）；新增
  `tools/refs/retraction_scan.py`（撤稿掃描，Crossref＋OpenAlex 雙源，**每次交付重掃**——撤稿持續
  發生，上次乾淨不代表這次乾淨）與 `tools/claims/uncited_claims_scan.py`（沒掛引用的量化／因果／
  最高級宣稱；查引用只看有引用標記的句子，這是它碰不到的盲區）。協作寫作補鐵則「檔案是唯一權威」
  （每個 Phase 回寫進度、壓縮後先重讀檔案再動手）、Phase 1A 檢索留痕、Phase 3.5 設計診斷（判
  coverage 不只 power；有偏設計加人更糟；單組前後測要加對照或降級為非因果）、Phase 6 交付前
  清單（撤稿／無引用宣稱／數字帳本勾稽／圖表溯源／投稿聲明六件套／終審附 `ADJUDICATED.md`）、
  Phase 7「先更帳本再改稿」。投稿前檢查補 Step 0 讀 `ADJUDICATED.md`（已裁定不重問）、質性
  四項與報告準則（COREQ／SRQR／TREND／CONSORT／PRISMA）、檢索策略、六件套、無引用宣稱掃描；
  查引用補逐子句判定、引述接地、嚴重度加權、撤稿；收文獻補三條；審稿回應掛英文去節奏複查；
  繁中包補 Typst。文風工具（中英四支）同步修正一批量測 bug。方法文件同步：流程改為 8 phase、
  鐵則補統計細則（ART 只限連續 DV、單題 Likert 走序數模型、SESOI 設計期宣告、貝氏三路分流）、
  論證工法每招補「何時別用」與實證論文手藝、`setup/TOOLS.md` 補數值雷區與 Harper／autocorrect。AWL 詞表不再隨包（CC BY-NC-ND 的 ND 條款），改由 `tools/vocab/fetch_awl.py` 抓取。README 改成完整清單：七個 skill 的名字與觸發句、`tools/` 全部檔案、安裝後電腦上會多出什麼、論文專案裡會長出哪些檔案、外部程式與線上服務各自被誰用到、送出什麼資料。
- **v1.2.0**（2026-08-24）：**修掉一批會給錯數字的量測 bug**——文風診斷工具（中英文四支）
  把 markdown 版面語法當成散文標點在數：YAML frontmatter 與表格分隔列被當破折號、HTML
  註解裡的字被當正文、pandoc 多鍵引用的分號被當文風、粗體標題讓斷句規則失效而把兩三句
  黏成一句。實測一份真實投稿：平均句長 44.22 詞（第 99 百分位）→ 26.52 詞（第 53 百分位）
  ——**照舊版數字去修，會把本來正常的句子改壞**。剝除規則抽成 `tools/common/md_prose.py`
  中英共用。另修 `snowball.py` 的 Semantic Scholar 後備線從未被觸發（撞每日額度時，
  第一個呼叫就 429，整顆種子被跳過）。
  新增：`rebuttal` skill（審稿回應逐點裁定＋修訂對照＋完整性驗證）、投稿狀態表與一稿多投
  防護、圖表色覺可及性檢查；協作寫作補 Phase 8「接受之後」（校樣／版權／傳播）、文字回收
  揭露、預印本政策查核。
- **v1.1.0**（2026-08）：投稿前檢查加入統計數字重算（statcheck 重算 p 值＋GRIM 查
  平均數可能性，裝了 R 才啟用，沒裝就退回手算）；新增引用滾雪球工具 `tools/refs/snowball.py`
  （零安裝）；查引用支援掃描檔／中文 PDF（選配 MinerU）；英文文法檢查可自動加掛 n-gram
  易混詞偵測（選配）；新增 `agents/` 兩個 subagent 範本：英文交付前的去 AI 節奏複查、
  引用查驗二審。
- **v1.0.0**（2026-07）：初版——方法本體、五個 skill 範本、中英文檢查工具、自我安裝流程。
