import os
import sqlite3
import json
import secrets
import hashlib
from datetime import datetime, timedelta

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(WORKSPACE_DIR, "clockee.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Enable foreign keys and WAL mode for high performance concurrency
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    return conn

def hash_password(password, salt=None):
    if not salt:
        salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return dk.hex(), salt

def init_db():
    conn = get_db()
    cur = conn.cursor()

    # 1. Users Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'JEE 2028 Aspirant',
            subtitle TEXT DEFAULT '',
            pfp TEXT DEFAULT '',
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            data_json TEXT DEFAULT '{}'
        )
    """)

    # 2. Auth Sessions Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # 3. Student States Table (Full state snapshot)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS student_states (
            user_id TEXT PRIMARY KEY,
            state_json TEXT NOT NULL,
            version INTEGER DEFAULT 1,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # 4. Question Logs Table (Sprint solving & mistake autopsy)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS question_logs (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            subject TEXT NOT NULL,
            chapter TEXT NOT NULL,
            question_num INTEGER DEFAULT 1,
            duration_seconds REAL DEFAULT 0.0,
            is_correct INTEGER DEFAULT 1,
            mistake_tag TEXT DEFAULT '',
            score_delta INTEGER DEFAULT 4,
            notes TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # 5. Tasks / Kanban Matrix Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            title TEXT NOT NULL,
            subject TEXT DEFAULT 'General',
            priority TEXT DEFAULT 'medium',
            completed INTEGER DEFAULT 0,
            due_date TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # 6. Coaching Syllabus Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS coaching_syllabus (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            subject TEXT NOT NULL,
            chapter TEXT NOT NULL,
            block TEXT NOT NULL,
            questions_solved INTEGER DEFAULT 0,
            hours_spent REAL DEFAULT 0.0,
            mastery_pct INTEGER DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # 7. CBT Exams History Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cbt_exams (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            test_id TEXT NOT NULL,
            title TEXT NOT NULL,
            mode TEXT DEFAULT 'mains',
            subject TEXT NOT NULL,
            chapter TEXT DEFAULT '',
            total_questions INTEGER DEFAULT 25,
            time_spent_seconds INTEGER DEFAULT 0,
            score INTEGER DEFAULT 0,
            max_score INTEGER DEFAULT 100,
            accuracy REAL DEFAULT 0.0,
            status TEXT DEFAULT 'completed',
            responses_json TEXT DEFAULT '[]',
            analytics_json TEXT DEFAULT '{}',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # 8. CBT Active Crash Recovery Sessions
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cbt_active_sessions (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            test_id TEXT NOT NULL,
            test_data_json TEXT NOT NULL,
            responses_json TEXT NOT NULL,
            palette_state_json TEXT NOT NULL,
            current_question INTEGER DEFAULT 1,
            remaining_seconds INTEGER DEFAULT 3600,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # 9. Master Question Bank Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id TEXT PRIMARY KEY,
            subject TEXT NOT NULL,
            chapter TEXT NOT NULL,
            topic TEXT DEFAULT '',
            type TEXT DEFAULT 'single',
            difficulty TEXT DEFAULT 'Moderate',
            ideal_time_sec INTEGER DEFAULT 60,
            question_text TEXT NOT NULL,
            options_json TEXT DEFAULT '[]',
            correct_answer TEXT DEFAULT '',
            solution_text TEXT DEFAULT '',
            reference_book TEXT DEFAULT '',
            book_name TEXT DEFAULT '',
            page INTEGER DEFAULT 1,
            section TEXT DEFAULT ''
        )
    """)

    # High-performance search & retrieval indexes
    cur.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(token)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_questions_subj_chap ON questions(subject, chapter)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_questions_subj_diff ON questions(subject, difficulty)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_questions_type ON questions(type)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_logs_user_subj ON question_logs(user_id, subject)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_tasks_user ON tasks(user_id, completed)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_cbt_exams_user ON cbt_exams(user_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_syllabus_user ON coaching_syllabus(user_id, subject)")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print(f"[✓] ClockEE Master Relational Database initialized at {DB_PATH}")
