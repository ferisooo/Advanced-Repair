@echo off
setlocal
:: =====================================================
::   Kawaii PC Repair - launcher  (｡♥‿♥｡)
::   double-click me~ asks for admin, opens in browser
:: =====================================================

:: --- force admin (the fixes need it) ---
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Need admin rights~ asking for them...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

title Kawaii PC Repair (keep me open~)
cd /d "%~dp0"

:: --- find python (py launcher first, then python) ---
where py >nul 2>&1 && (set "PY=py") || (set "PY=python")
%PY% --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  (>_<) Python isn't installed or not on PATH.
    echo  Grab it from https://www.python.org/downloads/
    echo  and tick "Add Python to PATH" during setup.
    echo.
    pause
    exit /b
)

echo.
echo  Starting Kawaii Repair~ your browser will open in a sec (^o^)
echo  Keep THIS window open while you use it. Close it to stop.
echo.
%PY% "%~dp0kawaii_repair.py"
pause
