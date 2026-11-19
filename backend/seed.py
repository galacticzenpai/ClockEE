import os
import sys
import json
import sqlite3
from datetime import datetime, timedelta

# Ensure parent directory is in path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, CURRENT_DIR)

from db import get_db, hash_password, init_db

def seed_database(force_questions=False):
    init_db()
    conn = get_db()
    cur = conn.cursor()

    print("[*] Starting ClockEE Database Seeding...")

    # ─────────────────────────────────────────────────────────────
    # 1. SEED TEST ACCOUNTS (Alpha, Beta, Admin)
    # ─────────────────────────────────────────────────────────────

    # 1.1 Student Alpha (Active Aspirant)
    alpha_id = "user_alpha"
    alpha_email = "alpha@clockee.app"
    alpha_name = "Student Alpha"
    alpha_role = "JEE 2028 Aspirant"
    alpha_subtitle = "JEE 2028 Advanced • IIT Bombay Target (AIR < 50)"
    alpha_pfp = "https://api.dicebear.com/7.x/bottts-neutral/svg?seed=AlphaCommander"
    alpha_pwd_hash, alpha_salt = hash_password("password123")

    # Sample realistic state for Alpha
    alpha_state = {
        "profile": {
            "name": alpha_name,
            "subtitle": alpha_subtitle,
            "pfp": alpha_pfp,
            "accent": "#00f2fe"
        },
        "examMode": "advanced",
        "dailyGoals": { "Physics": 35, "Chemistry": 35, "Maths": 35, "hours": 7.5 },
        "jeeDate": "2028-05-17",
        "nextMilestone": { "date": "2026-11-20", "title": "Phase Major Test #01 (Rotational Dynamics & Thermodynamics)" },
        "settings": { "dynamicAura": True, "auraTheme": "cyan_indigo", "auraSpeed": "fluid" },
        "apiKeys": { "ticktick": "", "gemini": "", "cloudUrl": "http://127.0.0.1:8000" },
        "stats": {
            "hoursToday": 5.8,
            "streakDays": 14,
            "questionsSolved": { "Physics": 64, "Chemistry": 58, "Maths": 63 },
            "todayTarget": 105
        },
        "tasks": [
            { "id": "task_a1", "title": "Solve Irodov 1.15 to 1.30 (Rigid Body Rotational Dynamics)", "subject": "Physics", "priority": "high", "completed": False },
            { "id": "task_a2", "title": "Review GOC Electrophilic Addition Reaction Mechanisms", "subject": "Chemistry", "priority": "medium", "completed": False },
            { "id": "task_a3", "title": "Master Definite Integrals with Leibniz Rule PYQs (2020-2025)", "subject": "Maths", "priority": "high", "completed": False },
            { "id": "task_a4", "title": "Complete Chemistry CBT Latency Speed Drill", "subject": "Chemistry", "priority": "low", "completed": True }
        ],
        "questionLogs": [
            { "id": "log_a1", "subject": "Physics", "chapter": "Rotational Motion", "qNum": 1, "duration": 42.4, "correct": True, "notes": "Moment of inertia of composite cone", "timestamp": "2026-11-15T18:10:00Z" },
            { "id": "log_a2", "subject": "Physics", "chapter": "Rotational Motion", "qNum": 2, "duration": 88.1, "correct": False, "mistake": "calculation", "notes": "Missed parallel axis theorem offset d^2 term", "timestamp": "2026-11-15T18:12:00Z" },
            { "id": "log_a3", "subject": "Chemistry", "chapter": "Thermodynamics", "qNum": 1, "duration": 52.0, "correct": True, "notes": "Adiabatic expansion reversible vs irreversible work done", "timestamp": "2026-11-15T19:00:00Z" },
            { "id": "log_a4", "subject": "Maths", "chapter": "Definite Integration", "qNum": 1, "duration": 110.5, "correct": True, "notes": "King's property f(a+b-x) symmetry", "timestamp": "2026-11-15T20:15:00Z" }
        ],
        "mockTests": [
            {
                "testId": "cbt_mock_001",
                "title": "JEE Advanced 2025 Paper-1 Full Mock",
                "score": 248,
                "maxScore": 360,
                "accuracy": 82.5,
                "date": "2026-11-14T14:30:00Z",
                "breakdown": { "Physics": 84, "Chemistry": 88, "Maths": 76 }
            }
        ]
    }

    # 1.2 Student Beta (Isolated Aspirant)
    beta_id = "user_beta"
    beta_email = "beta@clockee.app"
    beta_name = "Student Beta"
    beta_role = "JEE 2028 Aspirant"
    beta_subtitle = "JEE 2028 Aspirant • Strict Cloud Isolation"
    beta_pfp = "https://api.dicebear.com/7.x/bottts-neutral/svg?seed=BetaAspirant"
    beta_pwd_hash, beta_salt = hash_password("password456")

    beta_state = {
        "profile": {
            "name": beta_name,
            "subtitle": beta_subtitle,
            "pfp": beta_pfp,
            "accent": "#a855f7"
        },
        "examMode": "mains",
        "dailyGoals": { "Physics": 30, "Chemistry": 30, "Maths": 30, "hours": 6.0 },
        "jeeDate": "2028-05-17",
        "nextMilestone": { "date": "2026-11-22", "title": "Coaching Phase Unit Test #02" },
        "settings": { "dynamicAura": True, "auraTheme": "space_violet", "auraSpeed": "fluid" },
        "apiKeys": { "ticktick": "", "gemini": "", "cloudUrl": "http://127.0.0.1:8000" },
        "stats": {
            "hoursToday": 3.2,
            "streakDays": 4,
            "questionsSolved": { "Physics": 18, "Chemistry": 22, "Maths": 20 },
            "todayTarget": 90
        },
        "tasks": [
            { "id": "task_b1", "title": "Kinematics Relative Velocity Projectile Problems", "subject": "Physics", "priority": "high", "completed": False },
            { "id": "task_b2", "title": "Chemical Bonding Molecular Orbital Theory Diagrams", "subject": "Chemistry", "priority": "medium", "completed": False }
        ],
        "questionLogs": [
            { "id": "log_b1", "subject": "Physics", "chapter": "Kinematics", "qNum": 1, "duration": 55.0, "correct": True, "notes": "Rain man relative vector approach", "timestamp": "2026-11-15T15:00:00Z" }
        ],
        "mockTests": []
    }

    # 1.3 Master Admin & Mentor
    admin_id = "user_master_admin"
    admin_email = "admin@clockee.app"
    admin_name = "Master Admin & Mentor"
    admin_role = "Mentor / Faculty"
    admin_subtitle = "Director of Academic Roster & System Architecture"
    admin_pfp = "https://api.dicebear.com/7.x/bottts-neutral/svg?seed=ClockEECommander"
    admin_pwd_hash, admin_salt = hash_password("admin123")

    admin_state = {
        "profile": {
            "name": admin_name,
            "subtitle": admin_subtitle,
            "pfp": admin_pfp,
            "accent": "#6366f1"
        },
        "role": "Mentor / Faculty",
        "isAdmin": True,
        "settings": { "dynamicAura": True, "auraTheme": "cyan_indigo", "auraSpeed": "fluid" }
    }

    users_to_seed = [
        (alpha_id, alpha_email, alpha_name, alpha_role, alpha_subtitle, alpha_pfp, alpha_pwd_hash, alpha_salt, 0, "cyan_indigo", "fluid", json.dumps(alpha_state)),
        (beta_id, beta_email, beta_name, beta_role, beta_subtitle, beta_pfp, beta_pwd_hash, beta_salt, 0, "space_violet", "fluid", json.dumps(beta_state)),
        (admin_id, admin_email, admin_name, admin_role, admin_subtitle, admin_pfp, admin_pwd_hash, admin_salt, 1, "cyan_indigo", "fluid", json.dumps(admin_state))
    ]

    for u in users_to_seed:
        cur.execute("""
            INSERT OR REPLACE INTO users (id, email, name, role, subtitle, pfp, password_hash, salt, is_admin, theme_preference, aura_mode, data_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, u)
        
        # Also seed into student_states
        cur.execute("""
            INSERT OR REPLACE INTO student_states (user_id, state_json)
            VALUES (?, ?)
        """, (u[0], u[11]))

    print(f"[✓] Pre-seeded 3 core test accounts: Alpha, Beta, Admin")

    # ─────────────────────────────────────────────────────────────
    # 2. SEED SAMPLE RELATIONAL DATA (Tasks, Logs, CBT, Syllabus)
    # ─────────────────────────────────────────────────────────────

    # Seed Alpha's tasks
    for t in alpha_state["tasks"]:
        cur.execute("""
            INSERT OR REPLACE INTO tasks (id, user_id, title, subject, priority, completed)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (t["id"], alpha_id, t["title"], t["subject"], t["priority"], 1 if t.get("completed") else 0))

    # Seed Alpha's logs
    for ql in alpha_state["questionLogs"]:
        cur.execute("""
            INSERT OR REPLACE INTO question_logs (id, user_id, subject, chapter, question_num, duration_seconds, is_correct, mistake_tag, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (ql["id"], alpha_id, ql["subject"], ql["chapter"], ql.get("qNum", 1), ql.get("duration", 60.0), 1 if ql.get("correct") else 0, ql.get("mistake", ""), ql.get("notes", "")))

    # Seed Alpha's CBT mock
    cur.execute("""
        INSERT OR REPLACE INTO cbt_exams (id, user_id, test_id, title, mode, subject, total_questions, time_spent_seconds, score, max_score, accuracy, status, analytics_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, ("exam_a1", alpha_id, "cbt_mock_001", "JEE Advanced 2025 Paper-1 Full Mock", "advanced", "Full", 54, 10800, 248, 360, 82.5, "completed", json.dumps(alpha_state["mockTests"][0])))

    # Seed Coaching Syllabus for Alpha
    syllabus_samples = [
        ("Physics", "Kinematics 1D & 2D", "previous", 95, 12.5, 95),
        ("Physics", "Rotational Dynamics", "in_progress", 48, 8.0, 65),
        ("Physics", "Gravitation", "next", 0, 0.0, 0),
        ("Chemistry", "Atomic Structure", "previous", 80, 10.0, 90),
        ("Chemistry", "Thermodynamics", "in_progress", 42, 6.5, 60),
        ("Chemistry", "Chemical Bonding", "next", 0, 0.0, 0),
        ("Maths", "Quadratic Equations", "previous", 85, 9.0, 92),
        ("Maths", "Definite Integration", "in_progress", 56, 11.0, 70),
        ("Maths", "Conic Sections", "next", 0, 0.0, 0),
    ]
    for idx, (sub, chap, blk, qs, hrs, mast) in enumerate(syllabus_samples):
        cur.execute("""
            INSERT OR REPLACE INTO coaching_syllabus (id, user_id, subject, chapter, block, questions_solved, hours_spent, mastery_pct)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (f"syl_a_{idx}", alpha_id, sub, chap, blk, qs, hrs, mast))

    print(f"[✓] Pre-seeded relational logs, tasks, coaching syllabus, and CBT exams.")

    # ─────────────────────────────────────────────────────────────
    # 3. SEED MASTER QUESTION BANK (5,775 JEE PYQ Questions)
    # ─────────────────────────────────────────────────────────────
    cur.execute("SELECT COUNT(*) FROM questions")
    q_count = cur.fetchone()[0]

    if q_count == 0 or force_questions:
        q_file = os.path.join(ROOT_DIR, "cbt_question_bank.json")
        if os.path.isfile(q_file):
            print(f"[*] Ingesting master question bank from {os.path.basename(q_file)} into SQLite...")
            try:
                with open(q_file, "r", encoding="utf-8") as f:
                    q_data = json.load(f)
                
                rows_to_insert = []
                for q in q_data:
                    qid = q.get("id") or f"q_{len(rows_to_insert)}"
                    sub = q.get("subject", "General")
                    chap = q.get("chapter", "Mixed Chapters")
                    topic = q.get("topic", "")
                    qtype = q.get("type", "single")
                    diff = q.get("difficulty", "Moderate")
                    ideal_time = q.get("idealTimeSec", 60)
                    text = q.get("text", "")
                    options = json.dumps(q.get("options", []))
                    correct = str(q.get("correct", q.get("correctNum", "")))
                    sol = q.get("solution", q.get("sol", ""))
                    ref_book = q.get("referenceBook", "")
                    book_name = q.get("bookName", "")
                    page = q.get("page", 1)
                    sec = q.get("section", "")

                    rows_to_insert.append((
                        qid, sub, chap, topic, qtype, diff, ideal_time,
                        text, options, correct, sol, ref_book, book_name, page, sec
                    ))

                cur.executemany("""
                    INSERT OR REPLACE INTO questions (
                        id, subject, chapter, topic, type, difficulty, ideal_time_sec,
                        question_text, options_json, correct_answer, solution_text,
                        reference_book, book_name, page, section
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, rows_to_insert)

                print(f"[✓] Successfully ingested {len(rows_to_insert)} questions into 'questions' table!")
            except Exception as e:
                print(f"[!] Warning while ingesting question bank: {e}")
        else:
            print(f"[!] {q_file} not found; skipping question bank population.")
    else:
        print(f"[i] Question bank already populated with {q_count} questions. Skipping question re-ingestion.")

    conn.commit()
    conn.close()
    print("[✓] ClockEE Database Seeding Completed Successfully!")

if __name__ == '__main__':
    seed_database()
