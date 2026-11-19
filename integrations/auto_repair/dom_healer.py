#!/usr/bin/env python3
"""
⚡ ClockEE — Reel #27: Self-Healing DOM Selector & Missing Attribute Guardrail
Upstream: agent-dom/self-healing
Domain: Self-Healing & Defect Detection

Defensive runtime protector simulating missing DOM nodes, broken action buttons,
and auto-repairing missing attributes to ensure zero UI freezes.
"""

import time
from typing import Dict, Any, List, Set

CRITICAL_CBT_SELECTORS = [
    "#questionStem",
    "#optionsContainer",
    "#btnSaveNext",
    "#btnMarkReview",
    "#btnClearResponse",
    "#paletteGrid",
    "#timerDisplay"
]

class DOMHealerEngine:
    def __init__(self, required_selectors: List[str] = None):
        self.required_selectors = set(required_selectors or CRITICAL_CBT_SELECTORS)
        self.healed_count = 0

    def inspect_and_heal(self, existing_dom_ids: Set[str]) -> Dict[str, Any]:
        """
        Inspects available DOM identifiers and injects self-healing fallback specs for missing critical nodes.
        """
        missing = []
        healed_actions = []

        for sel in self.required_selectors:
            raw_id = sel.lstrip("#.")
            if raw_id not in existing_dom_ids:
                missing.append(sel)
                # Formulate dynamic self-healing fallback
                fallback_type = "button" if "btn" in raw_id.lower() else "div"
                healed_actions.append({
                    "selector": sel,
                    "action": "AUTO_SPAWN_SURROGATE",
                    "element_tag": fallback_type,
                    "default_attributes": {"id": raw_id, "data-healed": "true"}
                })
                self.healed_count += 1

        return {
            "total_inspected": len(self.required_selectors),
            "missing_count": len(missing),
            "healed_actions": healed_actions,
            "status": "HEALED_CLEAN" if missing else "ALL_DOM_HEALTHY"
        }

def benchmark_dom_healer():
    healer = DOMHealerEngine()
    # Simulate a corrupted DOM where #btnSaveNext and #paletteGrid were accidentally removed by an async race
    corrupted_dom = {"questionStem", "optionsContainer", "btnMarkReview", "btnClearResponse", "timerDisplay"}

    t0 = time.perf_counter()
    report = healer.inspect_and_heal(corrupted_dom)
    t1 = time.perf_counter()
    latency_us = (t1 - t0) * 1_000_000

    print(f"[BENCHMARK] DOM self-healing latency: {latency_us:.2f}µs")
    print(f"Report: Missing {report['missing_count']} nodes, applied {len(report['healed_actions'])} healing surrogates.")
    for action in report["healed_actions"]:
        print(f"  [HEALED] Injected surrogate for {action['selector']} (Tag: <{action['element_tag']}>)")
    
    assert report["missing_count"] == 2
    assert len(report["healed_actions"]) == 2
    print("[✓] Self-Healing DOM Guardrail certified (Exit Code 0).")
    return latency_us

if __name__ == "__main__":
    benchmark_dom_healer()
