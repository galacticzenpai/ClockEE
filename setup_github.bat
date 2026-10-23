@echo off
title Setup ClockEE GitHub Connection
cd /d "%~dp0"
python auto_sync.py --setup
echo.
echo Setup finished. Press any key to exit.
pause >nul
