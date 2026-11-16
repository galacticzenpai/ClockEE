import glob, re

print("Searching for tracker.html references across all HTML and JS files...")
for fname in sorted(glob.glob("*.html") + glob.glob("*.js") + glob.glob(".pipeline/*.py") + glob.glob(".pipeline/*.json") + glob.glob("api/*.py")):
    try:
        with open(fname, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        if "tracker.html" in content or "file:///D:/Desktop/ClockEE/tracker.html" in content or "clockee.vercel.app" in content or "clockee-os.vercel.app" in content:
            print(f"\nFile: {fname}")
            for m in re.finditer(r'(file:///D:/Desktop/ClockEE/tracker\.html|https?://[^\s"\'<>]+/tracker\.html|[^\s"\'<>]*/tracker\.html|https?://clockee[^\s"\'<>]*vercel\.app)', content):
                print(f"  Match: {m.group(0)}")
    except Exception as e:
        print(f"Error reading {fname}: {e}")
