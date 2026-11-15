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
