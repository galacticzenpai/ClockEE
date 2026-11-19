# 🌐 ClockEE Codebase Architecture & Knowledge Graph Report

*Generated on 2026-11-19 23:30:30 by Graphify*

### 📊 Metrics
- **Total Entities Mapped**: 356
- **Total Dependencies / Edges**: 351
- **God Nodes Identified**: 8

### ⚠️ Architectural God Nodes (High Risk Chokepoints)
Renaming or altering any function inside these files will cascade across the dependent files:

| Node / Module | Type | Inbound Dependents | Impact Risk |
| :--- | :--- | :---: | :--- |
| `cdn.tailwindcss.com` | SCRIPT_MODULE | **21 files** | 🔴 CRITICAL |
| `env.js` | SCRIPT_MODULE | **14 files** | 🔴 CRITICAL |
| `clockee_core.js` | SCRIPT_MODULE | **10 files** | 🔴 CRITICAL |
| `navbar.js` | SCRIPT_MODULE | **8 files** | 🟠 HIGH |
| `db.js` | SCRIPT_MODULE | **7 files** | 🟠 HIGH |
| `katex.min.js` | SCRIPT_MODULE | **6 files** | 🟠 HIGH |
| `chart.js` | SCRIPT_MODULE | **5 files** | 🟠 HIGH |
| `cbt_shared.js` | SCRIPT_MODULE | **5 files** | 🟠 HIGH |

---
*Use `python integrations/graphify/graph_runner.py query <name>` before modifying any symbol.*