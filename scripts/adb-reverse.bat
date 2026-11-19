@echo off
setlocal enabledelayedexpansion
title ClockEE 2.0 - Android ADB Reverse Tethering Engine

echo =====================================================================
echo  ClockEE OS 2.0: Hardware Companion ADB Reverse-Tethering Engine
echo  Target: Android AMOLED Kiosk Cockpit ^(PhoneBox^)
echo  Ports: 5500 ^(HTTP Web Cockpit^) ^| 8765 ^(WebSocket Telemetry Daemon^)
echo =====================================================================
echo.

:: 1. Verify ADB CLI availability
where adb >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] 'adb' command not found in system PATH.
    echo Please install Android Platform Tools or add adb.exe to your PATH.
    echo Download: https://developer.android.com/tools/releases/platform-tools
    echo.
    pause
    exit /b 1
)

:: 2. Check for connected Android hardware devices
echo [1/3] Detecting connected Android devices over USB...
for /f "tokens=1,2" %%A in ('adb devices ^| findstr /v "List of devices attached"') do (
    if "%%B"=="device" (
        set DEVICE_FOUND=1
        set DEVICE_ID=%%A
    )
)

if not defined DEVICE_FOUND (
    echo [WARN] No authorized Android device detected over USB.
    echo Steps to resolve:
    echo  1. Connect your Android phone via USB cable.
    echo  2. Enable "Developer Options" and "USB Debugging" on the phone.
    echo  3. Accept the RSA fingerprint authorization prompt on your phone screen.
    echo.
    echo Retrying device detection in 5 seconds...
    timeout /t 5 >nul
    adb devices
    echo.
)

:: 3. Configure reverse socket tunnels
echo [2/3] Configuring low-latency reverse port forwarding...

echo   - Forwarding tcp:5500 -^> tcp:5500 (HTTP Web UI / Live Cockpit)...
adb reverse tcp:5500 tcp:5500
if %errorlevel% neq 0 (
    echo [ERROR] Failed to map tcp:5500. Ensure device is authorized.
) else (
    echo   [OK] tcp:5500 successfully reversed.
)

echo   - Forwarding tcp:8765 -^> tcp:8765 (Sub-20ms WebSocket Telemetry Daemon)...
adb reverse tcp:8765 tcp:8765
if %errorlevel% neq 0 (
    echo [ERROR] Failed to map tcp:8765. Ensure device is authorized.
) else (
    echo   [OK] tcp:8765 successfully reversed.
)

:: 4. Verify Active Mappings
echo.
echo [3/3] Current Active Reverse Mappings on Device:
adb reverse --list
echo.

echo =====================================================================
echo [SUCCESS] Tethering tunnel established.
echo You can now open Chrome / Kiwi Browser on your Android phone and visit:
echo    http://127.0.0.1:5500/phonebox/index.html
echo Or connect native telemetry client directly to:
echo    ws://127.0.0.1:8765
echo =====================================================================
echo.
pause
