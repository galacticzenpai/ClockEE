#!/usr/bin/env python3
"""
ClockEE Package: Graphify Knowledge Graph & God-Node Analyzer
Adapted from Graphify-Labs/graphify (Apache-2.0 / MIT License).

Extracts local code entities, imports, script tags, schema definitions,
and cross-file dependencies into a deterministic knowledge graph.
"""

import os
import re
import sys
import json
import time
from pathlib import Path
from collections import defaultdict

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = Path(__file__).resolve().parent / "reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

class CodeKnowledgeGraph:
    def __init__(self, workspace: Path = ROOT_DIR):
        self.workspace = workspace
        self.nodes = {}  # {node_id: {type, file, name, lines}}
        self.edges = []  # [{source, target, relation}]
        self.in_degree = defaultdict(int)
        self.out_degree = defaultdict(int)

    def add_node(self, node_id: str, node_type: str, file_path: str, meta: dict = None):
        if node_id not in self.nodes:
            self.nodes[node_id] = {
                "id": node_id,
                "type": node_type,
                "file": file_path,
                "meta": meta or {}
            }

    def add_edge(self, source: str, target: str, relation: str):
        self.edges.append({
            "source": source,
            "target": target,
            "relation": relation
        })
        self.out_degree[source] += 1
        self.in_degree[target] += 1

    def scan_codebase(self):
        """Deterministically parses files, script inclusions, imports, and schemas."""
        # 1. Scan HTML entry points and script dependencies
        for html_file in self.workspace.glob("*.html"):
            rel_name = html_file.name
            self.add_node(rel_name, "HTML_ENTRYPOINT", rel_name)
            try:
                content = html_file.read_text(encoding="utf-8", errors="ignore")
                # Script src tags
                scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', content, re.I)
                for s in scripts:
                    clean_s = os.path.basename(s.split("?")[0])
                    self.add_node(clean_s, "SCRIPT_MODULE", clean_s)
                    self.add_edge(rel_name, clean_s, "INCLUDES_SCRIPT")
                # Stylesheet links
                links = re.findall(r'<link[^>]+href=["\']([^"\']+\.css)["\']', content, re.I)
                for l in links:
                    clean_l = os.path.basename(l.split("?")[0])
                    self.add_node(clean_l, "STYLESHEET", clean_l)
                    self.add_edge(rel_name, clean_l, "INCLUDES_STYLE")
                # Storage keys accessed
                storage_keys = re.findall(r'(?:localStorage|sessionStorage)\.(?:getItem|setItem)\(["\']([^"\']+)["\']', content)
                for k in set(storage_keys):
                    k_id = f"storage:{k}"
                    self.add_node(k_id, "STORAGE_KEY", rel_name, {"key": k})
                    self.add_edge(rel_name, k_id, "READS_WRITES_KEY")
            except Exception:
                pass

        # 2. Scan JavaScript files
        for js_file in self.workspace.glob("*.js"):
            if "vendor" in js_file.parts or ".git" in js_file.parts:
                continue
            rel_name = js_file.name
            self.add_node(rel_name, "JS_MODULE", rel_name)
            try:
                content = js_file.read_text(encoding="utf-8", errors="ignore")
                # Functions declared
                functions = re.findall(r'(?:function\s+([a-zA-Z0-9_$]+)|(?:const|let|var)\s+([a-zA-Z0-9_$]+)\s*=\s*(?:function|\([^)]*\)\s*=>))', content)
                for f_tuple in functions:
                    fn_name = f_tuple[0] or f_tuple[1]
                    if fn_name and len(fn_name) > 2:
                        fn_id = f"{rel_name}::{fn_name}"
                        self.add_node(fn_id, "FUNCTION", rel_name, {"name": fn_name})
                        self.add_edge(rel_name, fn_id, "DEFINES_FUNCTION")
                # Global window assignments (API contracts)
                window_props = re.findall(r'window\.([a-zA-Z0-9_$]+)\s*=', content)
                for wp in set(window_props):
                    wp_id = f"global:{wp}"
                    self.add_node(wp_id, "GLOBAL_API", rel_name, {"prop": wp})
                    self.add_edge(rel_name, wp_id, "EXPOSES_GLOBAL")
            except Exception:
                pass

        # 3. Scan Python Backend & Database Schemas
        for py_file in self.workspace.glob("**/*.py"):
            if ".git" in py_file.parts or "venv" in py_file.parts or ".gemini" in py_file.parts:
                continue
            rel_path = str(py_file.relative_to(self.workspace))
            self.add_node(rel_path, "PYTHON_MODULE", rel_path)
            try:
                content = py_file.read_text(encoding="utf-8", errors="ignore")
                # Table schemas
                tables = re.findall(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([a-zA-Z0-9_]+)', content, re.I)
                for t in set(tables):
                    t_id = f"table:{t}"
                    self.add_node(t_id, "DB_TABLE", rel_path, {"table": t})
                    self.add_edge(rel_path, t_id, "DEFINES_SCHEMA")
                # API Endpoints
                endpoints = re.findall(r'(?:@app\.route|def\s+do_[A-Z]+|url\s*==\s*)["\'](/[a-zA-Z0-9_/-]*)', content)
                for ep in set(endpoints):
                    ep_id = f"endpoint:{ep}"
                    self.add_node(ep_id, "API_ENDPOINT", rel_path, {"route": ep})
                    self.add_edge(rel_path, ep_id, "HANDLES_ROUTE")
            except Exception:
                pass

    def get_god_nodes(self, top_n: int = 8):
        """Identify architectural bottleneck nodes with highest inbound connections."""
        scored = []
        for n_id, data in self.nodes.items():
            if data["type"] in ["SCRIPT_MODULE", "JS_MODULE", "PYTHON_MODULE", "GLOBAL_API"]:
                score = self.in_degree[n_id]
                scored.append((n_id, score, data["type"], data["file"]))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_n]

    def query_symbol(self, query: str):
        """Trace what depends on or is connected to a specific symbol or filename."""
        query_lower = query.lower()
        matched_nodes = [nid for nid in self.nodes if query_lower in nid.lower()]
        results = []
        for nid in matched_nodes:
            incoming = [e["source"] for e in self.edges if e["target"] == nid]
            outgoing = [e["target"] for e in self.edges if e["source"] == nid]
            results.append({
                "node": self.nodes[nid],
                "depended_on_by": incoming,
                "depends_on": outgoing
            })
        return results

    def build_and_export(self):
        self.scan_codebase()
        god_nodes = self.get_god_nodes()

        graph_data = {
            "version": "1.0.0",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "generator": "Graphify Knowledge Graph (Graphify-Labs/graphify)",
            "metrics": {
                "total_nodes": len(self.nodes),
                "total_edges": len(self.edges),
                "god_nodes_detected": len(god_nodes)
            },
            "god_nodes": [
                {"id": gn[0], "inbound_dependents": gn[1], "type": gn[2], "file": gn[3]}
                for gn in god_nodes
            ],
            "nodes": list(self.nodes.values()),
            "edges": self.edges
        }

        # Write JSON graph
        out_json = OUTPUT_DIR / "graph.json"
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(graph_data, f, indent=2)

        # Write human-readable Markdown architectural report
        out_report = OUTPUT_DIR / "GRAPH_REPORT.md"
        with open(out_report, "w", encoding="utf-8") as f:
            f.write("# 🌐 ClockEE Codebase Architecture & Knowledge Graph Report\n\n")
            f.write(f"*Generated on {graph_data['timestamp']} by Graphify*\n\n")
            f.write("### 📊 Metrics\n")
            f.write(f"- **Total Entities Mapped**: {len(self.nodes)}\n")
            f.write(f"- **Total Dependencies / Edges**: {len(self.edges)}\n")
            f.write(f"- **God Nodes Identified**: {len(god_nodes)}\n\n")
            f.write("### ⚠️ Architectural God Nodes (High Risk Chokepoints)\n")
            f.write("Renaming or altering any function inside these files will cascade across the dependent files:\n\n")
            f.write("| Node / Module | Type | Inbound Dependents | Impact Risk |\n")
            f.write("| :--- | :--- | :---: | :--- |\n")
            for gn in god_nodes:
                risk = "🔴 CRITICAL" if gn[1] >= 10 else "🟠 HIGH" if gn[1] >= 5 else "🟡 MODERATE"
                f.write(f"| `{gn[0]}` | {gn[2]} | **{gn[1]} files** | {risk} |\n")
            f.write("\n---\n*Use `python integrations/graphify/graph_runner.py query <name>` before modifying any symbol.*")

        return graph_data, out_json, out_report

