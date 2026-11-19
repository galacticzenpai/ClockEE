import random
import time
from typing import Dict, Any, List

class NTAMockPaperCompiler:
    """
    Deterministic test paper assembler conforming to official NTA specifications:
    - 3 Subjects: Physics, Chemistry, Mathematics
    - Per Subject: 20 Single-Choice MCQs (+4/-1) + 10 Numerical Value (+4/0, attempt any 5)
    Total: 75 Questions attempted out of 90.
    """
    def __init__(self, seed: int = 42):
        self.random = random.Random(seed)

    def assemble_full_paper(self, mock_id: str = "JEE_MAIN_2026_MOCK_1") -> Dict[str, Any]:
        subjects = ["Physics", "Chemistry", "Mathematics"]
        paper = {
            "mock_id": mock_id,
            "generated_at": time.time(),
            "duration_minutes": 180,
            "total_marks": 300,
            "sections": {}
        }

        q_counter = 1
        for sub in subjects:
            sec_a = []
            for i in range(1, 21):
                sec_a.append({
                    "num": q_counter,
                    "id": f"{sub[:3].lower()}_mcq_{i}",
                    "type": "single_choice",
                    "subject": sub,
                    "marking": {"correct": 4, "wrong": -1}
                })
                q_counter += 1

            sec_b = []
            for j in range(1, 11):
                sec_b.append({
                    "num": q_counter,
                    "id": f"{sub[:3].lower()}_num_{j}",
                    "type": "numerical",
                    "subject": sub,
                    "marking": {"correct": 4, "wrong": 0}
                })
                q_counter += 1

            paper["sections"][sub] = {
                "section_a_mcq": sec_a,
                "section_b_numerical": sec_b
            }

        return paper

def benchmark_mock_compiler():
    compiler = NTAMockPaperCompiler()
    t0 = time.perf_counter()
    paper = compiler.assemble_full_paper()
    t1 = time.perf_counter()
    latency_us = (t1 - t0) * 1_000_000
    total_q = sum(len(s["section_a_mcq"]) + len(s["section_b_numerical"]) for s in paper["sections"].values())
    print(f"[BENCHMARK] Mock test paper compilation latency: {latency_us:.2f}µs ({total_q} questions assembled)")
    return latency_us

if __name__ == "__main__":
    benchmark_mock_compiler()
