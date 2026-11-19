#!/usr/bin/env python3
"""
ClockEE Package: Strix Static Application Security Scanner (SAST)
Audits codebase files for security vulnerabilities, hardcoded secrets,
unsafe innerHTML injections, and XSS hazards.
"""

import os
import re
import sys
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Security vulnerability patterns
VULN_RULES = [
    {
        "id": "SEC-001",
        "severity": "HIGH",
        "title": "Unsanitized innerHTML assignment (XSS Vector)",
        "pattern": r'\.innerHTML\s*=\s*(?!["\'`<][^$]*>)[^;]+',
        "description": "Direct dynamic assignment to innerHTML without sanitization can lead to DOM-based XSS."
    },
    {
        "id": "SEC-002",
        "severity": "CRITICAL",
        "title": "Potential Hardcoded API Key or Secret",
        "pattern": r'(?i)(?:api_key|secret|token|password)\s*[:=]\s*["\'][a-zA-Z0-9_\-]{20,}["\']',
        "description": "Sensitive credentials should be stored in environment variables, not in source code."
    },
    {
        "id": "SEC-003",
        "severity": "CRITICAL",
        "title": "Use of dangerous eval() or new Function()",
        "pattern": r'\b(?:eval|Function)\s*\(',
        "description": "Dynamic execution of arbitrary strings can allow remote code execution."
    },
    {
        "id": "SEC-004",
        "severity": "MEDIUM",
        "title": "Target blank link without rel='noopener noreferrer'",
        "pattern": r'<a[^>]+target=["\']_blank["\'](?!.*rel=["\'][^"\']*noopener)',
        "description": "Links opening in new tabs without noopener allow reverse-tabnabbing attacks."
    }
]

def scan_file(filepath: Path):
    findings = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
            for line_no, line in enumerate(lines, 1):
                # Skip comments
                stripped = line.strip()
                if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("#"):
                    continue
                for rule in VULN_RULES:
                    if re.search(rule["pattern"], line):
                        findings.append({
                            "rule_id": rule["id"],
                            "severity": rule["severity"],
                            "title": rule["title"],
                            "file": str(filepath.relative_to(ROOT_DIR)),
                            "line": line_no,
                            "snippet": stripped[:100]
                        })
    except Exception as e:
        pass
    return findings

def run_security_audit():
    all_findings = []
    scanned_count = 0
    
    for ext in ["*.js", "*.html"]:
        for file in ROOT_DIR.glob(ext):
            if "vendor" in file.parts or ".git" in file.parts:
                continue
            scanned_count += 1
            all_findings.extend(scan_file(file))
            
    report = {
        "files_scanned": scanned_count,
        "total_issues": len(all_findings),
        "critical": sum(1 for f in all_findings if f["severity"] == "CRITICAL"),
        "high": sum(1 for f in all_findings if f["severity"] == "HIGH"),
        "medium": sum(1 for f in all_findings if f["severity"] == "MEDIUM"),
        "findings": all_findings[:15]  # Top findings
    }
    return report

if __name__ == "__main__":
    report = run_security_audit()
    print(json.dumps(report, indent=2))
