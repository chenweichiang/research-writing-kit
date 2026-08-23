# 研究寫作套件 · Research Writing Kit

**版本 `v1.1.0`**（2026-08）

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
| `skills/` | 去個人化的 skill 範本（協作寫作 / 投稿前檢查 / 收文獻 / 查引用 / **審稿回應** / 排版 PDF），你的 Claude 會照你的情況改寫。 |
| `agents/` | 兩個 subagent 範本：英文交付前的去 AI 節奏複查（de-cadencing-scholar）、引用查驗二審（citation-skeptic）。 |
| `tools/` | **現成的本機小工具**，第一天就能用。中文三支（陸用語／中文 AI 味／聲音硬規則）、引用滾雪球、審稿回應驗證、投稿狀態表皆**零安裝**；英文兩支需一兩個免費離線程式，圖表可及性需 numpy 與 Pillow。見 `tools/README.md`。 |
| `templates/` | 你要填的空白檔（文風檔、投稿筆記、骨架、聲音規則）。 |
| `setup/` | 簡單模式（LITE）、選配的進階工具（TOOLS）、面談問法、繁中在地化包。 |
| `examples/` | 一份填好的骨架範例，讓 Claude 有具體參照。 |

---

## 會用到哪些工具

> 一句話版本：**只要 Claude Code 就能開始**。其他都是「有了更好」，而且 Claude 會在
> 你真的需要時才建議裝，一次一個。

### 一定需要的

| 工具 | 用途 | 怎麼取得 |
|------|------|----------|
| **Claude Code** | 整套方法的執行者：訪談你、找文獻、架骨架、寫稿、自我檢查 | [claude.com/claude-code](https://claude.com/claude-code)（需 Claude 訂閱） |
| **Python 3** | 跑隨包附的中文檢查工具 | macOS／Linux 內建，不用裝 |

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

### Claude 自己會上網用的（免費、不用裝、不用註冊）

| 服務 | 用在哪 |
|------|--------|
| Crossref／OpenAlex／Semantic Scholar | 找文獻、驗證 DOI 與書目資料、查撤稿 |
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

---

## 給進階使用者
所有 skill 都是純 Markdown 的 `SKILL.md`，Claude Code 會自動辨識。想手動掛成全域 skill，
把 `skills/<name>/` 複製或 symlink 到 `~/.claude/skills/` 即可；`agents/` 的兩個 subagent
範本同理，掛到 `~/.claude/agents/`（或專案的 `.claude/agents/`）。但還是建議讓 `CLAUDE.md`
的安裝流程幫你客製，不要照抄原版。

---

## 版本紀錄

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
