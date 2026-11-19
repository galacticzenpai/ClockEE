---
name: network-telemetry
description: Zero-network offline heartbeat and developer diagnostics console accessible via Ctrl+Shift+D for monitoring IndexedDB, sync queues, and heap memory.
---

# Zero-Network Offline Heartbeat & Sync Diagnostics Console

Reel: #24 (https://www.instagram.com/p/DfW6r1fCMd-/)
Package: `integrations/network_telemetry/`

## Capabilities
- Displays a retro technical terminal diagnostics console toggled via `Ctrl+Shift+D`.
- Telemetry worker monitors IndexedDB transactions, offline mutations queue size, and memory usage.
- Zero main-thread CPU overhead (<0.1%) using requestIdleCallback / Worker threads.
