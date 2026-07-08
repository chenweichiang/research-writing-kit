# 研究寫作套件 · Research Writing Kit

> ⚠️ **私人分享，請勿轉傳** — 你受個別邀請才看得到；請勿把內容散布給未受邀者。詳見 [`NOTICE.md`](NOTICE.md)。想邀請別人請直接找擁有者。

> 一套用 AI 協助寫**研究論文與計畫提案**的方法，而且它會**自己安裝、自己客製**。
> 你不用懂 AI、不用會設定——把資料夾交給你的 Claude，它會問你幾個問題，然後幫你把
> 適合你的工具建好。

**English tl;dr:** A method for AI-assisted academic writing that installs and
customizes itself. Open this folder in Claude Code and say *"Read CLAUDE.md and set
me up."* Your Claude interviews you, then generates writing skills tailored to your
field, language, and voice. See `CLAUDE.md` (the installer) and `method/` (the method).

---

## 這是什麼

不是一個「寫好給你貼」的模板，而是一套**方法**加一個會自我安裝的小工具箱。核心精神：

- **你擁有想法與論證，AI 負責跑腿**：找文獻、查證引用、架論證骨架、寫成稿、還自己檢查。
- **先架骨架再寫字**：不從空白頁生成（那正是「AI 味」的來源），先把論證結構立好，散文綁著它寫。
- **絕不編造引用**：每一條文獻都真的抓下來、確認方向對；查不到就標「未驗證」，不假裝。
- **像你的聲音**：用你的母語寫時，對齊你自己的文風，不磨成通用 AI 腔。
- **誠實內建**：效果量＋信賴區間（不只 p 值）、資料留在你電腦、交稿前去 AI 味、乾淨二審。

---

## 怎麼用（三步）

### 1. 拿到這個資料夾
朋友把 repo 分享給你後，用 Git 下載，或直接下載 ZIP 解壓。放哪裡都行。

### 2. 在資料夾裡打開 Claude Code
在終端機進到這個資料夾，輸入 `claude`。

### 3. 貼這一句話
> **「讀 CLAUDE.md，幫我設定。」**（英文：`Read CLAUDE.md and set me up.`）

接下來你的 Claude 會：
1. **問你幾個問題**——你寫什麼、用什麼語言、想投哪、有沒有自己的舊稿可以讓它學你的文風。
2. **幫你生出專屬工具**——依你的答案，把「協作寫作」「投稿前檢查」等 skill 客製好、裝到你的
   Claude 裡。
3. **教你實際會用到的幾句話**，例如「幫我寫這篇」「幫我檢查這篇」。然後你就可以開始了。

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
| `skills/` | 去個人化的 skill 範本（協作寫作 / 投稿前檢查 / 收文獻 / 查引用 / 排版 PDF），你的 Claude 會照你的情況改寫。 |
| `tools/` | **現成的本機小工具**，第一天就能用。中文三支（陸用語／中文 AI 味／聲音硬規則）**零安裝**；英文兩支需一兩個免費離線程式。見 `tools/README.md`。 |
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
| `lt_check.sh` | 英文文法＋美英拼字一致性（離線 LanguageTool） | `brew install languagetool pandoc` |
| `ai_style_diag.py` | 英文 AI 指紋（對照你領域已發表論文的百分位） | 自備語料；PDF 輸入才需 `pdftotext` |

### Claude 自己會上網用的（免費、不用裝、不用註冊）

| 服務 | 用在哪 |
|------|--------|
| Crossref／OpenAlex／Semantic Scholar | 找文獻、驗證 DOI 與書目資料、查撤稿 |
| Unpaywall／arXiv | 抓開放取用的論文 PDF |

### 之後想升級再裝的（選配；能力對照表在 `setup/TOOLS.md`）

| 想要的能力 | 裝什麼 |
|------------|--------|
| 本機統計分析（混合模型、貝氏） | R 或 Python（資料全程留在你電腦） |
| 可重跑的分析筆記本 | Jupyter |
| 付費牆內的文獻全文 | 你機構的圖書館 VPN |
| 自己文獻庫的語意檢索（哪篇、哪頁） | 本機 RAG（`setup/TOOLS.md` 有方向） |
| 排版成投稿 PDF | Typst 或 Quarto／LaTeX（用場域官方模板） |

---

## 給進階使用者
所有 skill 都是純 Markdown 的 `SKILL.md`，Claude Code 會自動辨識。想手動掛成全域 skill，
把 `skills/<name>/` 複製或 symlink 到 `~/.claude/skills/` 即可——但建議還是讓 `CLAUDE.md`
的安裝流程幫你客製，而不是照抄原版。
