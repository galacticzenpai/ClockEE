import time
from typing import Dict, Any, List

NTA_KEYMAP: Dict[str, str] = {
    "1": "SELECT_OPTION_A",
    "2": "SELECT_OPTION_B",
    "3": "SELECT_OPTION_C",
    "4": "SELECT_OPTION_D",
    "s": "SAVE_AND_NEXT",
    "Enter": "SAVE_AND_NEXT",
    "m": "MARK_FOR_REVIEW",
    "r": "MARK_FOR_REVIEW",
    "c": "CLEAR_RESPONSE",
    "Backspace": "CLEAR_RESPONSE",
    "p": "PREV_QUESTION",
    "ArrowLeft": "PREV_QUESTION",
    "n": "NEXT_QUESTION",
    "ArrowRight": "NEXT_QUESTION",
    "?": "TOGGLE_HUD_OVERLAY"
}

class KeymapValidator:
    def __init__(self, keymap: Dict[str, str] = None):
        self.keymap = keymap or NTA_KEYMAP

    def resolve_action(self, key_event: str) -> str:
        return self.keymap.get(key_event, "UNKNOWN")

    def simulate_exam_stream(self, key_sequence: List[str]) -> List[str]:
        actions = []
        for key in key_sequence:
            actions.append(self.resolve_action(key))
        return actions

def benchmark_keymap():
    validator = KeymapValidator()
    # Simulate 1000 keystrokes
    sequence = ["1", "s", "2", "m", "c", "3", "Enter", "ArrowRight", "p", "?"] * 100
    t0 = time.perf_counter()
    actions = validator.simulate_exam_stream(sequence)
    t1 = time.perf_counter()
    latency_us = ((t1 - t0) / len(sequence)) * 1_000_000
    print(f"[BENCHMARK] Keystroke resolution latency: {latency_us:.2f}µs per stroke ({len(actions)} keystrokes resolved)")
    return latency_us

if __name__ == "__main__":
    benchmark_keymap()
