# -*- coding: utf-8 -*-
# ============================================================
#  Kawaii PC Repair - local web UI that ACTUALLY runs fixes
#  by White Cat Feris  (｡♥‿♥｡)
#  No Tauri / no Vite / no build. Python is the engine,
#  your browser is the pretty face. Launch via Repair.bat (admin).
# ============================================================
import http.server, socketserver, subprocess, threading, webbrowser, sys, os, urllib.parse

PORT = 8777
HOST = "127.0.0.1"

# --- the real commands (run with cmd /C). reboot ones only SCHEDULE, safe. ---
MODULES = {
    "diagnostics": [
        'powershell -NoProfile -Command "$o=Get-CimInstance Win32_OperatingSystem; \'OS: \'+$o.Caption+\' build \'+$o.BuildNumber"',
        'powershell -NoProfile -Command "$c=Get-CimInstance Win32_Processor; \'CPU: \'+$c.Name+\' | load \'+$c.LoadPercentage+\'%%\'"',
        'powershell -NoProfile -Command "$m=Get-CimInstance Win32_OperatingSystem; \'RAM in use: \'+[math]::Round(($m.TotalVisibleMemorySize-$m.FreePhysicalMemory)/$m.TotalVisibleMemorySize*100)+\'%%\'"',
        'powershell -NoProfile -Command "Get-CimInstance Win32_VideoController | %%{$a=((Get-Date)-$_.DriverDate).Days; \'GPU: \'+$_.Name+\' driver \'+$a+\' days old\'+($(if($a -gt 365){\' <-- OLD! update it\'}else{\' (ok)\'}))}"',
        'powershell -NoProfile -Command "Get-PhysicalDisk | %%{$_.FriendlyName+\' health: \'+$_.HealthStatus}"',
        'powershell -NoProfile -Command "Get-CimInstance Win32_LogicalDisk -Filter \'DriveType=3\' | %%{$p=[math]::Round($_.FreeSpace/$_.Size*100); $_.DeviceID+\' \'+$p+\'%% free\'+($(if($p -lt 10){\' <-- LOW!\'}else{\'\'}))}"',
        'powershell -NoProfile -Command "if(Test-Connection 8.8.8.8 -Count 2 -Quiet){\'Internet: connected (ok)\'}else{\'Internet: NO CONNECTION\'}"',
    ],
    "sysinfo": ["systeminfo", "wmic diskdrive get model,status", "driverquery"],
    "temp": [
        r"del /s /f /q %temp%\*.*",
        r"del /s /f /q %windir%\Temp\*.*",
        r"del /s /f /q %windir%\Prefetch\*.*",
    ],
    "dism": [
        "DISM /Online /Cleanup-Image /CheckHealth",
        "DISM /Online /Cleanup-Image /ScanHealth",
        "DISM /Online /Cleanup-Image /RestoreHealth",
    ],
    "sfc": ["sfc /scannow"],
    "winupdate": [
        "net stop wuauserv & net stop bits & net stop cryptsvc & net stop msiserver",
        r"ren %windir%\SoftwareDistribution SoftwareDistribution.old",
        r"ren %windir%\System32\catroot2 catroot2.old",
        "net start wuauserv & net start bits & net start cryptsvc & net start msiserver",
    ],
    "appx": [
        'powershell -NoProfile -Command "Get-AppxPackage -AllUsers | Foreach {Add-AppxPackage -DisableDevelopmentMode -Register \\"$($_.InstallLocation)\\AppXManifest.xml\\" -ErrorAction SilentlyContinue}"',
        "wsreset.exe",
    ],
    "vcredist": [
        'powershell -NoProfile -Command "$d=\\"$env:TEMP\\vcredist_feris\\"; New-Item -ItemType Directory -Force -Path $d | Out-Null; Invoke-WebRequest \'https://aka.ms/vs/17/release/vc_redist.x64.exe\' -OutFile \\"$d\\x64.exe\\"; Start-Process \\"$d\\x64.exe\\" -ArgumentList \'/repair\',\'/quiet\',\'/norestart\' -Wait; Invoke-WebRequest \'https://aka.ms/vs/17/release/vc_redist.x86.exe\' -OutFile \\"$d\\x86.exe\\"; Start-Process \\"$d\\x86.exe\\" -ArgumentList \'/repair\',\'/quiet\',\'/norestart\' -Wait; Remove-Item $d -Recurse -Force"',
    ],
    "compcleanup": ["DISM /Online /Cleanup-Image /StartComponentCleanup /ResetBase"],
    "network": [
        "ipconfig /flushdns",
        "netsh winsock reset",
        "netsh int ip reset",
        "ipconfig /release",
        "ipconfig /renew",
    ],
    "chkdsk": ["echo Y| chkdsk %SystemDrive% /f /r"],
    "memdiag": ["bcdedit /bootsequence {memdiag}"],
    # Blue-screen doctor: shows recent bugchecks + crash dumps, then disables
    # the Realtek USB Audio device (driver RtUsbA64.sys) that causes the common
    # "Your PC ran into a problem" crash on boot. Reversible in Device Manager.
    "bsod": [
        'powershell -NoProfile -Command "$e=Get-WinEvent -FilterHashtable @{LogName=\'System\';ProviderName=\'Microsoft-Windows-WER-SystemErrorReporting\';Id=1001} -MaxEvents 5 -ErrorAction SilentlyContinue; if($e){\'Recent blue screens (newest first):\'; $e | %%{\' - \'+$_.TimeCreated}}else{\'No blue-screen (bugcheck) events logged - good sign\'}"',
        'powershell -NoProfile -Command "$d=\\"$env:SystemRoot\\Minidump\\"; if(Test-Path $d){$f=Get-ChildItem $d -Filter *.dmp -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 5; if($f){\'Crash dump files:\'; $f | %%{\' - \'+$_.Name+\'  (\'+$_.LastWriteTime+\')\'}}else{\'Minidump folder is empty\'}}else{\'No minidump folder (no recent crashes saved)\'}"',
        'powershell -NoProfile -Command "$dev=Get-PnpDevice -FriendlyName \'*Realtek*USB*Audio*\' -ErrorAction SilentlyContinue; if($dev){\'Found Realtek USB Audio (RtUsbA64.sys) device(s):\'; $dev | %%{\' - \'+$_.FriendlyName+\' [\'+$_.Status+\']\'}}else{\'No Realtek USB Audio device found - RtUsbA64.sys is not your culprit\'}"',
        'powershell -NoProfile -Command "$dev=Get-PnpDevice -FriendlyName \'*Realtek*USB*Audio*\' -Status OK -ErrorAction SilentlyContinue; if($dev){$dev | %%{ try{Disable-PnpDevice -InstanceId $_.InstanceId -Confirm:$false -ErrorAction Stop; \'Disabled: \'+$_.FriendlyName+\' (re-enable anytime in Device Manager)\'}catch{\'Could not disable \'+$_.FriendlyName+\' :: \'+$_.Exception.Message} }}else{\'Nothing to disable (no active Realtek USB Audio device)\'}"',
    ],
}

