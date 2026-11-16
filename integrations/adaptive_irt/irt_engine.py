#!/usr/bin/env python3
"""
⚡ ClockEE — Reel #11: Item Response Theory (IRT) Adaptive Sequencer
Upstream: item-response-theory/engine
Domain: Adaptive CBT Exam Engine

Implements the 3-Parameter Logistic (3PL) IRT Model:
P(θ) = c + (1 - c) / (1 + exp(-a * (θ - b)))
Where:
- θ (theta) = latent student ability [-3.0 to +3.0]
- a = item discrimination parameter
- b = item difficulty parameter
- c = pseudo-guessing parameter (0.25 for 4-option MCQs)

Selects the next question that maximizes Fisher Information at the student's current θ estimate.
"""

import math
import json
import time
import argparse
from typing import List, Dict, Any, Optional

DEFAULT_GUESSING_C = 0.25

class IRTEngine:
    def __init__(self, initial_theta: float = 0.0):
        self.theta = max(-3.0, min(3.0, initial_theta))
        self.history: List[Dict[str, Any]] = []

    @staticmethod
    def probability_correct(theta: float, a: float, b: float, c: float = DEFAULT_GUESSING_C) -> float:
        """Computes 3PL probability of correct response given student ability theta."""
        try:
            exp_term = math.exp(-a * (theta - b))
            return c + (1.0 - c) / (1.0 + exp_term)
        except OverflowError:
            return 1.0 if (theta - b) > 0 else c

    @staticmethod
    def fisher_information(theta: float, a: float, b: float, c: float = DEFAULT_GUESSING_C) -> float:
        """Computes Fisher Information of an item at ability level theta."""
        p = IRTEngine.probability_correct(theta, a, b, c)
        q = 1.0 - p
        if p <= c or q <= 0:
            return 0.0
        num = (a ** 2) * ((p - c) ** 2) * q
        denom = ((1.0 - c) ** 2) * p
        return num / denom if denom > 0 else 0.0

    def update_ability_eap(self, response_correct: bool, a: float, b: float, c: float = DEFAULT_GUESSING_C) -> float:
        """
        Expected A Posteriori (EAP) Bayesian update of theta with standard normal prior N(0, 1).
        Provides smooth convergence without infinite loops or edge-case singularities.
        """
        self.history.append({
            "step": len(self.history) + 1,
            "theta_before": self.theta,
            "correct": response_correct,
            "item_a": a,
            "item_b": b,
            "item_c": c
        })

        # Numerical integration over grid [-3.0, 3.0]
        points = 61
        grid = [-3.0 + i * 0.1 for i in range(points)]
        weights = []

        for pt in grid:
            prior = (1.0 / math.sqrt(2 * math.pi)) * math.exp(-0.5 * (pt ** 2))
            likelihood = 1.0
            for h in self.history:
                p_item = self.probability_correct(pt, h["item_a"], h["item_b"], h["item_c"])
                likelihood *= p_item if h["correct"] else (1.0 - p_item)
            weights.append(prior * likelihood)

        total_weight = sum(weights)
        if total_weight > 0:
            new_theta = sum(pt * w for pt, w in zip(grid, weights)) / total_weight
            self.theta = max(-3.0, min(3.0, round(new_theta, 3)))

        return self.theta

    def select_next_question(self, question_pool: List[Dict[str, Any]], excluded_ids: List[str] = None) -> Optional[Dict[str, Any]]:
        """Selects the unasked question maximizing Fisher Information at current theta."""
        excluded = set(excluded_ids or [])
        candidates = [q for q in question_pool if q.get("id") not in excluded]

        if not candidates:
            return None

        best_q = None
        max_info = -1.0

        for q in candidates:
            a = q.get("discrimination", 1.2)
            b = q.get("difficulty", 0.0)
            c = q.get("guessing", DEFAULT_GUESSING_C)
            info = self.fisher_information(self.theta, a, b, c)
            if info > max_info:
                max_info = info
                best_q = q

        if best_q:
            best_q = dict(best_q)
            best_q["fisher_information"] = round(max_info, 4)
            best_q["targeted_theta"] = self.theta

        return best_q

def main():
    print("=================================================================")
    print(" ⚡ CLOCKEE ADAPTIVE IRT SEQUENCER ENGINE (Reel #11)")
    print("=================================================================")

    # Create mock 20-question bank spanning theta range [-2.5 to +2.5]
    question_bank = []
    for i in range(25):
        b_diff = round(-2.0 + (i * 0.16), 2)
        question_bank.append({
            "id": f"q_irt_{i+1:02d}",
            "subject": "Physics" if i % 3 == 0 else "Maths" if i % 3 == 1 else "Chemistry",
            "topic": f"Adaptive Concept #{i+1}",
            "difficulty": b_diff,
            "discrimination": round(1.0 + (i % 5) * 0.15, 2),
            "guessing": 0.25
        })

    engine = IRTEngine(initial_theta=0.0)
    print(f"[*] Initial Student Ability: θ = {engine.theta:.2f} (Average / Mains Baseline)")

    asked = []
    simulated_responses = [True, True, True, False, True, False, True, True]

    for step, is_correct in enumerate(simulated_responses, 1):
        next_q = engine.select_next_question(question_bank, excluded_ids=asked)
        if not next_q:
            break
        asked.append(next_q["id"])

        old_theta = engine.theta
        new_theta = engine.update_ability_eap(
            response_correct=is_correct,
            a=next_q["discrimination"],
            b=next_q["difficulty"],
            c=next_q["guessing"]
        )

        status_str = "CORRECT  [✓]" if is_correct else "INCORRECT[!]"
        print(f"  Step #{step}: Served {next_q['id']} (b={next_q['difficulty']:+.2f}, a={next_q['discrimination']:.2f}) -> {status_str} | θ: {old_theta:+.2f} → {new_theta:+.2f}")

    print(f"\n[✓] Adaptive Test Terminated: Final Estimated Latent Ability θ = {engine.theta:+.2f}")
    assert engine.theta > 0.0, "Consistent correct answers should increase latent ability!"
    print("[✓] IRT 3PL Adaptive Sequencer certified (Exit Code 0).")

if __name__ == "__main__":
    main()
