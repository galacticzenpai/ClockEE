---
name: graphify-knowledge-graph
description: Codebase knowledge graph generator and god-node architectural analyzer adapted from Graphify (Graphify-Labs/graphify, Apache-2.0 / MIT). Parses cross-file imports, database schemas, and shared dependencies deterministically without requiring remote LLM calls.
---

# Graphify: Codebase Knowledge Graph & God-Node Analyzer for ClockEE

Adapted from the open-source **Graphify** tool (`Graphify-Labs/graphify`, Apache-2.0 / MIT License).

## Overview
When AI coding agents or developers rename fields, schemas, or variables, search-and-replace often fails to anticipate cascading failures across distant files, shared views, or startup configs.

Graphify scans the entire ClockEE repository:
1. **Deterministic AST Extraction**: Maps all JavaScript, Python, HTML `<script>` tags, and SQLite schemas into an entity-relationship graph.
2. **God-Node Identification**: Detects the architectural single points of failure (the files or modules that everything depends on, e.g., `clockee_core.js`, `cbt_shared.js`, `server.py`).
3. **Cross-Boundary Link Mapping**: Traces relationships between frontend storage keys, database table columns, and API endpoints before any rename is executed.
4. **Machine & Human Reports**: Outputs visual graph data (`graph.json`) and an architectural breakdown (`GRAPH_REPORT.md`).

---

## The Three Core Commands

### 1. Build Knowledge Graph
```powershell
python integrations/graphify/graph_runner.py build
```

### 2. Inspect God Nodes & Chokepoints
```powershell
python integrations/graphify/graph_runner.py god-nodes
```

### 3. Impact Analysis / "What Uses This?"
```powershell
python integrations/graphify/graph_runner.py query <symbol_or_filename>
```
