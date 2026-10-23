@echo off
title ClockEE GitHub Auto-Sync & Publisher
cd /d "%~dp0"
echo ========================================================
echo        Starting ClockEE GitHub Auto-Sync Watcher
echo ========================================================
python auto_sync.py
if errorlevel 1 (
    echo.
    echo [!] Process exited. Press any key to close this window.
    pause >nul
)
