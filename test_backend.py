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

    print("\n[🎉] ALL 10 TEST SUITES PASSED FLAWLESSLY!")

if __name__ == '__main__':
    run_tests()
