#!/usr/bin/env python3
"""
⚡ ClockEE — SQLite to Supabase PostgreSQL Database Migration Engine
Migrates users, states, study session logs, and CBT exam analytics from local SQLite (clockee.db)
into Supabase PostgreSQL schema with Row-Level Security (RLS) compatibility.
"""

import os
import sys
import json
import sqlite3
import uuid
import argparse
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, CURRENT_DIR)

from db import (
    DB_PATH, get_db, is_supabase_configured,
    get_supabase_client, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
)

def to_uuid(raw_id: str) -> str:
    """
    Ensure an identifier is converted to a valid, deterministic UUIDv5 string.
    If already a valid UUID, returns canonical UUID string.
    """
    if not raw_id:
        return str(uuid.uuid4())
    try:
        return str(uuid.UUID(str(raw_id)))
    except (ValueError, AttributeError):
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"clockee.app.user.{raw_id}"))

def escape_sql(val):
    """Safely format values for PostgreSQL SQL dump."""
    if val is None:
        return "NULL"
    if isinstance(val, bool):
        return "TRUE" if val else "FALSE"
    if isinstance(val, (int, float)):
        return str(val)
    if isinstance(val, (dict, list)):
        dumped = json.dumps(val, ensure_ascii=False)
        return "'" + dumped.replace("'", "''") + "'::jsonb"
    val_str = str(val).replace("'", "''")
    return f"'{val_str}'"

def extract_sqlite_data(conn):
    """Read all relational tables from clockee.db."""
    cur = conn.cursor()

    # 1. Users
    cur.execute("SELECT * FROM users")
    users = [dict(r) for r in cur.fetchall()]

    # 2. Student States
    cur.execute("SELECT * FROM student_states")
    student_states = [dict(r) for r in cur.fetchall()]

    # 3. Question Logs
    cur.execute("SELECT * FROM question_logs")
    question_logs = [dict(r) for r in cur.fetchall()]

    # 4. CBT Exams
    cur.execute("SELECT * FROM cbt_exams")
    cbt_exams = [dict(r) for r in cur.fetchall()]

    return {
        "users": users,
        "student_states": student_states,
        "question_logs": question_logs,
        "cbt_exams": cbt_exams
    }

def transform_records(raw_data):
    """
    Transform SQLite rows into Supabase PostgreSQL schema models:
    - profiles
    - student_states
    - study_sessions
    - cbt_results
    """
    profiles = []
    user_id_map = {}

    for u in raw_data["users"]:
        user_uuid = to_uuid(u["id"])
        user_id_map[u["id"]] = user_uuid
        user_id_map[u["email"]] = user_uuid

        profiles.append({
            "id": user_uuid,
            "email": u["email"],
            "full_name": u.get("name") or "JEE Aspirant",
            "avatar_url": u.get("pfp") or f"https://api.dicebear.com/7.x/bottts-neutral/svg?seed={u['email']}",
            "role": u.get("role") or "JEE 2028 Aspirant",
            "theme_preference": u.get("theme_preference") or "cyan_indigo",
            "aura_mode": u.get("aura_mode") or "fluid",
            "created_at": u.get("created_at") or datetime.now().isoformat(),
            "last_seen": u.get("last_login") or u.get("created_at") or datetime.now().isoformat()
        })

    # Student states
    states = []
    for s in raw_data["student_states"]:
        uid = user_id_map.get(s["user_id"], to_uuid(s["user_id"]))
        try:
            state_data = json.loads(s.get("state_json") or "{}")
        except Exception:
            state_data = {}

        states.append({
            "user_id": uid,
            "current_mode": state_data.get("examMode", "mains"),
            "timer_state": state_data.get("timer_state") or state_data.get("timerState") or {},
            "active_deck": state_data.get("activeDeck", "") or state_data.get("active_deck", ""),
            "daily_goals": state_data.get("dailyGoals", {"Physics": 30, "Chemistry": 30, "Maths": 30, "hours": 6.0}),
            "stats": state_data.get("stats", {"hoursToday": 0.0, "streakDays": 1, "questionsSolved": {"Physics": 0, "Chemistry": 0, "Maths": 0}}),
            "state_payload": state_data,
            "updated_at": s.get("updated_at") or datetime.now().isoformat()
        })

    # Study Sessions (from question_logs)
    study_sessions = []
    for ql in raw_data["question_logs"]:
        uid = user_id_map.get(ql["user_id"], to_uuid(ql["user_id"]))
        session_uuid = to_uuid(ql.get("id"))
        study_sessions.append({
            "id": session_uuid,
            "user_id": uid,
            "duration_seconds": float(ql.get("duration_seconds") or 60.0),
            "subject": ql.get("subject", "Physics"),
            "topic": ql.get("chapter") or "General",
            "chapter": ql.get("chapter", ""),
            "question_num": int(ql.get("question_num") or 1),
            "is_correct": bool(ql.get("is_correct")),
            "mistake_tag": ql.get("mistake_tag", ""),
            "score_delta": int(ql.get("score_delta") or 4),
            "notes": ql.get("notes", ""),
            "timestamp": ql.get("created_at") or datetime.now().isoformat()
        })

    # CBT Results (from cbt_exams)
    cbt_results = []
    for exam in raw_data["cbt_exams"]:
        uid = user_id_map.get(exam["user_id"], to_uuid(exam["user_id"]))
        result_uuid = to_uuid(exam.get("id"))
        try:
            answers = json.loads(exam.get("responses_json") or "[]")
        except Exception:
            answers = []
        try:
            analytics = json.loads(exam.get("analytics_json") or "{}")
        except Exception:
            analytics = {}

        cbt_results.append({
            "id": result_uuid,
            "user_id": uid,
            "test_id": exam.get("test_id", "test_cbt"),
            "title": exam.get("title", "CBT Mock Examination"),
            "mode": exam.get("mode", "mains"),
            "subject": exam.get("subject", "Full"),
            "chapter": exam.get("chapter", ""),
            "total_questions": int(exam.get("total_questions") or 25),
            "score": int(exam.get("score") or 0),
            "max_score": int(exam.get("max_score") or 100),
            "accuracy": float(exam.get("accuracy") or 0.0),
            "time_spent": int(exam.get("time_spent_seconds") or 0),
            "answers_json": answers,
            "analytics_json": analytics,
            "completed_at": exam.get("completed_at") or exam.get("created_at") or datetime.now().isoformat()
        })

    return {
        "profiles": profiles,
        "student_states": states,
        "study_sessions": study_sessions,
        "cbt_results": cbt_results,
        "user_id_map": user_id_map
    }

