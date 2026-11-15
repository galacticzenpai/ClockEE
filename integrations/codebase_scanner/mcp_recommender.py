#!/usr/bin/env python3
"""
ClockEE Package: Codebase Architecture & MCP Recommender
Analyzes project architecture, file dependencies, and configuration,
then generates recommended skills, MCP servers, and agent capabilities.
"""

import os
import sys
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

def scan_codebase_structure():
    files = []
    ext_counts = {}
    total_lines = 0

    for root, dirs, filenames in os.walk(ROOT_DIR):
        # Ignore git, cache, and vendor
        dirs[:] = [d for d in dirs if d not in {".git", "__pycache__", "node_modules", "temp_media"}]
        for f in filenames:
            ext = os.path.splitext(f)[1].lower()
            ext_counts[ext] = ext_counts.get(ext, 0) + 1
            full_path = Path(root) / f
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as fp:
                    total_lines += sum(1 for _ in fp)
            except Exception:
                pass

    # Determine recommended MCP servers & Skills based on tech stack
    recommended_mcps = []
    recommended_skills = []

    if ext_counts.get(".html", 0) > 0 or ext_counts.get(".js", 0) > 0:
        recommended_mcps.append({
            "name": "chrome-devtools",
            "reason": "ClockEE has rich client-side HTML5/Canvas UI requiring automated DOM and latency debugging.",
            "type": "browser"
        })
        recommended_skills.append("generative_ui")

    if ext_counts.get(".sqlite", 0) > 0 or ext_counts.get(".db", 0) > 0 or (ROOT_DIR / "clockee.db").is_file():
        recommended_mcps.append({
            "name": "sqlite-mcp",
            "reason": "Direct querying of student question attempts, streaks, and test results.",
            "type": "database"
        })

    if (ROOT_DIR / ".github").is_dir():
        recommended_mcps.append({
            "name": "github-actions-mcp",
            "reason": "Automate GitHub Pages deployment telemetry and build verification.",
            "type": "devops"
        })

    return {
        "project_name": "ClockEE",
        "total_lines_of_code": total_lines,
        "file_extensions": ext_counts,
        "recommended_mcps": recommended_mcps,
        "recommended_agent_skills": recommended_skills,
        "summary": "Client-first Single-Page Web Application with local SQLite & Git auto-publishing pipeline."
    }

if __name__ == "__main__":
    report = scan_codebase_structure()
    print(json.dumps(report, indent=2))
