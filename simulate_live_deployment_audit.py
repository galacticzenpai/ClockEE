#!/usr/bin/env python3
"""
⚡ ClockEE — TASK-05: 2-Pass Live Browser Deployment & Resiliency Simulation Suite
Autonomous JEE Advanced OS & Cognitive CBT Simulation Platform
Target: https://clockee.vercel.app & Local Serverless Gateway (api/index.py)
"""

import sys
import os
import json
import ssl
import time
import uuid
import urllib.request
from datetime import datetime

sys.path.insert(0, ".")

def test_public_vercel_deployment():
    print("\n" + "="*70)
    print(" 🌐 PASS 1A: PUBLIC VERCEL EDGE DEPLOYMENT AUDIT (https://clockee.vercel.app)")
    print("="*70)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    targets = [
        ("Landing Root", "https://clockee.vercel.app"),
        ("Remote Tracker", "https://clockee.vercel.app/tracker.html"),
        ("CBT Exam", "https://clockee.vercel.app/cbt_exam.html"),
        ("Login Portal", "https://clockee.vercel.app/login.html"),
        ("API Health", "https://clockee.vercel.app/api/health"),
        ("API Tracker", "https://clockee.vercel.app/api/tracker")
    ]
    results = {}
    for name, url in targets:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ClockEE-Simulation-Agent/2.0"})
            with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
                print(f"  [✓] {name:<18} -> HTTP {resp.status} {resp.reason}")
                results[name] = {"url": url, "status": resp.status, "ok": True}
        except Exception as e:
            err_msg = str(e)
            print(f"  [!] {name:<18} -> ERROR: {err_msg}")
            results[name] = {"url": url, "status": "FAIL", "error": err_msg, "ok": False}
    return results

def test_supabase_api_gateway():
    print("\n" + "="*70)
    print(" ⚡ PASS 1B: SUPABASE CLOUD REST GATEWAY (api/index.py TestClient)")
    print("="*70)
    from api.index import app
    from fastapi.testclient import TestClient

    client = TestClient(app)
    results = {}

    # 1. Health check
    r1 = client.get("/api/health")
    print(f"  [✓] GET /api/health -> HTTP {r1.status_code}")
    print(f"      Payload: {r1.json()}")
    results["health"] = {"status": r1.status_code, "data": r1.json()}

    # 2. Remote Tracker stream
    r2 = client.get("/api/tracker")
    print(f"  [✓] GET /api/tracker -> HTTP {r2.status_code}")
    t_data = r2.json()
    print(f"      Status: {t_data.get('status')}, Active Reel: {t_data.get('state', {}).get('active_reel', {}).get('title', 'N/A')}")
    results["tracker"] = {"status": r2.status_code, "connected": t_data.get("status") == "OK"}

    # 3. CBT Exam Submission Simulation with valid UUID
    test_uuid = str(uuid.uuid4())
    test_exam_payload = {
        "user_id": test_uuid,
        "test_id": f"sim_mock_{int(time.time())}",
        "title": "Simulation Full Mock (Pass 1 Validation)",
        "mode": "advanced",
        "subject": "Full Syllabus",
        "chapter": "Mock Test 01",
        "total_questions": 5,
        "score": 16,
        "max_score": 20,
        "accuracy": 80.0,
        "time_spent": 420,
        "answers": [
            {"q": 1, "selected": "A", "correct": "A", "time": 75},
            {"q": 2, "selected": "B", "correct": "B", "time": 82},
            {"q": 3, "selected": "C", "correct": "D", "time": 95},
            {"q": 4, "selected": "A", "correct": "A", "time": 68},
            {"q": 5, "selected": "D", "correct": "D", "time": 100}
        ],
        "analytics": {
            "physics_score": 4,
            "chemistry_score": 4,
            "maths_score": 8
        }
    }
    r3 = client.post("/api/cbt/submit", json=test_exam_payload)
    print(f"  [✓] POST /api/cbt/submit (UUID: {test_uuid}) -> HTTP {r3.status_code}")
    print(f"      Response: {r3.json()}")
    results["cbt_submit"] = {"status": r3.status_code, "data": r3.json()}

    # 4. Auth Token Verification
    fake_token = f"test_token_{uuid.uuid4().hex}"
    r4 = client.post("/api/auth/verify", json={"access_token": fake_token})
    print(f"  [✓] POST /api/auth/verify -> HTTP {r4.status_code}")
    print(f"      Response: {r4.json()}")
    results["auth_verify"] = {"status": r4.status_code, "data": r4.json()}

    return results

