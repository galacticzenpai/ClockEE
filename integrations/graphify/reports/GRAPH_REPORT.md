# 🌐 ClockEE Codebase Architecture & Knowledge Graph Report

*Generated on 2026-11-16 00:59:18 by Graphify*

### 📊 Metrics
- **Total Entities Mapped**: 263
- **Total Dependencies / Edges**: 320
- **God Nodes Identified**: 8

### ⚠️ Architectural God Nodes (High Risk Chokepoints)
Renaming or altering any function inside these files will cascade across the dependent files:

| Node / Module | Type | Inbound Dependents | Impact Risk |
| :--- | :--- | :---: | :--- |
| `env.js` | SCRIPT_MODULE | **21 files** | 🔴 CRITICAL |
| `cdn.tailwindcss.com` | SCRIPT_MODULE | **17 files** | 🔴 CRITICAL |
| `clockee_core.js` | SCRIPT_MODULE | **16 files** | 🔴 CRITICAL |
| `chart.js` | SCRIPT_MODULE | **9 files** | 🟠 HIGH |
| `cbt_shared.js` | SCRIPT_MODULE | **9 files** | 🟠 HIGH |
| `html2canvas.min.js` | SCRIPT_MODULE | **6 files** | 🟠 HIGH |
| `katex.min.js` | SCRIPT_MODULE | **4 files** | 🟡 MODERATE |
| `marked.min.js` | SCRIPT_MODULE | **4 files** | 🟡 MODERATE |

---
*Use `python integrations/graphify/graph_runner.py query <name>` before modifying any symbol.*