# ClockEE Developer Integrations & Vendor Packages

This directory contains the 5 packages adapted from the developer showcase (`petergriffin.ai [DeZzNXlTELF]`):

---

### 1. Multi-Model LLM Router (LiteLLM / FreeLLMAPI)
* **Directory**: `integrations/llm_router/`
* **Core Script**: `router.py`
* **Frontend Wrapper**: `client_wrapper.js` (`window.ClockEE_LLMRouter.generate(prompt)`)
* **Purpose**: Prevents rate-limit lockouts by automatically failing over across Gemini, DeepSeek, Claude, and OpenAI.

### 2. Strix Security Vulnerability Scanner (SAST)
* **Directory**: `integrations/security_scanner/`
* **Core Script**: `strix_scanner.py`
* **Run Command**: `python integrations/security_scanner/strix_scanner.py`
* **Purpose**: Scans ClockEE HTML, JS, and backend files for XSS vectors, unescaped innerHTML, hardcoded credentials, and unsafe eval functions.

### 3. Agent Long-Term Memory Vault (Claude-Mem / Mem0)
* **Directory**: `integrations/agent_memory/`
* **Core Script**: `memory_vault.py` (SQLite persistent database `agent_memory.db`)
* **Frontend Wrapper**: `memory_client.js` (`window.ClockEE_Memory.remember(key, val, category)`)
* **Purpose**: Preserves student habits, recurring mistakes, exam goals, and developer preferences across sessions.

### 4. Agent Reach Forum & Web Data Bridge
* **Directory**: `integrations/agent_reach/`
* **Core Script**: `reach.py`
* **Run Command**: `python integrations/agent_reach/reach.py`
* **Purpose**: Fetches public discussion threads (e.g. `r/JEENEETards`, educational forums) and extracts clean summaries without requiring API keys.

### 5. Codebase Architecture & MCP Recommender
* **Directory**: `integrations/codebase_scanner/`
* **Core Script**: `mcp_recommender.py`
* **Run Command**: `python integrations/codebase_scanner/mcp_recommender.py`
* **Purpose**: Scans project structure and line counts, recommending the optimal Model Context Protocol (MCP) servers and Antigravity skills.

---

### 6. Cloudflare Security Audit Skill (Adversarial False-Positive Disproval)
* **Source Showcase**: `waitwhatdidyoudo [De9bqWtoARc]`
* **Upstream**: Cloudflare open-source `cloudflare/security-audit-skill` (MIT License)
* **Directory**: `integrations/cloudflare_security_audit/`
* **Skill Specification**: `integrations/cloudflare_security_audit/SKILL.md`
* **Core Script**: `integrations/cloudflare_security_audit/audit_runner.py`
* **Run Command**: `python integrations/cloudflare_security_audit/audit_runner.py`
* **Output Reports**: `integrations/cloudflare_security_audit/reports/`
* **Purpose**: Performs a 4-phase static application security audit (Reconnaissance, Coverage Hunting, Adversarial Disproval to eliminate false positives, and Machine-Readable JSON reporting).

---

### 7. Hallmark Anti-AI-Slop Design Skill & Linter
* **Source Showcase**: `waitwhatdidyoudo [DfCznzwKh4k]`
* **Upstream**: Together AI / Hassan El Mghari `nutlope/hallmark` (MIT License)
* **Directory**: `integrations/hallmark_design/`
* **Skill Specification**: `integrations/hallmark_design/SKILL.md`
* **Core Linter**: `integrations/hallmark_design/sloplint.py`
* **Theme Catalog**: `integrations/hallmark_design/themes_catalog.json`
* **CLI Utility**: `integrations/hallmark_design/hallmark_cli.py`
* **Audit Command**: `python integrations/hallmark_design/hallmark_cli.py audit [file.html or --all]`
* **Theme Command**: `python integrations/hallmark_design/hallmark_cli.py themes`
* **Purpose**: Enforces human-crafted UI design and eliminates AI clichés (purple gradients, single colored words in headings, generic glass cards, dummy forms) with a 3-tier quality gate (Floor, Reflex, Finish) and 50 curated material themes.

---

### 8. Graphify Codebase Knowledge Graph & God-Node Analyzer
* **Source Showcase**: `waitwhatdidyoudo [DfFUVDVKwF5]`
* **Upstream**: `Graphify-Labs/graphify` (Apache-2.0 / MIT License)
* **Directory**: `integrations/graphify/`
* **Skill Specification**: `integrations/graphify/SKILL.md`
* **Core Script**: `integrations/graphify/graph_runner.py`
* **Build Command**: `python integrations/graphify/graph_runner.py build`
* **Query Command**: `python integrations/graphify/graph_runner.py query <symbol_or_filename>`
* **Reports Directory**: `integrations/graphify/reports/` (`graph.json`, `GRAPH_REPORT.md`)
* **Purpose**: Maps cross-file dependencies, script inclusions, and storage keys into a deterministic knowledge graph, detecting architectural "god nodes" (e.g. `env.js`, `clockee_core.js`, `cbt_shared.js`) to prevent cascading breaking changes during refactors.

---

### 9. LLM-Lint: AI Provenance & Attribution Sanitizer
* **Source Showcase**: `agentpoly [De63OT8Sqwg]`
* **Upstream**: `JadenRazo/llm-lint` (MIT License)
* **Directory**: `integrations/llm_lint/`
* **Skill Specification**: `integrations/llm_lint/SKILL.md`
* **Core Script**: `integrations/llm_lint/lint_runner.py`
* **Scan Command**: `python integrations/llm_lint/lint_runner.py scan`
* **Hook Install**: `python integrations/llm_lint/lint_runner.py install-hook`
* **Reports Directory**: `integrations/llm_lint/reports/`
* **Purpose**: Scans repository commits, docstrings, and pull requests to detect and clean unwanted AI attribution watermarks (`Co-authored-by: Claude`, `Generated with Claude Code`, prompt leaks) and installs an automatic Git `commit-msg` sanitizer hook.

---

### 10. Dray: Cross-Model Context Handoff Bridge (`/link`)
* **Source Showcase**: `withdray_ [DfDPuZjE-7Q]`
* **Upstream**: `monorepo-labs/dray` / `drayhq.com`
* **Directory**: `integrations/dray_cross_model/`
* **Skill Specification**: `integrations/dray_cross_model/SKILL.md`
* **Core Script**: `integrations/dray_cross_model/dray_bridge.py`
* **Commands**: `python integrations/dray_cross_model/dray_bridge.py demo | link | verify`
* **Payload File**: `integrations/dray_cross_model/dray_link_payload.md`
* **Purpose**: Solves AI usage limit cutoffs and session resets by capturing in-flight task progress, active files, and strict protected guardrails into a standardized `/link` handoff payload for the next model to resume without context loss.

### 11. OmniRoute Multi-Provider Token Gateway (integrations/omniroute/)
- **Origin**: Reel #4 (https://www.instagram.com/p/De6ttI-zAba/ by @tech.oak) / omniroute npm.
- **Purpose**: Local OpenAI-compatible gateway (http://localhost:20128/v1) unifying free AI inference tiers (Gemini, Groq, Cerebras, OpenRouter, Mistral) with auto-fallback cascades and rate-limit evasion.
- **Entry Points**:
  - integrations/omniroute/SKILL.md: Architecture specification and setup instructions.
  - integrations/omniroute/omniroute_client.py: Python client and failover gateway runner.
  - integrations/omniroute/providers_config.json: Tier catalog and fallback model chains.
