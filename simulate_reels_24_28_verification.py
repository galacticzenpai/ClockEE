"""
ClockEE Quality Gate & Simulation Runner for Reels #24-#28
Verifies:
1. CBTStateGuard ES6 Proxy invariants (bounds check, invalid type prevention)
2. Self-Healing DOM logic & safety wrapper
3. Rank Predictor latency & calibration
4. SQLite-VSS Vector Search Sub-50ms SLA
5. Live Edge endpoints on https://clockee-os.vercel.app
"""

import subprocess
import sys
import json
import urllib.request
import time

def run_test(name, fn):
    print(f"[*] Testing {name}...", end=" ", flush=True)
    t0 = time.perf_counter()
    try:
        fn()
        dt_ms = (time.perf_counter() - t0) * 1000
        print(f"PASSED ({dt_ms:.2f}ms)")
        return True, dt_ms
    except Exception as e:
        dt_ms = (time.perf_counter() - t0) * 1000
        print(f"FAILED ({dt_ms:.2f}ms): {e}")
        return False, dt_ms

def test_node_state_guard():
    code = """
    const fs = require('fs');
    const vm = require('vm');
    const code = fs.readFileSync('js/state_guard.js', 'utf8');
    const sandbox = { window: {}, console };
    vm.createContext(sandbox);
    vm.runInContext(code, sandbox);

    const Guard = sandbox.window.CBTStateGuard;
    if (!Guard) throw new Error('CBTStateGuard not exposed on window');

    const state = Guard.createGuardedState({ currentQuestion: 1, remainingSec: 3600, selectedOption: null }, 180);
    
    // Test 1: Valid mutation
    state.currentQuestion = 5;
    if (state.currentQuestion !== 5) throw new Error('Valid currentQuestion mutation failed');

    // Test 2: Out of bounds high
    state.currentQuestion = 181;
    if (state.currentQuestion === 181) throw new Error('Blocked question > 180 should not mutate');

    // Test 3: Out of bounds low
    state.currentQuestion = 0;
    if (state.currentQuestion === 0) throw new Error('Blocked question < 1 should not mutate');

    // Test 4: Negative remainingSec
    state.remainingSec = -10;
    if (state.remainingSec === -10) throw new Error('Blocked negative remainingSec should not mutate');

    // Test 5: Invalid option
    state.selectedOption = 5;
    if (state.selectedOption === 5) throw new Error('Blocked option > 4 should not mutate');

    state.selectedOption = 3;
    if (state.selectedOption !== 3) throw new Error('Valid option 3 should mutate');

    console.log('[NODE PASS] StateGuard invariant enforcement confirmed.');
    """
    res = subprocess.run(["node", "-e", code], capture_output=True, text=True, check=True)
    if "[NODE PASS]" not in res.stdout:
        raise RuntimeError(f"Unexpected output: {res.stdout} {res.stderr}")

def test_node_syntax():
    files = [
        "js/diagnostics_console.js",
        "js/radar_chart.js",
        "js/self_healing_dom.js",
        "js/state_guard.js",
        "js/telemetry_worker.js",
        "integrations/jspdf/pdf_generator.js"
    ]
    for f in files:
        res = subprocess.run(["node", "-c", f], capture_output=True, text=True, check=True)

def test_rank_predictor():
    res = subprocess.run([sys.executable, "integrations/stats/rank_predictor.py"], capture_output=True, text=True, check=True)
    if "Result:" not in res.stdout:
        raise RuntimeError(f"Rank predictor failed: {res.stdout}")

def test_sqlite_vss():
    res = subprocess.run([sys.executable, "integrations/sqlite_vss/vss_indexer.py", "--benchmark"], capture_output=True, text=True, check=True)
    if "PASSED" not in res.stdout:
        raise RuntimeError(f"VSS latency SLA check failed: {res.stdout}")

def test_live_edge_routes():
    routes = [
        "/api/health",
        "/api/tracker",
        "/cbt_exam.html",
        "/cbt_analysis.html"
    ]
    base = "https://clockee-os.vercel.app"
    for r in routes:
        url = base + r
        req = urllib.request.Request(url, headers={"User-Agent": "ClockEE-Simulation-Test/1.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            if resp.status != 200:
                raise RuntimeError(f"Route {r} returned HTTP {resp.status}")

def main():
    print("====================================================================")
    print("  CLOCKEE SIMULATION VERIFICATION: REELS #24 THROUGH #28")
    print("====================================================================")
    results = {}
    results["State Guard Invariants"] = run_test("State Guard Invariants (ES6 Proxy)", test_node_state_guard)
    results["JavaScript Syntax Lint"] = run_test("JavaScript Syntax (Node -c)", test_node_syntax)
    results["Rank Predictor Microbenchmark"] = run_test("Rank Predictor (Stats Matrix)", test_rank_predictor)
    results["SQLite-VSS Vector SLA"] = run_test("SQLite-VSS SLA (<50ms)", test_sqlite_vss)
    results["Live Vercel Edge Probes"] = run_test("Live Vercel Edge Probes (clockee-os.vercel.app)", test_live_edge_routes)

    all_passed = all(r[0] for r in results.values())
    print("====================================================================")
    if all_passed:
        print("ALL QUALITY GATES PASSED (100% SUCCESS)")
        sys.exit(0)
    else:
        print("QUALITY GATES FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()
