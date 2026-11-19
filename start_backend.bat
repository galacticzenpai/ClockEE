@echo off
title ClockEE Master Tactical Cockpit Engine & SQLite Backend
cd /d "%~dp0"
echo ========================================================
echo   ⚡ Starting ClockEE Full-Stack Server & SQLite Backend
echo ========================================================
python server.py
if errorlevel 1 (
    echo.
    echo [!] Server exited with error. Press any key to close.
    pause >nul
)
