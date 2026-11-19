import json
import os
import sys
from agentapi_rpc import AgentAPIRPCClient

def dispatch_clean_slate():
    client = AgentAPIRPCClient()

    # 1. DB / BACKEND
    content_db = (
        "=== PHASE 1 DIRECTIVE: CLEAN-SLATE DATABASE & STORAGE VERIFICATION ===\n"
        "Target: DB / BACKEND (d3700ff3-1bfb-458a-9968-8257ef2ca7e2)\n"
        "Mandate: Clean-Slate Rebuild with 100% Schema Preservation.\n"
        "Tasks:\n"
        "1. Verify clean SQLite & Supabase table structures (students, cbt_tests, mistakes, question_bank, session_logs).\n"
        "2. Ensure serverless Python adapter (api/index.py) is stateless and connects seamlessly to Supabase PostgreSQL.\n"
        "3. Assert zero schema regressions and verify database readiness for the fresh app shell."
    )
    lat_db = client.send_async(
        recipient_id="d3700ff3-1bfb-458a-9968-8257ef2ca7e2",
        content=content_db,
        title="[PHASE 1] Clean-Slate Database Verification"
    )
    print(f"✔ Dispatched Phase 1 to DB / BACKEND in {lat_db:.2f}ms")

    # 2. UI / UX
    content_ui = (
        "=== PHASE 2 DIRECTIVE: APPLE HIG + MATHONGO CLEAN DESIGN SYSTEM ===\n"
        "Target: UI / UX (06a7d47b-b225-40f4-b830-b58baaaf8b3a)\n"
        "Mandate: Ground-up authoring of the unified design system.\n"
        "Tasks:\n"
        "1. Author the clean Apple HIG + Mathongo design system tokens and responsive stylesheets.\n"
        "2. Enforce strict Fitts's Law button hierarchies (min 44x44px touch targets) with elastic feedback.\n"
        "3. Zero AI Slop: no saturated purple gradients, no floating neon glow, no emoji buttons.\n"
        "4. APCA contrast compliance (>=75 on text, >=60 on secondary labels) on pitch black (#000000) and dark slate (#12151c)."
    )
    lat_ui = client.send_async(
        recipient_id="06a7d47b-b225-40f4-b830-b58baaaf8b3a",
        content=content_ui,
        title="[PHASE 2] Apple HIG + Mathongo Design System"
    )
    print(f"✔ Dispatched Phase 2 to UI / UX in {lat_ui:.2f}ms")

    # 3. MAIN FEATURE
    content_feat = (
        "=== PHASE 2 DIRECTIVE: CLEAN-SLATE UNIFIED APP SHELL RECONSTRUCTION ===\n"
        "Target: MAIN FEATURE (6371cba6-7d2f-4b29-a250-627d88d1b4f1)\n"
        "Mandate: Unified application shell and core interaction logic.\n"
        "Tasks:\n"
        "1. Reconstruct the unified DOM layout, view switcher, and navigation flows from clean principles.\n"
        "2. Wire the 6,326 authentic question bank items with clean KaTeX formatting.\n"
        "3. Implement live Mathongo pacing benchmark timer (Student time vs Topper target) and mistake taxonomy.\n"
        "4. Enforce clean state transitions with sub-100ms response (Doherty Threshold)."
    )
    lat_feat = client.send_async(
        recipient_id="6371cba6-7d2f-4b29-a250-627d88d1b4f1",
        content=content_feat,
        title="[PHASE 2] Clean-Slate App Shell Reconstruction"
    )
    print(f"✔ Dispatched Phase 2 to MAIN FEATURE in {lat_feat:.2f}ms")

    # 4. SIMULATION
    content_sim = (
        "=== PHASE 3 STATUS: SIMULATION PRIMED & ARMED ===\n"
        "Target: SIMULATION (62adc180-be21-4671-848c-c8df59e2c202)\n"
        "Status: Phase 1 (DB/Backend) and Phase 2 (UI/UX & Main Feature) dispatches are active.\n"
        "Instruction: Maintain simulate_ux_laws_virtual_feedback.py and the 100-Point UX-GUARD rubric on standby for the incoming Phase 3 certification pass."
    )
    lat_sim = client.send_async(
        recipient_id="62adc180-be21-4671-848c-c8df59e2c202",
        content=content_sim,
        title="[PHASE 3] Simulation Armed on Standby"
    )
    print(f"✔ Dispatched Phase 3 status to SIMULATION in {lat_sim:.2f}ms")

if __name__ == "__main__":
    dispatch_clean_slate()
