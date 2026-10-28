# Changelog · 變更紀錄

版號採語意化版本（主版號．次版號．修訂號）：次版號加一表示方法、skill 或工具有新增或行為改變，修訂號加一表示只改文字、詞表或修正。
Versions follow semantic versioning (major.minor.patch): a minor bump adds or changes a method, skill or tool; a patch bump changes only wording, term tables or fixes.

## v1.11.5（2026-10-29）

- `zh_gloss_scan.py` 遇到一長串用 and 連起來的英文（例如引述的英文原句）而後面沒有年份時，處理時間會隨 and 的數量成倍增加，十幾個就要好幾秒，再多就像當掉；已改寫，判斷結果不變。`md_prose.py` 的多鍵引用與 `figure_check.py` 的複數圖表引用也照同樣方式改寫。這幾處是 GitHub 程式碼掃描（CodeQL）標出來的。
  `zh_gloss_scan.py` slowed down exponentially on a long run of English joined by "and" with no year after it (a quoted English sentence, for example): a dozen took seconds, more looked like a hang. Rewritten with the same results. The multi-key citation pattern in `md_prose.py` and the plural figure reference in `figure_check.py` are rewritten the same way. GitHub code scanning (CodeQL) flagged these.
- `pdf_fetch.py` 判斷出版社改看網址的主機名稱，不再只要網址裡出現網域字串就算；`refs_common.py` 從 bib 的 url 欄位讀 DOI 時也一樣，沒寫 `https://` 的 DOI 網址現在也認得。
  `pdf_fetch.py` recognises a publisher by the URL's host name rather than by the domain appearing anywhere in the URL; `refs_common.py` does the same when it reads a DOI from a bib entry's url field, and now also accepts DOI URLs written without `https://`.

## v1.11.4（2026-10-29）

- `tools/regress/dead_rule_check.py` 在 Python 3.9 上會出錯，已修正。CI 改在 Python 3.9 與 3.13 上各跑一次，並裝齊所有選配套件與程式；有任何測試被略過就算失敗。兩份 README 寫明需要 Python 3.9 或更新。
  `tools/regress/dead_rule_check.py` failed on Python 3.9; fixed. CI now runs on Python 3.9 and 3.13 with every optional package and program installed, and fails if any test is skipped. Both READMEs state that Python 3.9 or newer is required.
- 每支工具的檔頭用內嵌中繼資料（PEP 723）寫明它要的 Python 套件，裝了 uv 就能用 `uv run tools/<資料夾>/<工具>.py` 直接執行；新增測試，檢查標頭存在、且沒有備案的匯入都有列出。
  Each tool declares the Python packages it needs in an inline metadata block (PEP 723) at the top of the file, so with uv installed `uv run tools/<folder>/<tool>.py` runs it directly; a new test checks that the block is present and lists every import that has no fallback.
- README 與專案頁對引用查核與資料去向的說法改得更準確：方法規定每條文獻都要抓到原文、確認方向才能寫進稿子；稿件與資料除了 Claude 本身，不交給其他線上服務。
  The READMEs and the project page describe citation checking and where data goes more precisely: the method requires each reference to be fetched and its direction confirmed before it goes into a draft, and drafts and data go to no online service other than Claude itself.
- 新增行為準則（Contributor Covenant 3.0）、issue 表單（回報問題、建議）、pull request 範本與 Dependabot（GitHub Actions）；CI 用到的 Actions 改釘在 commit SHA，權限只給讀取。
  Added a code of conduct (Contributor Covenant 3.0), issue forms (bug report, suggestion), a pull request template and Dependabot for GitHub Actions; the Actions used in CI are pinned to commit SHAs with read-only permissions.
- `CITATION.cff` 加上作者的 ORCID。
  `CITATION.cff` adds the author's ORCID.

## v1.11.3（2026-10-29）

- 新增 `SECURITY.md`：哪些問題算漏洞、怎麼透過 GitHub 的 Report a vulnerability 私下回報；`CONTRIBUTING.md` 連過去，repo 也開啟了私下回報。
  Added `SECURITY.md`: what counts as a vulnerability and how to report one privately through GitHub's Report a vulnerability; `CONTRIBUTING.md` links to it, and private reporting is enabled on the repository.
- `tools/common/md_prose.py` 的說明文字整理。
  Docstring wording in `tools/common/md_prose.py` tidied.

## v1.11.2（2026-10-28）

