import subprocess

cmd = """
Get-Process | Where-Object { $_.MainWindowTitle -ne '' -or $_.ProcessName -match 'chrome|edge|browser' } | Select-Object Id, ProcessName, MainWindowTitle | Format-Table -AutoSize
"""

res = subprocess.run(['powershell', '-NoProfile', '-Command', cmd], capture_output=True, text=True)
print(res.stdout)
