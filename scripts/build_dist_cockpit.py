"""
Prepare dist_cockpit for standalone Vercel deployment of Antigravity Manager Cockpit.
"""
import os
import shutil

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DIST_DIR = os.path.join(ROOT_DIR, "dist_cockpit")

def build():
    os.makedirs(os.path.join(DIST_DIR, "mesh"), exist_ok=True)
    os.makedirs(os.path.join(DIST_DIR, "styles"), exist_ok=True)

    # Copy files
    shutil.copy(os.path.join(ROOT_DIR, "antigravity_manager.html"), os.path.join(DIST_DIR, "index.html"))
    shutil.copy(os.path.join(ROOT_DIR, "antigravity_manager.html"), os.path.join(DIST_DIR, "antigravity_manager.html"))
    
    css_src = os.path.join(ROOT_DIR, "styles", "antigravity_manager.css")
    if os.path.exists(css_src):
        shutil.copy(css_src, os.path.join(DIST_DIR, "styles", "antigravity_manager.css"))
        
    shutil.copy(os.path.join(ROOT_DIR, "mesh", "manager_state.json"), os.path.join(DIST_DIR, "mesh", "manager_state.json"))

    vercel_config = '''{
  "name": "antigravity-mesh-cockpit",
  "cleanUrls": true,
  "rewrites": [
    { "source": "/", "destination": "/index.html" },
    { "source": "/api/state", "destination": "/mesh/manager_state.json" },
    { "source": "/mesh/manager_state.json", "destination": "/mesh/manager_state.json" }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "no-cache, no-store, must-revalidate" },
        { "key": "Access-Control-Allow-Origin", "value": "*" }
      ]
    }
  ]
}
'''
    with open(os.path.join(DIST_DIR, "vercel.json"), "w", encoding="utf-8") as f:
        f.write(vercel_config)

    print("✅ dist_cockpit assembled successfully:")
    for r, d, files in os.walk(DIST_DIR):
        for f in files:
            rel = os.path.relpath(os.path.join(r, f), DIST_DIR)
            print(f"  • {rel}")

if __name__ == "__main__":
    build()