- `zh_ai_style.py` 拿掉選配的外部後設論述量表整合（該專案已不公開）；`setup/TOOLS.md` 與繁中選配包裡的說明一併移除。
  `zh_ai_style.py` drops the optional external metadiscourse-scale integration (that project is no longer public); the matching notes in `setup/TOOLS.md` and the zh-TW add-on are removed.
- `pdf_fetch.py` 加上負責任使用的限制：瀏覽器層每篇之間暫停（`--pause`，預設 5 秒）、單次最多 100 篇（`--max-browser`），也不再自動點「確認你是人類」。說明文件寫明出版社條款允許為自己的研究下載單篇，不允許大量下載。
  `pdf_fetch.py` adds responsible-use limits: the browser layer pauses between items (`--pause`, default 5 s), handles at most 100 per run (`--max-browser`) and no longer clicks a "verify you are human" check. The docs state that publishers' terms allow single articles for your own research, not bulk downloading.
- `citation-skeptic` 與 `verify-citations` 不再引用未發表的模型比較數字，改成文字說明。
  `citation-skeptic` and `verify-citations` no longer quote unpublished model-comparison figures.
- 新增 `pyproject.toml`（ruff 設定），CI 加上 ruff 檢查；`except Exception: pass` 改成捕捉具體的例外，無法確定例外種類的地方註明為何可以忽略。
  Added `pyproject.toml` with ruff settings and a ruff step in CI; `except Exception: pass` blocks now catch specific exceptions, or say why ignoring is safe where the exception types cannot be known.

## v1.11.1（2026-10-28）

- 版本紀錄從兩份 README 移到這份 CHANGELOG.md，README 本文精簡。
  Version history moves from the two READMEs into this CHANGELOG.md; the READMEs are shortened.
- 台灣用語詞表 `tools/zh-tw/zh_tw_terms.tsv` 的檔頭改寫成給使用者看的說明。
  The header of the Taiwan-Mandarin term table `tools/zh-tw/zh_tw_terms.tsv` is rewritten as a note for readers.
- 維護者用的 `release_check.py` 把會指名維護者的比對樣式移到不進版控的本機設定檔。
  The maintainer's `release_check.py` moves the patterns that would name the maintainer into an untracked local settings file.
- `zh_ai_style.py` 與 `wordcount_approx.py` 的 `--help` 不再被當成檔名讀；新增測試，涵蓋五支命令列工具的 `--help`。
  `--help` is no longer read as a file name by `zh_ai_style.py` and `wordcount_approx.py`; a new test covers `--help` for five command-line tools.
- 工具的說明文字（docstring）整理；新增 `CONTRIBUTING.md` 與 `CITATION.cff`。
  Tool docstrings are tidied; `CONTRIBUTING.md` and `CITATION.cff` are added.
- 作者英文名統一為 Chenwei Chiang。
  The author's name in English is unified as Chenwei Chiang.

## v1.11.0（2026-10-25）

- 新增第八個 skill `submit`：送件前的就緒判讀（重讀官方頁、截止時間換成你的時區、評分交乾淨審稿人）、從源檔建 Word 並回轉比對、照場域的計算方式算字數、對官方範本比格式、雙盲匿名檢查，以及送出後的確認信、送件紀錄、投稿台帳與版號收尾。
  New eighth skill `submit`: a readiness verdict before sending (re-read the official page, convert the deadline to your timezone, scoring by a clean reviewer), building the Word file from source and comparing it back, counting words the venue's way, a format diff against the official template, a double-blind anonymization check, and the wrap-up after sending (confirmation e-mail, submission record, ledger, version).
- 配套工具六支在 `tools/submit/`：`deadline.py`、`docx_roundtrip.py`、`word_count.sh`、`wordcount_approx.py`、`template_diff.py`、`anon_check.py`。
  Six matching tools in `tools/submit/`: `deadline.py`, `docx_roundtrip.py`, `word_count.sh`, `wordcount_approx.py`, `template_diff.py`, `anon_check.py`.
- 合作工具兩支：`tools/collab/docx_diff.py` 比對合作者傳回、沒開追蹤修訂的 Word 檔；`tools/collab/coding_pack.py` 把 codebook 與作答做成第二編碼者的離線判讀網頁，再轉回編碼表算 kappa。`method/COLLABORATION.md` 新增對應段落與群組聊天意見的處理。
  Two collaboration tools: `tools/collab/docx_diff.py` compares a Word file a co-author returns without tracked changes; `tools/collab/coding_pack.py` turns a codebook and the responses into an offline coding page for a second coder and scores kappa from the export. `method/COLLABORATION.md` gains matching sections and a note on feedback from group chats.
