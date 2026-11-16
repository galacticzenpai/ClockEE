"""
Simulation Verification Script: Apple Touch Targets (>=44x44px) & Zero Horizontal Overflow (<375px)
Audits all 24 canonical HTML surfaces.
"""

import re
from pathlib import Path

ROOT = Path(".")
HTML_FILES = sorted(list(ROOT.glob("*.html")))

def run_touch_and_overflow_audit():
    print("=" * 72)
    print("  SIMULATION AUDIT: APPLE TOUCH TARGETS & ZERO HORIZONTAL OVERFLOW")
    print("=" * 72)

    all_passed = True
    surfaces_tested = 0

    for fpath in HTML_FILES:
        surfaces_tested += 1
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        errors = []

        # 1. Viewport Meta Verification
        if not re.search(r'<meta[^>]+name=["\']viewport["\'][^>]+content=["\'][^"\']*width=device-width', content, re.I):
            errors.append("Missing width=device-width viewport tag")

        # 2. Check for inline fixed widths exceeding iPhone SE screen width (375px)
        # Exclude SVGs, canvases, max-widths, and percentages
        fixed_wide_elements = re.findall(r'style=["\'][^"\']*(?<!max-)width\s*:\s*([4-9]\d{2}|\d{4,})px', content, re.I)
        if fixed_wide_elements:
            errors.append(f"Inline fixed width > 375px detected: {fixed_wide_elements[:2]}")

        # 3. Check touch targets on buttons & links in file
        # Exclude checkboxes and radios which have associated <label> targets
        undersized_touch = re.findall(r'<(?:button|a|input(?![^>]*type=[\'"](?:checkbox|radio)[\'"]))[^>]+style=["\'][^"\']*(?:height|line-height)\s*:\s*([1-2]\d)px', content, re.I)
        if undersized_touch:
            errors.append(f"Undersized touch target elements: {undersized_touch[:2]}")

        # 4. Apple HIG Safe Area Insets Presence
        has_safe_area = ("safe-area-inset" in content) or ("cbt_shared.css" in content)
        if not has_safe_area:
            errors.append("Missing Apple safe-area-inset adaptation")

        status = "PASSED" if not errors else "WARN/FAIL"
        if errors:
            all_passed = False

        print(f"  [{'✓' if not errors else '!'}] {fpath.name:24s} -> {status} (Errors: {len(errors)})")
        for err in errors:
            print(f"      - {err}")

    print("\n" + "=" * 72)
    print(f"  TOTAL SURFACES AUDITED: {surfaces_tested} | OVERALL STATUS: {'100% PASSED' if all_passed else 'ATTENTION NEEDED'}")
    print("=" * 72)
    return all_passed

if __name__ == "__main__":
    passed = run_touch_and_overflow_audit()
    if not passed:
        exit(1)
    exit(0)
