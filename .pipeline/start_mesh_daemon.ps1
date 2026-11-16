# Launch ClockEE Continuous Mesh Bridge as a detached background process
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BridgeScript = Join-Path $ScriptDir "mesh_continuous_bridge.py"
$LogFile = Join-Path $ScriptDir "mesh_bridge.log"

# Check if already running
$Existing = Get-Process python, pythonw -ErrorAction SilentlyContinue | Where-Object {
    $cmd = (Get-CimInstance Win32_Process -Filter "ProcessId = $($_.Id)").CommandLine
    $cmd -like "*mesh_continuous_bridge.py*"
}

if ($Existing) {
    Write-Host "ClockEE Mesh Bridge is already running (PID: $($Existing.Id))."
} else {
    Write-Host "Starting ClockEE Mesh Bridge daemon..."
    Start-Process -FilePath "python.exe" -ArgumentList "-u", "`"$BridgeScript`"" -RedirectStandardOutput $LogFile -RedirectStandardError $LogFile -WindowStyle Hidden
    Start-Sleep -Seconds 1
    $Started = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
        $cmd = (Get-CimInstance Win32_Process -Filter "ProcessId = $($_.Id)").CommandLine
        $cmd -like "*mesh_continuous_bridge.py*"
    }
    if ($Started) {
        Write-Host "✔ Successfully launched Mesh Bridge daemon (PID: $($Started.Id))!"
    } else {
        Write-Host "⚠️ Process started. Check $LogFile for details."
    }
}