# --- reverse / "oops, undo that" steps for the modules that can be undone. ---
# Only fixes that make a *reversible* change get an entry here. Things like
# deleting temp files, sfc/DISM repairs, the VC++ reinstall and component
# cleanup (/ResetBase) change the system permanently and CANNOT be undone, so
# they intentionally have no reverse. The UI only shows an undo button for ids
# that appear in this dict.
UNDO = {
    # Update Repair renamed SoftwareDistribution/catroot2 to *.old. Put them
    # back: stop the services, drop the freshly-made empty folders, and restore
    # the backups. The "if exist *.old" guards mean this is a no-op (and never
    # deletes the live folder) when there's no backup to restore from.
    "winupdate": [
        "net stop wuauserv & net stop bits & net stop cryptsvc & net stop msiserver",
        r"if exist %windir%\SoftwareDistribution.old rmdir /s /q %windir%\SoftwareDistribution",
        r"if exist %windir%\SoftwareDistribution.old ren %windir%\SoftwareDistribution.old SoftwareDistribution",
        r"if exist %windir%\System32\catroot2.old rmdir /s /q %windir%\System32\catroot2",
        r"if exist %windir%\System32\catroot2.old ren %windir%\System32\catroot2.old catroot2",
        "net start wuauserv & net start bits & net start cryptsvc & net start msiserver",
    ],
    # Cancel the disk check that was queued for next boot.
    "chkdsk": ["chkntfs /x %SystemDrive%"],
    # Clear the one-time boot sequence so the RAM test won't run next boot.
    "memdiag": ["bcdedit /deletevalue {bootmgr} bootsequence"],
    # Turn the Realtek USB Audio device back on (reverse of Blue Screen Doctor).
    "bsod": [
        'powershell -NoProfile -Command "$dev=Get-PnpDevice -FriendlyName \'*Realtek*USB*Audio*\' -ErrorAction SilentlyContinue; if($dev){$dev | %%{ try{Enable-PnpDevice -InstanceId $_.InstanceId -Confirm:$false -ErrorAction Stop; \'Re-enabled: \'+$_.FriendlyName}catch{\'Could not enable \'+$_.FriendlyName+\' :: \'+$_.Exception.Message} }}else{\'No Realtek USB Audio device found - nothing to re-enable\'}"',
    ],
}

