---
name: page_audit
description: Automated headless Core Web Vitals audit suite enforcing 60FPS DOM rendering, zero layout shifts, and script deferral.
domain: Performance & CWV Guardrails
upstream: GoogleChromeLabs/lighthouse-batch
reel_id: reel_007
---

# ⚡ Page-Audit Core Web Vitals Guardrail (Reel #7)

Automated headless performance audit suite enforcing high-frame-rate rendering, zero layout shift (CLS < 0.05), and script non-blocking standards across ClockEE.

## Capabilities
1. **Script Blocking Detection**: Audits HTML `<head>` tags to ensure heavy third-party assets are deferred.
2. **Layout Shift (CLS) Analysis**: Validates explicit image and element dimension bounding.
3. **DOM Complexity Sentinel**: Monitors node count limits (<1800 nodes) to prevent mobile render stutter during exams.
4. **Automated Quality Gate**: Produces `page_audit_report.json` with average performance scoring.

## CLI Usage
```bash
python integrations/page_audit/audit_runner.py
```
