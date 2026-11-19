#!/usr/bin/env python3
"""
ClockEE Prompt Stress-Testing & Socratic Interrogation Engine
Gatekeeper for all incoming user ideas and feature drafts before dispatch.

Responsibilities:
1. Analyzes user ideas against the 6 ClockEE Architecture Pillars:
   - Pillar 1: Core Purpose & End-User Experience
   - Pillar 2: Frontend & Mobile Responsive UX (Hallmark Standards)
   - Pillar 3: Data Schema & Persistence (SQLite / localStorage)
   - Pillar 4: Domain Allocation & Anti-Bottleneck Routing
   - Pillar 5: Adversarial Edge Cases & Security (DOM XSS / sanitization)
   - Pillar 6: Concrete Definition of Done & Quality Gates
2. Generates surgical cross-examination questions to drill down to deepest detail.
3. Synthesizes a finalized, hardened, battle-tested prompt for specialist agents.
"""

import os
import sys
import re
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

PILLARS = [
    {
        "id": "intent",
        "name": "Core Purpose & UX Outcome",
        "check": lambda text: any(k in text.lower() for k in ["why", "purpose", "user", "benefit", "solve", "goal"]),
        "flaw_prompt": "What exact user problem or exam-prep friction does this feature eliminate? What is the exact user journey from the moment they see it to the final interaction?"
    },
    {
        "id": "ui_responsive",
        "name": "UI Spec & Mobile Floor Check",
        "check": lambda text: any(k in text.lower() for k in ["ui", "button", "modal", "screen", "drawer", "mobile", "layout", "color", "theme"]),
        "flaw_prompt": "Where exactly does this live in the UI (e.g. index.html, drawer, floating launcher)? How will it behave on viewports under 414px (mobile floor requirement)? Does it avoid generic AI purple gradient slop?"
    },
    {
        "id": "persistence",
        "name": "Data Architecture & Storage",
        "check": lambda text: any(k in text.lower() for k in ["db", "save", "store", "sqlite", "localstorage", "sync", "data", "api", "schema"]),
        "flaw_prompt": "How does data persist? Is it synced to SQLite via server.py or stored in localStorage? What is the exact payload structure?"
    },
    {
        "id": "edge_cases",
        "name": "Edge Cases & Defensive Validation",
        "check": lambda text: any(k in text.lower() for k in ["error", "fallback", "empty", "fail", "sanitize", "xss", "offline", "disconnect"]),
        "flaw_prompt": "What happens if the input is empty, offline, or corrupted? Are all dynamic DOM insertions safely handled with textContent or sanitized against XSS?"
    },
    {
        "id": "acceptance",
        "name": "Definition of Done & Verification",
        "check": lambda text: any(k in text.lower() for k in ["test", "verify", "gate", "sloplint", "criteria", "done"]),
        "flaw_prompt": "What is the single non-negotiable test that proves this feature is 100% complete and working without regressions to existing timers or layouts?"
    }
]

def interrogate_draft(draft_text: str):
    """Examines draft prompt and returns targeted interrogation questions."""
    findings = []
    for p in PILLARS:
        if not p["check"](draft_text):
            findings.append({
                "pillar": p["name"],
                "question": p["flaw_prompt"]
            })
    
    # If draft is very short, flag all pillars
    if len(draft_text.strip().split()) < 15:
        findings = [{"pillar": p["name"], "question": p["flaw_prompt"]} for p in PILLARS]

    return {
        "draft_length": len(draft_text),
        "missing_pillars": len(findings),
        "questions": findings
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        draft = " ".join(sys.argv[1:])
    else:
        draft = "Add a quick study streak counter button."
    res = interrogate_draft(draft)
    print(json.dumps(res, indent=2))