- 既有工具補強：`overclaim_lint.py` 多抓「就作者所知／尚無研究」類宣稱與沒標年份的官方文件；`version_check.py` 抓改了 `VERSION` 卻沒重建的交付檔並印出絕對路徑；`refs_common.py` 的內容驗證先做 NFKC 正規化、中文標題直接比字串；`missing_refs.py` 預設重驗資料夾裡已有的檔。
  Existing tools: `overclaim_lint.py` also reports nobody-did-it claims and official documents cited without a year; `version_check.py` catches delivered files not rebuilt after `VERSION` changed and prints their absolute paths; content verification in `refs_common.py` normalises text (NFKC) and compares Chinese titles as strings; `missing_refs.py` re-verifies files already in the folder by default.
- skill 與方法層：`co-author` 第一個 commit 就是 `.gitignore`、Phase 1.5 加場域比較表、術語首現預設寫定義句；`paper-review` 動手前先估每條增減字數；`verify-citations` 修訂迴圈可只重查有改動的引用，投稿前最後一輪全量，MinerU 改用 4.x 的 `mineru-kit parse`；四個 skill 開頭提醒對話壓縮後要重新叫用。
  Skills and method: `co-author` makes `.gitignore` the first commit, adds a venue comparison table at Phase 1.5 and defaults to a defining sentence at a term's first appearance; `paper-review` estimates each finding's change in words before acting; `verify-citations` may re-check only changed citations during revision, with a full check before submission, and uses the MinerU 4.x `mineru-kit parse` form; four skills open with a reminder to invoke them again after a context compaction.

## v1.10.1（2026-10-09）

- 台灣用語詞表新增兩條：儀表板、視覺化。
  Two entries added to the Taiwan-Mandarin term table: 儀表板 (dashboard) and 視覺化 (visualization).

## v1.10.0（2026-10-04）

