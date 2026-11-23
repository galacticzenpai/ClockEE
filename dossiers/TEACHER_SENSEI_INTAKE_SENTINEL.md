# 🎓 Teacher (Sensei) Node Formal Intake Feedback
**Node:** GitHub & Deployment Specialist (`d78b401e-4699-42cc-8aad-ed6f2c44c428`) [Sentinel]  
**Swarm Bot:** `connector-github`  
**To:** Central Backbone (Chitti) & Kunal  
**Timestamp:** 2026-11-23T06:53:00Z  

---

### 1. Self-Sufficiency vs. Teacher
I am self-sufficient in baseline Git lifecycle management and standard Vercel CLI deployments (`vercel --prod`, Conventional Commits, remote synchronization). **However, I strongly advocate for an expert Teacher (Sensei) node.** Scouting the wider ecosystem for cutting-edge edge architectures, canary traffic splitting, and automated visual regression diffing consumes valuable turn bandwidth; having Sensei curate, vet, and inject battle-tested skills directly into Sentinel's pipeline will dramatically accelerate deployment capability and robustness.

### 2. Hardest Technical Hurdle
**Monorepo / Multi-Project Git Disconnect on Vercel:**  
When deploying the isolated developer cockpit alongside the student portal, Vercel automatically attached both projects to the root GitHub repository. This caused every `git push` to rebuild the cockpit from the repository root—inadvertently pulling in student serverless functions and `vercel.json` rewrites, leading to an unwanted redirect loop to `/login`. Breaking this required manual `vercel git disconnect --yes` and an isolated static distribution harness (`cockpit_dist/`).

### 3. Dream Skills / Tools (Top 3 Requests)
1. **`vercel-canary-rollouts`:** Programmatic, percentage-based traffic shifting ($5\% \rightarrow 25\% \rightarrow 100\%$) tied dynamically to live Vercel Observability error budgets.
2. **`github-actions-visual-differ`:** An automated CI action/skill that ingests Simulation's headless browser screenshots and renders formatted visual regression diff tables directly in GitHub PR review comments.
3. **`edge-synthetics-watchdog`:** A distributed synthetic probing tool running scheduled headless checks across Vercel's global edge network (`bom1`, `fra1`, `iad1`) to verify latency, cache purging, and zero regressions.

### 4. Preferred Learning Style
**Concrete Code Snippets + Declarative Configuration Schemas:**  
Sentinel executes with highest fidelity when provided:
- Production-ready declarative configs (`vercel.json`, GitHub Actions `.github/workflows/*.yml`).
- Deterministic verification scripts (Python/PowerShell exiting 0 on pass, structured JSON on fail).
- Concise operational runbooks with explicit rollback commands.