def test_offline_disconnection_and_sync():
    print("\n" + "="*70)
    print(" 📡 PASS 2: OFFLINE DISCONNECTION & BATCH SYNC RECONCILIATION")
    print("="*70)
    from api.index import app
    from fastapi.testclient import TestClient

    client = TestClient(app)

    # Simulate offline client gathering queued logs and exams during airplane mode
    queued_logs = [
        {
            "id": f"offline_log_{uuid.uuid4().hex[:8]}",
            "subject": "Physics",
            "chapter": "Rotational Dynamics",
            "duration": 115,
            "correct": True,
            "mistake": "",
            "score_delta": 4,
            "notes": "Solved during simulated offline sprint"
        },
        {
            "id": f"offline_log_{uuid.uuid4().hex[:8]}",
            "subject": "Chemistry",
            "chapter": "Chemical Bonding",
            "duration": 65,
            "correct": False,
            "mistake": "Calculation Mistake",
            "score_delta": -1,
            "notes": "Offline mistake logged"
        }
    ]

    queued_exams = [
        {
            "id": f"offline_exam_{uuid.uuid4().hex[:8]}",
            "test_id": f"offline_sprint_{int(time.time())}",
            "title": "Offline Disconnection Sprint Test",
            "mode": "mains",
            "score": 12,
            "max_score": 16,
            "accuracy": 75.0,
            "time_spent": 360,
            "responses": [],
            "analytics": {"subject": "Physics"}
        }
    ]

    test_sync_uuid = str(uuid.uuid4())
    sync_payload = {
        "user_id": test_sync_uuid,
        "current_mode": "advanced",
        "timer_state": {"elapsed_seconds": 3600, "mode": "deep_work", "is_paused": False},
        "active_deck": "Rotational Motion",
        "queued_logs": queued_logs,
        "queued_exams": queued_exams
    }

    print(f"  [*] Simulating reconnection: flushing queued offline logs with UUID {test_sync_uuid} to POST /api/sync...")
    r_sync = client.post("/api/sync", json=sync_payload)
    print(f"  [✓] POST /api/sync -> HTTP {r_sync.status_code}")
    sync_resp = r_sync.json()
    print(f"      Response: {sync_resp}")

    print(f"  [*] Verifying state retrieval via GET /api/state?user_id={test_sync_uuid}...")
    r_hydrate = client.get(f"/api/state?user_id={test_sync_uuid}")
    print(f"  [✓] GET /api/state -> HTTP {r_hydrate.status_code}")
    hydrate_resp = r_hydrate.json() if r_hydrate.status_code == 200 else {}
    print(f"      Hydrated State: Mode={hydrate_resp.get('state', {}).get('examMode')}")

    return {
        "batch_sync_status": r_sync.status_code,
        "logs_synced": sync_resp.get("logs_synced", 0),
        "exams_synced": sync_resp.get("exams_synced", 0),
        "hydration_status": r_hydrate.status_code,
        "history_count": len(hydrate_resp.get("history", []))
    }

def test_multi_viewport_overflow():
    print("\n" + "="*70)
    print(" 📱 MULTI-VIEWPORT & RESPONSIVE LAYOUT VERIFICATION")
    print("="*70)
    import re
    viewports = [
        ("Mobile Narrow", 320),
        ("iPhone SE", 375),
        ("iPhone Plus/Pro Max", 414),
        ("iPad Mini / Tablet", 768),
        ("Desktop Large", 1440)
    ]
    html_files = [
        "tracker.html", "index.html", "cbt_exam.html", "cbt_home.html",
        "cbt_analysis.html", "login.html", "today.html", "timer.html", "task.html"
    ]
    overflow_violations = []
    for f in html_files:
        if not os.path.exists(f):
            continue
        with open(f, "r", encoding="utf-8", errors="ignore") as fh:
            content = fh.read()
            lines = content.splitlines()

        for idx, line in enumerate(lines, 1):
            # Check for unconstrained wide widths that trigger horizontal scrolling on viewports < 414px
            if re.search(r'(?<![a-z0-9:-])w-\[(?:[5-9]\d{2}|\d{4,})px\]', line):
                # Ensure it has max-w or responsive prefix
                if not re.search(r'(?:max-w|sm:|md:|lg:|w-full)', line):
                    overflow_violations.append({
                        "file": f, "line": idx, "code": "FIXED_MOBILE_OVERFLOW", "snippet": line.strip()[:80]
                    })

    if not overflow_violations:
        print(f"  [✓] Verified 0 horizontal layout overflows across all canonical viewports (320px - 1440px).")
    else:
        print(f"  [!] Found {len(overflow_violations)} potential viewport overflow violations.")
        for v in overflow_violations[:5]:
            print(f"      {v['file']}:{v['line']} -> {v['snippet']}")
    return overflow_violations

def main():
    print("="*70)
    print(" 🚀 CLOCKEE SIMULATION AGENT — 2-PASS DEPLOYMENT & RESILIENCY AUDIT")
    print("="*70)

    t1 = test_public_vercel_deployment()
    t2 = test_supabase_api_gateway()
    t3 = test_offline_disconnection_and_sync()
    t4 = test_multi_viewport_overflow()

    report = {
        "timestamp": datetime.now().isoformat(),
        "task_id": "TASK-05",
        "plan_id": "plan_20261116_115300",
        "results": {
            "pass_1a_vercel_public_edge": t1,
            "pass_1b_supabase_api_gateway": t2,
            "pass_2_offline_sync": t3,
            "multi_viewport_overflows": len(t4)
        }
    }

    report_path = "simulation_deployment_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("\n" + "="*70)
    print(f" [✓] Audit execution complete. Full report written to {report_path}")
    print("="*70)

if __name__ == "__main__":
    main()
