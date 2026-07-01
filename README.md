# Kawaii PC Repair (｡♥‿♥｡)

> 💖 **Feris's** idea. Code by the AI assistant **Claude**. Reach her → [mez.ink/ferisooo](https://mez.ink/ferisooo)

A cute, all-in-one **Windows** repair toolkit. No installer, no build step — Python is the engine, your browser is the pretty face. Double-click `Repair.bat`, approve the admin prompt, and a local page opens where you run real Windows fixes (`DISM`, `sfc`, `chkdsk`, network resets, and more) with one click.

> ⚠️ **Windows 10/11 only.** Needs **Python 3.x** (tick *Add Python to PATH*) and admin rights. 100% local (`127.0.0.1`), no telemetry, no hidden `.exe` — the whole app is two readable files: `advanced repair/kawaii_repair.py` and `advanced repair/Repair.bat`.

## Quick start

1. Install Python from <https://www.python.org/downloads/> — **tick "Add Python to PATH"**.
2. Download this repo (green **Code** → **Download ZIP**, then Extract All).
3. Open the **`advanced repair`** folder → double-click **`Repair.bat`** → click **Yes** on the admin prompt.
4. Your browser opens at <http://127.0.0.1:8777/>. Keep the black console window open while using it.
5. Click any fix — or the big **RUN EVERYTHING** button for a full sweep.

## Modules

| # | Module | What it does |
|---|--------|--------------|
| 01 | Full Diagnostics | Reads OS / CPU / RAM / GPU / disk / network health (fixes nothing). |
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

## Troubleshooting

- **"Python isn't installed / not on PATH."** Reinstall Python with *Add Python to PATH* ticked.
- **Browser didn't open.** Go to <http://127.0.0.1:8777/> manually.
- **A fix did nothing / access denied.** Launch via `Repair.bat` so it runs elevated.

## ⚠️ Disclaimer

These are standard Microsoft repair commands that modify your system (delete temp files, reset network, repair images, schedule checks). Use at your own risk; back up first. See [TERMS.md](TERMS.md) and [PRIVACY.md](PRIVACY.md).

---

**The idea and creative direction are Feris's; the code was written by Claude.** If you fork or share, please keep crediting both. Made with 💖 for Feris.
