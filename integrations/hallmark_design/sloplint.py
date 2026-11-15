#!/usr/bin/env python3
"""
ClockEE Package: Hallmark Anti-AI-Slop Linter (sloplint.py)
Adapted from Together AI's open-source Hallmark (nutlope/hallmark, MIT License).

Evaluates HTML, CSS, and JS files against the 3 Hallmark Quality Gates:
  1. Floor Gates: Non-negotiable responsive & functional requirements
  2. Reflex Gates: Detects the 6 common AI aesthetic clichés ("slop tells")
  3. Finish Checks: Advisory polish for typography, contrast, and data authenticity
"""

import os
import re
import sys
import json
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
REPORTS_DIR = Path(__file__).resolve().parent / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

class SlopLinter:
    def __init__(self, workspace_path: Path = ROOT_DIR):
        self.workspace = workspace_path
        self.results = []

    def lint_file(self, file_path: Path):
        file_rel = str(file_path.relative_to(self.workspace))
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                lines = content.splitlines()
        except Exception as e:
            return None

        file_report = {
            "file": file_rel,
            "floor_violations": [],
            "reflex_violations": [],
            "finish_advisories": [],
            "score": 100
        }

        # ----------------------------------------------------
        # 1. Floor Gates (Blocking Requirements)
        # ----------------------------------------------------
        # A. Viewport Meta Tag
        if file_path.suffix.lower() == ".html":
            if not re.search(r'<meta[^>]+name=["\']viewport["\'][^>]+content=["\'][^"\']*width=device-width', content, re.I):
                file_report["floor_violations"].append({
                    "gate": "FLOOR",
                    "code": "MISSING_VIEWPORT_META",
                    "message": "Missing responsive <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
                    "line": 1
                })

        # B. Dummy Forms / Dead "Thanks" Alerts
        for line_idx, line in enumerate(lines, 1):
            if re.search(r'alert\s*\(\s*["\'](?:Thank|Thanks|Submitted)[^"\']*["\']\s*\)', line, re.I):
                file_report["floor_violations"].append({
                    "gate": "FLOOR",
                    "code": "DUMMY_FORM_ALERT",
                    "message": "Dead form submission alert('Thanks') found without persistent or API handler",
                    "line": line_idx,
                    "snippet": line.strip()[:100]
                })

            # C. Fixed non-responsive widths over 380px without responsive modifier
            if re.search(r'(?<![a-z0-9:-])w-\[(?:[4-9]\d{2}|\d{4,})px\]', line):
                file_report["floor_violations"].append({
                    "gate": "FLOOR",
                    "code": "FIXED_MOBILE_OVERFLOW",
                    "message": "Hardcoded wide pixel width (w-[...px]) causes mobile viewport overflow. Use max-w or flex/grid.",
                    "line": line_idx,
                    "snippet": line.strip()[:100]
                })

        # ----------------------------------------------------
        # 2. Reflex Gates (AI Slop Clichés)
        # ----------------------------------------------------
        # A. Purple/Indigo Gradient Cliche
        for line_idx, line in enumerate(lines, 1):
            if re.search(r'bg-gradient-to-[a-z]+\s+from-(?:purple|violet|indigo)-\d+\s+to-(?:pink|fuchsia|cyan)-\d+', line):
                file_report["reflex_violations"].append({
                    "gate": "REFLEX",
                    "code": "PURPLE_GRADIENT_CLICHE",
                    "message": "Generic AI purple/indigo radial gradient background detected. Choose a distinct material theme.",
                    "line": line_idx,
                    "snippet": line.strip()[:100]
                })

            # B. Single Colored Word in Heading
            if re.search(r'<h[1-3][^>]*>[^<]*<span\s+class=["\'][^"\']*text-(?:purple|indigo|violet|blue|cyan)-\d+[^"\']*>[^<]+</span>[^<]*</h[1-3]>', line):
                file_report["reflex_violations"].append({
                    "gate": "REFLEX",
                    "code": "COLORED_HEADLINE_WORD",
                    "message": "The classic AI 'one colored word in headline' pattern. Restructure heading typography.",
                    "line": line_idx,
                    "snippet": line.strip()[:100]
                })

            # C. Overused Eyebrow Tracking Label
            if re.search(r'<span[^>]+class=["\'][^"\']*uppercase\s+tracking-(?:widest|wider)\s+text-xs[^"\']*>', line):
                file_report["reflex_violations"].append({
                    "gate": "REFLEX",
                    "code": "EYEBROW_OVERUSE",
                    "message": "Overused uppercase tracked-out eyebrow label above section. Limit to 1 per major page view.",
                    "line": line_idx,
                    "snippet": line.strip()[:100]
                })

            # D. Triple Glassmorphism Card Stack
            if re.search(r'backdrop-blur-(?:md|lg|xl)\s+bg-(?:white|slate-\d+)\/(?:10|20|5)', line):
                file_report["reflex_violations"].append({
                    "gate": "REFLEX",
                    "code": "GLASSMORPHISM_STACK",
                    "message": "AI glassmorphism card (backdrop-blur + translucent border). Consider crisp editorial borders or solid tactile surfaces.",
                    "line": line_idx,
                    "snippet": line.strip()[:100]
                })

            # E. Placeholder Copy
            if re.search(r'\b(?:Lorem\s+ipsum|John\s+Doe|Feature\s+1|Feature\s+2|Lorem)\b', line, re.I):
                file_report["reflex_violations"].append({
                    "gate": "REFLEX",
                    "code": "PLACEHOLDER_COPY",
                    "message": "Generic AI placeholder copy ('Lorem ipsum' / 'Feature 1'). Use real educational exam domain data.",
                    "line": line_idx,
                    "snippet": line.strip()[:100]
                })

        # ----------------------------------------------------
        # 3. Finish Checks (Advisory Polish)
        # ----------------------------------------------------
        if file_path.suffix.lower() == ".html":
            if "font-family" not in content and "fonts.googleapis.com" not in content and "font-" not in content:
                file_report["finish_advisories"].append({
                    "gate": "FINISH",
                    "code": "DEFAULT_SYSTEM_FONTS",
                    "message": "No customized typography pairing loaded. Apply an intentional editorial or monospace font pairing."
                })

        # Calculate Score
        deduction = (len(file_report["floor_violations"]) * 25) + (len(file_report["reflex_violations"]) * 10)
        file_report["score"] = max(0, 100 - deduction)

        return file_report

    def audit_all(self, target_pattern: str = "*.html"):
        all_reports = []
        for file in sorted(self.workspace.glob(target_pattern)):
            if "vendor" in file.parts or ".git" in file.parts or "node_modules" in file.parts:
                continue
            rep = self.lint_file(file)
            if rep:
                all_reports.append(rep)
        return all_reports

    def write_report(self, reports):
        total_files = len(reports)
        total_floor = sum(len(r["floor_violations"]) for r in reports)
        total_reflex = sum(len(r["reflex_violations"]) for r in reports)
        avg_score = round(sum(r["score"] for r in reports) / max(1, total_files), 1)

        summary = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "skill": "nutlope/hallmark (Together AI) Design & Slop Linter",
            "metrics": {
                "pages_scanned": total_files,
                "floor_gate_failures": total_floor,
                "reflex_slop_cliches": total_reflex,
                "average_design_score": avg_score
            },
            "reports": reports
        }

        out_file = REPORTS_DIR / f"sloplint_report_{int(time.time())}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        return summary, out_file

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "*.html"
    linter = SlopLinter()

    if target.endswith(".html") and "*" not in target:
        target_path = ROOT_DIR / target
        if target_path.exists():
            reports = [linter.lint_file(target_path)]
        else:
            print(f"File not found: {target}")
            sys.exit(1)
    else:
        reports = linter.audit_all("*.html")

    summary, out_file = linter.write_report(reports)

    print("=" * 68)
    print("  HALLMARK ANTI-AI-SLOP LINTER (nutlope/hallmark / Together AI)")
    print("=" * 68)
    print(f"Pages Audited       : {summary['metrics']['pages_scanned']}")
    print(f"Floor Gate Failures : {summary['metrics']['floor_gate_failures']} (Blocking mobile/functional bugs)")
    print(f"Reflex AI Clichés   : {summary['metrics']['reflex_slop_cliches']} (Purple gradients, glass cards, tells)")
    print(f"Average Design Score: {summary['metrics']['average_design_score']}/100")
    print(f"Report Generated    : {out_file}")
    print("=" * 68)

    # Print top violations if any
    for rep in reports:
        if rep["floor_violations"] or rep["reflex_violations"]:
            print(f"\n[{rep['file']}] Score: {rep['score']}/100")
            for f in rep["floor_violations"]:
                print(f"  ❌ [FLOOR] L{f.get('line', '?')}: {f['code']} - {f['message']}")
            for r in rep["reflex_violations"]:
                print(f"  ⚠️  [REFLEX] L{r.get('line', '?')}: {r['code']} - {r['message']}")
