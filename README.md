# Kawaii PC Repair (｡♥‿♥｡)

> ## 💖 This project exists because of **Feris's** idea.
> **Want to reach her? Here are her socials → [https://mez.ink/ferisooo](https://mez.ink/ferisooo)**

A cute, all-in-one **Windows** repair toolkit. The concept and creative
direction are **Feris's imagination**; the code was written by the AI assistant
**Claude** based on her ideas.

No Tauri, no Vite, no build step. **Python is the engine, your browser is the
pretty face.** Double-click `Repair.bat`, approve the admin prompt, and a
local web page opens where you can run real Windows repair and cleanup commands
with one click.

> ⚠️ **Windows only.** It runs `cmd`, `powershell`, `DISM`, `sfc`, `chkdsk`,
> etc. It will not work on macOS or Linux.

---

## ✨ "Wow, I must get this" features

- **One double-click, zero setup pain.** No installer, no account, no
  dependencies to chase. If you have Python, you're done.
- **A genuinely *cute* repair tool.** Pink, neon, animated — repair software
  that doesn't look like it's from 1998.
- **It actually runs the real fixes.** Behind the cute buttons are the exact
  Microsoft commands the pros use (`DISM`, `sfc`, `chkdsk`, network resets,
  Windows Update repair, and more).
- **Watch it work, live.** Every command streams its output to the page line by
  line, so you always see what's happening — nothing is hidden.
- **"RUN EVERYTHING" button.** One click does a full repair sweep across all 13
  modules. Grab a snack and let it cook.
- **100% local & offline-by-design.** The little server only listens on
  `127.0.0.1` (your own machine). Nothing is exposed to the internet, and your
  browser is the only thing that talks to it.
- **Nothing is collected.** No telemetry, no tracking, no data leaves your PC.
  (See [PRIVACY.md](PRIVACY.md).)
- **Totally readable.** The whole app is two small plain-text files you can open
  and read yourself in a few minutes — see the "Worried about viruses?" section
  below.

---

## 🆚 How it's different from other repair tools

- **Most repair utilities are either bloated installers or scary command-line
  walls of text.** This one is a single Python file plus a tiny launcher — no
  heavyweight install, and a friendly UI instead of a black console.
- **No hidden binaries.** Many "PC cleaner" tools ship compiled `.exe`s you
  can't inspect. Here the entire program is human-readable source you can read
  before you run it.
- **No upsells, no "your PC has 3,492 errors!" scare tactics, no paid tiers.**
  It just runs standard Microsoft maintenance commands.
- **It doesn't phone home.** No analytics SDK, no account, no cloud. It runs on
  your machine and only your machine.
- **It's cute on purpose.** Approachable for people who find normal repair tools
  intimidating.

---

## 🛡️ Worried about viruses? Read these files first

You should never run something off the internet on faith — especially a tool
that asks for administrator rights. The good news: this project is **tiny and
fully readable**. There are no hidden `.exe` files and nothing compiled. Open
these two files in Notepad (or on GitHub) and read them yourself:

1. **`advanced repair/kawaii_repair.py`** — this is the *entire* application:
   the small local web server, the exact list of commands each button runs (see
   the `MODULES = { ... }` section near the top), and the web page itself. If you
   want to know *exactly* what every button does, this is the file.
2. **`advanced repair/Repair.bat`** — the launcher. All it does is request admin
   rights, find your Python, and start the script above. That's it.

If you can read those two files (or have someone you trust read them), you can
see with your own eyes that there are no surprises. Every command it runs is a
standard, documented Microsoft tool.

---

## 📋 Requirements

- **Windows 10 or 11** (the repair commands are Windows-specific).
- **Administrator rights** — the fixes need them. `Repair.bat` will request
  elevation automatically.
- **Python 3.x** installed and on your `PATH`.
  - Get it from <https://www.python.org/downloads/>.
  - During setup, tick **"Add Python to PATH."**
  - No extra packages needed — only the Python standard library is used.
- A web browser (it opens automatically at `http://127.0.0.1:8777/`).

---

## 🐣 Setup for total beginners (never touched code before)

No coding knowledge required. Just follow these steps in order.

**Step 1 — Install Python (one time only).**
1. Go to <https://www.python.org/downloads/>.
2. Click the big yellow **"Download Python"** button.
3. Open the file you downloaded.
4. **VERY IMPORTANT:** at the bottom of the first window, tick the box that says
   **"Add Python to PATH"**, *then* click **Install Now**.
5. Wait for it to finish, then click Close.

**Step 2 — Get this project onto your PC.**
- The easy way: on the GitHub page, click the green **`Code`** button →
  **`Download ZIP`**. Then right-click the downloaded ZIP → **Extract All**.
- (Optional, if you have [Git](https://git-scm.com/downloads) installed, you can
  instead run `git clone https://github.com/ferisooo/advanced-repair.git`.)

**Step 3 — Run it.**
1. Open the extracted folder, then open the **`advanced repair`** folder inside.
2. **Double-click `Repair.bat`.**
3. A window pops up asking for permission to make changes — click **Yes**
   (it needs admin rights to repair Windows).
4. Your web browser opens automatically with the cute repair page.
5. **Keep the little black console window open** while you use it — closing it
   stops the tool.
6. Click any fix (or the big **RUN EVERYTHING** button) and watch the live log.

That's it. If your browser doesn't open on its own, type
`http://127.0.0.1:8777/` into your browser's address bar.

---

## ✨ What each module does

The web page exposes these modules:

| # | Module | What it does |
|---|--------|--------------|
| 01 | Full Diagnostics | Reads OS / CPU / RAM / GPU / disk / network health. Fixes nothing. |
| 02 | System Info Dump | Dumps specs, disks and drivers to the log. |
| 03 | Clean Temp Files | Wipes temp / prefetch junk. |
| 04 | DISM Image Repair | Heals the Windows image (CheckHealth / ScanHealth / RestoreHealth). |
| 05 | System File Check | `sfc /scannow` — restores protected system files. |
| 06 | Update Repair | Resets Windows Update and clears its cache. |
| 07 | Re-register Apps | Fixes broken Store / Xbox apps. |
| 08 | Repair VC++ | Re-installs Visual C++ runtimes (common game-crash fix). |
| 09 | Component Cleanup | Shrinks WinSxS to reclaim disk space. |
| 10 | Network Reset | Winsock + DNS + IP reset (restart after). |
| 11 | Schedule Disk Check | Queues `chkdsk` for next boot. |
| 12 | Schedule RAM Test | Queues the Windows Memory Diagnostic for next boot. |
| 13 | Blue Screen Doctor | Lists recent bugchecks + crash dumps, then disables the Realtek USB Audio driver (`RtUsbA64.sys`) that bluescreens on boot. Reversible in Device Manager. |

You can run a single fix, or hit **RUN EVERYTHING** for a full sweep.

---

## 🛟 Troubleshooting

- **"Python isn't installed or not on PATH."** Install Python and re-tick
  *Add Python to PATH*, then reopen `Repair.bat`.
- **Browser didn't open.** Go to <http://127.0.0.1:8777/> manually.
- **A fix did nothing / access denied.** Make sure you launched via
  `Repair.bat` so it runs elevated.

---

## ⚠️ Disclaimer

These commands modify your system (delete temp files, reset network settings,
repair system images, schedule disk/RAM checks). They are standard Microsoft
repair tools, but use them at your own risk. Back up anything important first.

See [TERMS.md](TERMS.md) for the terms of use and [PRIVACY.md](PRIVACY.md) for
the privacy policy.

---

## 🙏 Credit

- **The idea, concept, and creative direction belong to Feris** — this project
  is her imagination. Reach her at [https://mez.ink/ferisooo](https://mez.ink/ferisooo).
- **The code was written by the AI assistant Claude**, based on Feris's ideas.

If you fork, modify, or share this project, please keep crediting **Feris's
imagination** and **Claude's work**. See [TERMS.md](TERMS.md).

Made with 💖 for Feris.
</content>
</invoke>
