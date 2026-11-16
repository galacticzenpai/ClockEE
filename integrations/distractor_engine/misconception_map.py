#!/usr/bin/env python3
"""
⚡ ClockEE — Reel #12: Plausible MCQ Distractor & Misconception Analyzer
Upstream: question-bank-distractors
Domain: Adaptive CBT Exam Engine

Heuristic analyzer mapping incorrect MCQ distractor options to specific
conceptual traps, mathematical calculation mistakes, and NTA decoy patterns.
"""

import sys
import json
from typing import Dict, Any, List

TRAP_TAXONOMY = {
    "SIGN_ERROR": {
        "label": "Sign / Polarity Inversion",
        "desc": "Confused positive/negative sign (e.g. Lenz law negative sign omitted, work done on vs by system)."
    },
    "MISSED_FACTOR_OF_TWO": {
        "label": "Missing 1/2 or 2x Factor",
        "desc": "Omitted factor of 1/2 in kinetic energy (1/2 mv^2), spring potential, or rotational inertia."
    },
    "INVERTED_FRACTION": {
        "label": "Reciprocal / Inverted Ratio",
        "desc": "Calculated numerator/denominator inverted (e.g. parallel resistance formula 1/R = 1/R1 + 1/R2 inverted prematurely)."
    },
    "FORMULA_CONFUSION": {
        "label": "Analogous Formula Mismatch",
        "desc": "Applied series formula instead of parallel, or electric field instead of electric potential."
    },
    "DIMENSIONAL_MISMATCH": {
        "label": "Unit & Metric Power Mismatch",
        "desc": "Failed to convert cm to m, grams to kg, or eV to Joules."
    },
    "SUPERFICIAL_INTUITION": {
        "label": "Superficial Decoy Trap",
        "desc": "Selected simple arithmetic sum without accounting for vector angles or non-linear scaling."
    }
}

class DistractorAnalyzer:
    def __init__(self):
        pass

    def diagnose_selection(self, selected_option: str, correct_option: str, question_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Diagnoses why a student selected a particular incorrect option."""
        if selected_option.upper() == correct_option.upper():
            return {
                "correct": True,
                "diagnosis": "Optimal Execution",
                "trap_type": None,
                "pedagogical_advice": "Flawless concept application. Maintain this cadence."
            }

        distractor_maps = question_metadata.get("distractor_map", {})
        trap_key = distractor_maps.get(selected_option.upper(), "SUPERFICIAL_INTUITION")
        trap_info = TRAP_TAXONOMY.get(trap_key, TRAP_TAXONOMY["SUPERFICIAL_INTUITION"])

        advice = f"You selected option {selected_option.upper()} which exhibits a classic {trap_info['label']}. Focus on verifying intermediate algebraic steps."

        return {
            "correct": False,
            "selected_option": selected_option.upper(),
            "correct_option": correct_option.upper(),
            "trap_type": trap_key,
            "trap_label": trap_info["label"],
            "trap_description": trap_info["desc"],
            "pedagogical_advice": advice
        }

def main():
    print("=================================================================")
    print(" ⚡ CLOCKEE MCQ DISTRACTOR & MISCONCEPTION ANALYZER (Reel #12)")
    print("=================================================================")

    sample_question = {
        "question_id": "jee_phy_rot_04",
        "correct_option": "B",
        "options": {
            "A": "8 J",
            "B": "4 J",
            "C": "16 J",
            "D": "2 J"
        },
        "distractor_map": {
            "A": "MISSED_FACTOR_OF_TWO",
            "C": "SUPERFICIAL_INTUITION",
            "D": "INVERTED_FRACTION"
        }
    }

    analyzer = DistractorAnalyzer()
    print("[*] Simulating Student Selection of Option 'A' (Incorrect Distractor)...")
    diagnosis = analyzer.diagnose_selection("A", sample_question["correct_option"], sample_question)

    print(f"  • Selected Option : {diagnosis['selected_option']}")
    print(f"  • Correct Option  : {diagnosis['correct_option']}")
    print(f"  • Trap Category   : {diagnosis['trap_label']}")
    print(f"  • Trap Pathology  : {diagnosis['trap_description']}")
    print(f"  • Remediation     : {diagnosis['pedagogical_advice']}")

    assert diagnosis["trap_type"] == "MISSED_FACTOR_OF_TWO"
    print("\n[✓] Distractor Analyzer certified (Exit Code 0).")

if __name__ == "__main__":
    main()
