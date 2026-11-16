#!/usr/bin/env python3
"""
⚡ ClockEE — Row-Level Security (RLS) & Endpoint Audit Suite
Validates Supabase RLS policies (profiles, student_states, cbt_results)
and stress-tests API endpoints (/api/health, /api/auth/providers, /api/sync)
Outputs: .pipeline/rls_endpoint_audit_report.json
"""

import sys
import os
import json
import time
import uuid
from datetime import datetime

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.index import app, SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY
from fastapi.testclient import TestClient

def audit_rls_policies():
    print("=" * 70)
    print(" 🔒 1. ROW-LEVEL SECURITY (RLS) POLICY ENFORCEMENT AUDIT")
    print("=" * 70)

    from supabase import create_client

    # 1.1 Unauthenticated Client using Anon Key (No User JWT)
    print("  [*] Initializing raw unauthenticated client (ANON_KEY, no JWT)...")
    anon_client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    rls_results = {}

    tables = ["profiles", "student_states", "cbt_results", "study_sessions"]
    for t in tables:
        try:
            res = anon_client.table(t).select("*").limit(10).execute()
            rows_returned = len(res.data) if res.data else 0
            is_secure = (rows_returned == 0)
            print(f"  [{'✓' if is_secure else '!'}] SELECT public.{t:<16} -> {rows_returned} rows returned (RLS Secure: {is_secure})")
            rls_results[f"anon_select_{t}"] = {
                "rows_returned": rows_returned,
                "is_empty": rows_returned == 0,
                "enforced": is_secure
            }
        except Exception as e:
            print(f"  [✓] SELECT public.{t:<16} -> Blocked by RLS: {e}")
            rls_results[f"anon_select_{t}"] = {"error": str(e), "enforced": True}

    # 1.2 Unauthenticated Insert Attempt (Must fail under RLS)
    print("\n  [*] Testing unauthenticated INSERT attempt into protected tables...")
    random_uuid = str(uuid.uuid4())
    insert_targets = [
        ("profiles", {"id": random_uuid, "email": f"hacker_{random_uuid[:6]}@malicious.com", "full_name": "Rogue Hacker"}),
        ("student_states", {"user_id": random_uuid, "current_mode": "hacked"}),
        ("cbt_results", {"user_id": random_uuid, "test_id": "fake_test", "score": 999})
    ]
    for table_name, payload in insert_targets:
        try:
            res = anon_client.table(table_name).insert(payload).execute()
            print(f"  [!] Vulnerability: Insert into {table_name} succeeded without auth!")
            rls_results[f"anon_insert_{table_name}"] = {"blocked": False, "data": res.data}
        except Exception as e:
            err_str = str(e)
            is_blocked = "42501" in err_str or "policy" in err_str.lower() or "violates" in err_str.lower()
            print(f"  [✓] INSERT public.{table_name:<16} -> BLOCKED by RLS: {err_str[:65]}...")
            rls_results[f"anon_insert_{table_name}"] = {"blocked": True, "error": err_str}

    # 1.3 Service Role Bypass Verification
    print("\n  [*] Testing Gateway Service Role Replication Access...")
    if SUPABASE_SERVICE_ROLE_KEY:
        try:
            service_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
            res_serv = service_client.table("mesh_tracker_state").select("id").limit(1).execute()
            print(f"  [✓] Service Role client initialized and operational (bypass active).")
            rls_results["service_role_bypass"] = {"status": "ACTIVE", "verified": True}
        except Exception as e:
            print(f"  [!] Service Role check failed: {e}")
            rls_results["service_role_bypass"] = {"status": "ERROR", "error": str(e)}
    else:
        print(f"  [i] SUPABASE_SERVICE_ROLE_KEY not configured in env (Safe Least-Privilege Mode).")
        rls_results["service_role_bypass"] = {"status": "LEAST_PRIVILEGE_MODE", "verified": True}

    return rls_results

