# Security

The kit runs on your own machine: command-line tools that read your manuscripts, BibTeX files and PDFs, and skills and agents that Claude Code follows. The problems that matter most are:

- a crafted input file (Word, PDF, BibTeX, Markdown) that makes a tool run code, or read or write outside the folder you pointed it at;
- a skill, agent or setup step that leads Claude Code to run commands, change files or contact a service beyond what its documentation says;
- anything that sends manuscript text or API keys somewhere the documentation does not mention. The reference tools contact scholarly databases and publisher sites to look up and download references. Apart from those lookups and what Claude Code itself sends to Anthropic, nothing should leave your machine.

## Reporting

Please report vulnerabilities privately through **Report a vulnerability** on the repository's [Security tab](https://github.com/chenweichiang/research-writing-kit/security), not in a public issue. Include the version or commit, the steps or a sample file that reproduces it, and what an attacker gains. You should get a reply within a week. Once a fix is released, the report can be made public, with credit if you want it.

## Supported versions

Only the latest release receives fixes.

## Out of scope

- What Claude Code may do on your machine is decided by your Claude Code permission settings. Problems in Claude Code itself, or in the services the tools call, belong to those projects.
- A checking tool that flags the wrong sentence or misses a problem is a bug, not a vulnerability. Open an issue for it as described in [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

# 安全性

這套工具包在你自己的電腦上執行：命令列工具會讀你的稿件、BibTeX 與 PDF，skill 與 agent 則由 Claude Code 照著做。最在意的問題有三類：

- 特製的輸入檔（Word、PDF、BibTeX、Markdown）讓工具執行程式碼，或讀寫你指定資料夾以外的地方；
- skill、agent 或安裝步驟讓 Claude Code 執行文件沒寫的指令、改文件沒提到的檔，或連到文件沒提到的服務；
- 把稿件內容或 API 金鑰送到文件沒寫的地方。文獻工具會連到學術資料庫與出版社網站查詢、下載文獻。除了這些查詢，以及 Claude Code 本身會送給 Anthropic 的內容，不該有東西離開你的電腦。

## 回報方式

請到 repo 的 [Security 分頁](https://github.com/chenweichiang/research-writing-kit/security)按 **Report a vulnerability** 私下回報，不要開公開 issue。請附上版本或 commit、能重現的步驟或範例檔，以及攻擊者能得到什麼。一週內會回覆。修正發布後可以公開，要具名致謝也可以。

## 支援的版本

只有最新版會收到修正。

## 不算漏洞的範圍

- Claude Code 在你電腦上能做什麼，由你的 Claude Code 權限設定決定。Claude Code 本身或工具連到的外部服務出的問題，請回報給各自的專案。
- 檢查工具標錯句子或漏抓問題屬於一般錯誤，不算漏洞，請照 [`CONTRIBUTING.md`](CONTRIBUTING.md) 開 issue。
