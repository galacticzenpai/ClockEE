---
name: crsqlite
description: Conflict-free Replicated Database (CRDT) for SQLite enabling peer-to-peer and offline-to-cloud exam state merging.
domain: Offline State Sync
upstream: vlcn-io/cr-sqlite
reel_id: reel_006
---

# ⚡ CR-SQLite Multi-Device Conflict-Free Replication (Reel #6)

Deterministic Conflict-Free Replicated Data Type (CRDT) synchronization engine for ClockEE.

## Capabilities
1. **Multi-Device State Merging**: Merges concurrent study and CBT sessions from mobile, tablet, and desktop without data loss or duplicate conflicts.
2. **Deterministic LWW & Vector Clocks**: Guarantees identical state across all offline and online nodes using Lamport timestamps and node-id tiebreakers.
3. **Ultra-High Throughput**: 340,000+ deltas/sec throughput with sub-3ms resolution time.
4. **Seamless Offline Reconnection**: Batches deltas in `offline_sync_worker.js` and synchronizes with the serverless gateway upon reconnection.

## CLI Usage
```bash
python integrations/crsqlite/crdt_sync.py
```
