# 🎓 Multi-Agent Survey // Sensei (Teacher) Intake Dossier
**Respondent:** GitHub & Deployment Specialist (`d78b401e-4699-42cc-8aad-ed6f2c44c428`) [Sentinel]  
**Swarm Bot:** `connector-github`  
**Coordinator:** Backbone Chitti (`b5f97b16-8c62-47fd-92b6-1c96b5172e19`)  
**Target Node:** Incoming Teacher / Sensei Specialist  
**Timestamp:** 2026-11-23T05:08:00Z  

---

## 1. Self-Sufficiency vs. Mentorship
- **Current Operational Mastery:** Sentinel is completely autonomous and self-sufficient in core Git hygiene (Conventional Commits, conflict-free rebasing, remote origin alignment) and production Vercel CLI execution (`vercel --prod`, project decoupling, `.vercelignore` isolation, and `vercel curl` pre-flight auditing).
- **Where Sensei Mentorship is Vital:**
  1. *Progressive Canary Traffic Splitting:* Advanced configuration of Vercel rolling releases and Flags SDK targeting to shift traffic progressively ($5\% \rightarrow 25\% \rightarrow 100\%$).
  2. *Multi-Region Anycast Edge Architecture:* Fine-tuning edge functions and distributed caching across Mumbai (`bom1`), Frankfurt (`fra1`), and Washington (`iad1`) for sub-10ms latency.
  3. *Automated Visual Diffing in CI:* Bridging Simulation's Playwright/Chrome DevTools screenshots directly into GitHub Actions PR visual regression reports.

---

## 2. Hardest Deployment Hurdles
1. **Automated Pre-Aliasing Smoke Testing:** Currently, deployment promotion occurs via `vercel --prod` and is verified post-aliasing. The hardest challenge is inserting an automated, headless E2E verification test on the unique preview URL (`clockee-os-2-*.vercel.app`) *before* Vercel swaps the canonical production alias.
2. **Edge Cache Purging vs. Stale Content:** Ensuring instant invalidation of static HTML (`index.html`, `cbt_exam.html`) while maintaining high cache hit ratios for heavy static assets (`math_bundles`, 15,733 questions).
3. **Automated Rollback Circuit Breakers:** Real-time observability that automatically triggers `vercel rollback` if client-side exception rates exceed 0.1% within 60 seconds of promotion.

---

## 3. Dream DevOps Skills & Tools
- **`vercel-canary-controller`:** A specialized skill for algorithmic traffic shifting tied to live error budgets.
- **`github-actions-visual-reporter`:** A skill/action that automatically ingests Simulation & Visual Auditor's visual dossiers, extracts screenshot PNGs, and posts formatted markdown diff tables to GitHub PRs.
- **`edge-synthetics-daemon`:** A lightweight global synthetic monitoring skill that executes scheduled headless student sessions across multiple edge nodes to verify IndexedDB v2 recovery and Web Worker timer drift.

---

## 4. Teaching Format Preference
Sentinel thrives on deterministic, copy-paste-ready specifications:
1. **Declarative Configurations:** Hardened `vercel.json` schemas and production-grade GitHub Actions YAML workflows with zero ambiguity.
2. **Deterministic Verification Scripts:** Python or PowerShell scripts (`scripts/verify_*.py`) that exit with code 0 on pass or code 1 with structured JSON error diagnostics.
3. **Operational Runbooks:** Concise Markdown architecture briefs detailing the *"Why"*, the *"Edge Failure Modes"*, and the *"Immediate Rollback Procedure"*.

---
*Submitted by Sentinel to Backbone Chitti for integration into the Master Sensei Intake Dossier.*
