import os
import json
from pathlib import Path

BRAIN_DIR = Path(r"C:\Users\Kunal\.gemini\antigravity\brain")

CONVERSATIONS = {
    "untitled_conversation": "6371cba6-7d2f-4b29-a250-627d88d1b4f1",
    "ui_ux": "06a7d47b-b225-40f4-b830-b58baaaf8b3a",
    "simulation": "62adc180-be21-4671-848c-c8df59e2c202",
    "db_backend": "d3700ff3-1bfb-458a-9968-8257ef2ca7e2",
    "github": "a64c937f-bb58-4071-8eb9-32f5edbb6c2c",
    "q_a": "6029bc76-d833-4ab6-8672-b5f43511cf8f",
    "inspiration": "e6690e55-bfca-4ce1-af20-843015d7d01b",
    "bug_fixes": "6b74e384-a9b2-458e-ba34-4798334dd509",
    "backbone": "a80111ec-0657-4748-9e85-d620e8a2a535"
}

def get_tail_steps(file_path, max_bytes=65536, n=3):
    if not file_path.is_file():
        return []
    try:
        size = file_path.stat().st_size
        with open(file_path, "rb") as f:
            if size > max_bytes:
                f.seek(size - max_bytes)
            chunk = f.read()
        lines = chunk.decode("utf-8", errors="ignore").splitlines()
        # Parse from the end
        steps = []
        for line in reversed(lines):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                steps.append(obj)
                if len(steps) >= n:
                    break
            except Exception:
                continue
        return list(reversed(steps))
    except Exception as e:
        return [{"error": str(e)}]

def main():
    print("Scanning conversation transcripts...")
    for name, cid in CONVERSATIONS.items():
        t_path = BRAIN_DIR / cid / ".system_generated" / "logs" / "transcript.jsonl"
        steps = get_tail_steps(t_path, n=2)
        print(f"\n--- {name} ({cid[:8]}) ---")
        if not steps:
            print("  [No steps found]")
            continue
        for s in steps:
            s_idx = s.get("step_index", "?")
            s_type = s.get("type", "?")
            s_src = s.get("source", "?")
            s_status = s.get("status", "?")
            content = str(s.get("content", ""))
            preview = (content[:120] + "...") if len(content) > 120 else content
            preview = preview.replace("\n", " ")
            print(f"  Step {s_idx} [{s_src}/{s_type}|{s_status}]: {preview}")

if __name__ == "__main__":
    main()
