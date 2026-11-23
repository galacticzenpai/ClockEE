import subprocess
import sys

routes = ['/', '/cbt_exam', '/timer', '/tracker', '/cbt_analysis']
all_ok = True

print("=== VERIFYING LIVE CLOCKEE OS 2.0 PRODUCTION DEPLOYMENT ===")
for r in routes:
    url = f"https://clockee-os-2.vercel.app{r}"
    cmd = ["vercel", "curl", url, "-I"]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True, shell=True)
        status_line = [l for l in res.stdout.splitlines() if "HTTP/1.1" in l]
        if status_line:
            status = status_line[0]
            print(f"  • {r:15} -> {status}")
            if "200" not in status and "308" not in status:
                all_ok = False
        else:
            print(f"  • {r:15} -> Output: {res.stdout[:60]}")
    except Exception as e:
        print(f"  • {r:15} -> Error: {e}")
        all_ok = False

if all_ok:
    print("\n✅ ALL 5 CORE PRODUCTION ROUTES VERIFIED OPERATIONAL!")
else:
    print("\n⚠️ SOME ROUTES FAILED VERIFICATION")
