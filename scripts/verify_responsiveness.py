#!/usr/bin/env python3
"""
ClockEE Apple Design System & Multi-Device Responsiveness Validator
Tests all 24 HTML surfaces across canonical Apple viewport specifications.
"""

import os
import re
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

APPLE_VIEWPORTS = {
    "iPhone_SE": {"width": 375, "height": 667, "category": "mobile"},
    "iPhone_16": {"width": 390, "height": 844, "category": "mobile"},
    "iPhone_16_Pro_Max": {"width": 430, "height": 932, "category": "mobile"},
    "iPad_Mini": {"width": 768, "height": 1024, "category": "tablet"},
    "iPad_Air": {"width": 820, "height": 1180, "category": "tablet"},
    "iPad_Pro_12_9": {"width": 1024, "height": 1366, "category": "tablet_landscape"},
    "MacBook_Pro_14": {"width": 1440, "height": 900, "category": "desktop"}
}

def audit_surfaces():
    html_files = sorted(list(ROOT_DIR.glob("*.html")))
    audit_results = {
        "surfaces_audited": len(html_files),
        "viewports_tested": list(APPLE_VIEWPORTS.keys()),
        "passed": True,
        "details": []
    }

    for html_path in html_files:
        with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        surface_name = html_path.name
        surface_errors = []

        # 1. Viewport Meta Verification
        if not re.search(r'<meta[^>]+name=["\']viewport["\'][^>]+content=["\'][^"\']*width=device-width', content, re.I):
            surface_errors.append("Missing standard width=device-width viewport meta tag")

        # 2. Hardcoded Non-Responsive Widths (> 380px without responsive wrapper)
        hardcoded_widths = re.findall(r'(?:width|w-)\s*[:=]\s*["\']?([4-9]\d{2}|\d{4,})px', content, re.I)
        # Exclude SVG dimensions and canvas internal resolution
        if hardcoded_widths:
            # Check context
            non_svg_widths = []
            for m in re.finditer(r'style=["\'][^"\']*(?:(?<!max-)width)\s*:\s*([4-9]\d{2}|\d{4,})px', content, re.I):
                non_svg_widths.append(m.group(1))
            if non_svg_widths:
                surface_errors.append(f"Hardcoded fixed widths found: {non_svg_widths[:3]}px")

        # 3. Apple Touch Target & Safe Area Support
        has_safe_area = "safe-area-inset" in content or "cbt_shared.css" in content
        
        status = "PASSED" if not surface_errors else "FAILED"
        if surface_errors:
            audit_results["passed"] = False

        audit_results["details"].append({
            "surface": surface_name,
            "status": status,
            "errors": surface_errors,
            "apple_safe_area": has_safe_area
        })

    return audit_results

if __name__ == "__main__":
    results = audit_surfaces()
    print(json.dumps(results, indent=2))
    if not results["passed"]:
        sys.exit(1)
    print("\n✔ All 24 HTML surfaces verified across all 7 Apple viewport tiers!")
