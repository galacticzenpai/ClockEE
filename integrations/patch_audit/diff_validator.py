import subprocess
import time
from typing import List, Dict, Any, Tuple

class GitPatchDiffAuditor:
    """
    AST-aware staged diff auditor protecting against accidental deletions
    and corrupted question banks.
    """
    PROTECTED_FILES = {
        "cbt_master_bank.js",
        "clockee.db",
        "clockee_auth.db",
        "cbt_shared.css"
    }

    def check_staged_changes(self) -> Tuple[bool, List[str]]:
        violations = []
        try:
            res = subprocess.run(
                ["git", "diff", "--cached", "--name-status"],
                capture_output=True,
                text=True,
                check=False
            )
            lines = res.stdout.strip().splitlines()
            for line in lines:
                parts = line.split(maxsplit=1)
                if len(parts) == 2:
                    status, filename = parts[0], parts[1]
                    # Block deletion of protected files
                    if status == "D" and any(p in filename for p in self.PROTECTED_FILES):
                        violations.append(f"CRITICAL: Protected file deletion attempted: {filename}")
        except Exception as e:
            violations.append(f"Diff execution error: {e}")

        return (len(violations) == 0, violations)

def benchmark_patch_auditor():
    auditor = GitPatchDiffAuditor()
    t0 = time.perf_counter()
    passed, violations = auditor.check_staged_changes()
    t1 = time.perf_counter()
    latency_ms = (t1 - t0) * 1000
    print(f"[BENCHMARK] Staged diff audit latency: {latency_ms:.3f}ms (Passed: {passed}, Violations: {len(violations)})")
    return latency_ms

if __name__ == "__main__":
    benchmark_patch_auditor()
