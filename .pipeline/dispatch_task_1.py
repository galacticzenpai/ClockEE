import subprocess
from pathlib import Path

LANG_SERVER_BIN = r"C:\Users\Kunal\AppData\Local\Programs\antigravity\resources\bin\language_server.exe"
DB_BACKEND_ID = "d3700ff3-1bfb-458a-9968-8257ef2ca7e2"

task_1_prompt = """You are DB / BACKEND.

--- TASK ASSIGNMENT: TASK-01 (Vercel Serverless Python Adapter & Supabase Cloud Gateway) ---
Plan ID: plan_20261116_115300 (from .pipeline/daily_plan.json)
Target: api/index.py, requirements.txt, backend/db.py

Execution Instructions:
1. Supabase Cloud Connection & Verification:
   - Supabase project is LIVE:
     URL: https://qvrfakbhnsmknukaqmja.supabase.co
     Anon Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF2cmZha2JobnNta251a2FxbWphIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTQ4MDY5ODAsImV4cCI6MjExMDM4Mjk4MH0.GC7ZN6K4cQZs8JReviamFSRwbmTnmMy9GwJSNUMty-o
   - All 5 core tables are already created and verified in Supabase:
     * public.mesh_tracker_state (RLS enabled, public read)
     * public.profiles (RLS enabled)
     * public.student_states (RLS enabled)
     * public.cbt_results (RLS enabled)
     * public.study_sessions (RLS enabled)
   - .env is configured with these live credentials.

2. Implement Vercel Serverless Python Adapter (api/index.py):
   - Create api/index.py as a FastAPI application (or BaseHTTPRequestHandler / WSGI / ASGI) for Vercel Serverless Functions.
   - On Vercel, the filesystem is read-only (except /tmp). All reads/writes must target Supabase cloud REST/PostgreSQL, bypassing local clockee.db.
   - Endpoints required:
     * GET /api/health — Return 200 OK with database connection status: "connected" to Supabase.
     * GET /api/tracker — Return live mesh tracker state (from public.mesh_tracker_state or .pipeline/tracker_state.json fallback).
     * POST /api/tracker — Allow streaming/upserting mesh tracker state to public.mesh_tracker_state.
     * GET /api/state — Fetch student profile & active state using verified Supabase Auth JWT token.
     * POST /api/state — Upsert student state and daily goals into Supabase.
     * POST /api/cbt/submit — Save CBT examination results and analytics into public.cbt_results.
     * GET /api/cbt/history — Fetch test history for user.
     * POST /api/auth/verify — Verify Google OAuth / Supabase JWT token.

3. Provide requirements.txt:
   - Include dependencies required by Vercel:
     fastapi>=0.115.0
     uvicorn>=0.31.0
     supabase>=2.8.0
     pydantic>=2.9.2
     requests>=2.31.0

4. Verification & Handoff:
   - Verify that api/index.py imports and initializes cleanly with python.
   - In .pipeline/daily_plan.json, mark TASK-01 as COMPLETED.
   - Output your standard "### 🛰️ PIPELINE QUEUE & HANDOFF REPORT" block with handoff to GITHUB for TASK-02."""

res = subprocess.run(
    [LANG_SERVER_BIN, "agentapi", "send-message", "--title=ClockEE TASK-01 Full Dispatch", DB_BACKEND_ID, task_1_prompt],
    capture_output=True,
    text=True
)

print("AgentAPI Response:", res.stdout)
if res.stderr:
    print("AgentAPI Stderr:", res.stderr)
