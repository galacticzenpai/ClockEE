import time
from typing import List, Dict, Any, Tuple

class CBTTelemetryAggregator:
    """
    High-density student time-series telemetry aggregator for 60FPS charts.
    Processes question response times, cumulative scores, and rolling accuracy.
    """
    def __init__(self, raw_events: List[Dict[str, Any]] = None):
        self.events = raw_events or []

    def compute_time_series(self, question_times: List[float], correct_flags: List[bool]) -> Dict[str, Any]:
        """
        Computes 2D arrays compatible with lightweight Canvas line/scatter rendering.
        """
        n = len(question_times)
        if n == 0:
            return {"timestamps": [], "seconds_per_q": [], "cumulative_accuracy": []}

        timestamps = list(range(1, n + 1))
        cumulative_accuracy = []
        running_correct = 0

        for i, is_correct in enumerate(correct_flags):
            if is_correct:
                running_correct += 1
            cumulative_accuracy.append(round((running_correct / (i + 1)) * 100, 2))

        return {
            "questions": timestamps,
            "seconds_per_q": question_times,
            "cumulative_accuracy": cumulative_accuracy
        }

def benchmark_telemetry():
    aggregator = CBTTelemetryAggregator()
    # 180 questions (full 3-hour JEE test)
    times = [45.0 + (i % 15) for i in range(180)]
    flags = [(i % 3 != 0) for i in range(180)]

    t0 = time.perf_counter()
    res = aggregator.compute_time_series(times, flags)
    t1 = time.perf_counter()
    latency_ms = (t1 - t0) * 1000
    print(f"[BENCHMARK] Telemetry aggregation latency: {latency_ms:.3f}ms for {len(times)} questions")
    return latency_ms

if __name__ == "__main__":
    benchmark_telemetry()
