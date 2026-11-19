#!/usr/bin/env python3
"""
⚡ ClockEE — Reel #22: Time-Spent-Per-Question Cognitive Load Heatmap
Upstream: heatmap-js/exam-clickmap
Domain: Real-Time Telemetry & Heatmaps

Calculates cognitive load, classifies question dwell times into 4 speed zones,
and identifies dangerous time sinks versus careless rushed mistakes.
"""

import time
from typing import List, Dict, Any

IDEAL_JEE_DWELL_SEC = 120.0  # 2 minutes per question baseline

ZONE_THRESHOLDS = {
    "RUSHED": {"max_ratio": 0.25, "label": "Careless Rush Risk", "color": "#38bdf8"},
    "SWIFT": {"max_ratio": 0.75, "label": "Fast & Confident", "color": "#34d399"},
    "OPTIMAL": {"max_ratio": 1.25, "label": "Optimal Cadence", "color": "#10b981"},
    "CAUTION": {"max_ratio": 2.00, "label": "Hesitation / Slow", "color": "#f59e0b"},
    "TIME_SINK": {"max_ratio": float("inf"), "label": "Severe Time Sink Trap", "color": "#ef4444"}
}

class CognitiveHeatmapGenerator:
    def __init__(self, ideal_dwell_sec: float = IDEAL_JEE_DWELL_SEC):
        self.ideal_dwell_sec = ideal_dwell_sec

    def classify_dwell(self, dwell_sec: float, ideal_sec: float = None) -> Dict[str, Any]:
        target = ideal_sec or self.ideal_dwell_sec
        ratio = dwell_sec / target if target > 0 else 1.0

        if ratio < 0.25:
            zone = "RUSHED"
        elif ratio < 0.75:
            zone = "SWIFT"
        elif ratio <= 1.25:
            zone = "OPTIMAL"
        elif ratio <= 2.00:
            zone = "CAUTION"
        else:
            zone = "TIME_SINK"

        meta = ZONE_THRESHOLDS[zone]
        return {
            "dwell_sec": round(dwell_sec, 1),
            "ratio": round(ratio, 2),
            "zone": zone,
            "label": meta["label"],
            "color": meta["color"]
        }

    def generate_matrix(self, dwell_times: List[float], correct_flags: List[bool]) -> Dict[str, Any]:
        start = time.perf_counter()
        n = min(len(dwell_times), len(correct_flags))
        
        cells = []
        zone_counts = {k: 0 for k in ZONE_THRESHOLDS.keys()}
        careless_mistakes = 0
        wasted_seconds_in_traps = 0.0

        for i in range(n):
            dwell = dwell_times[i]
            is_correct = correct_flags[i]
            classified = self.classify_dwell(dwell)
            zone = classified["zone"]
            zone_counts[zone] += 1

            # Anomaly checks
            is_careless = (zone == "RUSHED" and not is_correct)
            is_time_sink_trap = (zone == "TIME_SINK" and not is_correct)

            if is_careless:
                careless_mistakes += 1
            if is_time_sink_trap:
                wasted_seconds_in_traps += max(0, dwell - self.ideal_dwell_sec)

            cells.append({
                "q_num": i + 1,
                "dwell_sec": classified["dwell_sec"],
                "ratio": classified["ratio"],
                "zone": zone,
                "label": classified["label"],
                "color": classified["color"],
                "is_correct": is_correct,
                "is_careless": is_careless,
                "is_trap": is_time_sink_trap
            })

        duration_ms = (time.perf_counter() - start) * 1000.0

        return {
            "total_questions": n,
            "latency_ms": round(duration_ms, 3),
            "zone_breakdown": zone_counts,
            "careless_mistakes_count": careless_mistakes,
            "wasted_trap_seconds": round(wasted_seconds_in_traps, 1),
            "cells": cells
        }

def main():
    print("=================================================================")
    print(" ⚡ CLOCKEE COGNITIVE LOAD HEATMAP GENERATOR (Reel #22)")
    print("=================================================================")

    # Generate 90 questions (Full JEE Mains paper)
    # 15 rushed, 30 swift, 30 optimal, 10 caution, 5 time-sinks
    dwells = (
        [20.0] * 15 +
        [70.0] * 30 +
        [110.0] * 30 +
        [180.0] * 10 +
        [320.0] * 5
    )
    # Flags: first 5 rushed are wrong (careless), 5 time-sinks are wrong (traps)
    flags = [False] * 5 + [True] * 10 + [True] * 60 + [True] * 10 + [False] * 5

    generator = CognitiveHeatmapGenerator()
    report = generator.generate_matrix(dwells, flags)

    print(f"[*] Processed {report['total_questions']} questions in {report['latency_ms']:.3f} ms")
    print("  • Zone Breakdown:")
    for zone, count in report["zone_breakdown"].items():
        print(f"    - {zone:10s}: {count:2d} questions ({ZONE_THRESHOLDS[zone]['label']})")
    print(f"  • Careless Rushed Mistakes: {report['careless_mistakes_count']}")
    print(f"  • Time Lost in Sinks/Traps: {report['wasted_trap_seconds']} seconds ({report['wasted_trap_seconds']/60:.1f} mins)")

    assert report["total_questions"] == 90
    assert report["careless_mistakes_count"] == 5
    assert report["zone_breakdown"]["TIME_SINK"] == 5
    assert report["latency_ms"] < 5.0, "Execution must be sub-millisecond!"

    print("\n[✓] Cognitive Load Heatmap Generator certified (Exit Code 0).")

if __name__ == "__main__":
    main()
