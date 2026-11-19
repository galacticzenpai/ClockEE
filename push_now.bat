@echo off
title Push ClockEE Changes Now
cd /d "%~dp0"
python auto_sync.py --once
echo.
echo Sync completed. Press any key to exit.
pause >nul
