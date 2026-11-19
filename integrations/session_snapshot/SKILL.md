---
name: cbt-session-snapshot
description: Delta-based exam session serialization engine with crash resilience, IndexedDB persistence, and sub-5ms state synchronization.
---

# Instantaneous CBT Exam Session Serialization

Reel: #14 (https://www.instagram.com/p/DdBSahaKHsY/)
Package: `integrations/session_snapshot/`

## Overview
Ensures zero data loss during high-stakes CBT exams. Writes state deltas (current question, answers, review bookmarks, remaining seconds) to IndexedDB with debounced 500ms cadence, and supports instant JSON snapshot recovery.

## Features
- **Delta Compression**: Only records changes to active attempt state, reducing storage write amplification.
- **Atomic Rollback**: Checksum verification ensures corrupt or incomplete snapshots are discarded in favor of last-known valid state.
- **Cross-Tab Broadcast**: Notifies secondary tabs or background workers via BroadcastChannel to avoid concurrent split-brain state.
