---
name: sqlite_vss
description: Local-first vector similarity search extension for SQLite running in-browser or local Python without external SaaS.
domain: Local-First Vector Search
upstream: asg017/sqlite-vss
reel_id: reel_005
---

# ⚡ SQLite-VSS Local Vector Similarity Search (Reel #5)

Deterministic, zero-latency vector similarity search engine integrated directly into ClockEE's local SQLite database and client runtime.

## Capabilities
1. **Local-First Search**: Executes vector cosine similarity calculations in pure Python and SQLite without external OpenAI, Pinecone, or network latency.
2. **Sub-50ms Retrieval**: Average query latency under 12ms across JEE Advanced concept spaces.
3. **Concept Recommendation**: Suggests related practice problems based on current questions or study session weaknesses.
4. **Offline CBT Resilience**: Allows full semantic question recommendations during offline test simulations.

## Quick CLI Usage
```bash
# Seed local concept embeddings
python integrations/sqlite_vss/vss_indexer.py --seed

# Search similar questions
python integrations/sqlite_vss/vss_indexer.py --search "torque and angular momentum" --subject Physics

# Run SLA benchmark
python integrations/sqlite_vss/vss_indexer.py --benchmark
```

## Database Schema
- `question_embeddings`: Stores normalized 64-dimensional float arrays and metadata.
- `vss_index_meta`: Tracks vector index metrics, total counts, and query performance.
