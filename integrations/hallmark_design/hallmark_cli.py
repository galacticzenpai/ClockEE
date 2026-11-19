#!/usr/bin/env python3
"""
Hallmark CLI: Anti-AI-Slop Command Line Interface for ClockEE
Enables auditing pages against Hallmark gates and browsing theme materials.
"""

import sys
import json
from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
THEMES_FILE = PACKAGE_DIR / "themes_catalog.json"

def show_themes():
    with open(THEMES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("=" * 70)
    print(" HALLMARK THEME MATERIAL CATALOG (nutlope/hallmark)")
    print("=" * 70)
    for theme in data.get("themes", []):
        print(f"\n🎨 Theme ID : {theme['id']}")
        print(f"   Name     : {theme['name']} ({theme['category']})")
        print(f"   Mood     : {theme['mood']}")
        print(f"   For      : {', '.join(theme.get('recommended_for', []))}")
        print(f"   Fonts    : Heading: {theme['fonts']['heading']} | Body: {theme['fonts']['body']}")
        print(f"   Palette  : BG: {theme['palette']['bg']} | Surface: {theme['palette']['surface']} | Text: {theme['palette']['text_primary']} | Accent: {theme['palette']['accent']}")
        print(f"   Rules    : {theme['rules']}")
    print("\n" + "=" * 70)

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
        print("Usage:")
        print("  python integrations/hallmark_design/hallmark_cli.py audit [file.html or --all]")
        print("  python integrations/hallmark_design/hallmark_cli.py themes")
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd == "themes":
        show_themes()
    elif cmd == "audit":
        target = sys.argv[2] if len(sys.argv) > 2 else "*.html"
        from sloplint import SlopLinter
        linter = SlopLinter()
        if target != "--all" and target.endswith(".html") and "*" not in target:
            target_path = Path(target)
            if not target_path.is_absolute():
                target_path = PACKAGE_DIR.parent.parent / target
            reports = [linter.lint_file(target_path)]
        else:
            reports = linter.audit_all("*.html")

        summary, out_file = linter.write_report(reports)
        print("=" * 68)
        print("  HALLMARK AUDIT SUMMARY")
        print("=" * 68)
        print(f"Pages Scanned       : {summary['metrics']['pages_scanned']}")
        print(f"Floor Failures      : {summary['metrics']['floor_gate_failures']}")
        print(f"Reflex Tells (Slop) : {summary['metrics']['reflex_slop_cliches']}")
        print(f"Average Design Score: {summary['metrics']['average_design_score']}/100")
        print(f"Report File         : {out_file}")
        print("=" * 68)
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
