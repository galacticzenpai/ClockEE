import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

t0 = time.time()
from integrations.hallmark_design.sloplint import SlopLinter
linter = SlopLinter()
rep = linter.lint_file(ROOT / "index.html")
print(f"sloplint in-process: score={rep['score']}, floor_violations={len(rep['floor_violations'])}, time={time.time()-t0:.3f}s")

t1 = time.time()
from integrations.cloudflare_security_audit.audit_runner import CloudflareSecurityAudit
auditor = CloudflareSecurityAudit(ROOT)
report, out_file = auditor.generate_report()
print(f"audit in-process: verified={report['metrics']['actionable_verified_vulnerabilities']}, time={time.time()-t1:.3f}s")
