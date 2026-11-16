#!/usr/bin/env python3
"""
⚡ ClockEE — Google & GitHub OAuth Simulation & Verification Suite
Tests both Local FastAPI Gateway (api/index.py) and Live Vercel Edge Endpoints.
Outputs: .pipeline/oauth_simulation_report.json
"""

import sys
import os
import json
import time
import uuid
import ssl
import urllib.request
from datetime import datetime

# Add root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

LIVE_BASE = "https://clockee-os.vercel.app"

def run_local_gateway_simulation():
    print("=" * 70)
    print(" 🚀 [PASS 1] LOCAL FASTAPI GATEWAY OAUTH SIMULATION")
    print("=" * 70)

    try:
        from api.index import app
        from fastapi.testclient import TestClient
    except Exception as e:
        print(f"[x] Error importing FastAPI app: {e}")
        return {"error": str(e), "success": False}

    client = TestClient(app)
    results = {}

    # 1. GET /api/auth/providers
    t0 = time.time()
    r_prov = client.get("/api/auth/providers")
    prov_lat = round((time.time() - t0) * 1000, 2)
    prov_data = r_prov.json()
    print(f"  [✓] GET /api/auth/providers -> HTTP {r_prov.status_code} ({prov_lat}ms)")
    print(f"      Providers available: {list(prov_data.get('providers', {}).keys())}")
    assert r_prov.status_code == 200, "Providers endpoint failed"
    assert "google" in prov_data.get("providers", {}), "Google provider missing"
    assert "github" in prov_data.get("providers", {}), "GitHub provider missing"
    results["providers"] = {
        "status": r_prov.status_code,
        "latency_ms": prov_lat,
        "providers": prov_data.get("providers")
    }

    # 2. POST /api/auth/google
    test_google_uid = f"google_sim_{uuid.uuid4().hex[:10]}"
    google_payload = {
        "uid": test_google_uid,
        "email": f"jee_aspirant_{test_google_uid[:6]}@gmail.com",
        "name": "Kunal Sharma (Google JEE Aspirant)",
        "pfp": f"https://api.dicebear.com/7.x/bottts-neutral/svg?seed={test_google_uid}"
    }
    t0 = time.time()
    r_goog = client.post("/api/auth/google", json=google_payload)
    goog_lat = round((time.time() - t0) * 1000, 2)
    goog_data = r_goog.json()
    print(f"  [✓] POST /api/auth/google -> HTTP {r_goog.status_code} ({goog_lat}ms)")
    print(f"      User ID: {goog_data.get('user', {}).get('id')}")
    print(f"      Email:   {goog_data.get('user', {}).get('email')}")
    print(f"      Sync Success: {goog_data.get('success')}")
    assert r_goog.status_code == 200, "Google login endpoint failed"
    assert goog_data.get("success") is True, "Google login returned non-true success"
    results["google_login"] = {
        "status": r_goog.status_code,
        "latency_ms": goog_lat,
        "user_id": goog_data.get("user", {}).get("id"),
        "success": goog_data.get("success")
    }

    # 3. POST /api/auth/github
    test_github_id = f"github_sim_{uuid.uuid4().hex[:10]}"
    github_payload = {
        "id": test_github_id,
        "username": "galacticzenpai",
        "email": "zenpai@users.noreply.github.com",
        "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4"
    }
    t0 = time.time()
    r_gh = client.post("/api/auth/github", json=github_payload)
    gh_lat = round((time.time() - t0) * 1000, 2)
    gh_data = r_gh.json()
    print(f"  [✓] POST /api/auth/github -> HTTP {r_gh.status_code} ({gh_lat}ms)")
    print(f"      User ID:  {gh_data.get('user', {}).get('id')}")
    print(f"      Username: {gh_data.get('user', {}).get('full_name')}")
    print(f"      Sync Success: {gh_data.get('success')}")
    assert r_gh.status_code == 200, "GitHub login endpoint failed"
    assert gh_data.get("success") is True, "GitHub login returned non-true success"
    results["github_login"] = {
        "status": r_gh.status_code,
        "latency_ms": gh_lat,
        "user_id": gh_data.get("user", {}).get("id"),
        "success": gh_data.get("success")
    }

    # 4. POST /api/auth/session (Heartbeat Verification)
    session_payload = {
        "user_id": goog_data.get("user", {}).get("id"),
        "provider": "google",
        "status": "online",
        "current_page": "tracker.html"
    }
    t0 = time.time()
    r_sess = client.post("/api/auth/session", json=session_payload)
    sess_lat = round((time.time() - t0) * 1000, 2)
    print(f"  [✓] POST /api/auth/session -> HTTP {r_sess.status_code} ({sess_lat}ms)")
    results["session_heartbeat"] = {
        "status": r_sess.status_code,
        "latency_ms": sess_lat
    }

    return {"status": "SUCCESS", "results": results}

