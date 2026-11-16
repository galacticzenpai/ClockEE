import time
from typing import Dict, Any, Tuple

class NTARankPredictor:
    """
    Historical percentile interpolator and All India Rank (AIR) projector
    based on JEE Advanced score distributions (300 Marks max).
    """
    # Score to AIR bands (Historical benchmarks)
    BENCHMARKS = [
        (280, 1, 50, 99.99),
        (250, 51, 250, 99.90),
        (220, 251, 1000, 99.50),
        (190, 1001, 2500, 98.80),
        (160, 2501, 5000, 97.50),
        (130, 5001, 10000, 95.00),
        (100, 10001, 25000, 88.00),
        (70, 25001, 50000, 75.00),
        (0, 50001, 150000, 0.00)
    ]

    def predict_rank(self, score: int, max_score: int = 300) -> Dict[str, Any]:
        normalized_score = min(max_score, max(0, score))
        percentage = (normalized_score / max_score) * 100

        for cutoff, air_min, air_max, percentile in self.BENCHMARKS:
            if normalized_score >= cutoff:
                return {
                    "raw_score": score,
                    "max_score": max_score,
                    "percentage": round(percentage, 2),
                    "predicted_air_range": f"{air_min} - {air_max}",
                    "estimated_percentile": percentile,
                    "confidence_band": "± 5%"
                }

        return {
            "raw_score": score,
            "max_score": max_score,
            "percentage": round(percentage, 2),
            "predicted_air_range": "100,000+",
            "estimated_percentile": 50.0,
            "confidence_band": "± 10%"
        }

    def compute_subject_breakdown(self, physics_score: int, chem_score: int, math_score: int) -> Dict[str, Any]:
        total = physics_score + chem_score + math_score
        pred = self.predict_rank(total)
        return {
            "physics": {"score": physics_score, "share": round((physics_score / max(1, total)) * 100, 1)},
            "chemistry": {"score": chem_score, "share": round((chem_score / max(1, total)) * 100, 1)},
            "maths": {"score": math_score, "share": round((math_score / max(1, total)) * 100, 1)},
            "total_score": total,
            "rank_prediction": pred
        }

def benchmark_rank_predictor():
    predictor = NTARankPredictor()
    t0 = time.perf_counter()
    res = predictor.compute_subject_breakdown(physics_score=78, chem_score=85, math_score=62)
    t1 = time.perf_counter()
    latency_us = (t1 - t0) * 1_000_000
    print(f"[BENCHMARK] Rank prediction latency: {latency_us:.2f}µs")
    print(f"Result: {res}")
    return latency_us

if __name__ == "__main__":
    benchmark_rank_predictor()
