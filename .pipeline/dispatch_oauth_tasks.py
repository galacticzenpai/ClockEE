#!/usr/bin/env python3
"""
⚡ ClockEE — Google & GitHub OAuth Multi-Agent Task Dispatcher
Dispatches specialized prompts to DB / BACKEND, Main Feature, SIMULATION, and GITHUB
conversations via agentapi CLI.
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

PIPELINE_DIR = Path(__file__).resolve().parent
AGENTAPI_BIN = r"C:\Users\Kunal\.gemini\antigravity\bin\agentapi.bat"

TARGETS = {
    "db_backend": {
        "name": "DB / BACKEND",
        "id": "d3700ff3-1bfb-458a-9968-8257ef2ca7e2",
        "title": "⚡ ClockEE [TASK-AUTH-01]: Backend Google & GitHub OAuth Verification & Supabase Sync",
        "prompt": """[CLOCKEE AUTONOMOUS TASK HANDOFF: GOOGLE & GITHUB OAUTH BACKEND HARDENING]
Target Conversation: DB / BACKEND
Production Edge: https://clockee-os.vercel.app

### Current Status:
1. Endpoints Deployed to Live Vercel Production & Local Gateway:
   - `GET /api/auth/providers`
   - `POST /api/auth/google` (Accepts uid, email, name, pfp; verifies and syncs to Supabase `profiles`)
   - `POST /api/auth/github` (Accepts id, username, email, avatar_url; verifies and syncs to Supabase `profiles`)
   - `POST /api/auth/session` (Accepts session heartbeat and token verification)
2. Database: Supabase Cloud `qvrfakbhnsmknukaqmja`
   - Trigger `on_auth_user_created` provisions `profiles` and `student_states`.
   - Deduplication by email implemented to avoid `profiles_email_key` unique violations.

### Your Assignment:
1. Inspect `api/index.py` around lines 530-630 for OAuth handling.
2. Review token exchange and session verification logic.
3. Verify that all profile mutations in Supabase preserve JEE aspirant metrics (e.g. `role`, `theme_preference`, `aura_mode`, `last_seen`).
4. Output your status report confirming backend readiness.
"""
    },
    "main_feature": {
        "name": "Main Feature (Untitled)",
        "id": "6371cba6-7d2f-4b29-a250-627d88d1b4f1",
        "title": "⚡ ClockEE [TASK-AUTH-02]: Client Session Flow for Google & GitHub Login",
        "prompt": """[CLOCKEE AUTONOMOUS TASK HANDOFF: OAUTH CLIENT INTEGRATION]
Target Conversation: Main Feature (Untitled)
Production Edge: https://clockee-os.vercel.app

### Current Status:
1. UI Elements Added to `login.html`:
   - `#btnGoogleLogin`: Google Cloud Identity 1-click button calling `window.handleGoogleSignIn()`
   - `#btnGithubLogin`: GitHub 1-click button calling `window.handleGithubSignIn()`
2. Both functions perform provider authentication with resilient fallback and post to `/api/auth/google` and `/api/auth/github`.
3. Session state is stored in `localStorage['clockee_current_user']` and `localStorage['clockee_auth_active']`.

### Your Assignment:
1. Ensure all downstream pages (`tracker.html`, `cbt_exam.html`, `hallmark_design.html`) properly read `localStorage['clockee_current_user']`.
2. Verify that the user's avatar (`pfp`) and display name appear in top navigation bars upon logging in via Google or GitHub.
3. Test guest sandbox transition to authenticated cloud user.
4. Output your verification report confirming client session continuity.
"""
    },
    "simulation": {
        "name": "SIMULATION",
        "id": "62adc180-be21-4671-848c-c8df59e2c202",
        "title": "⚡ ClockEE [TASK-AUTH-03]: OAuth Simulation Suite Ingestion & Regression Verification",
        "prompt": """[CLOCKEE AUTONOMOUS TASK HANDOFF: OAUTH SIMULATION VERIFICATION]
