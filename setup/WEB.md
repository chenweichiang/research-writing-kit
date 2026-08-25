# Web on-ramp — get the author onto Claude Code

> For a person who opened this kit on **claude.ai** (web or desktop) instead of Claude
> Code. The method needs a machine that can hold files and run the tools **privately** —
> that's Claude Code. claude.ai is the **on-ramp, not where the work happens**. Your job
> here is to get this (likely non-technical) person onto Claude Code — warmly, step by
> step, in their language. Don't try to fake a file-writing install from the browser, and
> don't sell the web app as equivalent.

## Why move at all (say this to them, plainly, in their language)

- The method keeps your **drafts and data on your own computer** — nothing unpublished
  goes to the cloud. That privacy only holds on your machine.
- Claude Code can **save your paper, skeleton, and references as real files**, and run
  the checking tools. The web app can read this method and talk it through, but it can't
  touch your computer.
- So we'll spend five minutes getting you set up where the real work happens — I'll walk
  you through every step.

## Do this in order

### 1. Interview first (optional, but kind — it carries over)
You may run `CLAUDE.md` Phase A right here (what they write, language, venues, voice
samples, zh-tw pack?). Then hand them a short **plain-text block** summarizing their
answers, and tell them: *"paste this to your Claude Code after setup, so it won't ask
again."* Do **not** build skills or a voice profile here — that happens in Claude Code.

### 2. Check they can actually run it (before they install anything)
- **Needs a paid Claude plan** (Pro / Max / Team) **or** an Anthropic Console (API) account.
  A **free** claude.ai account cannot run Claude Code. If they're on free, tell them
  plainly now — don't let them hit the wall mid-install.
- macOS 13+ or Windows 10 (1809)+. **No need to install Node/Python/git-first** — the
  installer bundles what it needs (git they may still want in step 5).

### 3. Install Claude Code (walk them through, in their language)
Offer the desktop app first to anyone terminal-averse:

- **Easiest — desktop app (no terminal):** download from <https://claude.ai/download>,
  open the installer, sign in, use the built-in **Code** area.
- **Official installer (terminal):**
  - **macOS** — open **Terminal** (`Cmd+Space` → type `terminal` → Enter), paste and run:
    ```
    curl -fsSL https://claude.ai/install.sh | bash
    ```
  - **Windows** — open **PowerShell** (`Win+X` → "Windows PowerShell"), paste and run:
    ```
    irm https://claude.ai/install.ps1 | iex
    ```
  - Wait for **"successfully installed"**.

### 4. First launch + login
Type `claude` and press Enter. It opens the browser to sign in with their Claude account.
Back in the terminal, a `>` prompt means they're in. (Login is remembered next time.)

### 5. Get the kit onto their machine
The kit is a public repository, so downloading it needs no account and no login:

1. **With git** (comes with Xcode Command Line Tools on macOS; on Windows install
   [Git for Windows](https://git-scm.com/download/win)):
   `git clone https://github.com/chenweichiang/research-writing-kit.git`
   Later, `git pull` inside that folder picks up updates.
2. **Without git:** open the repository page in the browser → green **Code** button →
   **Download ZIP** → unzip anywhere (e.g. Downloads). Simpler, but there's no easy way
   to pull updates later.

### 6. Open the kit folder in Claude Code — and hand off
- In Terminal, `cd` into the kit folder, then start Claude Code:
  ```
  cd ~/Downloads/research-writing-kit
  claude
  ```
  (Adjust the path to wherever they put it. On Windows: `cd` into the folder in PowerShell,
  then `claude`. Tip: right-clicking a folder often offers "Open in Terminal/PowerShell".)
- Tell them to type, in their language: **"Read CLAUDE.md and set me up."**
- `CLAUDE.md`'s installer now takes over from Phase A. If you interviewed them in step 1,
  they paste that block and it skips the repeat questions. **They're home** — the rest of
  the method runs here.

## If they get stuck (tell them the one line that fits)

- **`command not found: claude`** (mac): run
  `echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc`, then
  reopen Terminal.
- **`'irm' is not recognized`** (Win): they're in CMD, not PowerShell — reopen PowerShell
  (`Win+X` → "Windows PowerShell").
- **"not available in your region"**: Claude Code isn't in their region yet; no workaround.
- **login hangs**: check network / VPN, then type `/login` inside Claude Code to retry.
- **garbled Chinese folder names**: `export LANG=en_US.UTF-8`, then retry the command.

## The honest one-liner
The web app is a helpful guide and can talk method, but the kit's real value — files,
tools, privacy — lives in Claude Code. Getting them there is the whole job of this file.
