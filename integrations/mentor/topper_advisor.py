import time
from typing import Dict, Any, List

class TopperMentorAdvisor:
    """
    Data-driven study persona and exam strategy advisor.
    Generates tailored advice based on question-level time and accuracy metrics.
    """
    def generate_recommendations(self, score: int, accuracy: float, negative_marks: int, stuck_questions_cnt: int) -> List[Dict[str, str]]:
        tips = []

        if negative_marks >= 15:
            tips.append({
                "category": "NEGATIVE_MARK_TRIAGE",
                "severity": "CRITICAL",
                "title": "Strict Skip Discipline Required",
                "advice": f"You lost {negative_marks} marks to negative penalty. On round 1, do not guess when confidence is under 75%."
            })

        if stuck_questions_cnt >= 4:
            tips.append({
                "category": "TIME_MANAGEMENT",
                "severity": "HIGH",
                "title": "Break the 3-Minute Trap",
                "advice": f"You spent >3 minutes each on {stuck_questions_cnt} questions. If an equation doesn't simplify within 90s, mark for review and move on."
            })

        if accuracy >= 85.0:
            tips.append({
                "category": "ADVANCED_EXPANSION",
                "severity": "POSITIVE",
                "title": "Elite Accuracy Foundation",
                "advice": "Your accuracy is in the top 1% bracket. Focus on increasing round-1 speed to attempt 5-8 more questions."
            })
        else:
            tips.append({
                "category": "CONCEPTUAL_REVISION",
                "severity": "MODERATE",
                "title": "Strengthen Core NCERT Foundation",
                "advice": "Revise foundational chapter formula sheets before taking your next full mock."
            })

        return tips

def benchmark_topper_advisor():
    advisor = TopperMentorAdvisor()
    t0 = time.perf_counter()
    tips = advisor.generate_recommendations(score=195, accuracy=78.2, negative_marks=18, stuck_questions_cnt=5)
    t1 = time.perf_counter()
    latency_us = (t1 - t0) * 1_000_000
    print(f"[BENCHMARK] Topper advisor evaluation latency: {latency_us:.2f}µs ({len(tips)} tips generated)")
    return latency_us

if __name__ == "__main__":
    benchmark_topper_advisor()
