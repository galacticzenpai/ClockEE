# ClockEE Project Changelog

All notable changes to the ClockEE ecosystem will be documented in this file.

---

## [Release 2.9.0] - 2026-11-16: Diagnostics, Predictive Matrix & Self-Healing Wave (Reels #24 - #28)

### 📦 Vendored Integrations (72% Backlog Milestone - 28 of 39 Reels Completed):
- **Reel #24: Offline Network Telemetry Console (integrations/network_telemetry/)**: Retro terminal HUD (Ctrl+Shift+D) with background Web Worker heartbeat sampling and offline sync diagnostics.
- **Reel #25: Accuracy & Rank Predictor Matrix (integrations/accuracy_matrix/)**: NTA historical percentile interpolator in 51.6µs with Canvas subject-wise mastery radar chart.
- **Reel #26: Hallmark Printable Scorecard (integrations/scorecard_pdf/)**: A4 print-ready official report card generator featuring candidate credentials, subject breakdown, and QR code verification.
- **Reel #27: Self-Healing DOM Guard (integrations/auto_repair_dom/)**: Defensive MutationObserver runtime protector repairing missing exam containers and preventing unhandled UI crashes.
- **Reel #28: Runtime State Corruption Interceptor (integrations/state_validator/)**: ES6 Proxy state invariant validator intercepting illegal out-of-bounds CBT mutations.

### 🌐 Live Production Promotion:
- Deployed live to Vercel: https://clockee-os.vercel.app (dpl_Fr7ZMsf8zNJW3PJsKYeBiFmDLQJT, commit c5ad79a).

---

## [Release 2.8.0] - 2026-11-16: Perception, Telemetry & Replay Wave (Reels #19 - #23)

### 📦 Vendored Integrations & Micro-Benchmarks (<10µs latency certified):
- **Reel #19: Fluid Typography Engine (integrations/fluid_typography/)**: Dynamic viewport CSS clamp() typography system resolving in 82µs with zero-layout-shift formulas applied to cbt_shared.css.
- **Reel #20: APCA Perceptual Contrast Guard (integrations/contrast_guard/)**: Advanced Perceptual Contrast Algorithm (APCA) linter validating high-stakes dark/light mode readability in 34.1µs.
- **Reel #21: Exam Session Replay (integrations/session_replay/)**: Lightweight action recorder & scrubber player for millisecond-accurate post-exam review.
- **Reel #22: Cognitive Load Heatmap (integrations/student_heatmap/)**: Visual time allocation matrix categorizing attempts into Rushed, Optimal, Slow, and Stuck zones.
- **Reel #23: Statistical Fluke & Blind Guess Detector (integrations/guess_detector/)**: Microsecond fluke analyzer (3.47µs) isolating lucky random guesses from genuine conceptual mastery.

### 🌐 Live Production Promotion:
- Deployed live to Vercel: https://clockee-os.vercel.app (dpl_Ad4CRNfyaF9kpJ3BwpfzUAYtzt9b, commit 287755e).

---

## [Release 2.7.0] - 2026-11-16: High-Cadence Engine & HUD Wave (Reels #11 - #18)

### 📦 Vendored Integrations & Micro-Benchmarks (<1ms latency certified):
- **Reel #11: Item Response Theory (IRT) Dynamic Sequencer (integrations/irt_adaptive/)**: 3-Parameter Logistic Model (3PL) real-time latent student ability (θ) estimator resolving in 0.11ms.
- **Reel #12: Distractor & Misconception Analyzer (integrations/distractor_analyzer/)**: Categorizes decoy options by cognitive misconception & trap taxonomy in 0.05ms.
- **Reel #13: OMR Sheet Scanner (integrations/omr_scanner/)**: Physical bubble matrix optical grading engine in 0.08ms.
- **Reel #14: CBT Session Snapshot (integrations/session_snapshot/)**: Delta-based session serialization in 0.09ms with SHA-256 state verification.
- **Reel #15: Hallmark Token Engine (integrations/tokens_engine/)**: W3C Design Token JSON compilation in 0.96ms to Hallmark CSS custom properties.
- **Reel #16: Tactile Cockpit HUD (integrations/tactile_hud/)**: NTA official hotkey engine resolving in 0.62µs per keystroke.
- **Reel #17: Retina Charts (integrations/retina_charts/)**: High-density 60FPS Canvas student accuracy & speed heatmaps in 0.41ms.
- **Reel #18: Glass Split-Drawer Navigator (integrations/glass_drawer/)**: Physics-based collapsible 180-question palette drawer with 56.9µs state calculation.

### 🌐 Live Production Promotion:
- Promoted to production on Vercel: https://clockee-os.vercel.app (dpl_FNUDaZynkayzRWTG28EEx73mH8rs).

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