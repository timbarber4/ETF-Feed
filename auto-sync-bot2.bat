@echo off
title Live Data Auto-Sync
color 0A

echo ========================================
echo  Live Data Feed - Auto GitHub Upload
echo  Checking every 1 minute
echo ========================================
echo.

REM Change this path to your repository folder
cd /d "C:\Users\timot\OneDrive\Documents\GitHub\ETF-Feed

:LOOP
echo [%time%] Checking for file changes...

REM Add all files to git
git add .

REM Check if there are changes
git diff --staged --quiet
if %ERRORLEVEL% NEQ 0 (
    echo [%time%] File updated! Uploading to GitHub...
    git commit -m "Auto-update data file - %date% %time%"
    git push
    echo [%time%] ✓ Live data updated on GitHub!
    echo [%time%] ✓ Available at: https://raw.githubusercontent.com/timbarber4/Live-data-feed/main/Test%%20Spreader.txt
) else (
    echo [%time%] No changes detected.
)

echo [%time%] Next check in 1 minute...
echo.

timeout /t 30 /nobreak > nul
goto LOOP