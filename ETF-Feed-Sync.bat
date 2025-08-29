@echo off
title ETF Feed Auto Sync  
color 0A
cls

echo =====================================
echo        ETF FEED AUTO SYNC
echo   (Using GitHub Desktop Authentication)
echo =====================================
echo.

REM Navigate to your ETF-Feed folder
cd /d "C:\Users\timot\OneDrive\Documents\GitHub\ETF-Feed"

REM Verify we're in the right place
if not exist ".git" (
    echo ERROR: Not in a Git repository!
    pause
    exit /b 1
)

REM Configure git to use the same credentials as GitHub Desktop
git config credential.helper manager-core 2>nul
if %ERRORLEVEL% NEQ 0 (
    git config credential.helper manager 2>nul
)

echo Monitoring folder: %CD%
echo Using GitHub Desktop's saved credentials...
echo Checking every 15 seconds...
echo Press Ctrl+C to stop
echo.

:LOOP
echo [%TIME%] Checking for changes...

git add .

git diff --staged --quiet
if %ERRORLEVEL% EQU 0 (
    echo   No changes found
) else (
    echo   Changes detected - committing and pushing...
    git commit -m "Auto-update %DATE% %TIME%"
    
    REM This is the key - push with the same method that worked before
    git push origin main
    
    if %ERRORLEVEL% EQU 0 (
        echo   ✓ Successfully synced to GitHub!
        echo   ✓ Available at: https://raw.githubusercontent.com/timbarber4/ETF-Feed/main/[filename]
    ) else (
        echo   → Push attempted - check GitHub Desktop for status
    )
)

echo.
timeout /t 15 /nobreak >nul
goto LOOP