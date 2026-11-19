@echo off
title Chitti 2.0 Live Mesh Service
cd /d "%~dp0"
echo Starting Chitti 2.0 Continuous Mesh Service on http://localhost:5500...
start "" /b pythonw mesh\server.py
echo ✅ Service running silently in background.
echo Open http://localhost:5500 in your browser.
pause