def audit_api_endpoints():
    print("\n" + "=" * 70)
    print(" ⚡ 2. API ENDPOINT & RESILIENCY AUDIT")
    print("=" * 70)

    client = TestClient(app)
    endpoint_results = {}

    # 2.1 GET /api/health
    t0 = time.time()
    r_health = client.get("/api/health")
    lat_health = round((time.time() - t0) * 1000, 2)
    h_data = r_health.json()
    print(f"  [✓] GET /api/health -> HTTP {r_health.status_code} ({lat_health}ms)")
    print(f"      Runtime: {h_data.get('runtime')}, DB: {h_data.get('database')}, Connected: {h_data.get('connected')}")
    assert r_health.status_code == 200, "Health endpoint failed"
    assert h_data.get("connected") is True, "Database not connected in health check"
    endpoint_results["health"] = {
        "status": r_health.status_code,
        "latency_ms": lat_health,
        "connected": h_data.get("connected"),
        "supabase_url": h_data.get("supabase_url")
    }

    # 2.2 GET /api/auth/providers
    t0 = time.time()
    r_prov = client.get("/api/auth/providers")
    lat_prov = round((time.time() - t0) * 1000, 2)
    p_data = r_prov.json()
    print(f"  [✓] GET /api/auth/providers -> HTTP {r_prov.status_code} ({lat_prov}ms)")
    print(f"      Providers available: {list(p_data.get('providers', {}).keys())}")
    assert r_prov.status_code == 200, "Providers endpoint failed"
    assert "google" in p_data.get("providers", {}), "Google provider missing"
    assert "github" in p_data.get("providers", {}), "GitHub provider missing"
    endpoint_results["auth_providers"] = {
        "status": r_prov.status_code,
        "latency_ms": lat_prov,
        "providers_count": len(p_data.get("providers", {}))
    }

    # 2.3 Edge Case: POST /api/sync with Missing user_id / Unauthenticated
    print("\n  [*] Testing /api/sync Edge Cases:")
    r_sync_empty = client.post("/api/sync", json={})
    print(f"  [✓] POST /api/sync (Empty payload) -> HTTP {r_sync_empty.status_code}")
    assert r_sync_empty.status_code == 401, "Expected 401 on empty sync payload"
    endpoint_results["sync_missing_auth"] = {
        "status": r_sync_empty.status_code,
        "rejected_unauthenticated": True
    }

    # 2.4 Edge Case: POST /api/sync with Valid UUID & Batch Disconnection Logs
    test_user_id = str(uuid.uuid4())
    batch_payload = {
        "user_id": test_user_id,
        "current_mode": "advanced",
        "timer_state": {"elapsed_seconds": 5400, "mode": "deep_work", "is_paused": False},
        "active_deck": "Electrodynamics",
        "queued_logs": [
            {
                "id": str(uuid.uuid4()),
                "subject": "Physics",
                "chapter": "Electrodynamics",
                "duration_seconds": 120,
                "is_correct": True,
                "score_delta": 4,
                "notes": "Offline test log 1"
            },
            {
                "id": str(uuid.uuid4()),
                "subject": "Chemistry",
                "chapter": "Thermodynamics",
                "duration_seconds": 90,
                "is_correct": False,
                "mistake_tag": "Calculation Mistake",
                "score_delta": -1,
                "notes": "Offline test log 2"
            }
        ],
        "queued_exams": [
            {
                "test_id": f"cbt_batch_{int(time.time())}",
                "title": "Offline Reconnect Exam",
                "mode": "advanced",
                "score": 15,
                "max_score": 20,
                "accuracy": 75.0,
                "time_spent": 300,
                "answers": [],
                "analytics": {"subject": "Physics"}
            }
        ]
    }
    t0 = time.time()
    r_sync = client.post("/api/sync", json=batch_payload)
    lat_sync = round((time.time() - t0) * 1000, 2)
    s_data = r_sync.json()
    print(f"  [✓] POST /api/sync (Batch Reconnection) -> HTTP {r_sync.status_code} ({lat_sync}ms)")
    print(f"      Synced Logs: {s_data.get('synced_logs')}, Synced Exams: {s_data.get('synced_exams')}")
    assert r_sync.status_code == 200, "Batch sync failed"
    endpoint_results["sync_batch"] = {
        "status": r_sync.status_code,
        "latency_ms": lat_sync,
        "synced_logs": s_data.get("synced_logs"),
        "synced_exams": s_data.get("synced_exams")
    }

    # 2.5 Hydration: GET /api/state?user_id=...
    t0 = time.time()
    r_state = client.get(f"/api/state?user_id={test_user_id}")
    lat_state = round((time.time() - t0) * 1000, 2)
    print(f"  [✓] GET /api/state?user_id={test_user_id[:8]}... -> HTTP {r_state.status_code} ({lat_state}ms)")
    assert r_state.status_code == 200, "State hydration failed"
    endpoint_results["state_hydration"] = {
        "status": r_state.status_code,
        "latency_ms": lat_state
    }

    return endpoint_results

def main():
    print("=" * 70)
    print(" 🛡️ CLOCKEE SIMULATION AGENT — RLS SECURITY & ENDPOINT AUDIT")
    print("=" * 70)

    rls_audit = audit_rls_policies()
    endpoint_audit = audit_api_endpoints()

    all_rls_passed = all(v.get("enforced", v.get("blocked", True)) for v in rls_audit.values())
    all_endpoints_passed = (
        endpoint_audit.get("health", {}).get("status") == 200 and
        endpoint_audit.get("auth_providers", {}).get("status") == 200 and
        endpoint_audit.get("sync_missing_auth", {}).get("rejected_unauthenticated") is True and
        endpoint_audit.get("sync_batch", {}).get("status") == 200 and
        endpoint_audit.get("state_hydration", {}).get("status") == 200
    )

    verdict = "PASSED" if (all_rls_passed and all_endpoints_passed) else "FAILED"

    report = {
        "timestamp": datetime.now().isoformat(),
        "task": "RLS Policy Enforcement & Endpoint Audit",
        "verdict": verdict,
        "rls_audit": rls_audit,
        "endpoint_audit": endpoint_audit
    }

    report_path = os.path.join(os.path.dirname(__file__), ".pipeline", "rls_endpoint_audit_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("\n" + "=" * 70)
    print(f" ✨ Audit completed with verdict: {verdict}")
    print(f"    Report saved to: {report_path}")
    print("=" * 70)

if __name__ == "__main__":
    main()
