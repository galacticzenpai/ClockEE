@echo off
title ClockEE 24/7 Autonomous Mesh Daemon
cd /d "d:\Desktop\ClockEE"

echo =========================================================================
echo   CLOCKEE 24/7 AUTONOMOUS MESH DAEMON & REAL-TIME IPC DISPATCHER
echo =========================================================================
echo Workspace: d:\Desktop\ClockEE
echo Target: All 10 Autonomous Mesh Conversations
echo Timestamp: %DATE% %TIME%
echo =========================================================================

:: 1. Ensure local HTTP server on port 8000 is running for tracker.html
netstat -ano | findstr ":8000" | findstr "LISTENING" >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] Starting local HTTP Server on port 8000...
    start /b python -m http.server 8000 >nul 2>&1
    echo [✔] Local HTTP Server running on http://localhost:8000/tracker.html
) else (
    echo [✔] Local HTTP Server already active on port 8000.
)

:: 2. Continuous Resilient Daemon Loop for Mesh Continuous Bridge
:daemon_loop
echo.
echo [*] Launching Continuous Mesh Bridge (python -u .pipeline/mesh_continuous_bridge.py)...
python -u .pipeline\mesh_continuous_bridge.py >> .pipeline\daemon.log 2>&1
echo [!] Warning: Mesh Bridge exited with code %errorlevel%. Restarting in 3 seconds...
timeout /t 3 /nobreak >nul
goto daemon_loop