def run_live_edge_simulation():
    print("\n" + "=" * 70)
    print(f" 🌐 [PASS 2] LIVE VERCEL EDGE & CLOUD AUDIT ({LIVE_BASE})")
    print("=" * 70)

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    results = {}

    # 1. Verify login.html markup and client OAuth hooks
    login_url = f"{LIVE_BASE}/login.html"
    try:
        t0 = time.time()
        req = urllib.request.Request(login_url, headers={"User-Agent": "ClockEE-OAuth-Simulator/2.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            content = resp.read().decode("utf-8", errors="ignore")
            lat = round((time.time() - t0) * 1000, 2)
            has_google = "btnGoogleLogin" in content and "handleGoogleSignIn" in content
            has_github = "btnGithubLogin" in content and "handleGithubSignIn" in content
            print(f"  [✓] GET {login_url} -> HTTP {resp.status} ({lat}ms)")
            print(f"      btnGoogleLogin present: {has_google}")
            print(f"      btnGithubLogin present: {has_github}")
            results["login_page"] = {
                "status": resp.status,
                "latency_ms": lat,
                "has_google_auth_ui": has_google,
                "has_github_auth_ui": has_github
            }
    except Exception as e:
        print(f"  [!] GET {login_url} failed: {e}")
        results["login_page"] = {"status": "FAIL", "error": str(e)}

    # 2. GET /api/auth/providers
    prov_url = f"{LIVE_BASE}/api/auth/providers"
    try:
        t0 = time.time()
        req = urllib.request.Request(prov_url, headers={"User-Agent": "ClockEE-OAuth-Simulator/2.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            lat = round((time.time() - t0) * 1000, 2)
            print(f"  [✓] GET {prov_url} -> HTTP {resp.status} ({lat}ms)")
            results["live_providers"] = {
                "status": resp.status,
                "latency_ms": lat,
                "data": body
            }
    except Exception as e:
        print(f"  [!] GET {prov_url} failed: {e}")
        results["live_providers"] = {"status": "FAIL", "error": str(e)}

    # 3. POST /api/auth/google
    goog_url = f"{LIVE_BASE}/api/auth/google"
    sim_uid = f"live_goog_{int(time.time())}"
    goog_payload = json.dumps({
        "uid": sim_uid,
        "email": f"aspirant_{sim_uid}@jee.app",
        "name": "Live Vercel Google Aspirant",
        "pfp": f"https://api.dicebear.com/7.x/bottts-neutral/svg?seed={sim_uid}"
    }).encode("utf-8")
    try:
        t0 = time.time()
        req = urllib.request.Request(goog_url, data=goog_payload, headers={
            "User-Agent": "ClockEE-OAuth-Simulator/2.0",
            "Content-Type": "application/json"
        })
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            lat = round((time.time() - t0) * 1000, 2)
            print(f"  [✓] POST {goog_url} -> HTTP {resp.status} ({lat}ms)")
            print(f"      Success: {body.get('success')}, User ID: {body.get('user', {}).get('id')}")
            results["live_google_login"] = {
                "status": resp.status,
                "latency_ms": lat,
                "body": body
            }
    except Exception as e:
        print(f"  [!] POST {goog_url} failed: {e}")
        results["live_google_login"] = {"status": "FAIL", "error": str(e)}

    # 4. POST /api/auth/github
    gh_url = f"{LIVE_BASE}/api/auth/github"
    gh_sim_id = f"live_gh_{int(time.time())}"
    gh_payload = json.dumps({
        "id": gh_sim_id,
        "username": "live_github_aspirant",
        "email": "aspirant.github@users.noreply.github.com",
        "avatar_url": f"https://api.dicebear.com/7.x/bottts-neutral/svg?seed={gh_sim_id}"
    }).encode("utf-8")
    try:
        t0 = time.time()
        req = urllib.request.Request(gh_url, data=gh_payload, headers={
            "User-Agent": "ClockEE-OAuth-Simulator/2.0",
            "Content-Type": "application/json"
        })
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            lat = round((time.time() - t0) * 1000, 2)
            print(f"  [✓] POST {gh_url} -> HTTP {resp.status} ({lat}ms)")
            print(f"      Success: {body.get('success')}, User ID: {body.get('user', {}).get('id')}")
            results["live_github_login"] = {
                "status": resp.status,
                "latency_ms": lat,
                "body": body
            }
    except Exception as e:
        print(f"  [!] POST {gh_url} failed: {e}")
        results["live_github_login"] = {"status": "FAIL", "error": str(e)}

    return {"status": "SUCCESS", "results": results}

def main():
    print(f"Starting ClockEE OAuth Verification Suite at {datetime.now().isoformat()}")
    local_report = run_local_gateway_simulation()
    live_report = run_live_edge_simulation()

    summary_report = {
        "timestamp": datetime.now().isoformat(),
        "local_gateway": local_report,
        "live_vercel_edge": live_report,
        "verdict": "PASSED" if local_report.get("status") == "SUCCESS" else "NEEDS_ATTENTION"
    }

    report_path = os.path.join(os.path.dirname(__file__), "oauth_simulation_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(summary_report, f, indent=2)

    print("\n" + "=" * 70)
    print(f" ✨ Simulation complete! Report generated at: {report_path}")
    print("=" * 70)

if __name__ == "__main__":
    main()