def generate_sql_dump(transformed):
    """Generate PostgreSQL SQL statements for direct execution in Supabase SQL editor."""
    lines = [
        "-- ==============================================================================",
        "-- ClockEE SQLite to Supabase PostgreSQL Migration Dump",
        f"-- Generated at: {datetime.now().isoformat()}",
        "-- ==============================================================================",
        "BEGIN;",
        ""
    ]

    # Profiles
    lines.append("-- 1. Insert / Upsert Profiles")
    for p in transformed["profiles"]:
        lines.append(f"""INSERT INTO public.profiles (id, email, full_name, avatar_url, role, theme_preference, aura_mode, created_at, last_seen)
VALUES ({escape_sql(p['id'])}, {escape_sql(p['email'])}, {escape_sql(p['full_name'])}, {escape_sql(p['avatar_url'])}, {escape_sql(p['role'])}, {escape_sql(p['theme_preference'])}, {escape_sql(p['aura_mode'])}, {escape_sql(p['created_at'])}, {escape_sql(p['last_seen'])})
ON CONFLICT (id) DO UPDATE SET
    full_name = EXCLUDED.full_name,
    avatar_url = EXCLUDED.avatar_url,
    role = EXCLUDED.role,
    theme_preference = EXCLUDED.theme_preference,
    aura_mode = EXCLUDED.aura_mode,
    last_seen = EXCLUDED.last_seen;""")

    lines.append("")
    # Student states
    lines.append("-- 2. Insert / Upsert Student States")
    for s in transformed["student_states"]:
        lines.append(f"""INSERT INTO public.student_states (user_id, current_mode, timer_state, active_deck, daily_goals, stats, state_payload, updated_at)
VALUES ({escape_sql(s['user_id'])}, {escape_sql(s['current_mode'])}, {escape_sql(s['timer_state'])}, {escape_sql(s['active_deck'])}, {escape_sql(s['daily_goals'])}, {escape_sql(s['stats'])}, {escape_sql(s['state_payload'])}, {escape_sql(s['updated_at'])})
ON CONFLICT (user_id) DO UPDATE SET
    current_mode = EXCLUDED.current_mode,
    timer_state = EXCLUDED.timer_state,
    active_deck = EXCLUDED.active_deck,
    daily_goals = EXCLUDED.daily_goals,
    stats = EXCLUDED.stats,
    state_payload = EXCLUDED.state_payload,
    updated_at = EXCLUDED.updated_at;""")

    lines.append("")
    # Study sessions
    lines.append("-- 3. Insert Study Sessions")
    for sess in transformed["study_sessions"]:
        lines.append(f"""INSERT INTO public.study_sessions (id, user_id, duration_seconds, subject, topic, chapter, question_num, is_correct, mistake_tag, score_delta, notes, timestamp)
VALUES ({escape_sql(sess['id'])}, {escape_sql(sess['user_id'])}, {escape_sql(sess['duration_seconds'])}, {escape_sql(sess['subject'])}, {escape_sql(sess['topic'])}, {escape_sql(sess['chapter'])}, {escape_sql(sess['question_num'])}, {escape_sql(sess['is_correct'])}, {escape_sql(sess['mistake_tag'])}, {escape_sql(sess['score_delta'])}, {escape_sql(sess['notes'])}, {escape_sql(sess['timestamp'])})
ON CONFLICT (id) DO NOTHING;""")

    lines.append("")
    # CBT results
    lines.append("-- 4. Insert CBT Results")
    for cbt in transformed["cbt_results"]:
        lines.append(f"""INSERT INTO public.cbt_results (id, user_id, test_id, title, mode, subject, chapter, total_questions, score, max_score, accuracy, time_spent, answers_json, analytics_json, completed_at)
VALUES ({escape_sql(cbt['id'])}, {escape_sql(cbt['user_id'])}, {escape_sql(cbt['test_id'])}, {escape_sql(cbt['title'])}, {escape_sql(cbt['mode'])}, {escape_sql(cbt['subject'])}, {escape_sql(cbt['chapter'])}, {escape_sql(cbt['total_questions'])}, {escape_sql(cbt['score'])}, {escape_sql(cbt['max_score'])}, {escape_sql(cbt['accuracy'])}, {escape_sql(cbt['time_spent'])}, {escape_sql(cbt['answers_json'])}, {escape_sql(cbt['analytics_json'])}, {escape_sql(cbt['completed_at'])})
ON CONFLICT (id) DO NOTHING;""")

    lines.append("")
    lines.append("COMMIT;")
    lines.append("-- End of Migration Dump")

    return "\n".join(lines)

