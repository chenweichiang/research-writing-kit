# 研究寫作套件 · Research Writing Kit

[![版本](https://img.shields.io/github/v/tag/chenweichiang/research-writing-kit?label=version&sort=semver&color=blue)](https://github.com/chenweichiang/research-writing-kit/tags) [![最近更新](https://img.shields.io/github/last-commit/chenweichiang/research-writing-kit/main?label=updated&color=green)](https://github.com/chenweichiang/research-writing-kit/commits/main) [![程式 MIT](https://img.shields.io/badge/code-MIT-lightgrey)](LICENSE) [![文件 CC BY 4.0](https://img.shields.io/badge/docs-CC%20BY%204.0-lightgrey)](LICENSE-DOCS)

**版本 `v1.11.4`**（2026-10-29）· 專案頁：<https://course.interaction.tw/research-writing-kit/>

**English → [README.en.md](README.en.md)**

> 一套用 AI 協助寫研究論文與計畫提案的方法，而且它會自己安裝、自己客製。
> 你不用懂 AI、不用會設定。把資料夾交給你的 Claude，它會問你幾個問題，再幫你把
> 適合你的工具建好。

**English tl;dr:** A method for AI-assisted academic writing that installs and
customizes itself. Open this folder in Claude Code and say *"Read CLAUDE.md and set
me up."* Your Claude interviews you, then generates writing skills tailored to your
field, language, and target journals. See `CLAUDE.md` (the installer) and `method/` (the method).

---

## 這是什麼

這是一套寫作方法，加一個會自我安裝的小工具箱：安裝後，你的 Claude 照這套方法找文獻、架論證、寫稿、自我檢查。幾個原則：

- **你擁有想法與論證，AI 負責跑腿**：找文獻、查證引用、架論證骨架、寫成稿、還自己檢查。
- **先架骨架再寫字**：不從空白頁硬擠出稿（那種硬擠就是「AI 味」的來源），先把論證結構立好，再照著它寫成文字。
- **引用要對過原文才能用**：方法規定每一條文獻都要真的抓下來、確認方向對，才能寫進稿子；查不到的標「未驗證」，不假裝。
- **論文像你的領域，信件像你**：論文、計畫書、申請書拿同領域已發表論文當準繩，稿子的每項語言特徵要落在真人論文的常見區間內，不磨成通用 AI 腔，也不套個人口吻；你自己的文風只用在信件與自述。
- **誠實內建**：效果量＋信賴區間（不只 p 值）、稿件與資料除了 Claude 本身不交給其他線上服務、交稿前去 AI 味、乾淨二審。

---

## 怎麼用

這套方法最終在你自己電腦的 Claude Code 上跑，這樣檔案才存在你手上、工具才跑得動。
依你現在手上有什麼，選一條路開始：

### 情況 A ｜ 你電腦上已經有 Claude Code

1. **拿到這個資料夾**：這是公開 repo，不用登入。有 git 的話
   `git clone https://github.com/chenweichiang/research-writing-kit.git`；
   不想裝 git 也可以在 GitHub 頁面按綠色「Code → Download ZIP」解壓，只是之後沒辦法
   `git pull` 一鍵更新。放哪裡都行。
2. **在資料夾裡打開 Claude Code**：開終端機，`cd` 進到這個資料夾，輸入 `claude`。
3. **貼這一句話**：
   > **「讀 CLAUDE.md，幫我設定。」**（英文：`Read CLAUDE.md and set me up.`）

### 情況 B ｜ 你現在在 claude.ai 網頁版，還沒有 Claude Code

把這個 repo 連給網頁版的 Claude（用 GitHub 連接器），跟它說「讀 CLAUDE.md，幫我設定」。
它就會一步步帶你把 Claude Code 裝到你電腦，再把資料夾搬過去（細節見
[`setup/WEB.md`](setup/WEB.md)）。裝好後回到上面情況 A 的第 2 步。

> ⚠️ Claude Code 需要付費的 Claude 方案（Pro／Max／Team，或 API 計費）。**免費的
> claude.ai 帳號不能用**。網頁版的 Claude 會在動手裝之前先提醒你這件事。

---

### 設定好之後，你的 Claude 會做這三件事
1. 問你幾個問題：你寫什麼、用什麼語言、想投哪、能不能收一批同領域已發表的論文當對照基準，以及有沒有自己寫的信件或自述可以讓它學你的文風。
2. 幫你生出專屬工具：照你的答案，把「協作寫作」「投稿前檢查」等 skill 客製好、裝進你的
   Claude。
3. 教你實際會用到的幾句話，然後你就可以開始了。

### 之後每天怎麼用
在放論文的資料夾裡開 Claude Code，用平常講話的方式說要做什麼（你也可以直接打 `/skill名`）：

| 你打這句 | Claude 幫你做 | 對應的 skill／工具 |
|----------|---------------|-------------------|
| 「幫我寫這篇論文／提案」 | 協作寫作：找文獻、架論證骨架、寫成稿、自己檢查 | `/co-author` |
| 「這段讀起來像翻譯／不像這個領域的論文」 | 母語潤稿：先量出稿子哪些語言特徵偏離同領域論文的常見區間，潤稿子代理只交改動清單，由你逐條裁定；數字、引用、術語動了就擋 | `/co-author` Phase 5.5 → `tools/register/register_profile.py`、`polish_check.py` |
| 「幫我檢查這篇再投」 | 投稿前的品質與格式檢查（五層） | `/paper-review` |
| 「幫我把這些引用的 PDF 收齊」 | 收集並查證參考文獻 | `/fetch-refs` |
| 「這些引用真的撐得住我寫的話嗎？」 | 逐句對照 PDF 原文判定引用方向、DOI 權威查驗 | `/verify-citations`（＋`citation-skeptic` 二審） |
| 「誰引用了這篇？有沒有我漏掉的後續研究」 | 引用滾雪球：從一篇（或整份書目）長出該讀而未讀的文獻清單 | `/fetch-refs` → `tools/refs/snowball.py` |
| 「審稿意見回來了，幫我回」 | 逐點回應：拆解意見→逐點裁定→修訂對照→回應信→交付前完整性驗證 | `/rebuttal` → `tools/rebuttal/check_response.py` |
| 「我這篇短文要擴寫成期刊全文」 | 逆向盤點入線，並盤點文字回收與揭露措辭（擴寫本質上就是重用） | `/co-author` Phase 0.5 |
| 「我要再投一個地方，可以吧？」 | 查投稿狀態表，確認同一份稿件沒有同時在別處審查中 | `tools/submissions/check_submissions.py` |
| 「這張圖印成黑白會不會看不懂？」 | 圖表色覺可及性：色盲模擬＋灰階對比，並產生模擬圖給你看 | `/paper-review` → `tools/figures/figure_a11y.py` |
| 「別再犯同樣的錯」「改 A 又弄壞 B」 | 文件回歸：把抓到的錯寫成一條常駐檢查，改完全庫重掃，復發就擋下 | `/doc-regress` → `tools/regress/regress.py` |
| 「把引用的 PDF 抓齊」 | 分層取檔：OA 源 → 一般 HTTP 連線 → 用你自己存取權的真實瀏覽器；拿不到的標明原因（沒訂閱／要人過驗證／工具還沒支援） | `/fetch-refs` → `tools/refs/pdf_fetch.py` |
| 「有沒有哪篇被撤稿了？」 | 撤稿掃描：整份書目對 Crossref＋OpenAlex 查撤稿，每次交付前重跑 | `tools/refs/retraction_scan.py` |
| 「這句沒掛引用，站得住嗎？」 | 無引用宣稱掃描：找出沒有引用的量化／因果／最高級句子，逐筆補引用、指出自家資料、或降級措辭 | `tools/claims/uncited_claims_scan.py` |
| 「這句話說得太滿了嗎？」 | 過度宣稱掃描：找出「完全／永遠／唯一／證明了」這類資料撐不起的字眼；去 AI 味的另一半，中英文都適用 | `tools/claims/overclaim_lint.py` |
| 「稿裡的數字跟分析結果對得上嗎？」 | 數字帳本勾稽：每個數字回溯到產生它的運算；改數字先更帳本再改稿，回歸檢查擋舊值復發 | `/doc-regress` §3.5 |
| 「把這篇排成投稿 PDF」「中文 PDF」 | 依場域模板排版；第二語言稿連同回譯稿成對交付 | `/build-pdf` |
| 「投出去之前還缺哪些聲明？」 | 投稿聲明六件套：AI 使用揭露／研究倫理／資料可得性／作者貢獻／利益衝突／預註冊 | `/co-author` Phase 6-2a、`/paper-review` 第 7 項 |
| 「交出去前全部跑一遍」 | 全套潤修：引用查驗→校對→母語潤稿→去 AI 味→去過度宣稱→在地用語→回歸→出新版號 PDF，依序跑完、最後一次回報 | `/co-author`〈全套潤修〉 |
| 「這個期刊准不准用 AI 寫？AI 畫的圖能放嗎？」 | 各出版社生成式 AI 規定對照（附查閱日，每案重讀原文）；場域不准 AI 起草時先攤給你選，聲明照實寫 | `method/AI_DISCLOSURE.md`、`/co-author` Phase 1.5 |
| 「這個題目值得寫成全文嗎？」 | 貢獻閘門：乾淨審稿人以該場域編輯的眼光判斷，五選一：寫全文／縮成短文或海報／換場域／先補資料／不值得寫 | `/co-author` Phase 1.5、`clean-reviewer` |
| 「這是合作者主筆的稿，改完要對得回原稿」 | 原檔不改、改動寫成潤稿層；新稿逐句比對原稿與對方回覆，指不回來源的方法與數字標紅 | `method/COLLABORATION.md` → `tools/collab/source_trace.py` |
| 「超頁了／字數超過」 | 先查官方怎麼算、找被釘死的邊界、各節預算、由輕到重下刀並逐刀回報；不縮圖、不拿證據換頁數 | `method/COMPRESSION.md` |
| 「版號怎麼定？交哪一份？」 | 版號＝送出次數．內容．措辭；`VERSION` 檔是唯一來源，CHANGELOG 先寫再建置，交付資料夾只放一版 | `method/VERSIONING.md` → `tools/versioning/version_check.py` |
| 「PDF 裡的圖表編號對不對？圖是不是縮太小？」 | 排好的 PDF 圖表機械檢查：跳號重號、正文提到卻沒圖說、超出版心或頁面、圖內字太小 | `/paper-review` 1f → `tools/figures/figure_check.py` |
| 「還缺哪些文獻要我自己下載？」「我載好了，幫我收」 | 先扣掉你自己文獻庫已有的才列缺件；下載匣裡的 PDF 比對、驗內容、歸檔、清下載匣 | `/fetch-refs` → `tools/refs/missing_refs.py`、`inbox_ingest.py` |
| 「還要審幾輪？是不是在原地打轉？」 | 審查輪次帳本：每輪致命與重大分新提與重提，連兩輪沒有新的就建議停審 | `/paper-review` → `tools/review/review_rounds.py` |
| 「這篇投哪裡比較好？」 | 場域比較表：至少三個候選（含一個保底），每格取自當年度官方頁或索引並附查閱日，查不到就寫查不到，不估錄取率與審查時間；表下給一個建議，選擇權在你 | `/co-author` Phase 1.5 |
| 「合作者改完傳回來，沒開追蹤修訂」 | 拿你寄出的那份逐段比對，列出改了、加了、刪了、搬了哪裡，再逐條寫回源檔 | `method/COLLABORATION.md` → `tools/collab/docx_diff.py` |
| 「要找第二位編碼者算一致性」 | 把 codebook 與作答做成一個離線判讀網頁給編碼者，匯出後轉回編碼表、算每個代碼的 kappa；網頁含受試者作答，不上網 | `method/COLLABORATION.md` → `tools/collab/coding_pack.py` |
| 「能投了嗎？還差什麼？」「截止是我這裡幾點？」 | 就緒判讀：重讀官方頁、截止時間換成你的時區、硬性規定逐條量、評分交乾淨審稿人；分成硬性規定、擋件項目、只有你能做的事、時程四段回報 | `/submit` → `tools/submit/deadline.py` |
| 「做成 Word 給我」「格式跟官方範本一樣嗎？」「匿名有沒有漏？」 | 從源檔建 Word 並回轉比對、用 Word 算字數、對範本逐項比格式、雙盲匿名檢查；作者待辦另放一檔，不留在交付檔裡 | `/submit` → `tools/submit/` |
| 「我送出了，幫我收尾」 | 找確認信、寫送件紀錄、投稿台帳改成已投、放榜日進行事曆、主版號加一並打 tag | `/submit` 第 6 節 |

> 預設走最簡單的模式：只要 Claude ＋ 網路，什麼都不用安裝。之後真的需要更強的工具
> （本機統計、文獻庫、語言檢查）再一次加一個就好。

---

## 隱私

- 這個 repo 裡只有方法與工具，沒有任何人的稿件或資料。
- 隨包的檢查工具與統計分析都在你的電腦上跑。線上檢索只送出 DOI、標題、作者這類書目資料（見〈會用到哪些外部程式與服務〉）。
- 方法本身要求：**未發表稿件與研究原始資料不交給第三方線上服務**，不丟公開的 AI 偵測器，也不貼到其他雲端 AI 工具。
- **Claude Code 本身是雲端模型**，它讀到的檔案內容（包括稿件與資料）會傳到 Anthropic 處理。有受試者資料或保密要求時，先確認機構與研究倫理審查的規定，以及你 Claude 帳號的資料使用設定。規定不允許送出的資料，就不要讓 Claude 讀。
- 你生成的個人設定（文風檔、投稿筆記、骨架）不會被這個 repo 收走（見 `.gitignore`）。

## 授權

- **程式碼**（`tools/`）：MIT，可自由使用、修改與商業使用，保留版權聲明即可（[`LICENSE`](LICENSE)）。
- **方法與文件**（`method/`、`skills/`、`agents/`、`templates/`、`setup/`、README）：CC BY 4.0，可改寫、翻譯、教學、做自己的版本，唯一條件是標示出處（[`LICENSE-DOCS`](LICENSE-DOCS)）。
- **第三方詞表**（`data/academic-vocab/`）：隨包的 AVL、ACL 為研究／教學免費使用、需標示出處；AWL 是 CC BY-NC-ND（不得改作），不隨附，由你用 `tools/vocab/fetch_awl.py` 自行抓取到本機。都不在上面兩種授權範圍內。
- 引用格式與細則見 [`NOTICE.md`](NOTICE.md)。

---

## 資料夾裡有什麼（完整清單）

| 位置 | 內容 |
|------|------|
| `CLAUDE.md` | 安裝器：你的 Claude 讀這個來訪談你、生成你的專屬設定。 |
| `NOTICE.md` | 分享條件與第三方資料授權。 |
| `method/` | 方法本體十一份（英文）：`PHILOSOPHY.md`（心法）、`IRON-RULES.md`（鐵則）、`WORKFLOW.md`（Phase 0 到 8 的完整流程，含 5.5 母語潤稿）、`ARGUMENTATION.md`（論證工法，內部診斷用）、`RIGOR_PROCESS.md`（從文獻到報告的十三階段嚴謹流程）、`METHOD_DECISION.md`（研究方法決策程序與報告準則）、`METHOD_CARDS.md`（38 張研究方法分析卡，含決策索引與條件警訊）、`VERSIONING.md`（版號、CHANGELOG、交付資料夾）、`COLLABORATION.md`（合作者稿與多人計畫書）、`COMPRESSION.md`（超頁超字的壓縮程序）、`AI_DISCLOSURE.md`（各出版社生成式 AI 規定與聲明寫法）。 |
| `skills/` | 八個 skill 範本（見下表）。 |
| `agents/` | 五個 subagent 範本（見下表）。 |
| `tools/` | 四十二支本機腳本＋共用模組＋輔助檔＋模板（見下表），說明在 `tools/README.md`。 |
| `templates/` | 四份空白檔：`VOICE_PROFILE.template.md`（文風檔，信件與自述用）、`venue-notes.template.md`（投稿場域筆記）、`skeleton.template.md`（論證骨架）、`voice_rules.template.json`（聲音硬規則）。 |
| `data/academic-vocab/` | 開放學術詞表：隨包兩份（`avl_core_words.tsv`、`acl_collocations.tsv`），第三份 `awl_families.tsv` 由 `tools/vocab/fetch_awl.py` 在你電腦上產生（授權不允許隨包）。投稿前檢查的用字層拿來當錨點，不是自動替換；授權見 `NOTICE.md`。 |
| `examples/skeleton.example.md` | 一份填好的骨架範例，讓 Claude 有具體參照。 |
| `setup/` | `LITE.md`（零安裝模式）、`TOOLS.md`（選配工具與降級對照）、`INTERVIEW.md`（面談問法）、`WEB.md`（從 claude.ai 網頁版上手）、`addons/zh-tw/README.md`（繁中在地化包）。 |

### 八個 skill

安裝後，用講的或直接打 `/名稱` 都會觸發。

| skill | 做什麼 | 會用到的工具 |
|-------|--------|--------------|
| `co-author` | 從無到有的協作寫作（論文與提案）：骨架→查證→寫稿→交付前關卡；也走既有稿改寫、轉投、擴寫、合作者主筆的稿；一句話「全套潤修」 | 交付前掃描三支（撤稿／無引用宣稱／回歸）、`check_submissions.py`、Phase 5.5 母語潤稿（`register_profile.py`、`polish_check.py`、兩個潤稿 subagent）、`clean-reviewer` 貢獻閘門與乾淨終審、`source_trace.py`、`docx_diff.py`、`coding_pack.py`、`figure_check.py`、`version_check.py` |
| `paper-review` | 投稿前五層檢查：機械層→用字→語言→邏輯與審稿視角→交付完整性；只檢查不改稿；記錄每輪審查、判斷何時停審 | 中文三支（`voice_lint.py --paper`）、`zh_gloss_scan.py --en`、`lt_check.sh`、`ai_style_diag.py`、`figure_a11y.py`、`figure_check.py`、`uncited_claims_scan.py`、`overclaim_lint.py`、`review_rounds.py`、`clean-reviewer` 審稿模擬（第 4 層）、（選配）R `statcheck`＋`scrutiny` |
| `fetch-refs` | 把書目的 PDF 收齊、逐篇確認內容真的相符、歸檔＋清單；列出要你自己下載的缺件、收下載匣；含引用滾雪球 | `pdf_fetch.py`（分層取檔＋失敗分類）、`missing_refs.py`、`inbox_ingest.py`、`snowball.py`、線上 API |
| `verify-citations` | 逐句對照 PDF 判定引用是否被原文支撐、方向對不對；DOI 權威查驗；撤稿掃描 | `retraction_scan.py`、`citation-skeptic` 二審、（選配）MinerU |
| `rebuttal` | 審稿回應：拆點→裁定→落實修訂→回應信→完整性驗證 | `check_response.py`＋三份模板、`clean-reviewer` 起草裁定表、修訂段落走 Phase 5.5 母語潤稿、`de-cadencing-scholar`、（選配）`latexdiff` |
| `doc-regress` | 抓到一次錯就寫成常駐檢查；數字帳本；死規則健檢 | `regress.py`、`dead_rule_check.py`＋兩份模板 |
| `build-pdf` | 依場域模板排版成 PDF；第二語言稿連同回譯稿成對交付；繁中用 Typst 配方 | Typst 或 Quarto／LaTeX |
| `submit` | 送出那一段：能不能投的就緒判讀（重讀官方頁、截止時間換成你的時區、評分交 `clean-reviewer` 不自評）、從源檔建 Word 並回轉比對、照場域的計算方式算字數、對官方範本比格式、雙盲匿名檢查、上傳包與欄位清單；送出後歸檔確認信、寫送件紀錄、更新投稿台帳、主版號加一打 tag | `deadline.py`、`docx_roundtrip.py`、`word_count.sh`（＋`wordcount_approx.py`）、`template_diff.py`、`anon_check.py`、`version_check.py`、`check_submissions.py`、`clean-reviewer` |

### 五個 subagent

| agent | 做什麼 | 何時派 |
|-------|--------|--------|
| `clean-reviewer` | 乾淨脈絡的終審：不帶寫稿史，用審稿人的眼睛找稿件、審稿意見裁定表或網頁的真弱點。要用最強的一級模型與最高的推理強度；Claude Code 2.1.292 起 Agent 呼叫也能帶推理強度，但釘在範本的 frontmatter 裡只要設一次，不靠每次呼叫記得帶 | `co-author` Phase 6 終審、`paper-review` 第 4 層審稿模擬、`rebuttal` 裁定表 |
| `en-native-editor` | 英文母語學術編輯：照同領域論文的語域區間，把區間外的特徵往內移，另修華語作者常見的冠詞、介系詞、搭配與時態；只交改動清單，不直接改稿 | `co-author` Phase 5.5 英文稿（在 de-cadencing 之前） |
| `zh-tw-native-editor` | 台灣學術中文母語編輯（繁中在地化包）：同樣以語域區間為準，處理翻譯腔、過度切短的句子、非台灣慣用詞；只交改動清單 | `co-author` Phase 5.5 中文稿 |
| `de-cadencing-scholar` | 母語學者視角挑掉英文稿「一看就是 AI 潤過」的節奏痕跡並改寫（七類 tic，第六類＝過度宣稱、第七類＝開場套語）；改完重量語域，避免把特徵推出區間 | 英文稿交付前（母語潤稿之後）；審稿回應信交付前 |
| `citation-skeptic` | 對被標記「引用可能有問題」的判定做校準二審：預設引用正確，只有 PDF 逐字直接矛盾才維持指控 | `verify-citations` 有 flag 時 |

### 隨包工具（`tools/`，全部）

| 檔案 | 用途 | 額外要裝什麼 |
|------|------|--------------|
| `common/md_prose.py` | 共用模組：把 markdown／LaTeX 版面語法（frontmatter、表格、註解、code）剝掉只留散文，四支文風工具都靠它；不直接執行 | — |
| `zh-tw/zh_localize.py` | 陸用語→台灣用語、台／臺一致性（只報不改） | 不用 |
| `zh-tw/zh_ai_style.py` | 中文 AI 句法指紋：破折號、三連並列、趨同詞、句長節奏、「並非…而是」密度、120 字以上長句清單；可對照你自己的親筆語料 | 不用 |
| `zh-tw/voice_lint.py` | 你自己的聲音硬規則（吃 `voice_rules.json`），交稿前守門，不乾淨不放行；另掃句型標題、八股套語，並列出 AI 套話候選供人判。論文、計畫書、申請書加 `--paper`，改套範本裡的論文規則（例如不擋期刊常用的分號） | 不用 |
| `zh-tw/zh_register.py` | 中文語域剖面：52 項特徵（自稱、翻譯腔、連接詞、後設論述、立場、標點、句長），對照你自己收的同領域期刊論文語料，給每項的 p10／中位數／p90；這是量表，不做偵測 | 自備語料（30 篇以上） |
| `zh-tw/zh_gloss_scan.py` | 括號夾註盤點：列出 12 字以上、非引用非指路的夾註，供你決定改定義句、保留或刪；`--en` 改列中文詞後的英文夾註（第二次起標「首次已給」）與正文沒括號的英文詞排行 | 不用 |
| `zh-tw/zh_tw_terms.py` | 台灣慣用語詞表的讀取與比對模組，`zh_localize.py` 靠它；不直接執行 | — |
| `en/lt_check.sh` | 英文文法＋美英拼字一致性（離線 LanguageTool）；有 n-gram 資料會自動加掛易混詞偵測 | `brew install languagetool pandoc` |
| `en/lt_strip_noprose.lua` | `lt_check.sh` 用的 pandoc 濾鏡，剝掉非散文再送檢；不直接執行 | （隨 pandoc） |
| `en/ai_style_diag.py` | 英文 AI 指紋：對照你領域已發表論文語料的百分位；含 LLM 趨同詞密度並印出命中的詞；自動排除自家草稿與模板檔以免污染基線 | 自備語料；讀 PDF 需 `pdftotext`（`brew install poppler`） |
| `en/en_slop_terms.tsv` | `ai_style_diag.py` 用的英文 LLM 趨同詞表（162 條，取自 slop-forensics 再篩掉 HCI 論文本來就常用的詞）；不直接執行 | — |
| `en/bundle_diag.py` | 詞束過度使用診斷（英文與繁中皆可）：LLM 寫作會反覆用同一批固定搭配，這支量它的密度並列出命中 | 不用 |
| `en/metadiscourse_en.py` | 英文後設論述量測（Hyland 框架）：避險、強調、態度標記等各類的密度，附 p10／中位數／p90 與偏高偏低的方向；`--groups` 只比單一期刊、`--json` 給程式讀。這是量表，用來看自己的分布落在哪，不用來判定誰寫的 | 不用 |
| `en/biber_diag.py` | 英文句法特徵比較（Biber tagger），對照你領域的語料看自己偏在哪、往哪個方向偏；`--groups` 只比單一期刊、`--json` 給程式讀；跑在獨立的選配環境，套件其餘部分都不需要它 | `pip install pybiber spacy polars` 加語言模型（建議另開虛擬環境，路徑記成 `BIBER_PYTHON`） |
| `register/register_profile.py` | 母語潤稿的偏離清單（中英文）：哪些特徵落在同領域論文 p10–p90 區間外、該往哪個方向移，並依行號範圍給上下限，免得潤過頭跑到另一端 | 自備語料；英文句法層另需 `biber_diag.py` 的環境（沒有就 `--no-biber`） |
| `register/polish_check.py` | 潤稿改動清單套進稿子之前的檢查：數字、引用、引文與鎖定術語不得變動，字數增幅不超過預算，不得新增禁用寫法，語域特徵不得往錯的方向移；全部通過才用 `--apply` 寫回。改動清單只當資料讀，不執行 | 不用 |
| `figures/figure_a11y.py` | 圖表色覺可及性：三種色盲模擬＋灰階對比，寫出模擬圖供目檢 | `pip install numpy pillow`（PDF 另需 `pymupdf`） |
| `figures/figure_check.py` | 排好的 PDF 圖表機械檢查：圖說編號跳號重號、正文提到的圖表有沒有圖說（跨行與複數引用都認）、圖超出版心（黃）或頁面（紅）、向量圖內字太小、點陣圖縮到字看不清（由等效 dpi 推估字級）；每張圖裁成 PNG 供目檢 | `pip install pymupdf` |
| `refs/pdf_fetch.py` | 取檔分三層：OA 源（增補 Europe PMC／CORE／OpenAIRE）→ 模擬瀏覽器連線的 HTTP 用戶端（curl_cffi）→ 你電腦上的 Chrome（持久 profile，用你自己的存取權）。ACM／Wiley／SAGE／AIP／Elsevier 這類會擋程式連線的出版社頁面，要到最後一層才打得開。瀏覽器層每篇之間暫停、單次最多 100 篇，不會替你點「確認你是人類」；出版社條款允許為自己的研究下載單篇，不允許大量下載。拿不到的一律分類成 `PAYWALL`／`CAPTCHA`／`NO-LINK`；沒有 DOI 的條目讀 arXiv `eprint`，再不行以標題在 arXiv／OpenAlex 精確比對，只有專書才交回人工 | `pip install curl_cffi patchright`（沒裝則退回 stdlib＋OA 源） |
| `refs/snowball.py` | 引用滾雪球：誰引用了這篇／這篇引了誰／相近研究，多種子聚合排序 | 不用（需網路） |
| `refs/retraction_scan.py` | 撤稿掃描：`.bib` 或 DOI 清單對 Crossref 更新關係＋OpenAlex `is_retracted` 雙源查核；無 DOI 條目另列不算已掃 | 不用（需網路） |
| `refs/lit_map.py` | 文獻地圖：一批同主題文獻彼此共同引用誰的排行（不看全球被引數），當「這個領域的經典」候選；結果要人工判定 | 不用（需網路） |
| `refs/missing_refs.py` | 缺件清單：書目裡還沒有 PDF 的條目，先扣掉你自己文獻庫已有的（年份＋第一作者姓＋標題相似度三道關卡），剩下的才列 DOI／網址／ISBN 給你下載；資料夾裡已經有的檔也重驗一次內容，可疑的寫進 `_check_present.md`，只標記不搬也不刪（`--no-check-present` 關掉） | 不用（驗內容需 `pdftotext`） |
| `refs/inbox_ingest.py` | 下載匣收件：把你手動下載的 PDF 比對缺件、驗內容、改名歸檔，可順手複製進文獻庫；只把歸檔成功的來源檔移到垃圾桶，不刪除 | 驗內容需 `pdftotext`（`brew install poppler`） |
| `refs/refs_common.py` | 共用模組：BibTeX 解析、三道關卡比對、PDF 內容驗證，上面兩支靠它；比對前先做 NFKC 正規化並接回連字，中文標題直接比字串，首頁 arXiv 年份比書目晚兩年以上就降成 `LOW-CONFIDENCE`；不直接執行 | 不用（裝了 OpenCC 會順手做簡繁轉換再比對） |
| `claims/uncited_claims_scan.py` | 沒掛引用的量化／因果／最高級宣稱（`.md`／`.tex`／`.qmd`，中英文都適用）；逐筆裁決後可加豁免註記 | 不用 |
| `claims/overclaim_lint.py` | 過度宣稱候選（絕對化／程度誇大／證據強度／最高級，中英雙語詞表）；另抓兩類：「就作者所知／尚無研究」這類「沒人做過」的宣稱（旁邊有引註也照報，因為撐得起它的是檢索留痕，不是引註），以及引用要點、辦法、指引卻沒標年份的官方文件；只報不改，每筆人判「資料撐不撐得起」 | 不用 |
| `method/method_decision_check.py` | 方法決策備忘錄的格式閘門：有沒有真的比對過同類研究、每個宣稱有沒有對應的方法支撐；不判斷方法選得對不對 | 不用 |
| `method/analysis_plan_check.py` | 資料收集前計畫的閘門：分析方法、樣本數依據、偏離登記等欄位齊不齊；這一關事後補不回來 | 不用 |
| `method/tea_second_opinion.py` | 統計的第二意見：給它資料與研究設計，它自動挑並跑對應的檢定，用來對照你自己選的那個 | Tea（Python 3.10–3.13，會釘舊版 numpy／pandas，給它自己的虛擬環境） |
| `regress/regress.py` | 文件回歸：照專案的 `regress.json` 掃全庫；內建懸空引用、個資、待辦、舊值復發、歸屬缺漏等規則，專案自訂規則用 `--extra my_rules.py` | 不用 |
| `regress/dead_rule_check.py` | 規則健檢三項：哪條規則的主體其實沒有執行（設定是空的，一進來就 return）、哪條寫了卻沒註冊進 `RULES`、哪條呼叫了檔案裡不存在的函式 | 不用 |
| `regress/rules.template.json`、`regress/numbers-ledger.template.md` | 回歸規則設定檔與數字帳本的空白模板 | — |
| `rebuttal/check_response.py` | 回應信完整性：每點都答了嗎／說要改的真的改了嗎／不接受的有沒有依據 | 不用 |
| `rebuttal/points.template.tsv`、`revisions.template.tsv`、`response-letter.template.md` | 審稿意見拆點表、修訂對照表、回應信模板 | — |
| `submissions/check_submissions.py` | 一稿多投防護＋投稿狀態總覽（同一份稿件不得同時在兩處審查） | 不用 |
| `submissions/style_reaudit.py` | 文風量測規則改過之後，照投稿台帳把所有進行中與審查中的稿件重量一次，避免舊稿停在舊標準 | 不用 |
| `submissions/SUBMISSIONS.template.tsv` | 投稿狀態表模板 | — |
| `review/review_rounds.py`、`review/review-rounds.template.tsv` | 審查輪次收斂帳本：每輪致命與重大分新提與重提，重提已裁定事項卻沒附新證據就擋；連兩輪沒有新的致命或重大就建議停審 | 不用 |
| `collab/source_trace.py` | 合作者稿逐句溯源：改寫後的每一句能不能指回原稿、對方回覆或計畫書；指不回來源的數字、方法詞、現場事實標紅，新增的文獻主張標橘 | 不用（讀 `.docx` 需 `python-docx`、讀 PDF 需 `pdftotext`） |
| `collab/docx_diff.py` | 合作者改完傳回的 Word 沒開追蹤修訂時，拿你寄出的那份比對：逐段列出修改、新增、刪除、搬移（含表格儲存格、頁首頁尾、註腳），並回報對方留下的追蹤修訂與註解；`--out` 給人讀的清單、`--json` 給你逐條寫回源檔 | `pip install python-docx` |
| `collab/coding_pack.py` | 第二編碼者判讀包：codebook 加上作答 CSV 變成一個離線網頁，一次看一筆、數字鍵勾代碼、最後匯出一份 CSV；`import` 轉回專案的 0／1 編碼表，`score` 算每個代碼的 Cohen's kappa、PABAK、盛行率與 bootstrap 信賴區間。網頁含受試者作答，只在本機開或直接交給編碼者 | `build`、`import` 不用；`score` 需 `numpy` |
| `versioning/version_check.py` | 交付前查版號：`VERSION`、CHANGELOG 最上面一節、交付資料夾只放一版、PDF metadata 帶版號、送件版正文不印版號、已打 tag 的版號沒被重用；`VERSION` 改了卻沒重建交付檔報錯，源檔比交付檔新就提醒；最後印出交付檔的絕對路徑，回報時照抄 | 不用（查 PDF 需 poppler） |
| `submit/deadline.py` | 截止時間換成你的時區（AoE、PST／PDT、`UTC+8`、IANA 名稱都認，夏令時間照日期判斷），印出剩餘時間與提早 24 小時的建議送出時間 | 不用 |
| `submit/docx_roundtrip.py` | 從源檔建好的 docx 轉回文字，逐句跟源檔比對（源檔有、docx 沒有／docx 有、源檔沒有），再掃殘留：沒解析的 `[@key]`、`??`、TODO、【待確認】、沒替換的 `{{`、Word 參照錯誤、連續空段落 | `brew install pandoc`（空段落檢查另需 `python-docx`） |
| `submit/word_count.sh` | 叫 Microsoft Word 自己算字數（很多場域的上限就是照 Word 的計算方式），可順便讓 Word 輸出 PDF；只限 macOS＋Word，其他環境退回 `wordcount_approx.py` 並以離開碼 3 標明是概估 | macOS＋Microsoft Word |
| `submit/wordcount_approx.py` | 概估字數（中日韓字元＋英文詞＋數字串），可能和 Word 差一成以上，回報時一律寫「概估」；`word_count.sh` 叫不到 Word 時用它 | 讀 `.docx` 需 `pandoc` |
| `submit/template_diff.py` | 稿件 docx 對官方範本 docx 逐項比格式：紙張、邊界、頁首頁尾距離、預設字型（英文與東亞字型分開）、字級、行距、段前段後、首行縮排、對齊，以及稿件用了範本沒有的樣式；只比樣式定義，段落上的手動格式要目檢 | `pip install python-docx` |
| `submit/anon_check.py` | 雙盲匿名檢查：docx 的建立者與最後修改者、追蹤修訂與註解的作者、正文與頁首頁尾裡的姓名與機構、超連結、PDF 的 Author 與 XMP、內嵌圖片與圖檔的 EXIF（作者、GPS）；「我們先前的研究」這類自我揭露另列橘色給你判斷，並列出實際檢查了哪些區域 | 圖片 EXIF 需 `exiftool`，PDF 需 `pymupdf` |
| `vocab/fetch_awl.py` | 從 Victoria University of Wellington 官方頁面抓 Coxhead 的 AWL 詞表，轉成 `data/academic-vocab/awl_families.tsv`（AWL 授權不得改作，所以 kit 不隨包、請你自己抓；跑一次即可） | 不用（需網路） |

---

## 安裝後，你的電腦上會多出什麼

安裝器（`CLAUDE.md`）會問你「只給這篇，還是全部」，然後：

| 東西 | 放哪 | 說明 |
|------|------|------|
| 八個 skill | `~/.claude/skills/<名稱>/SKILL.md`（全域）或你論文資料夾的 `.claude/skills/`（單一專案） | 照你的答案改寫過，不照原檔複製；領域、語言、場域、模式都填進去了 |
| 五個 subagent | `~/.claude/agents/` 或專案 `.claude/agents/` | `clean-reviewer` 人人都裝；`citation-skeptic` 給要查引用的人；`en-native-editor`、`de-cadencing-scholar` 給寫英文的人；`zh-tw-native-editor` 隨繁中在地化包。安裝時會在 frontmatter 補上你手上最強的模型 |
| 你的 `CLAUDE.md` 多一段 | `~/.claude/CLAUDE.md` 或專案 `CLAUDE.md` | 記你的領域、語言、場域、模式（lite／full）、語域語料的位置與期刊資料夾名、文風檔位置，以及 kit 的路徑（`KIT PATH`），全機只記這一處，搬 kit 只改這一行 |
| `voice-samples/` | 你的專案或家目錄 | **只放你親筆寫的文章**（給了舊稿才有）；文風工具的 `--authored` 指這裡，絕不指向混有 AI 稿的資料夾 |
| 語域語料資料夾（`<語料>/<期刊>/*.txt`） | 你指定的位置 | **只放別人已發表的論文**（完整模式才有），轉成純文字、一個期刊一個資料夾；`register_profile.py` 拿它當準繩 |
| `VOICE_PROFILE.md`、`voice_rules.json` | 同上 | 從你的信件與自述抽出的文風描述與硬規則，用在信件、投稿信與自述；`voice_lint.py` 吃後者（論文加 `--paper`） |

沒安裝的選配工具，生成的 skill 會寫成「若已安裝才用」，不會假裝它存在。

---

## 跑起來後，你的論文專案裡會長出的檔案

這些都是你的檔案（在你的論文資料夾，不在這個 repo），建議連同稿子一起版控。

| 檔案 | 誰建的 | 用途 |
|------|--------|------|
| `skeleton.md` | `co-author` | 論證骨架＝唯一權威；每個 Phase 結束回寫 `## Progress`，新 session 先讀它 |
| `venue-notes.md` | `co-author` | 目標場域當年度的格式、字數、審查慣例、AI 揭露政策、預印本政策 |
| `search-log.md` | `co-author` | 檢索留痕：用了哪些資料庫、查詢字串、日期、納入排除，審稿人問「為何漏了 X」時要答得出來 |
| `ADJUDICATED.md` | `co-author`／`paper-review`／`doc-regress` | 已裁定事項：「看起來錯、查過、其實對」的清單，之後的檢查不重問 |
| 文獻 PDF 資料夾＋清單檔 | `fetch-refs` | 手動歸檔依 `NN [作者 年] 標題.pdf` 命名，`pdf_fetch.py` 與 `inbox_ingest.py` 寫成 `refs-pdf/<citekey>.pdf`；清單記找到什麼、沒找到什麼、驗證層級（verified／LOW-CONFIDENCE）、自署著作標記 |
| `refs-pdf/_missing.md`、`_missing.tsv`、`_inbox_log.tsv` | `missing_refs.py`、`inbox_ingest.py` | 要你自己下載的缺件清單（已扣掉你的文獻庫）；下載匣收件紀錄 |
| `VERSION`、`CHANGELOG.md`、`latest/`、`versions/vX.Y.Z/` | `co-author`（`method/VERSIONING.md`） | 版號唯一來源、每版改了什麼與依據、只放當下一版的交付資料夾、每版快照；中文專案可用 `最新交付/`、`版本/` |
| `docs/received/YYYYMMDD-來源/` | `co-author`（`method/COLLABORATION.md`） | 合作者傳來的原檔，原名封存不改 |
| `docs/source-trace.md` | `source_trace.py --report` | 合作者稿逐句溯源報告 |
| `docs/review-rounds.tsv` | `paper-review` | 審查輪次帳本，`review_rounds.py` 讀它判斷是否收斂 |
| `figures/ai-generation-log.md` | `co-author` | AI 生成圖的引擎、版本、seed、完整提示詞；圖說與聲明照它寫 |
| `snowball.csv` | `snowball.py` | 滾雪球結果（可自訂檔名） |
| `regress.json`、`my_rules.py`（選） | `doc-regress` | 回歸規則設定與專案自訂規則；隨稿版控 |
| 數字帳本（照 `numbers-ledger.template.md`） | `doc-regress`／`co-author` Phase 3 | 稿中每個數字回溯到產生它的運算；重跑分析→先更帳本→再改稿 |
| `rebuttal/points.tsv`、`rebuttal/revisions.tsv`、`rebuttal/response-letter.md` | `rebuttal` | 意見拆點、修訂對照、回應信 |
| `<圖檔名>_a11y/`（`protan.png`、`deutan.png`、`tritan.png`、`grayscale.png`） | `figure_a11y.py` | 色盲與灰階模擬圖，一定要開來看，數字只是證據，判決由你下 |
| 撤稿／無引用宣稱掃描的 JSON 報告（選） | `retraction_scan.py --out`、`uncited_claims_scan.py --json` | 給 CI 或留檔用；平常看終端輸出即可 |
| 回譯稿＋兩份 PDF | `co-author`／`build-pdf` | 第二語言稿的簽核入口：原稿 PDF 與回譯 PDF 成對交付 |
| `SUBMISSIONS.tsv` | `check_submissions.py` | 放在所有論文專案之上一層（一份台帳管全部；`SUBMISSIONS_TSV` 環境變數指向它）；一稿多投在單一專案資料夾裡看不出來 |

> 這個 repo 的 `.gitignore` 排除 `VOICE_PROFILE.md`／`venue-notes.md`／`skeleton.md`，是為了不讓任何人的個人設定回流到 kit；在你自己的論文專案裡，這些檔案該跟著稿子一起版控。

---

## 會用到哪些外部程式與服務（完整對照）

> 一句話版本：只要 Claude Code 就能開始。其他都是「有了更好」，而且 Claude 會在
> 你真的需要時才建議裝，一次一個。

### 一定需要的

| 工具 | 用途 | 怎麼取得 |
|------|------|----------|
| Claude Code | 整套方法的執行者：訪談你、找文獻、架骨架、寫稿、自我檢查 | [claude.com/claude-code](https://claude.com/claude-code)（需付費 Claude 方案：Pro／Max／Team 或 API 計費） |
| Python 3.9 或更新 | 跑隨包附的本機檢查工具（CI 在 3.9 與 3.13 上測） | macOS 要先裝 Xcode Command Line Tools（`xcode-select --install`）或 `brew install python`；Linux 多數發行版內建；Windows 到 python.org 抓安裝檔 |
| git | 下載與更新這個 repo（`git clone` / `git pull`） | macOS 裝 Xcode Command Line Tools 就有；或用 GitHub 頁面的 Download ZIP（之後無法一鍵更新） |

### 選配的本機程式（哪個功能用到、怎麼裝）

下表的 Python 套件可以用 `pip install` 裝，也可以裝了 [uv](https://docs.astral.sh/uv/) 之後用 `uv run tools/<資料夾>/<工具>.py` 執行：每支工具檔頭都寫了它要的套件，uv 會自動備好。

| 程式 | 哪裡用到 | 怎麼裝 |
|------|----------|--------|
| LanguageTool＋pandoc | `lt_check.sh` 英文文法（`paper-review` 第 3 層）；pandoc 另給 `submit` 建 Word 檔與 `docx_roundtrip.py`、`wordcount_approx.py` 讀 docx | `brew install languagetool pandoc`；n-gram 資料選配，放到 `$LT_NGRAMS` |
| poppler（`pdftotext`、`pdfinfo`） | `ai_style_diag.py` 讀 PDF、`verify-citations` 讀文獻 PDF、`inbox_ingest.py` 與 `missing_refs.py` 驗內容、`source_trace.py` 讀 PDF、`version_check.py` 查 PDF | `brew install poppler` |
| numpy、Pillow（＋pymupdf） | `figure_a11y.py` | `pip install numpy pillow`（PDF 圖另加 `pymupdf`） |
| pymupdf | `figure_check.py` 排好的 PDF 圖表檢查、`anon_check.py` 讀 PDF | `pip install pymupdf` |
| python-docx | `source_trace.py` 讀合作者的 Word 檔、`docx_diff.py` 比對傳回的 Word 檔、`template_diff.py` 比範本格式 | `pip install python-docx` |
| exiftool | `anon_check.py` 查圖片 EXIF（作者、GPS）；沒裝就標「未檢查」 | `brew install exiftool` |
| Microsoft Word（macOS） | `word_count.sh` 照 Word 的計算方式算字數；沒有就退回概估 | 你自己的 Office 授權 |
| numpy | `coding_pack.py score` 算一致性與 bootstrap 信賴區間 | `pip install numpy` |
| OpenCC | `missing_refs.py`、`inbox_ingest.py` 比對中文標題前先簡轉繁（沒裝就直接比） | `pip install opencc-python-reimplemented` |
| MinerU | 掃描檔／中文 PDF 抽成乾淨文字（`verify-citations`） | `uv tool install mineru`；4.x 的批次指令是 `mineru-kit parse`，不要加 `--remote`（會把檔案送到 MinerU 的雲端） |
| R＋`statcheck`、`scrutiny` | `paper-review` 第 1 層重算 p 值、GRIM 查平均數可能性（沒裝就退回手算） | 裝 R 後 `install.packages(c("statcheck","scrutiny"))` |
| R＋`DeclareDesign` | `co-author` Phase 3.5 設計診斷（看 coverage 不只看 power） | `install.packages("DeclareDesign")` |
| R 或 Python 統計 | 本機統計分析：混合模型（`lme4`／`afex`）、序數 Likert（`ordinal::clmm`）、事後比較與效果量；分流規則見 `setup/TOOLS.md` | 計算在你電腦上跑；數值雷區見 `setup/TOOLS.md` |
| R 貝氏三路 | 公式寫得出的階層模型→`brms`；「無差異」結論要 BF01→`BayesFactor`；離散潛在變數／混合模型／自訂 sampler／JAGS 舊模型移植→`nimble`（BUGS 語法，Stan 寫不出離散參數）；三者都要報先驗與收斂診斷 | `install.packages(c("brms","BayesFactor","nimble"))`；`brms` 另需 CmdStan 或 rstan |
| Harper | 英文毫秒級第一遍文法（存檔就報；LanguageTool 仍是主力） | 編輯器外掛或 CLI，離線 |
| autocorrect | 中文全半形、盤古空格自動整理 | `brew install autocorrect` |
| Typst 或 Quarto／LaTeX | `build-pdf` 排版；繁中走 Typst 配方（`setup/addons/zh-tw/`） | 依場域官方模板選；`latexdiff` 給 `rebuttal` 做修訂對照 |
| Jupyter | 可重跑的分析筆記本 | `pip install jupyterlab` |
| 機構圖書館 VPN | 付費牆內的文獻全文（`fetch-refs`） | 依你的機構 |
| 本機 RAG | 自己文獻庫的語意檢索（哪篇、哪頁） | `setup/TOOLS.md` 給方向，不給實作 |

### Claude 與工具會連的線上服務（免費、不用裝、不用註冊）

| 服務 | 哪裡用到 | 送出什麼 |
|------|----------|----------|
| Crossref | `retraction_scan.py`（撤稿更新關係）、`verify-citations` DOI／書目查驗 | 只送 DOI |
| OpenAlex | `retraction_scan.py`（`is_retracted`）、`snowball.py`、`lit_map.py`、無 DOI 條目的標題補查（可選免費金鑰 `OPENALEX_API_KEY`：沒設每天 $0.10 額度、設了 $1，標題搜尋一次 $0.001、DOI 單筆免費） | DOI 或標題 |
| Semantic Scholar | `snowball.py` 後備線、引用補查 | DOI 或標題 |
| Europe PMC／CORE／OpenAIRE | `pdf_fetch.py` 的 OA 源（CORE 需免費金鑰 `CORE_API_KEY`，沒設就跳過） | DOI |
| 出版社網站 | `pdf_fetch.py` 的瀏覽器層，用你自己的存取權在真實瀏覽器 session 取檔 | 就是你手動開網頁會送的東西 |
| Unpaywall、arXiv | `fetch-refs` 抓開放取用的 PDF | DOI |

上表的線上服務只拿到書目資料（DOI、標題、作者）。稿件內容會送出去的地方只有 Claude Code 本身（見〈隱私〉）。

### 不收錄的環節

有幾件事這個套件刻意不收錄，因為它們超出「論文與提案」的範圍，或綁死在特定機器與資料上：

- 發表影片的製作（講稿、配音、影片合成）：超出論文與提案的範圍，且每一段都要自架模型。
- 反向查驗「我的文獻庫裡有沒有人反駁我」：需要本機文獻全文索引與本機模型做極性判斷；`setup/TOOLS.md` 只給方向，不給實作。「缺的 PDF 先從自己的文獻庫補」這一半自 v1.10.0 起隨附（`missing_refs.py --library`，以檔名比對，不需要全文索引）。
- 派工分工表（哪一步派哪個型號的子代理）：綁訂閱方案與當下的型號版本，換一家或換一代就不成立。判準有隨附（哪一步是機械可降級、哪一步要用最強的模型，寫在各 skill 與 subagent 範本裡），型號沒有，因為你手上有哪幾級模型只有你知道。
- 整篇術語譯名對照樂詞網：需要自行下載並建立樂詞網資料庫；單詞查詢請你的 Claude 上網查即可。

---

## 給進階使用者
所有 skill 都是純 Markdown 的 `SKILL.md`，Claude Code 會自動辨識。想手動掛成全域 skill，
把 `skills/<name>/` 複製或 symlink 到 `~/.claude/skills/` 即可；`agents/` 的五個 subagent
範本同理，掛到 `~/.claude/agents/`（或專案的 `.claude/agents/`）。但還是建議讓 `CLAUDE.md`
的安裝流程幫你客製，不要照抄原版。

兩個原則：乾淨二審只給檔案路徑（不餵主對話的寫稿史，否則盲點共享）；終審與引用二審是需要判斷的工作，
用你手上最強的一級模型，別為省錢降級。機械層的掃描（撤稿、無引用宣稱、回歸）不需要模型，直接跑腳本。

---

## 版本紀錄

每一版改了什麼見 [CHANGELOG.md](CHANGELOG.md)。
