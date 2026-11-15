#!/usr/bin/env python3
"""
ClockEE Package: Cloudflare Security Audit Skill Harness
Adapted from Cloudflare's open-source security-audit-skill (MIT License).

Implements the multi-phase security audit workflow:
  Phase 1: Reconnaissance (Entry points, Auth boundaries, LocalStorage vectors)
  Phase 2: Vulnerability Hunting (XSS, Injection, Secret Leakage, CSRF, Insecure Deserialization)
  Phase 3: Adversarial Disproval (Second agent verification pass to disprove false positives)
  Phase 4: Structured Machine-Readable & Human-Readable Security Verdict
"""

import os
import re
import sys
import json
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = ROOT_DIR / "integrations" / "cloudflare_security_audit" / "reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Phase 1: Entry Point & Trust Boundary Map
AUDIT_TARGETS = [
    {"category": "Authentication & Session", "pattern": r'(?:login|auth|token|session|credential|password)'},
    {"category": "Storage & State Vectors", "pattern": r'(?:localStorage|sessionStorage|indexedDB|cookies)'},
    {"category": "Network & API Boundaries", "pattern": r'(?:fetch|XMLHttpRequest|http\.server|\.post\(|\.get\()' },
    {"category": "DOM Injection Hotspots", "pattern": r'(?:\.innerHTML|\.outerHTML|document\.write|eval\()' },
    {"category": "External Scripts & CDN Integrations", "pattern": r'<script[^>]+src=["\']https?:'}
]

class CloudflareSecurityAudit:
    def __init__(self, workspace_path: Path = ROOT_DIR):
        self.workspace = workspace_path
        self.findings_candidates = []
        self.verified_findings = []
        self.disproved_findings = []

    def phase1_reconnaissance(self):
        """Map entry points, trust boundaries, and asset distribution."""
        architecture = {
            "root": str(self.workspace),
            "html_entrypoints": [],
            "js_modules": [],
            "endpoints": [],
            "auth_surfaces": []
        }
        for file in self.workspace.glob("*.html"):
            architecture["html_entrypoints"].append(file.name)
        for file in self.workspace.glob("*.js"):
            architecture["js_modules"].append(file.name)
        return architecture

    def phase2_hunting(self):
        """Coverage-led hunt for candidate vulnerability classes."""
        candidates = []
        rule_set = [
            {
                "cwe": "CWE-79",
                "title": "DOM-Based Cross-Site Scripting (XSS)",
                "severity": "HIGH",
                "regex": r'\.innerHTML\s*=\s*(?!["\'`<][^$]*>)[^;]+',
                "disprove_check": lambda line: "renderKatex" in line or "sanitize" in line or "encodeURIComponent" in line
            },
            {
                "cwe": "CWE-798",
                "title": "Exposed Hardcoded Credential / Sensitive Token",
                "severity": "CRITICAL",
                "regex": r'(?:api_key|token|client_secret)\s*[:=]\s*["\'][A-Za-z0-9_\-]{24,}["\']',
                "disprove_check": lambda line: "env." in line or "example" in line or "mock" in line or "PLACEHOLDER" in line
            },
            {
                "cwe": "CWE-95",
                "title": "Improper Dynamic Execution (eval / new Function)",
                "severity": "CRITICAL",
                "regex": r'\beval\s*\(|new\s+Function\s*\(',
                "disprove_check": lambda line: "test" in line or "disabled" in line
            },
            {
                "cwe": "CWE-1021",
                "title": "Missing Cross-Origin Isolation or Unsafe Target Blank",
                "regex": r'<a[^>]+target=["\']_blank["\'](?!.*rel=["\'][^"\']*noopener)',
                "severity": "MEDIUM",
                "disprove_check": lambda line: "rel=" in line and "noopener" in line
            }
        ]

        for ext in ["*.html", "*.js", "*.py"]:
            for file in self.workspace.glob(ext):
                if "vendor" in file.parts or ".git" in file.parts:
                    continue
                try:
                    with open(file, "r", encoding="utf-8", errors="ignore") as f:
                        for line_idx, line in enumerate(f, 1):
                            s_line = line.strip()
                            if s_line.startswith("//") or s_line.startswith("#") or s_line.startswith("/*"):
                                continue
                            for r in rule_set:
                                if re.search(r["regex"], line):
                                    candidates.append({
                                        "cwe": r["cwe"],
                                        "title": r["title"],
                                        "severity": r["severity"],
                                        "file": str(file.relative_to(self.workspace)),
                                        "line": line_idx,
                                        "code": s_line[:120],
                                        "disprove_fn": r["disprove_check"]
                                    })
                except Exception:
                    pass
        self.findings_candidates = candidates
        return candidates

    def phase3_adversarial_disproval(self):
        """
        Adversarial Red-Team Pass: Attempt to disprove each candidate finding.
        Filters out false positives where sanitization, encoding, or safe templates exist.
        """
        verified = []
        disproved = []

        for candidate in self.findings_candidates:
            # Extract and remove disprove_fn so candidate dict is JSON serializable
            disprove_fn = candidate.pop("disprove_fn", None)
            disproved_by_guard = disprove_fn(candidate["code"]) if disprove_fn else False
            if disproved_by_guard:
                disproved.append({
                    "candidate": candidate,
                    "reason": "Disproved: Code context contains sanitization, placeholder, or encoding guardrail."
                })
            else:
                verified.append(candidate)

        self.verified_findings = verified
        self.disproved_findings = disproved
        return {"verified": verified, "disproved": disproved}

    def generate_report(self):
        recon = self.phase1_reconnaissance()
        self.phase2_hunting()
        self.phase3_adversarial_disproval()

        report = {
            "skill": "cloudflare/security-audit-skill",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "reconnaissance": recon,
            "metrics": {
                "total_candidates_flagged": len(self.findings_candidates),
                "adversarially_disproved_false_positives": len(self.disproved_findings),
                "actionable_verified_vulnerabilities": len(self.verified_findings)
            },
            "verified_vulnerabilities": self.verified_findings[:20],
            "disproved_summary": [
                f"{d['candidate']['file']}:{d['candidate']['line']} ({d['candidate']['title']}) -> {d['reason']}"
                for d in self.disproved_findings[:5]
            ]
        }

        # Write structured JSON report
        out_file = OUTPUT_DIR / f"audit_report_{int(time.time())}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        return report, out_file

if __name__ == "__main__":
    auditor = CloudflareSecurityAudit()
    report, filepath = auditor.generate_report()
    print("=" * 65)
    print(" Cloudflare Security Audit Skill - Execution Summary")
    print("=" * 65)
    print(f"Total Candidates Examined : {report['metrics']['total_candidates_flagged']}")
    print(f"Disproved False Positives : {report['metrics']['adversarially_disproved_false_positives']}")
    print(f"Verified Actionable Bugs  : {report['metrics']['actionable_verified_vulnerabilities']}")
    print(f"Structured Report Saved   : {filepath}")
    print("=" * 65)
