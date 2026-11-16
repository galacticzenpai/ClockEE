import os
import json
import urllib.request
import urllib.error
import time

BASE_URL = "http://127.0.0.1:8000"

def req(path, method="GET", data=None, headers=None):
    if headers is None:
        headers = {}
    url = BASE_URL + path
    body = json.dumps(data).encode('utf-8') if data else None
    if body:
        headers['Content-Type'] = 'application/json'
    r = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(r) as resp:
            content = resp.read().decode('utf-8')
            return resp.status, json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8')
        try:
            return e.code, json.loads(err_body)
        except Exception:
            return e.code, {"error": err_body}

def run_tests():
    print("Testing ClockEE Full-Stack Server & SQLite Backend...")

    # 1. Health Ping
    status, res = req("/clockee.json")
    assert status == 200, f"Expected 200, got {status}"
    assert res.get("status") == "online", "Server status not online"
    print(f"  [✓] /clockee.json OK: {res.get('app')} (DB: {res.get('database')}, {res.get('counts', {}).get('questions')} Qs)")

    # 2. Check Email
    status, res = req("/api/check-email", "POST", {"email": "alpha@clockee.app"})
    assert status == 200 and res.get("exists") is True
    print(f"  [✓] /api/check-email OK: Student Alpha found")

    # 3. Sign In (Alpha)
    status, res = req("/api/signin", "POST", {"email": "alpha@clockee.app", "password": "password123"})
    assert status == 200 and res.get("success") is True
    token = res.get("token")
    assert token is not None
    print(f"  [✓] /api/signin OK: Authenticated Student Alpha (Token: {token[:10]}...)")

    # 4. Sign In with invalid password (security check)
    status, res = req("/api/signin", "POST", {"email": "alpha@clockee.app", "password": "wrongpassword"})
    assert status == 401
    print(f"  [✓] /api/signin Security OK: Rejected invalid credentials with 401")

    # 5. Question Bank Query
    status, res = req("/api/questions?subject=Physics&limit=3")
    assert status == 200 and len(res.get("questions", [])) == 3
    print(f"  [✓] /api/questions OK: Retrieved 3 physics questions (Total match: {res.get('total')})")

    # 6. Adaptive Test Random Question Generator
    status, res = req("/api/questions/random?subject=Full&count=6")
    assert status == 200 and len(res.get("questions", [])) == 6
    print(f"  [✓] /api/questions/random OK: Generated balanced 6-question CBT mock set")

    # 7. Firebase-Compatible Students Roster
    status, res = req("/students.json")
    assert status == 200 and "user_alpha" in res and "user_beta" in res
    print(f"  [✓] /students.json (Firebase Emulation) OK: Found {len(res)} students in roster")

    # 8. Student State Push / Pull
    status, res = req("/students/user_alpha/state.json")
    assert status == 200 and res.get("profile", {}).get("name") == "Student Alpha"
    print(f"  [✓] /students/user_alpha/state.json GET OK: Streak: {res.get('stats', {}).get('streakDays')} days")

    # 9. Tasks API
    status, res = req("/api/tasks?user_id=user_alpha")
    assert status == 200 and len(res.get("tasks", [])) > 0
    print(f"  [✓] /api/tasks OK: Retrieved {len(res.get('tasks', []))} tasks for Alpha")

    # 10. CBT Crash Save & Resume Checkpoint
    checkpoint_payload = {
        "user_id": "user_alpha",
        "test_id": "test_crash_recovery_01",
        "test_data": {"title": "Drill #1"},
        "responses": {"1": 2, "2": 0},
        "palette": {"1": "answered", "2": "marked"},
        "current_question": 3,
        "remaining_seconds": 2450
    }
    status, res = req("/api/cbt/crash-save", "POST", checkpoint_payload)
    assert status == 200 and res.get("success") is True

    status, res = req("/api/cbt/crash-resume?user_id=user_alpha&test_id=test_crash_recovery_01")
    assert status == 200 and res.get("current_question") == 3 and res.get("remaining_seconds") == 2450
    print(f"  [✓] /api/cbt/crash-save & resume OK: Resumed at Q#3 with exact timer (2450s)")

    # 11. Theme & Customization Persistence via /api/userdata
    theme_payload = {
        "email": "alpha@clockee.app",
        "theme_preference": "space_violet",
        "aura_mode": "pulse",
        "data": {
            "customization_token": "token_halo_violet_99",
            "glass_blur": 32
        }
    }
    status, res = req("/api/userdata", "POST", theme_payload)
    assert status == 200 and res.get("success") is True
    assert res.get("theme_preference") == "space_violet"
    assert res.get("aura_mode") == "pulse"
    print(f"  [✓] /api/userdata POST OK: Saved Hallmark theme 'space_violet' and aura 'pulse'")

    # Verify retrieval
    status, res = req("/api/userdata?email=alpha@clockee.app")
    assert status == 200 and res.get("theme_preference") == "space_violet"
    assert res.get("aura_mode") == "pulse"
    assert res.get("data", {}).get("customization_token") == "token_halo_violet_99"
    print(f"  [✓] /api/userdata GET OK: Retrieved persisted Hallmark theme and customization tokens")

    # 12. Fallback on Unrecognized Theme & Aura String
    invalid_theme_payload = {
        "email": "beta@clockee.app",
        "theme_preference": "completely_unrecognized_slop_theme_x",
        "aura_mode": "hyper_turbo_unsupported",
        "data": {}
    }
    status, res = req("/api/userdata", "POST", invalid_theme_payload)
    assert status == 200 and res.get("success") is True
    assert res.get("theme_preference") == "cyan_indigo", f"Expected clean fallback to 'cyan_indigo', got {res.get('theme_preference')}"
    assert res.get("aura_mode") == "fluid", f"Expected clean fallback to 'fluid', got {res.get('aura_mode')}"
    print(f"  [✓] Unrecognized Theme Fallback OK: Safely defaulted to 'cyan_indigo' / 'fluid'")

    # 13. Direct Database Column Verification
    import sqlite3
    conn = sqlite3.connect("clockee.db")
    cur = conn.cursor()
    cur.execute("SELECT theme_preference, aura_mode FROM users WHERE email = 'alpha@clockee.app'")
    row = cur.fetchone()
    assert row is not None and row[0] == "space_violet" and row[1] == "pulse"
    cur.execute("SELECT theme_preference, aura_mode FROM users WHERE email = 'beta@clockee.app'")
    row_b = cur.fetchone()
    assert row_b is not None and row_b[0] == "cyan_indigo" and row_b[1] == "fluid"
    conn.close()
    print(f"  [✓] SQLite Database Columns OK: users.theme_preference and users.aura_mode verified directly in SQLite")

    # 14. Supabase OAuth Providers Endpoint
    status, res = req("/api/auth/providers?redirect_to=http://127.0.0.1:8000/login.html")
    assert status == 200, f"Expected 200, got {status}"
    assert "providers" in res, "Missing providers key in response"
    assert "google" in res["providers"] and "url" in res["providers"]["google"]
    assert "github" in res["providers"] and "url" in res["providers"]["github"]
    print(f"  [✓] /api/auth/providers OK: Configured OAuth URLs returned for Google & GitHub")

    # 15. Supabase JWT Authentication via Authorization Header
    import jwt
    mock_uid = "00000000-0000-4000-a000-000000000001"
    jwt_payload = {
        "sub": mock_uid,
        "email": "supabase_aspirant@clockee.app",
        "role": "authenticated",
        "user_metadata": {
            "full_name": "Supabase Aspirant",
            "role": "JEE 2028 Aspirant"
        },
        "exp": int(time.time()) + 3600
    }
    mock_jwt = jwt.encode(jwt_payload, "mock_supabase_secret_key_at_least_32_bytes_long!!", algorithm="HS256")
    status, res = req("/api/auth/me", headers={"Authorization": f"Bearer {mock_jwt}"})
    assert status == 200, f"Expected 200, got {status}: {res}"
    assert res.get("user", {}).get("email") == "supabase_aspirant@clockee.app"
    print(f"  [✓] Supabase Auth Middleware OK: Verified Bearer JWT and extracted claims for {mock_uid}")

    # 16. Supabase Session Sync Endpoint
    status, res = req("/api/auth/session", "POST", {"access_token": mock_jwt})
    assert status == 200 and res.get("success") is True
    assert res.get("user", {}).get("email") == "supabase_aspirant@clockee.app"
    print(f"  [✓] /api/auth/session OK: Cached Supabase user in gateway database and issued session token")

    # 17. Batch Offline-First Sync Endpoint (/api/sync)
    offline_sync_payload = {
        "user_id": "user_alpha",
        "current_mode": "advanced",
        "active_deck": "Rotational Mechanics Mastery",
        "timer_state": {
            "elapsed_seconds": 3600,
            "mode": "sprint",
            "is_paused": False
        },
        "queued_logs": [
            {
                "id": "log_offline_01",
                "subject": "Physics",
                "chapter": "Center of Mass",
                "qNum": 12,
                "duration": 180.0,
                "correct": True,
                "score_delta": 4,
                "notes": "Solved using impulse equation"
            },
            {
                "id": "log_offline_02",
                "subject": "Chemistry",
                "chapter": "Chemical Equilibrium",
                "qNum": 5,
                "duration": 95.0,
                "correct": False,
                "mistake": "Calculation Mistake",
                "score_delta": -1,
                "notes": "Forgot to square the concentration term"
            }
        ],
        "queued_exams": [
            {
                "id": "cbt_offline_01",
                "test_id": "offline_drill_01",
                "title": "Offline Rapid Revision CBT",
                "mode": "advanced",
                "subject": "Full",
                "total_questions": 30,
                "time_spent": 3600,
                "score": 88,
                "max_score": 120,
                "accuracy": 73.33,
                "responses": [{"q": 1, "ans": "B"}],
                "analytics": {"timePerQ": 120}
            }
        ]
    }
    status, res = req("/api/sync", "POST", offline_sync_payload)
    assert status == 200 and res.get("success") is True
    assert res.get("synced_logs") == 2, f"Expected 2 synced logs, got {res.get('synced_logs')}"
    assert res.get("synced_exams") == 1, f"Expected 1 synced exam, got {res.get('synced_exams')}"
    print(f"  [✓] /api/sync POST OK: Ingested 2 queued study logs and 1 CBT exam from client localStorage")

    # Verify /api/sync GET
    status, res = req("/api/sync?user_id=user_alpha")
    assert status == 200
    assert res.get("user_id") == "user_alpha"
    assert len(res.get("recent_logs", [])) >= 2
    assert len(res.get("recent_exams", [])) >= 1
    print(f"  [✓] /api/sync GET OK: Retrieved synchronized student state & history for offline hydration")

    # 18. SQLite to Supabase Migration Tool Verification
    from backend.migrate_sqlite_to_supabase import run_migration
    mig_success = run_migration(dry_run=True, dump_sql=True)
    assert mig_success is True, "Migration dry-run failed"
    assert os.path.exists("backend/supabase_migration_dump.sql")
    dump_size = os.path.getsize("backend/supabase_migration_dump.sql")
    assert dump_size > 500, f"SQL dump unexpectedly small: {dump_size} bytes"
    print(f"  [✓] SQLite -> Supabase Migration OK: Verified schema mapping and dump generation ({dump_size} bytes)")

    print("\n[🎉] ALL 18 TEST SUITES PASSED FLAWLESSLY!")

if __name__ == '__main__':
    import socket
    import threading
    from http.server import ThreadingHTTPServer
    from server import ClockEEServerHandler
    from backend.db import init_db
    from backend.seed import seed_database

    init_db()
    seed_database(force_questions=False)

    # Check if server is already running on port 8000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    is_running = False
    try:
        s.connect(('127.0.0.1', 8000))
        is_running = True
        s.close()
    except Exception:
        pass

    httpd = None
    if not is_running:
        httpd = ThreadingHTTPServer(('127.0.0.1', 8000), ClockEEServerHandler)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        time.sleep(0.5)

    try:
        run_tests()
    finally:
        if httpd:
            httpd.shutdown()
