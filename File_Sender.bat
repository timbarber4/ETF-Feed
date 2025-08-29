@echo off
title Auto GitHub Sync - Live Data Feed
color 0A

echo ================================
echo    AUTO GITHUB SYNC STARTED
echo ================================
echo.

REM Change to your repository directory
cd /d "%~dp0"
echo Current directory: %CD%
echo.

REM Check if Git is installed
git --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)

:MAIN_LOOP
echo [%DATE% %TIME%] Checking for file changes...

REM Add all changed files except large ones
git add . --ignore-errors

REM Check if there are staged changes
git diff --staged --quiet
if %ERRORLEVEL% EQU 0 (
    echo No changes detected.
) else (
    echo Changes detected! Committing and pushing...
    
    REM Commit with timestamp
    git commit -m "Auto-update: %DATE% %TIME%"
    
    REM Push to GitHub
    git push origin main 2>error.log
    if %ERRORLEVEL% EQU 0 (
        echo Success! Pushed to GitHub!
    ) else (
        echo Push failed. Check error.log for details.
        type error.log
    )
)

echo.
echo Waiting 15 seconds for next check...
echo Press Ctrl+C to stop
timeout /t 15 /nobreak >nul

goto MAIN_LOOP