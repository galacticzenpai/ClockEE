import os
import shutil

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DIST_DIR = os.path.join(ROOT_DIR, "cockpit_dist")

os.makedirs(os.path.join(DIST_DIR, "mesh"), exist_ok=True)
os.makedirs(os.path.join(DIST_DIR, "styles"), exist_ok=True)

shutil.copy(os.path.join(ROOT_DIR, "antigravity_manager.html"), os.path.join(DIST_DIR, "index.html"))

css_src = os.path.join(ROOT_DIR, "styles", "antigravity_manager.css")
if os.path.exists(css_src):
    shutil.copy(css_src, os.path.join(DIST_DIR, "styles", "antigravity_manager.css"))

shutil.copy(os.path.join(ROOT_DIR, "mesh", "manager_state.json"), os.path.join(DIST_DIR, "mesh", "manager_state.json"))

with open(os.path.join(DIST_DIR, "vercel.json"), "w", encoding="utf-8") as f:
    f.write('{\n  "cleanUrls": true\n}\n')

print("cockpit_dist prepared successfully")
