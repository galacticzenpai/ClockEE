---
name: mesh-switchboard
description: Multi-agent event switchboard tracking active phases, floor prompts, and priority queues across all 10 conversations in ClockEE.
---

# Centralized IPC Message Routing & Handoff Priority Queue

Reel: #33 (https://www.instagram.com/p/DfWuPg8p5Ho/)
Package: `integrations/mesh_switchboard/`

## Capabilities
- Routes tasks across 10 specialized conversations (Main Feature, UI/UX, Simulation, DB, GitHub, Q&A, Inspiration, Bug Fixes, Backbone).
- Anti-bottleneck classification preventing task starvation.
- In-process quality gates integration.
- Automated stage queue persistence (`.pipeline/queue.json`).
