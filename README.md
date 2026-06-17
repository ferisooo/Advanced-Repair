# Kawaii PC Repair (｡♥‿♥｡)

> ## 💖 This was only made possible by Feris.
> **Here are her socials if you'd like to contact her → [https://mez.ink/ferisooo](https://mez.ink/ferisooo)**

A cute, all-in-one **Windows** repair toolkit by **White Cat Feris**.

No Tauri, no Vite, no build step. **Python is the engine, your browser is the
pretty face.** Double-click `Repair.bat`, approve the admin prompt, and a
local web UI opens where you can run real Windows repair and cleanup commands
with one click.

> ⚠️ **Windows only.** It runs `cmd`, `powershell`, `DISM`, `sfc`, `chkdsk`,
> etc. It will not work on macOS or Linux.

---

## ✨ What it does

The web UI exposes these modules:

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

You can run a single fix, or hit **RUN EVERYTHING** for a full sweep.

---

## 📋 Requirements

- **Windows 10 or 11** (the repair commands are Windows-specific).
- **Administrator rights** — the fixes need them. `Repair.bat` will request
  elevation automatically.
- **Python 3.x** installed and on your `PATH`.
  - Get it from <https://www.python.org/downloads/>.
  - During setup, tick **“Add Python to PATH.”**
  - No extra packages needed — only the Python standard library is used.
- A web browser (it opens automatically at `http://127.0.0.1:8777/`).

---

## ⬇️ Getting the code (clone the GitHub repo)

Install [Git](https://git-scm.com/downloads), then run:

```bash
# Clone the repository
git clone https://github.com/ferisooo/advanced-repair.git

# Go into the folder
cd advanced-repair
```

To update your copy later:

```bash
git pull origin main
```

> Don't have Git? On the GitHub page click **Code → Download ZIP** and extract
> it instead.

---

## 🚀 Running it

1. Open the **`advanced repair`** folder.
2. **Double-click `Repair.bat`.**
3. Approve the **“Yes”** admin (UAC) prompt.
4. Your browser opens the Kawaii Repair UI. **Keep the black console window
   open** while you use it — closing it stops the server.
5. Click a fix (or **RUN EVERYTHING**) and watch the live log.

Prefer the command line? From inside the `advanced repair` folder:

```bash
python kawaii_repair.py
```

(but you still need to run it **as administrator** for the fixes to work.)

---

## 🛟 Troubleshooting

- **“Python isn't installed or not on PATH.”** Install Python and re-tick
  *Add Python to PATH*, then reopen `Repair.bat`.
- **Browser didn't open.** Go to <http://127.0.0.1:8777/> manually.
- **A fix did nothing / access denied.** Make sure you launched via
  `Repair.bat` so it runs elevated.

---

## ⚠️ Disclaimer

These commands modify your system (delete temp files, reset network settings,
repair system images, schedule disk/RAM checks). They are standard Microsoft
repair tools, but use them at your own risk. Back up anything important first.

Made with 💖 for feris.
