import time
from typing import Dict, Any, List

class FlukeGuessAnalyzer:
    """
    Statistical fluke detector for high-stakes MCQs.
    Evaluates whether a correct response represents authentic mastery
    or a lucky blind guess based on response latency and question complexity.
    """
    DIFFICULTY_MIN_SECONDS = {
        "Easy": 10.0,
        "Moderate": 25.0,
        "Tough": 45.0,
        "Advanced": 60.0
    }

    def evaluate_response(self, is_correct: bool, spent_sec: float, difficulty: str = "Moderate", num_options: int = 4) -> Dict[str, Any]:
        if not is_correct:
            return {
                "is_correct": False,
                "is_fluke": False,
                "confidence": 0.0,
                "verdict": "INCORRECT"
            }

        min_time = self.DIFFICULTY_MIN_SECONDS.get(difficulty, 20.0)
        base_guess_prob = 1.0 / num_options # 0.25 for 4 options

        if spent_sec < min_time * 0.25:
            # Answered in under 25% of absolute minimum read time: High fluke probability
            confidence = round(max(0.1, (spent_sec / min_time) * base_guess_prob), 2)
            is_fluke = True
            verdict = "HIGH_PROBABILITY_LUCKY_GUESS"
        elif spent_sec < min_time * 0.6:
            confidence = round(0.5 + 0.3 * (spent_sec / min_time), 2)
            is_fluke = False
            verdict = "FAST_SOLVE_POSSIBLE_INTUITION"
        else:
            confidence = 1.0
            is_fluke = False
            verdict = "AUTHENTIC_MASTERY"

        return {
            "is_correct": True,
            "is_fluke": is_fluke,
            "confidence": confidence,
            "verdict": verdict,
            "spent_sec": spent_sec,
            "min_expected_sec": min_time
        }

    def analyze_exam_session(self, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        fluke_count = 0
        total_correct = 0
        authentic_correct = 0

        for q in questions:
            is_corr = q.get("is_correct", False)
            if is_corr:
                total_correct += 1
                res = self.evaluate_response(
                    is_correct=True,
                    spent_sec=q.get("spent_sec", 60.0),
                    difficulty=q.get("difficulty", "Moderate")
                )
                if res["is_fluke"]:
                    fluke_count += 1
                else:
                    authentic_correct += 1

        calibrated_score = (authentic_correct * 4) - (len(questions) - total_correct)
        
        return {
            "total_questions": len(questions),
            "total_correct": total_correct,
            "fluke_guesses_detected": fluke_count,
            "authentic_correct": authentic_correct,
            "raw_score": (total_correct * 4) - (len(questions) - total_correct),
            "calibrated_mastery_score": calibrated_score
        }

def benchmark_fluke():
    analyzer = FlukeGuessAnalyzer()
    # 75 questions mock
    q_stream = [
        {"is_correct": True, "spent_sec": 4.5, "difficulty": "Tough"}, # Lucky guess
        {"is_correct": True, "spent_sec": 95.0, "difficulty": "Tough"}, # Authentic
        {"is_correct": False, "spent_sec": 120.0, "difficulty": "Moderate"},
        {"is_correct": True, "spent_sec": 35.0, "difficulty": "Easy"} # Authentic
    ] * 20

    t0 = time.perf_counter()
    report = analyzer.analyze_exam_session(q_stream)
    t1 = time.perf_counter()
    latency_us = ((t1 - t0) / len(q_stream)) * 1_000_000
    print(f"[BENCHMARK] Fluke analysis latency: {latency_us:.2f}µs per question")
    print(f"Report: {report}")
    return latency_us

if __name__ == "__main__":
    benchmark_fluke()
