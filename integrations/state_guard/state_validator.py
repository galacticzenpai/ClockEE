#!/usr/bin/env python3
"""
⚡ ClockEE — Reel #28: Runtime Client-Side State Mutation & Corruption Interceptor
Upstream: zod-lite/state-guard
Domain: Self-Healing & Defect Detection

Strict schema validator inspecting exam state transitions, boundary limits,
and data integrity to intercept and reject state corruption.
"""

import time
import math
from typing import Dict, Any, Optional

ALLOWED_OPTIONS = {"A", "B", "C", "D", None, ""}
ALLOWED_STATUSES = {"ANSWERED", "NOT_ANSWERED", "MARKED_FOR_REVIEW", "NOT_VISITED"}

class StateCorruptionError(ValueError):
    pass

class StateGuard:
    def __init__(self, total_questions: int = 180, total_duration_sec: int = 10800):
        self.total_questions = total_questions
        self.total_duration_sec = total_duration_sec

    def validate_mutation(self, key: str, value: Any, current_state: Dict[str, Any]) -> bool:
        """Validates an incoming state property update. Raises StateCorruptionError on violation."""
        if key == "current_question":
            if not isinstance(value, int) or value < 1 or value > self.total_questions:
                raise StateCorruptionError(f"Illegal current_question index: {value}. Must be in [1, {self.total_questions}].")
        elif key == "selected_option":
            if value is not None and value not in {"A", "B", "C", "D"}:
                raise StateCorruptionError(f"Illegal option selected: '{value}'. Expected A, B, C, D or None.")
        elif key == "remaining_sec":
            if not isinstance(value, (int, float)) or math.isnan(value) or value < 0 or value > self.total_duration_sec:
                raise StateCorruptionError(f"Corrupt remaining_sec: {value}. Must be a finite number between 0 and {self.total_duration_sec}.")
        elif key == "status":
            if value not in ALLOWED_STATUSES:
                raise StateCorruptionError(f"Illegal palette status: '{value}'. Expected one of {ALLOWED_STATUSES}.")
        return True

def benchmark_state_guard():
    guard = StateGuard(total_questions=180, total_duration_sec=10800)
    current_state = {"current_question": 1, "selected_option": "A", "remaining_sec": 10790}

    # 1. Benchmark valid mutations
    t0 = time.perf_counter()
    iterations = 10000
    for i in range(iterations):
        guard.validate_mutation("current_question", (i % 180) + 1, current_state)
        guard.validate_mutation("selected_option", ["A", "B", "C", "D"][i % 4], current_state)
        guard.validate_mutation("remaining_sec", 10800 - (i % 1000), current_state)
    t1 = time.perf_counter()
    latency_us = ((t1 - t0) / (iterations * 3)) * 1_000_000

    print(f"[BENCHMARK] State mutation validation latency: {latency_us:.2f}µs per check ({iterations*3} checks)")

    # 2. Verify illegal mutations are blocked
    blocked = 0
    test_cases = [
        ("current_question", -5),
        ("current_question", 999),
        ("selected_option", "HACK_PAYLOAD"),
        ("remaining_sec", float("nan")),
        ("remaining_sec", -10),
        ("status", "INVALID_PALETTE_STATE")
    ]
    for key, val in test_cases:
        try:
            guard.validate_mutation(key, val, current_state)
        except StateCorruptionError as e:
            blocked += 1

    assert blocked == len(test_cases), f"Expected {len(test_cases)} violations blocked, got {blocked}"
    print(f"[✓] Interceptor correctly blocked {blocked}/{len(test_cases)} illegal mutations.")
    print("[✓] Runtime State Corruption Interceptor certified (Exit Code 0).")
    return latency_us

if __name__ == "__main__":
    benchmark_state_guard()