- 方法層新增四份文件：`VERSIONING.md`（版號＝送出次數．內容．措辭，`VERSION` 檔為唯一來源，交付資料夾只放一版）、`COLLABORATION.md`（合作者主筆的稿與多人計畫書：原檔不改、每句要指得回來源）、`COMPRESSION.md`（超頁超字的壓縮程序）、`AI_DISCLOSURE.md`（八家國際出版社的生成式 AI 規定與聲明寫法）。
  Four new method files: `VERSIONING.md` (version = times sent out . content . wording; `VERSION` is the only source; one version in the delivery folder), `COLLABORATION.md` (co-authored manuscripts and multi-team proposals: never edit the original, every sentence traceable to a source), `COMPRESSION.md` (cutting to a page or word limit), `AI_DISCLOSURE.md` (eight international publishers' generative-AI rules and how to write the statement).
- 新工具六支：`figures/figure_check.py`（排好的 PDF 圖表檢查）、`collab/source_trace.py`（合作者稿逐句溯源）、`versioning/version_check.py`（交付前查版號）、`review/review_rounds.py`（審查輪次收斂與停審）、`refs/missing_refs.py` 與 `inbox_ingest.py`（缺件清單與下載匣收件）。
  Six new tools: `figures/figure_check.py` (figures and tables in the typeset PDF), `collab/source_trace.py` (sentence-by-sentence trace of a co-authored draft), `versioning/version_check.py` (pre-delivery version check), `review/review_rounds.py` (review-round convergence and the stop condition), `refs/missing_refs.py` and `inbox_ingest.py` (the missing list and filing hand downloads).
- `zh_gloss_scan.py` 加 `--en` 列出中文稿裡的英文夾註；`regress.py` 的 R6 加 `internal_suspect`，施工進度句報 WARN。
  `zh_gloss_scan.py` gains `--en` for English glosses inside Chinese prose; `regress.py` R6 gains `internal_suspect`, reporting progress talk as WARN.
- skill 層：`co-author` 加一句話觸發的「全套潤修」、Phase 1.5 的場域相容性與貢獻閘門；`paper-review` 加輪次收斂與 1f 圖表檢查；`fetch-refs` 加缺件清單與收件；`doc-regress` 補 WARN 層說明。
  Skills: `co-author` gains the one-line "full polish", the venue-compatibility check and contribution gate at Phase 1.5; `paper-review` gains review-round convergence and the 1f figure check; `fetch-refs` gains the missing list and filing; `doc-regress` documents the WARN tier.
- `RIGOR_PROCESS.md` 階段 11 補上人工判讀看過 AI 預標時要揭露的程序事實。
  `RIGOR_PROCESS.md` Stage 11 adds what to disclose when a human coder could see the AI's pre-labels.

## v1.9.5（2026-10-04）

- `verify-citations` 的 OpenLibrary 說明改成照實記錄：舊端點 `/api/books?bibkeys=` 官方標為 Legacy，仍以 `/isbn/<isbn>.json` 為準。
  `verify-citations` now records OpenLibrary as documented: the legacy `/api/books?bibkeys=` endpoint may be phased out, so `/isbn/<isbn>.json` stays the source.
- `co-author`、`paper-review`、`verify-citations`、`rebuttal` 的 description 補上內文早已支援、卻沒寫進觸發詞的用途（擴寫、檢索留痕、圖表可及性、無引用宣稱）；`co-author` 的 description 精簡到 Claude Code skill 清單的長度上限內。
  The descriptions of `co-author`, `paper-review`, `verify-citations` and `rebuttal` now name uses their bodies already supported (expansion, the search log, figure accessibility, uncited claims); the `co-author` description is shortened to fit Claude Code's skill-listing cap.
- `rebuttal` 內文補上審稿人問檢索方法時以 `search-log.md` 回答的做法。
  The `rebuttal` body gains the way to answer a reviewer's search-method question from `search-log.md`.

## v1.9.4（2026-09-28）

- `NOTICE.md` 引用範例的版本號改為目前版本，並納入發版對帳。
  The citation example in `NOTICE.md` now carries the current version and is covered by the release sync check.
- 從這一版起每個版本在 GitHub 也發 Release，不再只有標籤。
  From this version on, each release is also published as a GitHub Release, not only as a tag.

## v1.9.3（2026-09-28）

- `fetch-refs` 的檔案比對補上短標題的兩道檢查：首頁印著別的 DOI、或標題實詞太少且第一作者姓氏在前八頁沒出現，就降成 `LOW-CONFIDENCE` 並寫出理由；回報分別列出 `LOW-CONFIDENCE`、`PREVIEW-ONLY` 與拿不到的三類。
  `fetch-refs` adds two checks for short titles: a file whose first page prints a different DOI, or whose title has few content words and no first-author surname in the first eight pages, is downgraded to `LOW-CONFIDENCE` with the reason; the report lists `LOW-CONFIDENCE`, `PREVIEW-ONLY` and the three kinds of misses separately.
- `verify-citations` 的 OpenAlex 標題查詢先去掉逗號、問號、星號等語法字元；查詢失敗報「未能查核」，不報成查無。
  `verify-citations` strips commas, question marks, asterisks and other syntax characters before an OpenAlex title lookup; a failed query is reported as "not checked", never as "not found".
- `paper-review` 新增「稿件是誰的」：替期刊審別人的稿時，預設只把本機工具的指令交給使用者自己跑。
  `paper-review` adds "whose manuscript is it?": when reviewing someone else's submission, by default only the commands for the local tools are handed over.
- `rebuttal` 修訂表的欄位說明補上 `evidence`；`doc-regress` 的死規則說明補齊三種判定；README 工具表 `dead_rule_check.py` 的描述更正。
  The `rebuttal` revision-table column list adds `evidence`; the `doc-regress` dead-rule paragraph names all three checks; the README row for `dead_rule_check.py` is corrected.

## v1.9.2（2026-09-28）

- OpenAIRE 舊 Search API 已停用，`pdf_fetch.py` 改走 Graph API V3。
  OpenAIRE's old Search API was retired, so `pdf_fetch.py` now calls Graph API V3.
- 修正 Frontiers 這類 `/articles/<DOI>/pdf` 網址被誤判成別篇而丟棄的問題；同一篇只查一次 API。
  Fixes a url like Frontiers' `/articles/<DOI>/pdf` being mistaken for a different paper and discarded; one DOI now calls the API once.

## v1.9.1（2026-09-26）

- `lit_map.py` 的主題查詢先把 OpenAlex 會當成語法的字元（逗號、問號、星號、驚嘆號、直線）換成空白，帶逗號的主題原本查不到東西。
  `lit_map.py` blanks out the characters OpenAlex reads as syntax (comma, question mark, asterisk, exclamation mark, vertical bar) before a topic query; a topic with a comma used to return nothing.

## v1.9.0（2026-09-26）

- 鐵則 5 改為「論文照場域的語域寫，信件才照你的聲音」：論文、計畫書、申請書拿同領域已發表論文當準繩，每項語言特徵落在真人論文的 p10 到 p90 區間內；從舊稿學來的文風只用在信件與自述。
  Iron Rule 5 becomes "papers follow the field's register; only letters follow your voice": papers, proposals and applications are measured against published papers in the same field, each language feature inside the p10 to p90 band; the voice learned from past writing is used only for letters and statements.
- 安裝器改問能不能收一批同領域已發表論文（完整模式 30 篇以上）與有沒有自己寫的信件或自述；lite 模式改由 Claude 閱讀目標期刊的範例論文比對。
  The installer now asks whether you can collect published papers from your field (full mode: 30 or more) and whether you have letters or statements of your own; lite mode compares by reading sample papers from the target journal.
- `co-author` 新增 Phase 5.5 母語潤稿：`register_profile.py` 量出偏離清單，`en-native-editor` 或 `zh-tw-native-editor` 只交改動清單，`polish_check.py` 在寫回前擋下數字、引用與鎖定術語的變動。新增 `zh_register.py`（中文 52 項特徵）；`metadiscourse_en.py` 與 `biber_diag.py` 加 `--groups`、`--json`；`voice_lint.py` 加 `--paper`。
  `co-author` gains Phase 5.5 native polish: `register_profile.py` measures the deviation list, `en-native-editor` or `zh-tw-native-editor` return change lists only, and `polish_check.py` blocks changed numbers, citations and locked terms before writing back. New `zh_register.py` (52 Chinese features); `metadiscourse_en.py` and `biber_diag.py` gain `--groups` and `--json`; `voice_lint.py` gains `--paper`.
- 新增 `agents/clean-reviewer.md`，終審、審稿模擬與裁定表交給乾淨脈絡的 subagent，推理強度釘在範本的 frontmatter；subagent 範本由兩個變成五個。
  New `agents/clean-reviewer.md`: the final review, reviewer simulation and verdict table go to a clean-context subagent with the effort pinned in its frontmatter; the subagent templates go from two to five.
- 文獻工具：四支打 OpenAlex 的工具可選帶免費 API key（`OPENALEX_API_KEY`）；`verify-citations` 帶頁碼或前綴的引用只取 `@` 後的鍵，跑完對帳「查過的文獻數＝稿中不重複的鍵數」，Crossref 只有 404 算查無。
  Literature tools: the four tools that call OpenAlex take an optional free API key (`OPENALEX_API_KEY`); in `verify-citations`, citations with a locator or prefix are reduced to the key after `@`, a run reconciles the count of checked references against the distinct keys in the draft, and only a Crossref 404 counts as "not found".
- `doc-regress`：`dead_rule_check.py` 改以「從哪一行離開」判定死規則；`regress.py` 的引用鍵不再要求四位數年份，並排除 Quarto 交互參照。新增維護者用的 `tools/dev/release_check.py` 與 GitHub Actions CI。
  `doc-regress`: `dead_rule_check.py` decides by the line a rule left through; `regress.py` no longer requires a four-digit year in citation keys and skips Quarto cross-references. New maintainer gate `tools/dev/release_check.py` and a GitHub Actions CI.

## v1.8.1（2026-09-20）

- 引用二審統一改為需要判斷的工作，要用最強的一級模型；`skills/verify-citations` 與 `agents/citation-skeptic` 原本寫成便宜模型即可，與 README 矛盾。
  The citation second review is now consistently judgment work for the strongest model tier; `skills/verify-citations` and `agents/citation-skeptic` had called it a job for a cheaper model, contradicting the README.
- README 工具表補齊先前漏列的工具與模組，`dead_rule_check.py` 的描述補成三項。
  The README tools table adds the tools and modules it had been missing, and the `dead_rule_check.py` row names all three checks.
- `verify-citations` 補作者欄粒度的警告：Crossref 的 `family` 是姓氏、OpenLibrary 的 `author_name` 是全名，只比整串會把正確引用報成錯的。
  `verify-citations` warns about author-field granularity: Crossref's `family` is a surname and OpenLibrary's `author_name` a full name, so whole-string comparison misreports correct references.
- `dead_rule_check.py` 加未定義呼叫偵測：規則呼叫了檔案裡不存在的函式會被當成早退而診斷錯方向。
  `dead_rule_check.py` gains undefined-call detection: a rule calling a function the file never defines used to be filed as an early return.

## v1.8.0（2026-09-20）

- `pdf_fetch.py` 的 OpenAIRE 改成正確解析 JSON，並把機構典藏的紀錄頁交給瀏覽器層；原本用 `\.pdf` 正則在整包 JSON 撈，永遠零命中。
  `pdf_fetch.py` now parses OpenAIRE's JSON and hands repository landing pages to the browser layer; the old `\.pdf` regex over the whole blob never matched anything.
- 同一支檔案裡 `extra_urls`、`cookies_for()` 與 urllib 後備路徑的 cookie 移交原本都沒接上，現已接通。
  In the same file, `extra_urls`, `cookies_for()` and the cookie handoff in the urllib fallback were never wired; they now are.
- `dead_rule_check.py` 新增未註冊規則偵測，並加 `RULES_DEREGISTERED` 慣例記錄刻意除役的規則。
  `dead_rule_check.py` reports unregistered rules and adds the `RULES_DEREGISTERED` convention for deliberate deregistration.
- `regress.py` 的 `ledger_rows` 分清「沒設定」與「設定了但檔案不見」兩種狀態。
  `ledger_rows` in `regress.py` distinguishes "not configured" from "configured but the file is missing".
- `verify-citations` 的 OpenLibrary 改用 `/isbn/<isbn>.json`，並註明 `search.json?q=isbn:` 是模糊檢索。
  `verify-citations` uses OpenLibrary's `/isbn/<isbn>.json` and notes that `search.json?q=isbn:` is a fuzzy search.

## v1.7.2（2026-09-17）

- 隱私說明改成照實寫：隨包工具與統計在本機跑、線上檢索只送書目資料、稿件不交給第三方服務，並明講 Claude Code 會把它讀到的內容送到 Anthropic 處理。README、`CLAUDE.md`、`method/`、`setup/`、三個 skill 與 `tools/` 說明一併改。
  The privacy statement now says what actually happens: bundled tools and statistics run locally, online lookups send only bibliographic data, drafts are not handed to third-party services, and Claude Code sends what it reads to Anthropic. The READMEs, `CLAUDE.md`, `method/`, `setup/`, three skills and the `tools/` notes change together.

## v1.7.1（2026-09-17）

- 文件清掉長破折號：英文文件只留原文引句、文獻標題與表格裡代表「無」的那幾個，中文文件清到零；改法依作用換成句號、逗號、括號或冒號，分號與對比句數量沒有增加。
  The documents drop their em dashes: the English ones keep only those inside quoted sources, paper titles and table cells meaning "none", the Chinese ones go to zero; each dash became a period, comma, parenthesis or colon, with no rise in semicolons or contrast sentences.
- 修正 `skills/co-author/SKILL.md` 的 frontmatter 含「冒號＋空格」而無法被嚴格 YAML 解析的問題；所有 skill 與 agent 的 frontmatter 都能解析。
  Fixes the `skills/co-author/SKILL.md` frontmatter, which a strict YAML parser rejected over a colon followed by a space; all skill and agent frontmatter now parses.

## v1.7.0（2026-09-17）

- 方法決策（`METHOD_DECISION.md`、`METHOD_CARDS.md`）：先查同類論文再選方法，至少 8 篇讀方法段、5 篇抽出分析做法；38 張分析卡附決策索引與 12 條條件警訊。範本與檢查程式：`templates/method-decision.template.md`、`tools/method/method_decision_check.py`。
  Method decisions (`METHOD_DECISION.md`, `METHOD_CARDS.md`): check comparable papers before choosing, reading at least eight methods sections and extracting the analysis from five; 38 method cards with a decision index and twelve condition-triggered warnings. Template and checker: `templates/method-decision.template.md`, `tools/method/method_decision_check.py`.
- 嚴謹研究流程（`RIGOR_PROCESS.md`）：十三階段，唯一的硬閘門是資料收集前計畫（`analysis-plan.template.md`、`analysis_plan_check.py`）。新增 `literature-matrix.template.md`、`refs/lit_map.py`、`method/tea_second_opinion.py`；繁中範本在 `setup/addons/zh-tw/templates/`。
  Rigorous research process (`RIGOR_PROCESS.md`): thirteen stages, with the pre-data-collection plan as the one hard gate (`analysis-plan.template.md`, `analysis_plan_check.py`). New `literature-matrix.template.md`, `refs/lit_map.py`, `method/tea_second_opinion.py`; Traditional Chinese templates in `setup/addons/zh-tw/templates/`.
- 對比句改看總量：`ai_style_diag.py` 與 `zh_ai_style.py` 把各種對比句型一起算，超過基線 p90 就逐句列出，`--gate` 可擋下一步。新增 `biber_diag.py`、`bundle_diag.py`、`metadiscourse_en.py` 與 `submissions/style_reaudit.py`。
  Contrast sentences are counted in total: `ai_style_diag.py` and `zh_ai_style.py` count every contrast frame together, list each sentence past the baseline p90, and `--gate` can block the next step. New `biber_diag.py`, `bundle_diag.py`, `metadiscourse_en.py` and `submissions/style_reaudit.py`.
- `setup/TOOLS.md` 補上 bibliometrix、ASReview、Tea、Argdown，以及會上傳稿件或資料、不建議使用的工具清單。
  `setup/TOOLS.md` adds bibliometrix, ASReview, Tea and Argdown, and a list of tools not recommended because they upload manuscripts or data.

## v1.6.0（2026-09-14）

- 中文學術語體四條入鏈：小節標題名詞短語、對比句只留承重的、超過 120 字拆句、術語首現只處理一次。`zh_ai_style.py` 加對比句密度與長句清單，`voice_lint.py` 加句型標題與八股套語規則，新增 `zh_gloss_scan.py` 盤點括號夾註；規則同步進 co-author、paper-review 與繁中在地化包。
  Four academic-register rules for Chinese enter the pipeline: noun-phrase headings, contrast frames only where they carry weight, sentences over 120 characters split, a term handled once at first mention. `zh_ai_style.py` gains frame density and a long-sentence list, `voice_lint.py` gains heading and stock-closer rules, new `zh_gloss_scan.py` inventories parenthetical asides; the rules are mirrored in co-author, paper-review and the zh-TW add-on.
- 英文 `ai_style_diag.py` 加 LLM 趨同詞密度（隨包 `en_slop_terms.tsv`），以你的語料算百分位並印出命中的詞。
  English `ai_style_diag.py` adds LLM convergence-word density (bundled `en_slop_terms.tsv`), as a percentile against your corpus with the words that carry it.
- 取檔：沒有 DOI 的條目改讀 arXiv `eprint`，再以標題在 arXiv 與 OpenAlex 精確比對，只有專書交回人工；對 arXiv 加節流與 429 退避。
  Retrieval: entries without a DOI are read from the arXiv `eprint`, then resolved by exact title match on arXiv and OpenAlex; only books go back to you. arXiv calls are throttled with 429 back-off.
- `verify-citations` 補上 `UNGROUNDED` 的意思是「該判定不可信」而非「該判定錯」，以及專書比對的固定雜訊來源。
  `verify-citations` records that `UNGROUNDED` means "this verdict cannot be trusted", not "this verdict is wrong", and the structural false matches for books.

## v1.5.0（2026-08-30）

- 新增 `tools/refs/pdf_fetch.py`，取檔分三層：OA 源（增補 Europe PMC、CORE、OpenAIRE）、`curl_cffi` TLS 偽裝、真實 Chrome 持久 profile；最後一層才過得了 Cloudflare 出版社。
  New `tools/refs/pdf_fetch.py` fetches in three layers: open-access sources (adding Europe PMC, CORE, OpenAIRE), `curl_cffi` TLS impersonation, and a real Chrome on a persistent profile, which is the layer that clears Cloudflare publishers.
- 拿不到的檔一律分類成 `PAYWALL`、`CAPTCHA`、`NO-LINK`，每一筆都有下一步。
  Every miss is classified `PAYWALL`, `CAPTCHA` or `NO-LINK`, so each one has a next step.
- 記下三個取檔雷區：`/doi/pdf/` 常不是 PDF（一律驗 `%PDF-`）、Elsevier 網址含一次性 token、連結發現要看 class 與 aria-label；Zotero translation-server 拿不到 PDF 連結。
  Three retrieval pitfalls recorded: `/doi/pdf/` is often not a PDF (always check for `%PDF-`), Elsevier URLs carry a one-time token, link discovery must read class and aria-label; Zotero translation-server cannot return PDF links.

## v1.4.0（2026-08-29）

- 新增 `tools/claims/overclaim_lint.py`（中英雙語，四類：絕對化、程度誇大、證據強度、最高級；只報不改），去 AI 味補上消過度宣稱這一半；引述原文與引號內的對象語言不掃。
  New `tools/claims/overclaim_lint.py` (English and Traditional Chinese; four categories: absolute, intensifier, evidence-strength, superlative; report-only) completes the de-AI pass with overclaim removal; quoted source text is out of scope.
- 接進 `co-author` Phase 5 與 6-3、`paper-review` 第 1 與第 3 層、`WORKFLOW.md` Phase 5 與 6；`de-cadencing-scholar` 的 tic 由五類擴為六類。
  Wired into `co-author` Phases 5 and 6-3, `paper-review` layers 1 and 3 and `WORKFLOW.md` Phases 5 and 6; `de-cadencing-scholar` goes from five tics to six.

## v1.3.0（2026-08-25）

- 新增第七個 skill `doc-regress`：抓到一次錯就寫成常駐檢查，含數字帳本模板、`regress.py` 與 `dead_rule_check.py`。
  New seventh skill `doc-regress`: a caught mistake becomes a standing check, with the numbers ledger template, `regress.py` and `dead_rule_check.py`.
- 新增 `refs/retraction_scan.py`（Crossref 與 OpenAlex 雙源撤稿掃描，每次交付重掃）與 `claims/uncited_claims_scan.py`（沒掛引用的量化、因果、最高級宣稱）。
  New `refs/retraction_scan.py` (retraction scan against Crossref and OpenAlex, rerun on every delivery) and `claims/uncited_claims_scan.py` (quantitative, causal and superlative claims with no citation).
- `co-author` 補鐵則「檔案是唯一權威」、Phase 1A 檢索留痕、Phase 3.5 設計診斷、Phase 6 交付前清單、Phase 7「先更帳本再改稿」；`paper-review` 補 Step 0 讀 `ADJUDICATED.md`、質性四項與報告準則、投稿聲明六件套。
  `co-author` gains the iron rule "the file is the single source of truth", a Phase 1A search log, Phase 3.5 design diagnosis, a Phase 6 pre-delivery checklist and Phase 7 "update the ledger before the draft"; `paper-review` gains Step 0 (read `ADJUDICATED.md`), four qualitative items with reporting guidelines, and the six submission statements.
- 方法文件同步：流程改為 8 phase，鐵則補統計細則，論證工法每招補「何時別用」，`setup/TOOLS.md` 補數值雷區與 Harper、autocorrect。
  Method documents updated to match: the workflow is now 8 phases, the iron rules gain statistical details, every argument move gains a "when not to use it", and `setup/TOOLS.md` gains numerical pitfalls plus Harper and autocorrect.
- AWL 詞表因 ND 條款不再隨包，改由 `tools/vocab/fetch_awl.py` 抓取；README 改成完整清單。
  The AWL is no longer shipped because of its ND term and is fetched by `tools/vocab/fetch_awl.py` instead; the README becomes a complete inventory.

## v1.2.0（2026-08-24）

- 修掉文風診斷工具（中英四支）把 markdown 版面語法當成散文標點在數的一批 bug：frontmatter、表格分隔列、HTML 註解、多鍵引用的分號、粗體標題都不再計入；剝除規則抽成共用的 `tools/common/md_prose.py`。
  Fixes a batch of bugs where the four style tools counted markdown layout syntax as prose punctuation: frontmatter, table separator rows, HTML comments, multi-key citation semicolons and bold headings no longer count; the stripping rules move into the shared `tools/common/md_prose.py`.
- `snowball.py` 的 Semantic Scholar 後備線原本從未被觸發，已修正。
  The Semantic Scholar fallback in `snowball.py` never fired; fixed.
- 新增 `rebuttal` skill、投稿狀態表與一稿多投防護、圖表色覺可及性檢查；`co-author` 補 Phase 8「接受之後」、文字回收揭露與預印本政策查核。
  New `rebuttal` skill, the submission ledger with duplicate-submission guard, and the figure colour accessibility check; `co-author` gains Phase 8 "after acceptance", text-recycling disclosure and a preprint policy check.

## v1.1.0（2026-08）

- 投稿前檢查加入統計數字重算（statcheck 與 GRIM，裝了 R 才啟用）。
  The pre-submission check adds statistical recomputation (statcheck and GRIM, enabled only if R is installed).
- 新增引用滾雪球工具 `tools/refs/snowball.py`；查引用支援掃描檔與中文 PDF（選配 MinerU）；英文文法檢查可加掛 n-gram 易混詞偵測。
  New citation snowballing tool `tools/refs/snowball.py`; citation verification supports scanned and Chinese PDFs (optional MinerU); English grammar checking can add n-gram confused-word detection.
- 新增 `agents/` 兩個 subagent 範本：英文交付前的去 AI 節奏複查、引用查驗二審。
  New `agents/` with two subagent templates: the de-AI rhythm pass before English delivery and the citation second review.

## v1.0.0（2026-07）

- 初版：方法本體、五個 skill 範本、中英文檢查工具、自我安裝流程。
  First release: the method itself, five skill templates, Chinese and English checking tools, the self-install flow.
