# About Kawaii PC Repair

**Kawaii PC Repair** is a small Windows maintenance and repair toolkit with a
deliberately cute, neon "kawaii" web interface. It was created by
**White Cat Feris** to make common Windows troubleshooting — the kind you'd
normally run by typing `DISM`, `sfc`, `chkdsk` and friends into an admin
console — friendly enough to do with a single click.

## The idea

Most repair utilities are either heavyweight installers or intimidating
command-line walls of text. Kawaii PC Repair takes a lighter approach:

- **Python is the engine.** A tiny local HTTP server (Python standard library
  only) runs the actual Windows commands and streams their output live.
- **Your browser is the face.** The UI is a single self-contained HTML page
  served at `http://127.0.0.1:8777/` — animated, pink, and readable.
- **No build, no dependencies.** No Node, no Tauri, no Vite, no `pip install`.
  Just Python plus a double-click on `Repair.bat`.

Everything stays **local** — the server only listens on `127.0.0.1`, so nothing
is exposed to the network.

## How it's put together

| File | Role |
|------|------|
| `advanced repair/Repair.bat` | Launcher. Requests admin rights, finds Python, starts the server. |
| `advanced repair/kawaii_repair.py` | The whole app: the HTTP server, the repair command definitions, and the embedded web UI. |

When you start it, the batch file elevates to administrator (the fixes require
it), locates Python via the `py` launcher or `python`, and runs the script.
The script then serves the UI and opens your browser. Each module you click
maps to a list of real shell commands that are executed with `cmd /C` and
streamed back to the page line by line.

## Who it's for

Anyone who wants a quick, approachable way to run standard Windows repair and
cleanup steps without memorizing commands — and who likes their tools a little
bit cute.

See [README.md](README.md) for requirements, install/clone instructions, and
how to run it.

---

*Made with 💖 for feris.*
