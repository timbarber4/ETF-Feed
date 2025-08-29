@echo off
title Auto Sync via GitHub Desktop Commands
color 0A

echo =========================================
echo    AUTO SYNC - GITHUB DESKTOP METHOD
echo =========================================
echo.

cd /d "C:\Users\timot\OneDrive\Documents\GitHub\ETF-Feed"

echo Using GitHub Desktop's exact commands...
echo Monitoring every 15 seconds...
echo.

:LOOP
echo [%TIME%] Checking for changes...

REM Use the exact same Git configuration that GitHub Desktop uses
git config --local user.name "timbarber4" 2>nul
git config --local credential.helper manager-core 2>nul

git add .

git status --porcelain | findstr . >nul
if %ERRORLEVEL% EQU 0 (
    echo   Changes detected - using GitHub Desktop method...
    
    REM Commit exactly like GitHub Desktop does
    git commit -m "Auto-update %DATE% %TIME%"
    
    REM Push using GitHub Desktop's exact method  
    git push "origin" HEAD:main --progress
    
    if %ERRORLEVEL% EQU 0 (
        echo   ✓ SUCCESS! Files pushed to GitHub!
    ) else (
        echo   → Trying alternative push method...
        git push
    )
) else (
    echo   No changes found
)

echo.
timeout /t 15 /nobreak >nul
goto LOOP