Target Conversation: SIMULATION
Production Edge: https://clockee-os.vercel.app

### Current Status:
1. Simulation Suite `.pipeline/simulate_oauth_suite.py` has been built and executed.
2. 2-Pass Audit Results:
   - PASS 1 (Local Gateway): Providers 200 OK, Google Login 200 OK, GitHub Login 200 OK, Session Heartbeat 200 OK.
   - PASS 2 (Live Vercel Edge): `login.html` markup has both buttons, endpoints returning 200 OK with live Supabase Cloud writes.
3. Report saved at `.pipeline/oauth_simulation_report.json`.

### Your Assignment:
1. Review `.pipeline/simulate_oauth_suite.py` and `.pipeline/oauth_simulation_report.json`.
2. Incorporate this test suite into the master automated regression pipeline.
3. Run continuous health checks against `https://clockee-os.vercel.app/api/auth/providers`.
4. Output your simulation audit report.
"""
    },
    "github": {
        "name": "GITHUB",
        "id": "a64c937f-bb58-4071-8eb9-32f5edbb6c2c",
        "title": "⚡ ClockEE [TASK-AUTH-04]: Git Sync & OAuth Feature Documentation",
        "prompt": """[CLOCKEE AUTONOMOUS TASK HANDOFF: GIT SYNC & CHANGELOG]
Target Conversation: GITHUB
Repository: galacticzenpai/ClockEE

### Current Status:
1. Latest commit `e75d5bc` pushed to `origin/main`.
2. Features added:
   - Full Google & GitHub OAuth backend in `api/index.py`
   - Cockpit 1-click buttons and handlers in `login.html`
   - Automated 2-pass simulation suite `.pipeline/simulate_oauth_suite.py`
   - Successful production deployment to `https://clockee-os.vercel.app`

### Your Assignment:
1. Pull the latest `origin/main` changes.
2. Update the repository CHANGELOG / README with the new OAuth capabilities and live endpoints.
3. Confirm git status clean on your end.
"""
    }
}

def record_transmission(source, target, subject, status="DELIVERED_AUTO"):
    tx_file = PIPELINE_DIR / "transmissions.json"
    txs = []
    if tx_file.is_file():
        try:
            with open(tx_file, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                if isinstance(loaded, list):
                    txs = loaded
                elif isinstance(loaded, dict) and "transmissions" in loaded:
                    txs = loaded["transmissions"]
        except Exception:
            txs = []

    txs.insert(0, {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": source,
        "target": target,
        "subject": subject,
        "status": status
    })
    try:
        with open(tx_file, "w", encoding="utf-8") as f:
            json.dump(txs[:100], f, indent=2)
    except Exception as e:
        print(f"Error saving transmission: {e}")

def main():
    print("=" * 70)
    print(" 🚀 DISPATCHING GOOGLE & GITHUB OAUTH TASKS TO CLOCKEE MESH")
    print(f" Timestamp: {datetime.now().isoformat()}")
    print("=" * 70)

    for key, item in TARGETS.items():
        name = item["name"]
        cid = item["id"]
        title = item["title"]
        prompt = item["prompt"]

        print(f"\n📡 Sending dispatch to {name} ({cid})...")
        try:
            cmd = [
                AGENTAPI_BIN,
                "send-message",
                f"--title={title}",
                cid,
                prompt
            ]
            subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=False
            )
            print(f"   [✓] Dispatched successfully: {title}")
            record_transmission(
                source="BACKBONE COORDINATOR",
                target=name,
                subject=title,
                status="DELIVERED_AUTO"
            )
        except Exception as e:
            print(f"   [!] Failed dispatching to {name}: {e}")

    print("\n" + "=" * 70)
    print(" ✨ All OAuth development tasks dispatched across the mesh!")
    print("=" * 70)

if __name__ == "__main__":
    main()
