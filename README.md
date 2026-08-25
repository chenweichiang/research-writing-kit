# 研究寫作套件 · Research Writing Kit

**版本 `v1.3.0`**（2026-08）

> ⚠️ **私人分享，請勿轉傳** — 你受個別邀請才看得到；請勿把內容散布給未受邀者。詳見 [`NOTICE.md`](NOTICE.md)。想邀請別人請直接找擁有者。

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

1. **拿到這個資料夾**：這是**私人 repo**，第一次下載要先登入 GitHub。最省事的方式是裝
   **GitHub CLI**（macOS `brew install gh`，或到 [cli.github.com](https://cli.github.com)
   抓安裝檔），裝好跑 `gh auth login`（選 GitHub.com、HTTPS、用瀏覽器登入），再用
   `gh repo clone <owner>/<repo>` 下載。不想裝也可以在 GitHub 頁面按綠色 **Code →
   Download ZIP** 解壓，只是之後沒辦法一鍵更新。放哪裡都行。
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
在放論文的資料夾裡開 Claude Code，用平常講話的方式說要做什麼：

| 你打這句 | Claude 幫你做 |
|----------|---------------|
| **「幫我寫這篇論文／提案」** | 協作寫作：找文獻、架論證骨架、寫成稿、自己檢查 |
| **「幫我檢查這篇再投」** | 投稿前的品質與格式檢查 |
| **「幫我把這些引用的 PDF 收齊」** | 收集並查證參考文獻 |
| **「誰引用了這篇？有沒有我漏掉的後續研究」** | 引用滾雪球：從一篇（或整份書目）長出該讀而未讀的文獻清單 |
| **「審稿意見回來了，幫我回」** | 逐點回應：拆解意見→逐點裁定→修訂對照→回應信→交付前完整性驗證 |
| **「我這篇短文要擴寫成期刊全文」** | 逆向盤點入線，並盤點文字回收與揭露措辭（擴寫本質上就是重用） |
| **「我要再投一個地方，可以吧？」** | 查投稿狀態表，確認同一份稿件沒有同時在別處審查中 |
| **「這張圖印成黑白會不會看不懂？」** | 圖表色覺可及性：色盲模擬＋灰階對比，並產生模擬圖給你看 |
| **「別再犯同樣的錯」「改 A 又弄壞 B」** | 文件回歸：把抓到的錯寫成一條常駐檢查，改完全庫重掃，復發就擋下 |
| **「有沒有哪篇被撤稿了？」** | 撤稿掃描：整份書目對 Crossref＋OpenAlex 查撤稿，每次交付前重跑 |
| **「這句沒掛引用，站得住嗎？」** | 無引用宣稱掃描：找出沒有引用的量化／因果／最高級句子，逐筆補引用、指出自家資料、或降級措辭 |
| **「稿裡的數字跟分析結果對得上嗎？」** | 數字帳本勾稽：每個數字回溯到產生它的運算；改數字先更帳本再改稿，回歸檢查擋舊值復發 |

> 預設走**最簡單的模式**：只要 Claude ＋ 網路，什麼都不用安裝。之後真的需要更強的工具
> （本機統計、文獻庫、語言檢查）再一次加一個就好。

---

## 隱私

- 這是**私人 repo**，只分享給你信任的人。裡面只有**方法**，沒有任何人的稿件或資料。
- 方法本身要求：**未發表的稿件與研究原始資料永遠留在你自己的電腦**，不上傳雲端、不丟公開的
  AI 偵測器。你生成的個人設定（文風檔、投稿筆記、骨架）也不會被這個 repo 收走
  （見 `.gitignore`）。

---

## 資料夾裡有什麼

| 位置 | 內容 |
|------|------|
| `CLAUDE.md` | **安裝器**：你的 Claude 讀這個來訪談你、生成你的專屬設定。 |
| `method/` | **方法本體**：心法（PHILOSOPHY）、鐵則（IRON-RULES）、完整流程（WORKFLOW）、論證工法（ARGUMENTATION）。 |
| `skills/` | 去個人化的 skill 範本，共七個（協作寫作 / 投稿前檢查 / 收文獻 / 查引用 / 審稿回應 / **文件回歸** / 排版 PDF），你的 Claude 會照你的情況改寫。 |
| `agents/` | 兩個 subagent 範本：英文交付前的去 AI 節奏複查（de-cadencing-scholar）、引用查驗二審（citation-skeptic）。 |
| `tools/` | **現成的本機小工具**，第一天就能用。中文三支（陸用語／中文 AI 味／聲音硬規則）、引用滾雪球、撤稿掃描、無引用宣稱掃描、文件回歸兩支、審稿回應驗證、投稿狀態表皆**零安裝**；英文兩支需一兩個免費離線程式，圖表可及性需 numpy 與 Pillow。見 `tools/README.md`。 |
| `templates/` | 你要填的空白檔（文風檔、投稿筆記、骨架、聲音規則）。 |
| `setup/` | 簡單模式（LITE）、選配的進階工具（TOOLS）、面談問法（INTERVIEW）、從 claude.ai 網頁版上手的引導（WEB）、繁中在地化包（addons/zh-tw）。 |
| `data/academic-vocab/` | 三份開放學術詞表（AWL／AVL／ACL 搭配詞，TSV），投稿前檢查的用字層拿來當錨點，不是自動替換；授權見 `NOTICE.md`。 |
| `examples/` | 一份填好的骨架範例，讓 Claude 有具體參照。 |

---

## 會用到哪些工具

> 一句話版本：**只要 Claude Code 就能開始**。其他都是「有了更好」，而且 Claude 會在
> 你真的需要時才建議裝，一次一個。

### 一定需要的

| 工具 | 用途 | 怎麼取得 |
|------|------|----------|
| **Claude Code** | 整套方法的執行者：訪談你、找文獻、架骨架、寫稿、自我檢查 | [claude.com/claude-code](https://claude.com/claude-code)（需 Claude 訂閱） |
| **Python 3** | 跑隨包附的本機檢查工具 | macOS 要先裝 Xcode Command Line Tools（`xcode-select --install`）或 `brew install python`；Linux 多數發行版內建；Windows 到 python.org 抓安裝檔 |

### 隨包附贈的本機檢查工具（在 `tools/`，詳見 `tools/README.md`）

| 工具 | 檢查什麼 | 額外要裝什麼 |
|------|----------|--------------|
| `zh_localize.py` | 陸用語→台灣用語、台／臺一致性 | 不用 |
| `zh_ai_style.py` | 中文 AI 句法指紋（破折號、三連並列、趨同詞、句長節奏） | 不用 |
| `voice_lint.py` | 你自己的聲音硬規則（交稿前守門，不乾淨不放行） | 不用 |
| `lt_check.sh` | 英文文法＋美英拼字一致性（離線 LanguageTool；有裝 n-gram 資料會自動加掛易混詞統計偵測） | `brew install languagetool pandoc` |
| `ai_style_diag.py` | 英文 AI 指紋（對照你領域已發表論文的百分位） | 自備語料；PDF 輸入才需 `pdftotext` |
| `snowball.py` | 引用滾雪球：誰引用了這篇／這篇引了誰／相近研究，多種子聚合排序 | 不用（免金鑰免註冊） |
| `check_response.py` | 回應信完整性：每點都答了嗎／說要改的真的改了嗎／不接受的有沒有依據 | 不用 |
| `check_submissions.py` | 一稿多投防護：同一份稿件有沒有同時在兩個地方審查中 | 不用 |
| `figure_a11y.py` | 圖表色覺可及性：色盲模擬＋灰階對比，輸出模擬圖供目檢 | `pip install numpy pillow`（PDF 另需 pymupdf） |
| `retraction_scan.py` | 撤稿掃描：整份 .bib 對 Crossref 更新關係＋OpenAlex `is_retracted` 雙源查核；標紅的必人工複核 | 不用（需網路） |
| `uncited_claims_scan.py` | 沒掛引用的量化／因果／最高級宣稱（查引用只看有引用標記的句子，這支補盲區）；中英通吃，逐筆裁決後可加豁免註記 | 不用 |
| `regress.py` | 文件回歸：照專案內的規則檔掃全庫，抓到一次的錯復發就擋下；內建數字帳本比對（舊值復發→FAIL、現值找不到→WARN） | 不用 |
| `dead_rule_check.py` | 回歸規則健檢：哪條規則已經永遠不會觸發（錨點文字改掉了），避免規則集腐爛 | 不用 |

### Claude 自己會上網用的（免費、不用裝、不用註冊）

| 服務 | 用在哪 |
|------|--------|
| Crossref／OpenAlex／Semantic Scholar | 找文獻、驗證 DOI 與書目資料、查撤稿（`tools/refs/retraction_scan.py` 就是打這兩個 API） |
| Unpaywall／arXiv | 抓開放取用的論文 PDF |

### 之後想升級再裝的（選配；能力對照表在 `setup/TOOLS.md`）

| 想要的能力 | 裝什麼 |
|------------|--------|
| 本機統計分析（混合模型、貝氏） | R 或 Python（資料全程留在你電腦） |
| 查稿件裡的統計數字自不自洽（重算 p 值、GRIM） | R 套件 `statcheck`＋`scrutiny` |
| 掃描檔／中文 PDF 抽成乾淨文字 | MinerU（`uv tool install mineru`） |
| 可重跑的分析筆記本 | Jupyter |
| 付費牆內的文獻全文 | 你機構的圖書館 VPN |
| 自己文獻庫的語意檢索（哪篇、哪頁） | 本機 RAG（`setup/TOOLS.md` 有方向） |
| 排版成投稿 PDF | Typst 或 Quarto／LaTeX（用場域官方模板） |
| 英文毫秒級第一遍文法（存檔就報） | Harper（離線，編輯器外掛或 CLI；選配，LanguageTool 仍是主力） |
| 中文全半形、盤古空格自動整理 | autocorrect（`brew install autocorrect`；選配） |
| 收新資料前先問「這個設計答得了問題嗎」 | R 套件 `DeclareDesign`（設計診斷：看 coverage 不只看 power） |

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
  論證工法每招補「何時別用」與實證論文手藝、`setup/TOOLS.md` 補數值雷區與 Harper／autocorrect。
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
