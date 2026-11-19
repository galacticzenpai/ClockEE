---
name: dray-cross-model-bridge
description: Cross-model context handoff and rate-limit continuity bridge adapted from Dray (drayhq.com / monorepo-labs/dray). Enables seamless state handoffs between Claude, ChatGPT, Gemini, and DeepSeek via structured snapshot files and a `/link` CLI command.
---

# Dray: Cross-Model Context Handoff & Session Bridge for ClockEE

Adapted from the architecture of **Dray** ([`drayhq.com`](https://drayhq.com) / [`monorepo-labs/dray`](https://github.com/monorepo-labs/dray)).

## Overview
When an AI coding assistant (like Claude) hits its usage cap, rate limit, or 5-hour session reset halfway through an implementation task, work stalls. Handing off to another model (like ChatGPT or Gemini) manually causes hallucinated refactors, forgotten architectural decisions, and broken endpoints.

Dray's **`/link`** mechanism solves this by capturing:
1. **Active Task Context**: Goal, current step, finished steps, and remaining steps.
2. **Architectural Guardrails**: Files touched, files that must NOT be touched (e.g. payment/auth endpoints), and active coding guidelines.
3. **Structured Snapshot**: Exports a clean, standardized `dray_context.md` snapshot that the receiving model ingests to resume work instantly without context degradation.

---

## The Core Command Set

### 1. Capture Session State & Freeze Context
```powershell
python integrations/dray_cross_model/dray_bridge.py capture --task "CBT Exam Timer Refactor" --step 2 --guardrails "Do not touch cbt_master_bank.js"
```

### 2. Generate `/link` Handoff Payload for Receiving Model
```powershell
python integrations/dray_cross_model/dray_bridge.py link
```

### 3. Verify Resumed Session Consistency
```powershell
python integrations/dray_cross_model/dray_bridge.py verify
```
