---
name: dray-cross-context
description: Multi-model session bridge and state handoff protocol adapted from Dray (withdray.com). Synchronizes active conversation state, context memory, and task checkpoints across Claude, ChatGPT, Gemini, and local coding agents via a standardized /link snapshot protocol.
---

# Dray: Cross-Model Context Bridge & Session Handoff for ClockEE

Adapted from **Dray** ([`withdray.com`](https://withdray.com)).

## Overview
When an AI assistant (Claude Code, ChatGPT, Gemini, or a specialized subagent) hits a rate limit, runs out of context tokens, or needs to hand off a partially completed feature, traditional workflows force the developer to re-explain the entire repository architecture and recent progress from scratch.

Dray solves this with the **/link snapshot protocol**:
1. **Context Snapshotting (`/link`)**: Captures the active file context, last execution error, pending tasks, and recent git diff into a compact, model-agnostic session token.
2. **Cross-Model Handoff**: A second model (e.g., ChatGPT or Gemini resuming after Claude hits a quota threshold) ingests the link snapshot and immediately resumes work without hallucinations.
3. **Task Boundary Preservation**: Preserves untouched payment boundaries, database credentials, and security rules across handoffs.

---

## Core Usage Commands

### 1. Create a Cross-Model Handoff Snapshot
```powershell
python integrations/dray_cross_context/dray_bridge.py link --task "Refactor CBT Timer"
```

### 2. Resume / Ingest a Link in Another Agent
```powershell
python integrations/dray_cross_context/dray_bridge.py resume <snapshot_token_or_file>
```

### 3. Inspect Active Bridge Sessions
```powershell
python integrations/dray_cross_context/dray_bridge.py status
```