NO_WINDOW = 0x08000000  # CREATE_NO_WINDOW so no popup consoles


def run_module_stream(module, write, undo=False):
    """Run each step, streaming every output line through write(line)."""
    steps = (UNDO if undo else MODULES).get(module)
    if not steps:
        write("! nothing to undo for this fix" if undo else "! unknown module")
        return
    for step in steps:
        write("$ " + step)
        try:
            p = subprocess.Popen(
                ["cmd", "/C", step],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                creationflags=NO_WINDOW, text=True,
                encoding="utf-8", errors="replace",
            )
            for line in p.stdout:
                line = line.rstrip()
                if line:
                    write(line)
            p.wait()
        except Exception as e:
            write("! " + str(e))


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass  # quiet

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/":
            body = PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if parsed.path == "/run":
            q = urllib.parse.parse_qs(parsed.query)
            module = (q.get("module") or [""])[0]
            undo = (q.get("undo") or ["0"])[0] == "1"
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.end_headers()

            def write(line):
                try:
                    self.wfile.write(("data: " + line + "\n\n").encode("utf-8"))
                    self.wfile.flush()
                except Exception:
                    pass

            run_module_stream(module, write, undo)
            try:
                self.wfile.write(b"event: done\ndata: ok\n\n")
                self.wfile.flush()
            except Exception:
                pass
            return

        self.send_error(404)


class ThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True


def main():
    url = "http://%s:%d/" % (HOST, PORT)
    srv = ThreadingServer((HOST, PORT), Handler)
    print("=" * 52)
    print("  Kawaii PC Repair running at " + url)
    print("  Keep this window OPEN while you use it.")
    print("  Close it to stop the server.")
    print("=" * 52)
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()


