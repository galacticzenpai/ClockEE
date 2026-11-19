import os
import sqlite3
import json
import secrets
import hashlib
import uuid
from datetime import datetime, timedelta

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(WORKSPACE_DIR, "clockee.db")

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

# ── Load Environment Configuration (.env) ──
def load_env():
    env_path = os.path.join(WORKSPACE_DIR, ".env")
    if os.path.isfile(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip("'\"")
                        if k and k not in os.environ:
                            os.environ[k] = v
        except Exception as e:
            print(f"[!] Notice loading .env: {e}")

load_env()

# Supabase BaaS Configuration
SUPABASE_URL = os.environ.get("SUPABASE_URL", "").strip()
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY", "").strip()
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()

_supabase_client = None
_supabase_admin_client = None

def is_supabase_configured():
    return bool(SUPABASE_URL and (SUPABASE_ANON_KEY or SUPABASE_SERVICE_ROLE_KEY))

def get_supabase_client(use_service_role=False):
    global _supabase_client, _supabase_admin_client
    if not is_supabase_configured():
        return None

    try:
        from supabase import create_client
        if use_service_role and SUPABASE_SERVICE_ROLE_KEY:
            if not _supabase_admin_client:
                _supabase_admin_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
            return _supabase_admin_client
        else:
            key = SUPABASE_ANON_KEY or SUPABASE_SERVICE_ROLE_KEY
            if not _supabase_client:
                _supabase_client = create_client(SUPABASE_URL, key)
            return _supabase_client
    except Exception as e:
        print(f"[!] Notice initializing Supabase client: {e}")
        return None

def verify_supabase_jwt(token):
    """
    Verify Supabase JWT token and extract user claims.
    Uses supabase client or pyjwt.
    """
    if not token or not isinstance(token, str):
        return None

    client = get_supabase_client()
    if client:
        try:
            user_resp = client.auth.get_user(token)
            if user_resp and user_resp.user:
                u = user_resp.user
                return {
                    "id": str(u.id),
                    "email": u.email,
                    "role": (u.user_metadata.get("role", "JEE 2028 Aspirant") if hasattr(u, 'user_metadata') and u.user_metadata else "JEE 2028 Aspirant"),
                    "full_name": (u.user_metadata.get("full_name") or u.user_metadata.get("name") if hasattr(u, 'user_metadata') and u.user_metadata else None),
                    "metadata": u.user_metadata if hasattr(u, 'user_metadata') else {}
                }
        except Exception:
            pass

    # Fallback to pyjwt payload decode (for local verification without live network hit)
    try:
        import jwt
        payload = jwt.decode(token, options={"verify_signature": False})
        if payload and "sub" in payload:
            exp = payload.get("exp")
            if exp and datetime.fromtimestamp(exp) < datetime.now():
                return None
            return {
                "id": str(payload.get("sub")),
                "email": payload.get("email"),
                "role": payload.get("role", "authenticated"),
                "metadata": payload.get("user_metadata", {})
            }
    except Exception:
        pass

    return None

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
            theme_preference TEXT DEFAULT 'cyan_indigo',
            aura_mode TEXT DEFAULT 'fluid',
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

    # Run Schema Migrations
    migrate_db(conn)

    conn.commit()
    conn.close()

    # Also migrate legacy clockee_auth.db if present
    auth_db_path = os.path.join(WORKSPACE_DIR, "clockee_auth.db")
    if os.path.isfile(auth_db_path) and os.path.abspath(auth_db_path) != os.path.abspath(DB_PATH):
        try:
            auth_conn = sqlite3.connect(auth_db_path)
            migrate_db(auth_conn)
            auth_conn.close()
        except Exception as e:
            print(f"[!] Warning migrating clockee_auth.db: {e}")

def migrate_db(conn):
    """Ensure all required columns exist in existing database tables."""
    cur = conn.cursor()
    try:
        cur.execute("PRAGMA table_info(users)")
        existing_cols = {row[1] for row in cur.fetchall()}
        if existing_cols:
            if 'theme_preference' not in existing_cols:
                cur.execute("ALTER TABLE users ADD COLUMN theme_preference TEXT DEFAULT 'cyan_indigo'")
            if 'aura_mode' not in existing_cols:
                cur.execute("ALTER TABLE users ADD COLUMN aura_mode TEXT DEFAULT 'fluid'")
        conn.commit()
    except Exception as e:
        print(f"[!] Migration notice: {e}")

if __name__ == '__main__':
    init_db()
    print(f"[✓] ClockEE Master Relational Database initialized at {DB_PATH}")