def run_migration(dry_run=False, dump_sql=False, live=False):
    print("=" * 68)
    print("  ⚡ ClockEE SQLite to Supabase PostgreSQL Migration")
    print("=" * 68)
    print(f"  📂 Source SQLite DB: {DB_PATH}")

    if not os.path.exists(DB_PATH):
        print(f"[!] Error: Source database not found at {DB_PATH}")
        return False

    conn = get_db()
    raw_data = extract_sqlite_data(conn)
    conn.close()

    print(f"  [✓] Extracted from SQLite:")
    print(f"      • Users:          {len(raw_data['users'])}")
    print(f"      • Student States: {len(raw_data['student_states'])}")
    print(f"      • Question Logs:  {len(raw_data['question_logs'])}")
    print(f"      • CBT Exams:      {len(raw_data['cbt_exams'])}")

    transformed = transform_records(raw_data)

    print(f"\n  [✓] Mapped to Supabase PostgreSQL Schema:")
    print(f"      • public.profiles:       {len(transformed['profiles'])} records")
    print(f"      • public.student_states: {len(transformed['student_states'])} records")
    print(f"      • public.study_sessions: {len(transformed['study_sessions'])} records")
    print(f"      • public.cbt_results:    {len(transformed['cbt_results'])} records")

    # Generate SQL dump if requested or by default
    dump_path = os.path.join(CURRENT_DIR, "supabase_migration_dump.sql")
    sql_content = generate_sql_dump(transformed)
    with open(dump_path, "w", encoding="utf-8") as f:
        f.write(sql_content)
    print(f"\n  [✓] Migration SQL Dump generated: {dump_path} ({len(sql_content.splitlines())} lines)")

    if dry_run:
        print("\n  [ℹ️] Dry run complete. No network or remote modifications executed.")
        return True

    # Live Supabase Migration
    sb_ready = is_supabase_configured() and bool(SUPABASE_SERVICE_ROLE_KEY)
    if live or (sb_ready and not dump_sql):
        if not sb_ready:
            print("\n  [!] Supabase Service Role Key is not configured in .env.")
            print("      To execute live upserts, provide SUPABASE_SERVICE_ROLE_KEY in .env.")
            print(f"      You can execute {dump_path} directly in Supabase SQL Editor.")
            return True

        print(f"\n  [🚀] Connecting to Supabase at {SUPABASE_URL} via Service Role Key...")
        try:
            client = get_supabase_client(use_service_role=True)
            if not client:
                print("  [!] Failed to initialize Supabase admin client.")
                return False

            # Batch upsert profiles
            print("  [*] Migrating profiles...")
            for p in transformed["profiles"]:
                client.table("profiles").upsert(p).execute()

            # Batch upsert student_states
            print("  [*] Migrating student_states...")
            for s in transformed["student_states"]:
                client.table("student_states").upsert(s).execute()

            # Batch insert study_sessions
            print("  [*] Migrating study_sessions...")
            for sess in transformed["study_sessions"]:
                client.table("study_sessions").upsert(sess).execute()

            # Batch insert cbt_results
            print("  [*] Migrating cbt_results...")
            for cbt in transformed["cbt_results"]:
                client.table("cbt_results").upsert(cbt).execute()

            print("\n  [🎉] Live Supabase PostgreSQL Migration successfully completed!")
        except Exception as e:
            print(f"\n  [!] Live migration error: {e}")
            print(f"      Fallback to SQL Dump: {dump_path}")
            return False
    else:
        print("\n  [ℹ️] Ready for deployment. Apply dump with Supabase CLI or SQL Editor:")
        print(f"      supabase db execute --file {dump_path}")

    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="ClockEE SQLite to Supabase Migration Tool")
    parser.add_argument("--dry-run", action="store_true", help="Inspect and validate mapping without executing live upserts")
    parser.add_argument("--dump-sql", action="store_true", help="Generate backend/supabase_migration_dump.sql only")
    parser.add_argument("--live", action="store_true", help="Execute live upserts to Supabase instance")
    args = parser.parse_args()

    success = run_migration(dry_run=args.dry_run, dump_sql=args.dump_sql, live=args.live)
    sys.exit(0 if success else 1)
