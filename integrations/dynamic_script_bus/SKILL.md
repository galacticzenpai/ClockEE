---
name: dynamic-script-bus
description: CORS-immune local-first dynamic JavaScript synchronization bus bypassing browser local file restrictions completely for instant cockpit dashboard hydration.
---

# CORS-Immune Local-First Dynamic JavaScript Bus

Reel: #34 (https://www.instagram.com/p/DfcssAvBG7L/)
Package: `integrations/dynamic_script_bus/`

## Capabilities
- Injects dynamic `<script src=".pipeline/tracker_data.js?t=...">` tags on local `file:///` viewports.
- Bypasses all browser cross-origin policy restrictions when viewing offline files without a local web server.
- Synchronized in sub-10ms via `.pipeline/tracker_sync.py`.
