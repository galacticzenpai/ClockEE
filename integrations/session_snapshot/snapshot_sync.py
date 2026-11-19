import copy
import hashlib
import json
import time
from typing import Dict, Any, Optional, Tuple, List

class SessionSnapshotEngine:
    """
    High-speed exam session state serializer and delta tracker.
    Provides sub-5ms delta generation and checksum verification.
    """
    def __init__(self, exam_id: str, student_id: str):
        self.exam_id = exam_id
        self.student_id = student_id
        self.last_snapshot: Dict[str, Any] = {}
        self.last_checksum: str = ""
        self.version: int = 0

    def compute_checksum(self, payload: Dict[str, Any]) -> str:
        # Avoid including checksum key itself
        clean_copy = {k: v for k, v in payload.items() if k != "checksum"}
        serialized = json.dumps(clean_copy, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def serialize_full(self, current_question: int, answers: Dict[str, Any], marked_for_review: List[int], remaining_sec: int) -> Dict[str, Any]:
        self.version += 1
        data = {
            "exam_id": self.exam_id,
            "student_id": self.student_id,
            "version": self.version,
            "timestamp": time.time(),
            "current_question": current_question,
            "answers": copy.deepcopy(answers),
            "marked_for_review": sorted(copy.deepcopy(marked_for_review)),
            "remaining_sec": remaining_sec
        }
        checksum = self.compute_checksum(data)
        data["checksum"] = checksum
        self.last_snapshot = copy.deepcopy(data)
        self.last_checksum = checksum
        return data

    def compute_delta(self, current_state: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
        """
        Computes delta between last snapshot and current state.
        Returns (delta_dict, has_changed).
        """
        if not self.last_snapshot:
            full = self.serialize_full(
                current_state.get("current_question", 1),
                current_state.get("answers", {}),
                current_state.get("marked_for_review", []),
                current_state.get("remaining_sec", 10800)
            )
            return full, True

        delta = {}
        changed = False

        for k in ["current_question", "remaining_sec"]:
            if current_state.get(k) != self.last_snapshot.get(k):
                delta[k] = current_state.get(k)
                changed = True

        cur_answers = current_state.get("answers", {})
        last_answers = self.last_snapshot.get("answers", {})
        if cur_answers != last_answers:
            # find modified or new answers
            answer_delta = {}
            for q_id, ans in cur_answers.items():
                if last_answers.get(q_id) != ans:
                    answer_delta[q_id] = ans
            delta["answers_delta"] = answer_delta
            changed = True

        cur_review = sorted(current_state.get("marked_for_review", []))
        last_review = self.last_snapshot.get("marked_for_review", [])
        if cur_review != last_review:
            delta["marked_for_review"] = cur_review
            changed = True

        if changed:
            self.version += 1
            delta["version"] = self.version
            delta["timestamp"] = time.time()
            # update last snapshot state
            self.last_snapshot.update(current_state)
            self.last_snapshot["version"] = self.version
            self.last_checksum = self.compute_checksum(self.last_snapshot)
            delta["checksum"] = self.last_checksum

        return delta, changed

    def verify_and_restore(self, raw_snapshot: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, Any]]]:
        if "checksum" not in raw_snapshot:
            return False, None
        expected = raw_snapshot.pop("checksum")
        computed = self.compute_checksum(raw_snapshot)
        raw_snapshot["checksum"] = expected
        if computed == expected:
            self.last_snapshot = raw_snapshot
            self.version = raw_snapshot.get("version", 0)
            return True, raw_snapshot
        return False, None

def benchmark_snapshot_engine():
    engine = SessionSnapshotEngine(exam_id="JEE_ADV_2026_MOCK_1", student_id="STU_9941")
    t0 = time.perf_counter()
    initial = engine.serialize_full(
        current_question=1,
        answers={"q1": "A", "q2": "B"},
        marked_for_review=[5, 12],
        remaining_sec=10750
    )
    t1 = time.perf_counter()
    
    # Delta benchmark
    t2 = time.perf_counter()
    delta, changed = engine.compute_delta({
        "current_question": 2,
        "answers": {"q1": "A", "q2": "C", "q3": "D"},
        "marked_for_review": [5, 12, 19],
        "remaining_sec": 10740
    })
    t3 = time.perf_counter()

    valid, restored = engine.verify_and_restore(initial)
    full_ms = (t1 - t0) * 1000
    delta_ms = (t3 - t2) * 1000
    print(f"[BENCHMARK] Full snapshot: {full_ms:.3f}ms | Delta: {delta_ms:.3f}ms | Checksum valid: {valid}")
    return full_ms, delta_ms, valid

if __name__ == "__main__":
    benchmark_snapshot_engine()