PAGE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kawaii Repair</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Space+Mono:wght@400;700&display=swap');
:root{--bg:#08070d;--panel:#110f1a;--panel2:#17141f;--pink:#ff4d97;--pink-soft:#ff8fc7;--pink-deep:#c41368;--yellow:#ffe14d;--text:#f5ecf3;--dim:#8a7f95;--line:rgba(255,77,151,.16);}
*{box-sizing:border-box;margin:0;padding:0;}
body{min-height:100vh;padding:28px 22px 60px;background:radial-gradient(120% 80% at 50% -10%,#1a0b1f 0%,var(--bg) 60%);color:var(--text);font-family:'Fredoka',system-ui,sans-serif;overflow-x:hidden;position:relative;}
.grid{position:fixed;inset:0;pointer-events:none;opacity:.4;background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);background-size:44px 44px;-webkit-mask-image:radial-gradient(80% 60% at 50% 0%,#000 30%,transparent 80%);mask-image:radial-gradient(80% 60% at 50% 0%,#000 30%,transparent 80%);}
.aura{position:fixed;inset:-40%;pointer-events:none;opacity:0;transition:opacity .6s;background:conic-gradient(from 0deg,transparent,rgba(255,77,151,.12),transparent,rgba(255,225,77,.1),transparent);animation:spin 14s linear infinite;}
.aura.on{opacity:1;}
@keyframes spin{to{transform:rotate(360deg);}}
.wrap{max-width:1100px;margin:0 auto;position:relative;}
.head{display:flex;align-items:center;gap:20px;flex-wrap:wrap;margin-bottom:26px;}
.core{position:relative;width:64px;height:64px;flex:0 0 64px;display:grid;place-items:center;}
.ring{position:absolute;inset:0;border-radius:50%;border:1.5px solid var(--pink);opacity:.5;}
.ring.r1{animation:pulse 2.4s ease-out infinite;}
.ring.r2{border-color:var(--yellow);animation:pulse 2.4s ease-out .8s infinite;}
.ring.r3{border-color:var(--pink-soft);animation:pulse 2.4s ease-out 1.6s infinite;}
.core.on .ring{animation-duration:1s;}
.heart{font-size:26px;color:var(--pink);filter:drop-shadow(0 0 10px var(--pink));animation:beat 1.6s ease-in-out infinite;}
@keyframes pulse{0%{transform:scale(.6);opacity:.7}100%{transform:scale(1.5);opacity:0}}
@keyframes beat{0%,100%{transform:scale(1)}25%{transform:scale(1.18)}40%{transform:scale(1)}}
.titles{flex:1 1 220px;}
.eyebrow{font-size:11px;letter-spacing:.32em;text-transform:uppercase;color:var(--pink-soft);font-weight:600;}
.title{font-size:clamp(34px,6vw,52px);font-weight:700;line-height:.95;background:linear-gradient(100deg,var(--pink) 0%,var(--yellow) 50%,var(--pink) 100%);background-size:200% auto;-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:transparent;animation:shift 5s linear infinite;filter:drop-shadow(0 2px 18px rgba(255,77,151,.35));margin:2px 0 4px;}
@keyframes shift{to{background-position:200% center;}}
.mode{font-size:12.5px;font-family:'Space Mono',monospace;color:#6dffc2;}
.meter{flex:0 0 150px;text-align:right;}
.meter-num{font-size:38px;font-weight:700;line-height:1;color:var(--yellow);text-shadow:0 0 22px rgba(255,225,77,.4);}
.meter-num span{font-size:16px;color:var(--dim);}
.meter-bar{height:7px;border-radius:99px;background:rgba(255,255,255,.07);overflow:hidden;margin:6px 0;}
.meter-bar i{display:block;height:100%;width:0;border-radius:99px;background:linear-gradient(90deg,var(--pink),var(--yellow));transition:width .5s cubic-bezier(.4,0,.2,1);box-shadow:0 0 12px var(--pink);}
.meter-lbl{font-size:11px;color:var(--dim);font-family:'Space Mono',monospace;}
.run{position:relative;width:100%;margin-bottom:26px;padding:22px;border:none;cursor:pointer;border-radius:20px;text-align:left;overflow:hidden;color:#1a0010;font-family:'Fredoka',sans-serif;background:linear-gradient(105deg,var(--pink) 0%,var(--pink-soft) 45%,var(--yellow) 100%);box-shadow:0 10px 40px -8px rgba(255,77,151,.6),inset 0 1px 0 rgba(255,255,255,.4);transition:transform .15s,box-shadow .3s;}
.run:hover{transform:translateY(-3px) scale(1.005);box-shadow:0 18px 55px -8px rgba(255,77,151,.75);}
.run.stop{background:linear-gradient(105deg,#2a0a18,#3a0f22);color:var(--pink);box-shadow:0 0 0 1.5px var(--pink) inset;}
.run-glow{position:absolute;top:0;left:-60%;width:50%;height:100%;transform:skewX(-20deg);background:linear-gradient(90deg,transparent,rgba(255,255,255,.5),transparent);animation:sweep 3.2s ease-in-out infinite;}
.run.stop .run-glow{display:none;}
@keyframes sweep{0%{left:-60%}55%,100%{left:160%}}
.run-txt{display:block;font-size:26px;font-weight:700;}
.run-sub{display:block;font-size:13px;opacity:.78;margin-top:2px;}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:14px;margin-bottom:26px;}
.card{position:relative;overflow:hidden;cursor:pointer;text-align:left;padding:16px;border-radius:16px;border:1px solid var(--line);color:var(--text);font-family:'Fredoka',sans-serif;background:linear-gradient(160deg,var(--panel2),var(--panel));display:flex;flex-direction:column;gap:8px;transition:transform .18s,border-color .3s,box-shadow .3s;min-height:158px;}
.card:hover:not([disabled]){transform:translateY(-4px);border-color:var(--pink);box-shadow:0 14px 34px -12px rgba(255,77,151,.5);}
.card[disabled]{opacity:.45;cursor:not-allowed;}
.card.active{border-color:var(--yellow);box-shadow:0 0 0 1px var(--yellow),0 14px 40px -10px rgba(255,225,77,.45);}
.scan{position:absolute;left:0;right:0;top:0;height:40%;opacity:0;background:linear-gradient(180deg,rgba(255,225,77,.22),transparent);}
.card.running .scan{opacity:1;animation:scandown 1.4s linear infinite;}
@keyframes scandown{0%{transform:translateY(-100%)}100%{transform:translateY(260%)}}
.ctop{display:flex;justify-content:space-between;align-items:center;}
.num{font-family:'Space Mono',monospace;font-size:12px;color:var(--dim);}
.tag{font-size:9.5px;text-transform:uppercase;letter-spacing:.12em;padding:3px 8px;border-radius:99px;font-weight:700;}
.t-scan{background:rgba(255,225,77,.14);color:var(--yellow);}
.t-fix{background:rgba(255,77,151,.16);color:var(--pink-soft);}
.t-clean{background:rgba(109,255,194,.14);color:#6dffc2;}
.t-reboot{background:rgba(255,255,255,.08);color:#cbbfd6;}
.glyph{font-size:26px;filter:drop-shadow(0 0 8px rgba(255,77,151,.4));}
.ctitle{font-size:16px;font-weight:600;}
.cblurb{font-size:12px;color:var(--dim);line-height:1.4;flex:1;}
.cfoot{display:flex;justify-content:space-between;align-items:center;gap:8px;}
.cfr{display:flex;align-items:center;gap:8px;}
.time{font-family:'Space Mono',monospace;font-size:11px;color:var(--pink-soft);}
.undo{font-family:'Space Mono',monospace;font-size:10px;color:var(--pink-soft);border:1px solid var(--line);border-radius:8px;padding:2px 8px;cursor:pointer;opacity:.5;transition:opacity .2s,color .2s,border-color .2s,background .2s;}
.card:hover .undo{opacity:1;}
.undo:hover{color:var(--pink);border-color:var(--pink);background:rgba(255,77,151,.1);}
.stamp.undone{color:var(--pink-soft);}
.dots{display:inline-flex;gap:3px;}.dots i{width:5px;height:5px;border-radius:50%;background:var(--yellow);animation:blink 1s infinite;}
.dots i:nth-child(2){animation-delay:.2s;}.dots i:nth-child(3){animation-delay:.4s;}
@keyframes blink{0%,100%{opacity:.25}50%{opacity:1}}
.stamp{font-family:'Space Mono',monospace;font-size:11px;font-weight:700;color:#6dffc2;animation:pop .35s ease-out;}
.stamp.err{color:var(--pink);}
@keyframes pop{0%{transform:scale(.4);opacity:0}70%{transform:scale(1.25)}100%{transform:scale(1);opacity:1}}
.reboot{position:absolute;top:14px;right:14px;font-size:9px;color:var(--yellow);}
.term{border:1px solid var(--line);border-radius:16px;overflow:hidden;background:#060509;box-shadow:0 18px 50px -20px #000;}
.tbar{display:flex;align-items:center;gap:7px;padding:10px 14px;background:var(--panel);border-bottom:1px solid var(--line);}
.tdot{width:11px;height:11px;border-radius:50%;}.tdot.a{background:var(--pink);}.tdot.b{background:var(--yellow);}.tdot.c{background:var(--pink-soft);}
.tname{font-family:'Space Mono',monospace;font-size:12px;color:var(--dim);margin-left:6px;flex:1;}
.clear{background:none;border:1px solid var(--line);color:var(--dim);font-size:11px;padding:3px 10px;border-radius:8px;cursor:pointer;font-family:'Space Mono',monospace;}
.clear:hover{color:var(--pink);border-color:var(--pink);}
.tbody{height:240px;overflow:auto;padding:14px 16px;font-family:'Space Mono',monospace;font-size:12.5px;line-height:1.7;}
.empty{color:var(--dim);text-align:center;padding-top:84px;}
.line{color:#d8cfe0;animation:slidein .25s ease-out;}.line.all{color:var(--yellow);font-weight:700;}
.arrow{color:var(--pink);margin-right:6px;}
@keyframes slidein{from{opacity:0;transform:translateX(-8px)}to{opacity:1;transform:none}}
.tbody::-webkit-scrollbar{width:8px;}.tbody::-webkit-scrollbar-thumb{background:var(--pink-deep);border-radius:9px;}
.foot{text-align:center;margin-top:22px;font-size:11.5px;color:var(--dim);}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important;}}
</style></head>
<body>
<div class="grid"></div><div class="aura" id="aura"></div>
<div class="wrap">
  <div class="head">
    <div class="core" id="core"><span class="ring r1"></span><span class="ring r2"></span><span class="ring r3"></span><span class="heart">&#9829;</span></div>
    <div class="titles">
      <p class="eyebrow">white cat feris &middot; pc rescue</p>
      <h1 class="title">Kawaii Repair</h1>
      <p class="mode">&#9679; live &mdash; connected to your PC</p>
    </div>
    <div class="meter">
      <div class="meter-num"><span id="pct">0</span><span>%</span></div>
      <div class="meter-bar"><i id="bar"></i></div>
      <div class="meter-lbl"><span id="dn">0</span>/13 fixed</div>
    </div>
  </div>
  <button class="run" id="runAll"><span class="run-glow"></span><span class="run-txt">&#10022; RUN EVERYTHING</span><span class="run-sub">full repair, grab a snack ~</span></button>
  <div class="cards" id="cards"></div>
  <div class="term">
    <div class="tbar"><span class="tdot a"></span><span class="tdot b"></span><span class="tdot c"></span><span class="tname">~/repair.log</span><button class="clear" id="clear">clear</button></div>
    <div class="tbody" id="tbody"><p class="empty">pick a fix above and watch it work &#10022;</p></div>
  </div>
  <p class="foot">made with &#128156; for feris &middot; close nothing while it runs</p>
</div>
<script>
var MODULES=[
 {id:"diagnostics",n:"01",title:"Full Diagnostics",blurb:"Reads everything. Fixes nothing. Tells you what's broken.",g:"\uD83D\uDD0D",tag:"scan",time:"~30s"},
 {id:"sysinfo",n:"02",title:"System Info Dump",blurb:"Specs, disks, drivers straight to the log.",g:"\uD83D\uDCCB",tag:"scan",time:"~20s"},
 {id:"temp",n:"03",title:"Clean Temp Files",blurb:"Wipes temp / prefetch junk. Instant room.",g:"\uD83E\uDDF9",tag:"clean",time:"~10s"},
 {id:"dism",n:"04",title:"DISM Image Repair",blurb:"Heals the Windows image itself. The slow one.",g:"\uD83E\uDE79",tag:"fix",time:"10-30m"},
 {id:"sfc",n:"05",title:"System File Check",blurb:"Scans + restores protected system files.",g:"\uD83D\uDEE1\uFE0F",tag:"fix",time:"5-15m"},
 {id:"winupdate",n:"06",title:"Update Repair",blurb:"Resets Windows Update + clears its cache.",g:"\uD83D\uDD04",tag:"fix",time:"~1m",undo:1},
 {id:"appx",n:"07",title:"Re-register Apps",blurb:"Fixes broken Store / Xbox apps.",g:"\uD83D\uDCE6",tag:"fix",time:"~2m"},
 {id:"vcredist",n:"08",title:"Repair VC++",blurb:"Re-installs VC++ runtimes (game crash fixer).",g:"\u2699\uFE0F",tag:"fix",time:"~2m"},
 {id:"compcleanup",n:"09",title:"Component Cleanup",blurb:"Shrinks WinSxS. Reclaims gigabytes.",g:"\uD83D\uDCBE",tag:"clean",time:"~5m"},
 {id:"network",n:"10",title:"Network Reset",blurb:"Winsock + DNS + IP. Restart after.",g:"\uD83C\uDF10",tag:"fix",time:"~10s",reboot:1},
 {id:"chkdsk",n:"11",title:"Schedule Disk Check",blurb:"Queues chkdsk for next boot.",g:"\uD83D\uDCBF",tag:"reboot",time:"next boot",reboot:1,undo:1},
 {id:"memdiag",n:"12",title:"Schedule RAM Test",blurb:"Queues the memory test for next boot.",g:"\uD83E\uDDE0",tag:"reboot",time:"next boot",reboot:1,undo:1},
 {id:"bsod",n:"13",title:"Blue Screen Doctor",blurb:"Shows recent crashes + disables the Realtek USB Audio driver (RtUsbA64.sys) that bluescreens on boot.",g:"\uD83D\uDC8A",tag:"fix",time:"~20s",undo:1}
];
var ORDER=MODULES.map(function(m){return m.id;});
var status={},running=false,active=null,stopFlag=false;
var cardsEl=document.getElementById("cards"),tbody=document.getElementById("tbody"),aura=document.getElementById("aura"),core=document.getElementById("core");
var els={};
MODULES.forEach(function(m){
 var c=document.createElement("button");c.className="card";c.id="c_"+m.id;
 var undoBtn=m.undo?'<span class="undo" title="Reverse this fix if it didn\'t help">\u21A9 undo</span>':'';
 c.innerHTML='<span class="scan"></span><span class="ctop"><span class="num">'+m.n+'</span><span class="tag t-'+m.tag+'">'+m.tag+'</span></span>'+
   '<span class="glyph">'+m.g+'</span><span class="ctitle">'+m.title+'</span><span class="cblurb">'+m.blurb+'</span>'+
   '<span class="cfoot"><span class="time">'+m.time+'</span><span class="cfr">'+undoBtn+'<span class="state"></span></span></span>'+(m.reboot?'<span class="reboot" style="opacity:0">\u27F3 reboot</span>':'');
 c.onclick=function(){handleOne(m.id);};
 cardsEl.appendChild(c);els[m.id]={el:c,state:c.querySelector(".state"),rb:c.querySelector(".reboot")};
 var u=c.querySelector(".undo");
 if(u)u.onclick=function(ev){ev.stopPropagation();handleOne(m.id,true);};
});
function log(line,all){
 var e=tbody.querySelector(".empty");if(e)e.remove();
 var p=document.createElement("p");p.className="line"+(all?" all":"");p.innerHTML='<span class="arrow">&rsaquo;</span> '+esc(line);
 tbody.appendChild(p);while(tbody.children.length>240)tbody.removeChild(tbody.firstChild);tbody.scrollTop=tbody.scrollHeight;
}
function esc(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");}
function setState(id,s){
 status[id]=s;var o=els[id];o.el.className="card "+((s==="running"||s==="undoing")?"running ":"")+(active===id?"active":"");
 if(s==="running"||s==="undoing")o.state.innerHTML='<span class="dots"><i></i><i></i><i></i></span>';
 else if(s==="done"){o.state.innerHTML='<span class="stamp">DONE</span>';if(o.rb)o.rb.style.opacity=".8";}
 else if(s==="error")o.state.innerHTML='<span class="stamp err">ERR</span>';
 else if(s==="reverted"){o.state.innerHTML='<span class="stamp undone">UNDONE</span>';if(o.rb)o.rb.style.opacity="0";}
 else o.state.innerHTML="";
 var dn=ORDER.filter(function(i){return status[i]==="done";}).length;
 document.getElementById("dn").textContent=dn;var pc=Math.round(dn/ORDER.length*100);
 document.getElementById("pct").textContent=pc;document.getElementById("bar").style.width=pc+"%";
}
function runOne(id,undo){return new Promise(function(res){
 active=id;setState(id,undo?"undoing":"running");
 var m=MODULES.filter(function(x){return x.id===id;})[0];log((undo?"\u21A9 Reverting ":"\u25B6 ")+m.title);
 var es=new EventSource("/run?module="+encodeURIComponent(id)+(undo?"&undo=1":""));var ok=false;
 es.onmessage=function(ev){log(ev.data);};
 es.addEventListener("done",function(){ok=true;es.close();
   if(undo){setState(id,"reverted");log("\u21A9 reverted");}else{setState(id,"done");log("\u2713 complete");}res();});
 es.onerror=function(){if(!ok){es.close();setState(id,"error");log("\u2717 failed (is the server still running?)");res();}};
});}
function handleOne(id,undo){if(running||status[id]==="running"||status[id]==="undoing")return;running=true;stopFlag=false;core.className="core on";aura.className="aura on";
 runOne(id,undo).then(function(){active=null;running=false;core.className="core";aura.className="aura";});}
document.getElementById("runAll").onclick=function(){
 if(running){stopFlag=true;return;}
 running=true;stopFlag=false;this.classList.add("stop");this.querySelector(".run-txt").innerHTML="&#10022; STOP THE SWEEP";
 core.className="core on";aura.className="aura on";tbody.innerHTML="";
 log("\u2550\u2550\u2550 FULL REPAIR SWEEP STARTED \u2550\u2550\u2550",true);
 var i=0,self=this;
 (function next(){
   if(stopFlag||i>=ORDER.length){if(!stopFlag)log("\uD83C\uDF80 SWEEP DONE \u2014 restart to finish reboot-scheduled fixes",true);else log("\u25A0 stopped by you",true);
     running=false;active=null;core.className="core";aura.className="aura";self.classList.remove("stop");self.querySelector(".run-txt").innerHTML="&#10022; RUN EVERYTHING";return;}
   runOne(ORDER[i++]).then(next);
 })();
};
document.getElementById("clear").onclick=function(){tbody.innerHTML='<p class="empty">cleared \u2014 pick a fix &#10022;</p>';};
</script>
</body></html>"""

if __name__ == "__main__":
    main()
