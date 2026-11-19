#!/usr/bin/env python3
"""
⚡ ClockEE — Reel #7: Core Web Vitals & Retinal Performance Guardrail
Upstream: GoogleChromeLabs/lighthouse-batch
Domain: Performance & CWV Guardrails

Scans ClockEE HTML surfaces for:
1. Script blocking & async/defer loading
2. Layout shift risks (missing image width/height attributes)
3. Font display: swap compliance
4. DOM tree depth & node budget
Outputs: integrations/page_audit/page_audit_report.json
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = Path(__file__).resolve().parent / "perf_thresholds.json"
REPORT_PATH = Path(__file__).resolve().parent / "page_audit_report.json"

def audit_file(filepath: Path, thresholds: dict) -> dict:
    if not filepath.is_file():
        return {"error": "File not found", "score": 0}

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    findings = []
    penalties = 0

    # 1. Check blocking external scripts in head
    head_match = re.search(r"<head>(.*?)</head>", html, re.DOTALL | re.IGNORECASE)
    head_content = head_match.group(1) if head_match else html[:2000]

    blocking_scripts = re.findall(r'<script\s+src="([^"]+)"(?!\s+(?:defer|async|type="module"))', head_content, re.IGNORECASE)
    # Ignore safe local config scripts like env.js
    blocking_scripts = [s for s in blocking_scripts if not s.endswith("env.js") and "tailwindcss" not in s]
    if blocking_scripts:
        penalties += len(blocking_scripts) * 2
        findings.append(f"Found {len(blocking_scripts)} non-deferred script(s) in head: {blocking_scripts[:3]}")

    # 2. Check layout shifts: images without width/height
    img_tags = re.findall(r'<img\s+[^>]+>', html, re.IGNORECASE)
    cls_risks = [img for img in img_tags if "width=" not in img.lower() and "w-" not in img.lower() and "h-" not in img.lower()]
    if cls_risks:
        penalties += min(len(cls_risks) * 2, 10)
        findings.append(f"Found {len(cls_risks)} image(s) missing width/height layout bounds")

    # 3. Check font-display swap in styles
    if "@font-face" in html and "font-display: swap" not in html and "font-display:swap" not in html:
        penalties += 5
        findings.append("Custom @font-face detected without 'font-display: swap'")

    # 4. Rough DOM node count estimate
    tag_count = len(re.findall(r'<[a-zA-Z0-9]+(?:\s+[^>]*)?>', html))
    max_nodes = thresholds.get("max_dom_nodes", 1800)
    if tag_count > max_nodes:
        penalties += 8
        findings.append(f"High DOM complexity: ~{tag_count} elements (Threshold: <={max_nodes})")

    score = max(100 - penalties, 0)
    return {
        "file": filepath.name,
        "score": score,
        "estimated_dom_nodes": tag_count,
        "findings": findings,
        "passed": score >= 85
    }

def main():
    print("=================================================================")
    print(" ⚡ CLOCKEE CORE WEB VITALS & PAGE AUDIT GUARDRAIL (Reel #7)")
    print("=================================================================")

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    thresholds = config.get("thresholds", {})
    targets = config.get("targets", [])

    results = {}
    total_score = 0
    pages_passed = 0

    for filename in targets:
        fp = ROOT_DIR / filename
        res = audit_file(fp, thresholds)
        results[filename] = res
        total_score += res.get("score", 0)
        if res.get("passed", False):
            pages_passed += 1
        status = "PASSED" if res.get("passed", False) else "NEEDS_ATTENTION"
        print(f"  • {filename:<22} -> Score: {res.get('score')}/100 [{status}]")
        if res.get("findings"):
            for f in res["findings"]:
                print(f"      - {f}")

    avg_score = round(total_score / len(targets), 1) if targets else 100.0
    print("-" * 65)
    print(f"  🏆 Average CWV Performance Score: {avg_score}/100 ({pages_passed}/{len(targets)} pages passed)")

    report = {
        "timestamp": datetime.now().isoformat(),
        "average_score": avg_score,
        "pages_audited": len(targets),
        "pages_passed": pages_passed,
        "details": results
    }
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"\n[✓] Audit report saved to: {REPORT_PATH}")
    assert avg_score >= 85.0, f"Average CWV Performance score {avg_score} < 85.0 threshold!"
    print("[✓] Reel #7 Page Audit Guardrail certified (Exit Code 0).")

if __name__ == "__main__":
    main()
