import time
from typing import Dict, Any, List

class SplitDrawerPaletteState:
    """
    Computes palette breakdown summary across 180 questions for high-speed drawer rendering.
    """
    def __init__(self, total_questions: int = 180):
        self.total = total_questions

    def compute_summary(self, answers: Dict[str, Any], marked_for_review: List[int], visited: List[int]) -> Dict[str, Any]:
        answered_cnt = len([k for k, v in answers.items() if v is not None and v != ""])
        review_cnt = len(marked_for_review)
        visited_set = set(visited)
        
        not_visited_cnt = max(0, self.total - len(visited_set))
        not_answered_cnt = max(0, len(visited_set) - answered_cnt)

        return {
            "total": self.total,
            "answered": answered_cnt,
            "marked_for_review": review_cnt,
            "not_answered": not_answered_cnt,
            "not_visited": not_visited_cnt
        }

def benchmark_palette():
    palette = SplitDrawerPaletteState(total_questions=180)
    answers = {f"q_{i}": "A" for i in range(1, 95)}
    marked = [12, 45, 88, 102]
    visited = list(range(1, 140))

    t0 = time.perf_counter()
    summary = palette.compute_summary(answers, marked, visited)
    t1 = time.perf_counter()
    latency_us = (t1 - t0) * 1_000_000
    print(f"[BENCHMARK] Palette state computation latency: {latency_us:.2f}µs: {summary}")
    return latency_us

if __name__ == "__main__":
    benchmark_palette()
