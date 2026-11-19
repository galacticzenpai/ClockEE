---
name: cloudflare-security-audit
description: Cloudflare open-source multi-phase security audit skill with adversarial disproval for web applications.
---

# Cloudflare Security Audit Skill

Adapted from [`cloudflare/security-audit-skill`](https://github.com/cloudflare/security-audit-skill) (MIT License).

## How This Skill Works
Unlike generic code review prompts, this skill enforces a **six-phase adversarial audit**:
1. **Reconnaissance**: Discovers all entry points (`*.html`), client state stores (`localStorage`, `sessionStorage`, `indexedDB`), and API endpoints.
2. **Coverage-Led Hunting**: Systematically checks every route for XSS (`.innerHTML`), token exposure, and dynamic code execution.
3. **Candidate Validation (Adversarial Pass)**: Deploys a distinct sub-agent to attempt to *disprove* each finding before it is reported (filtering out false positives).
4. **Structured Output**: Produces exact line numbers, code snippets, and remediation instructions.
5. **Repeated Runs Warning**: Cloudflare notes that a single pass identifies ~50% of deep vulnerabilities. Repeat runs across complex files are strongly advised.

## CLI Execution
```bash
python integrations/cloudflare_security_audit/audit_runner.py
```

## Prompt Template for AI Agents
To run this skill across your codebase, invoke:
> "Run Cloudflare Security Audit on this codebase. Map all entry points, dispatch adversarial checkers to disprove false positives, and output verified high-priority fixes."