if __name__ == "__main__":
    runner = CodeKnowledgeGraph()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"

    if cmd == "build":
        data, j_path, r_path = runner.build_and_export()
        print("=" * 68)
        print(" GRAPHIFY: CODEBASE KNOWLEDGE GRAPH & ARCHITECTURE MAP")
        print("=" * 68)
        print(f"Entities Indexed      : {data['metrics']['total_nodes']}")
        print(f"Dependency Edges      : {data['metrics']['total_edges']}")
        print(f"Top God Node Detected : {data['god_nodes'][0]['id'] if data['god_nodes'] else 'None'} ({data['god_nodes'][0]['inbound_dependents']} dependents)")
        print(f"Graph Data Saved      : {j_path}")
        print(f"Architecture Report   : {r_path}")
        print("=" * 68)
    elif cmd == "god-nodes":
        runner.scan_codebase()
        gn = runner.get_god_nodes()
        print("=" * 68)
        print(" TOP ARCHITECTURAL GOD NODES (Single Points of Failure)")
        print("=" * 68)
        for idx, item in enumerate(gn, 1):
            print(f"{idx}. {item[0]} [{item[2]}] ➔ {item[1]} dependent files")
        print("=" * 68)
    elif cmd == "query":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        if not query:
            print("Please specify a symbol or file: python graph_runner.py query <name>")
            sys.exit(1)
        runner.scan_codebase()
        res = runner.query_symbol(query)
        print("=" * 68)
        print(f" GRAPHIFY IMPACT QUERY FOR: '{query}'")
        print("=" * 68)
        for r in res:
            print(f"\nNode: {r['node']['id']} ({r['node']['type']})")
            print(f"  Used by ({len(r['depended_on_by'])} files): {', '.join(r['depended_on_by'][:6])}")
            print(f"  Depends on ({len(r['depends_on'])} targets): {', '.join(r['depends_on'][:6])}")
        print("=" * 68)
