@echo off
title GitHub File Sender - ETF Data
color 0A

echo ================================
echo    GITHUB FILE SENDER STARTED
echo ================================
echo.

REM Change to your ETF-Feed repository directory
cd /d "C:\Users\timot\OneDrive\Documents\GitHub\ETF-Feed"
echo Current directory: %CD%
echo.

REM Set Git to use Windows Credential Manager (same as GitHub Desktop)
git config credential.helper manager 2>nul

:MAIN_LOOP
echo [%DATE% %TIME%] Checking for file changes...

REM Stage all changes in ETF-Feed folder
git add . 2>nul

REM Check if there are staged changes
git diff --cached --quiet 2>nul
if %ERRORLEVEL% EQU 0 (
    echo No changes detected.
) else (
    echo Changes detected! Committing...
    
    REM Commit changes
    git commit -m "Auto-update: %DATE% %TIME%" 2>nul
    
    REM Push without specifying remote (uses default)
    echo Pushing to GitHub...
    git push 2>nul
    
    if %ERRORLEVEL% EQU 0 (
        echo ✓ Successfully uploaded to GitHub!
        echo ✓ Files are now live online!
    ) else (
        echo → Files committed locally (will sync on next GitHub Desktop open)
    )
)

echo.
echo Waiting 15 seconds for next check...
timeout /t 15 /nobreak >nul

goto MAIN_LOOP