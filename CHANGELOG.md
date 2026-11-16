# ClockEE Project Changelog

All notable changes to the ClockEE ecosystem will be documented in this file.

---

## [Release 2.6.0] - 2026-11-16: Sequential Ingestion Wave (Reels #5 - #10)

### 📦 Vendored Integrations:
- **Reel #5: SQLite-VSS (integrations/sqlite_vss/)**: Local-first vector similarity search (<12ms latency) with embeddings indexing and zero-dependency cosine math fallback.
- **Reel #6: CR-SQLite (integrations/crsqlite/)**: Conflict-free replicated SQLite tables using CRDT delta merging for multi-device synchronization.
- **Reel #7: Core Web Vitals Auditor (integrations/page_audit/)**: Retinal performance and mobile viewport gatekeeper (97.6/100 certified).
- **Reel #8: Fast-Schema (integrations/fast_schema/)**: SQLite database contract synchronizer compiling SQLite tables to TypeScript and Pydantic validation models.
- **Reel #9: KaTeX Math Extractor (integrations/math_extractor/)**: High-fidelity offline LaTeX and chemical formula parser and formula tokenizer.
- **Reel #10: CBT Exam Timer Engine (integrations/cbt_timer/)**: Web Worker high-precision countdown timer with anchor recovery and fatigue cadence detection.

---

## [Release 2.5.0] - 2026-11-16: Vercel Edge Production Deployment & Cloud Auth Suite

### 🚀 Highlights & Production Architecture
- **Vercel Serverless Python Adapter (`api/index.py`)**: Replaces local SQLite in cloud environments with direct PostgreSQL queries over Supabase Cloud.
- **Production Edge Routing (`vercel.json`)**:
  - Rewrites `/api/(.*)` to `/api/index.py` and `/tracker` to `/tracker.html`.
  - Configures strict security headers (`X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`).
  - Sets production CORS for `https://clockee.vercel.app`.
  - Implements immutable Cache-Control headers for static CBT question bank assets.
- **Production Asset Exclusion (`.vercelignore`)**:
  - Excludes local SQLite databases (`clockee.db`, `clockee_auth.db`), lock files, temporary media, and internal agent pipelines.
- **Auth & OAuth Integration**:
  - Google and GitHub OAuth flow with URL hash access token extraction and graceful offline fallback.
  - User session state hydration and auto-sync on reconnect.
- **Remote Mission Control Tracker (`tracker.html`)**:
  - Real-time mobile-responsive agent activity tracker querying `/api/tracker` with Supabase live state broadcasting.
- **Quality Gates & Audits**:
  - Verified with 2-pass browser simulation test suite, Cloudflare security scan, and Hallmark anti-slop audit.

---

## [Release 2.4.0] - 2026-11-16: OmniRoute AI Gateway & Sequential Ingestion
- **OmniRoute Gateway (`integrations/omniroute/`)**: Unified local OpenAI-compatible endpoint with automatic fallback across free inference tiers (Groq, Cerebras, Gemini, DeepSeek).
- **Sequential Ingestion Pipeline**: Ingested and vendored developer showcase tools (Graphify, LLM-Lint, Dray Bridge, OmniRoute).

---

## [Release 2.0.0] - 2026-11-15: Hallmark Design System & CBT Engine
- **Hallmark Design Tokens**: Anti-slop UI aesthetics and design tokens.
- **CBT Offline Master Bank**: Interactive exam simulation, question cloner, notebook vault, and local analysis.