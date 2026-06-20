@echo off
setlocal EnableExtensions

rem ==========================================================================
rem  update.bat - Force-update this folder from the project's main branch.
rem
rem  This overwrites EVERYTHING in the folder this script lives in with the
rem  latest contents of the "main" branch on GitHub. Any local changes,
rem  untracked files, or edits will be discarded.
rem
rem  If the folder is not a git repository yet (no .git folder), this script
rem  bootstraps one: it initializes a repo, points it at the GitHub remote,
rem  then force-pulls main.
rem ==========================================================================

set "REPO_URL=https://github.com/ferisooo/advanced-repair.git"
set "BRANCH=main"

rem Work in the folder where this script is located.
cd /d "%~dp0"

rem Make sure git is available.
where git >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed or not on your PATH.
    echo         Install Git from https://git-scm.com/download/win and retry.
    goto :fail
)

echo This will OVERWRITE everything in:
echo     "%CD%"
echo with the latest "%BRANCH%" branch from:
echo     %REPO_URL%
echo.
echo Any local changes will be permanently lost.
echo.
choice /C YN /N /M "Continue? [Y/N] "
if errorlevel 2 (
    echo Cancelled.
    goto :end
)
echo.

rem Bootstrap git if this is not a repository yet.
if not exist ".git" (
    echo [*] No .git folder found - bootstrapping a new repository...
    git init || goto :fail
    git remote add origin "%REPO_URL%" || goto :fail
) else (
    rem Repo exists: make sure the remote is present and correct.
    git remote get-url origin >nul 2>&1
    if errorlevel 1 (
        git remote add origin "%REPO_URL%" || goto :fail
    ) else (
        git remote set-url origin "%REPO_URL%" || goto :fail
    )
)

echo [*] Fetching latest "%BRANCH%"...
git fetch origin "%BRANCH%" || goto :fail

echo [*] Force-resetting working tree to origin/%BRANCH%...
git checkout -B "%BRANCH%" || goto :fail
git reset --hard "origin/%BRANCH%" || goto :fail

echo [*] Removing untracked files and folders...
git clean -fdx

echo.
echo [OK] Update complete. Folder now matches origin/%BRANCH%.
goto :end

:fail
echo.
echo [ERROR] Update failed. See the messages above for details.
endlocal
exit /b 1

:end
endlocal
exit /b 0
