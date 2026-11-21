with open('live_tracker.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Make sure live_tracker.html checks mesh/mesh_tracker_state.json directly with no server dependency
target = "let res = await fetch('/api/tracker?t=' + Date.now());"
replacement = """let resFallback = await fetch('mesh/mesh_tracker_state.json?t=' + Date.now());
        if (resFallback.ok) {
          globalData = await resFallback.json();
          renderAll();
          return;
        }
        let res = await fetch('/api/tracker?t=' + Date.now());"""

if target in text:
    text = text.replace(target, replacement)
    print("Replaced /api/tracker primary with mesh/mesh_tracker_state.json file-based loader")

with open('live_tracker.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Saved live_tracker.html successfully")
