import os
import sys
import json
import sqlite3
import secrets
import urllib.parse
from datetime import datetime, timedelta

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, CURRENT_DIR)

from db import get_db, hash_password, DB_PATH
from seed import seed_database

def parse_body(handler):
    content_length = int(handler.headers.get('Content-Length', 0))
    if content_length > 0:
        data = handler.rfile.read(content_length)
        try:
            return json.loads(data.decode('utf-8'))
        except Exception:
            return {}
    return {}

def get_auth_user_id(handler):
    # Try Authorization header: Bearer <token>
    auth_header = handler.headers.get('Authorization', '')
    token = None
    if auth_header.startswith('Bearer '):
        token = auth_header.split('Bearer ', 1)[1].strip()
    
    # Or query string ?token=...
    parsed = urllib.parse.urlparse(handler.path)
    qs = urllib.parse.parse_qs(parsed.query)
    if not token and 'token' in qs:
        token = qs['token'][0]

    if token:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT user_id, expires_at FROM sessions WHERE token = ?", (token,))
        row = cur.fetchone()
        conn.close()
        if row:
            try:
                expires = datetime.fromisoformat(row['expires_at'])
                if expires > datetime.now():
                    return row['user_id']
            except Exception:
                return row['user_id']
    
    # Fallback to query param ?user_id=... or ?email=...
    if 'user_id' in qs:
        return qs['user_id'][0]
    if 'email' in qs:
        email = qs['email'][0].strip().lower()
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE email = ?", (email,))
        row = cur.fetchone()
        conn.close()
        if row:
            return row['id']
            
    return None

class ClockEEBackendRouter:
    """
    Central API router handling REST, dual-mode Firebase Realtime DB emulation,
    Master Question Bank querying, CBT crash-recovery, and full telemetry.
    """

    @staticmethod
    def handle_request(handler, method):
        parsed = urllib.parse.urlparse(handler.path)
        path = parsed.path
        qs = urllib.parse.parse_qs(parsed.query)

        # ── 1. SYSTEM HEALTH & DIAGNOSTICS (Firebase & ClockEE Ping) ──
        if path == '/clockee.json' or path == '/api/health':
            conn = get_db()
            cur = conn.cursor()
            tables = ['users', 'student_states', 'question_logs', 'tasks', 'cbt_exams', 'questions']
            counts = {}
            for t in tables:
                try:
                    cur.execute(f"SELECT COUNT(*) FROM {t}")
                    counts[t] = cur.fetchone()[0]
                except Exception:
                    counts[t] = 0
            conn.close()

            db_size_kb = round(os.path.getsize(DB_PATH) / 1024, 2) if os.path.exists(DB_PATH) else 0

            return handler.send_json(200, {
                "status": "online",
                "app": "ClockEE Master Tactical Engine",
                "version": "2.0.0",
                "database": "SQLite 3 (WAL mode)",
                "db_size_kb": db_size_kb,
                "counts": counts,
                "timestamp": datetime.now().isoformat()
            })

        # ── 2. AUTHENTICATION & SESSIONS ──
        if path == '/api/check-email' and method == 'POST':
            req = parse_body(handler)
            email = req.get('email', '').strip().lower()
            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT id, name, role FROM users WHERE email = ?", (email,))
            row = cur.fetchone()
            conn.close()
            return handler.send_json(200, {
                "exists": bool(row),
                "name": row['name'] if row else "",
                "role": row['role'] if row else ""
            })

        if (path == '/api/signup' or path == '/api/auth/register') and method == 'POST':
            req = parse_body(handler)
            email = req.get('email', '').strip().lower()
            password = req.get('password', '')
            name = req.get('name', '').strip()
            role = req.get('role', 'JEE 2028 Aspirant')

            if not email or len(email) < 5 or '@' not in email:
                return handler.send_json(400, {"error": "Invalid email address format."})
            if not password or len(password) < 8:
                return handler.send_json(400, {"error": "Password must be at least 8 characters long."})
            if not name or len(name) < 2:
                return handler.send_json(400, {"error": "Name must be at least 2 characters."})

            pwd_hash, salt = hash_password(password)
            user_id = "user_" + secrets.token_hex(8)
            pfp = f"https://api.dicebear.com/7.x/bottts-neutral/svg?seed={urllib.parse.quote(name)}"

            initial_state = {
                "profile": { "name": name, "subtitle": f"{role} • Cloud Account", "pfp": pfp, "accent": "#00f2fe" },
                "examMode": "mains",
                "dailyGoals": { "Physics": 30, "Chemistry": 30, "Maths": 30, "hours": 6.0 },
                "jeeDate": "2028-05-17",
                "tasks": [],
                "questionLogs": [],
                "mockTests": [],
                "stats": { "hoursToday": 0.0, "streakDays": 1, "questionsSolved": { "Physics": 0, "Chemistry": 0, "Maths": 0 } }
            }

            conn = get_db()
            cur = conn.cursor()
            try:
                cur.execute("""
                    INSERT INTO users (id, email, name, role, subtitle, pfp, password_hash, salt, data_json)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (user_id, email, name, role, f"{role} • Cloud Account", pfp, pwd_hash, salt, json.dumps(initial_state)))

                cur.execute("""
                    INSERT INTO student_states (user_id, state_json) VALUES (?, ?)
                """, (user_id, json.dumps(initial_state)))

                # Generate session token
                session_token = secrets.token_hex(24)
                expires_at = (datetime.now() + timedelta(days=30)).isoformat()
                cur.execute("""
                    INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)
                """, (session_token, user_id, expires_at))

                conn.commit()
            except sqlite3.IntegrityError:
                conn.close()
                return handler.send_json(409, {"error": "An account with this email already exists."})
            conn.close()

            return handler.send_json(200, {
                "success": True,
                "token": session_token,
                "user": {
                    "uid": user_id,
                    "id": user_id,
                    "email": email,
                    "name": name,
                    "role": role,
                    "pfp": pfp
                },
                "userData": initial_state
            })

        if (path == '/api/signin' or path == '/api/auth/login') and method == 'POST':
            req = parse_body(handler)
            email = req.get('email', '').strip().lower()
            password = req.get('password', '')

            conn = get_db()
            cur = conn.cursor()
            cur.execute("""
                SELECT id, name, role, subtitle, pfp, password_hash, salt, is_admin, data_json
                FROM users WHERE email = ?
            """, (email,))
            row = cur.fetchone()

            if not row:
                conn.close()
                return handler.send_json(404, {"error": "Account not found. Please register first."})

            user_id = row['id']
            name = row['name']
            role = row['role']
            subtitle = row['subtitle']
            pfp = row['pfp'] or f"https://api.dicebear.com/7.x/bottts-neutral/svg?seed={urllib.parse.quote(name)}"
            stored_hash = row['password_hash']
            salt = row['salt']
            is_admin = bool(row['is_admin'])

            check_hash, _ = hash_password(password, salt)
            if check_hash != stored_hash:
                conn.close()
                return handler.send_json(401, {"error": "Invalid email or password. Please verify credentials."})

            # Fetch fresh state from student_states
            cur.execute("SELECT state_json FROM student_states WHERE user_id = ?", (user_id,))
            state_row = cur.fetchone()
            state_data = json.loads(state_row['state_json'] if state_row else (row['data_json'] or '{}'))

            # Issue session token
            session_token = secrets.token_hex(24)
            expires_at = (datetime.now() + timedelta(days=30)).isoformat()
            cur.execute("INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)", (session_token, user_id, expires_at))
            cur.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()

            return handler.send_json(200, {
                "success": True,
                "token": session_token,
                "user": {
                    "uid": user_id,
                    "id": user_id,
                    "email": email,
                    "name": name,
                    "role": role,
                    "subtitle": subtitle,
                    "pfp": pfp,
                    "isAdmin": is_admin
                },
                "userData": state_data
            })

        if path == '/api/auth/me' or path == '/api/me':
            uid = get_auth_user_id(handler)
            if not uid:
                return handler.send_json(401, {"error": "Not authenticated"})
            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT id, email, name, role, subtitle, pfp, is_admin FROM users WHERE id = ?", (uid,))
            user_row = cur.fetchone()
            cur.execute("SELECT state_json FROM student_states WHERE user_id = ?", (uid,))
            state_row = cur.fetchone()
            conn.close()

            if not user_row:
                return handler.send_json(404, {"error": "User profile not found"})

            return handler.send_json(200, {
                "user": dict(user_row),
                "state": json.loads(state_row['state_json']) if state_row else {}
            })

        # ── 3. DUAL-MODE FIREBASE REALTIME DB EMULATION & STUDENT STATE SYNC ──

        # 3.1 Fetch all students (/students.json or /api/students)
        if (path == '/students.json' or path == '/api/students') and method == 'GET':
            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT u.id, u.email, u.name, u.role, u.subtitle, u.pfp, u.is_admin, u.created_at, s.state_json FROM users u LEFT JOIN student_states s ON u.id = s.user_id")
            rows = cur.fetchall()
            conn.close()

            result = {}
            for r in rows:
                state_data = json.loads(r['state_json'] or '{}') if r['state_json'] else {}
                result[r['id']] = {
                    "profile": {
                        "name": r['name'],
                        "email": r['email'],
                        "role": r['role'],
                        "subtitle": r['subtitle'],
                        "pfp": r['pfp'],
                        "isAdmin": bool(r['is_admin']),
                        "createdAt": r['created_at']
                    },
                    "state": state_data
                }
            return handler.send_json(200, result)

        # 3.2 Individual Student State Sync (/students/{id}/state.json or /api/students/{id}/state)
        # Supports GET and PUT (pushToCloud / pullFromCloud)
        if '/state' in path and (path.startswith('/students/') or path.startswith('/api/students/')):
            # Extract user id from path
            # /students/<id>/state.json or /api/students/<id>/state
            parts = path.strip('/').split('/')
            user_id = parts[1] if parts[0] == 'students' else parts[2]
            user_id = user_id.replace('.json', '')

            if method == 'GET':
                conn = get_db()
                cur = conn.cursor()
                cur.execute("SELECT state_json FROM student_states WHERE user_id = ?", (user_id,))
                row = cur.fetchone()
                if not row:
                    cur.execute("SELECT data_json FROM users WHERE id = ?", (user_id,))
                    row = cur.fetchone()
                conn.close()

                if row and (row['state_json'] if 'state_json' in row.keys() else row['data_json']):
                    raw = row['state_json'] if 'state_json' in row.keys() else row['data_json']
                    return handler.send_json(200, json.loads(raw or '{}'))
                return handler.send_json(404, {"error": "Student state not found"})

            elif method in ('PUT', 'POST'):
                state_body = parse_body(handler)
                state_json_str = json.dumps(state_body)

                conn = get_db()
                cur = conn.cursor()
                # Update student_states
                cur.execute("""
                    INSERT INTO student_states (user_id, state_json, updated_at)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                    ON CONFLICT(user_id) DO UPDATE SET state_json = excluded.state_json, updated_at = CURRENT_TIMESTAMP
                """, (user_id, state_json_str))

                # Update users.data_json
                cur.execute("UPDATE users SET data_json = ? WHERE id = ?", (state_json_str, user_id))

                # Also automatically synchronize relational tasks and question logs if present in state
                try:
                    tasks = state_body.get('tasks', [])
                    for t in tasks:
                        if isinstance(t, dict) and t.get('title'):
                            tid = t.get('id') or f"task_{secrets.token_hex(4)}"
                            cur.execute("""
                                INSERT OR REPLACE INTO tasks (id, user_id, title, subject, priority, completed)
                                VALUES (?, ?, ?, ?, ?, ?)
                            """, (tid, user_id, t.get('title'), t.get('subject', 'General'), t.get('priority', 'medium'), 1 if t.get('completed') else 0))

                    logs = state_body.get('questionLogs', [])
                    for ql in logs:
                        if isinstance(ql, dict) and ql.get('subject'):
                            lid = ql.get('id') or f"log_{secrets.token_hex(4)}"
                            cur.execute("""
                                INSERT OR REPLACE INTO question_logs (id, user_id, subject, chapter, question_num, duration_seconds, is_correct, mistake_tag, notes)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (lid, user_id, ql.get('subject'), ql.get('chapter', 'Mixed'), ql.get('qNum', 1), ql.get('duration', 60.0), 1 if ql.get('correct') else 0, ql.get('mistake', ''), ql.get('notes', '')))
                except Exception as sync_e:
                    print(f"[!] Relational extraction error: {sync_e}")

                conn.commit()
                conn.close()
                return handler.send_json(200, {"success": True, "user_id": user_id, "updated_at": datetime.now().isoformat()})

        # 3.3 Student Profile Update (/students/{id}/profile.json or /api/students/{id}/profile)
        if '/profile' in path and (path.startswith('/students/') or path.startswith('/api/students/')):
            parts = path.strip('/').split('/')
            user_id = parts[1] if parts[0] == 'students' else parts[2]
            user_id = user_id.replace('.json', '')

            if method in ('PATCH', 'POST', 'PUT'):
                req = parse_body(handler)
                conn = get_db()
                cur = conn.cursor()

                name = req.get('name')
                role = req.get('role')
                subtitle = req.get('subtitle')

                if name:
                    cur.execute("UPDATE users SET name = ? WHERE id = ?", (name, user_id))
                if role:
                    cur.execute("UPDATE users SET role = ? WHERE id = ?", (role, user_id))
                if subtitle:
                    cur.execute("UPDATE users SET subtitle = ? WHERE id = ?", (subtitle, user_id))

                # Also update inside student_states JSON
                cur.execute("SELECT state_json FROM student_states WHERE user_id = ?", (user_id,))
                s_row = cur.fetchone()
                if s_row and s_row['state_json']:
                    try:
                        s_obj = json.loads(s_row['state_json'])
                        s_obj['profile'] = s_obj.get('profile', {})
                        if name: s_obj['profile']['name'] = name
                        if role: s_obj['profile']['role'] = role
                        if subtitle: s_obj['profile']['subtitle'] = subtitle
                        cur.execute("UPDATE student_states SET state_json = ? WHERE user_id = ?", (json.dumps(s_obj), user_id))
                    except Exception:
                        pass

                conn.commit()
                conn.close()
                return handler.send_json(200, {"success": True, "user_id": user_id})

        # 3.4 Delete Student Account (/students/{id}.json or /api/students/{id})
        if (path.startswith('/students/') or path.startswith('/api/students/')) and method == 'DELETE':
            parts = path.strip('/').split('/')
            user_id = parts[1] if parts[0] == 'students' else parts[2]
            user_id = user_id.replace('.json', '')

            conn = get_db()
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()
            return handler.send_json(200, {"success": True, "deleted_id": user_id})

        # 3.5 Legacy /api/userdata (GET / POST)
        if path == '/api/userdata':
            if method == 'POST':
                req = parse_body(handler)
                email = req.get('email', '').strip().lower()
                user_data = req.get('data', {})
                conn = get_db()
                cur = conn.cursor()
                cur.execute("UPDATE users SET data_json = ? WHERE email = ?", (json.dumps(user_data), email))
                # Also find id and update student_states
                cur.execute("SELECT id FROM users WHERE email = ?", (email,))
                row = cur.fetchone()
                if row:
                    cur.execute("""
                        INSERT INTO student_states (user_id, state_json) VALUES (?, ?)
                        ON CONFLICT(user_id) DO UPDATE SET state_json = excluded.state_json, updated_at = CURRENT_TIMESTAMP
                    """, (row['id'], json.dumps(user_data)))
                conn.commit()
                conn.close()
                return handler.send_json(200, {"success": True})
            elif method == 'GET':
                email = qs.get('email', [''])[0].strip().lower()
                conn = get_db()
                cur = conn.cursor()
                cur.execute("SELECT data_json FROM users WHERE email = ?", (email,))
                row = cur.fetchone()
                conn.close()
                if row:
                    return handler.send_json(200, {"success": True, "data": json.loads(row['data_json'] or '{}')})
                return handler.send_json(404, {"error": "User not found"})

        # ── 4. MASTER QUESTION BANK API (5,775 JEE PYQs) ──

        # 4.1 Filtered Question Query
        if path == '/api/questions' and method == 'GET':
            sub = qs.get('subject', [None])[0]
            chap = qs.get('chapter', [None])[0]
            diff = qs.get('difficulty', [None])[0]
            qtype = qs.get('type', [None])[0]
            search = qs.get('q', [None])[0]
            limit = min(int(qs.get('limit', [30])[0]), 100)
            offset = int(qs.get('offset', [0])[0])

            query = "SELECT * FROM questions WHERE 1=1"
            params = []

            if sub and sub != 'Full' and sub != 'All':
                query += " AND subject = ?"
                params.append(sub)
            if chap and chap.lower() != 'all' and 'mixed' not in chap.lower():
                query += " AND (chapter LIKE ? OR topic LIKE ?)"
                params.extend([f"%{chap}%", f"%{chap}%"])
            if diff:
                query += " AND difficulty = ?"
                params.append(diff)
            if qtype:
                query += " AND type = ?"
                params.append(qtype)
            if search:
                query += " AND question_text LIKE ?"
                params.append(f"%{search}%")

            conn = get_db()
            cur = conn.cursor()
            
            # Count total matching
            count_query = query.replace("SELECT *", "SELECT COUNT(*)", 1)
            cur.execute(count_query, params)
            total_matching = cur.fetchone()[0]

            query += f" LIMIT {limit} OFFSET {offset}"
            cur.execute(query, params)
            rows = cur.fetchall()
            conn.close()

            questions = []
            for r in rows:
                q = dict(r)
                q['options'] = json.loads(q['options_json'] or '[]')
                questions.append(q)

            return handler.send_json(200, {
                "total": total_matching,
                "limit": limit,
                "offset": offset,
                "questions": questions
            })

        # 4.2 Dynamic Adaptive Test Generator (Random balanced question pool)
        if path == '/api/questions/random' and method == 'GET':
            sub = qs.get('subject', ['Full'])[0]
            chap = qs.get('chapter', [''])[0]
            count = min(int(qs.get('count', [25])[0]), 90)

            conn = get_db()
            cur = conn.cursor()
            pool = []

            if sub == 'Full':
                per_sub = count // 3
                rem = count - (per_sub * 2)
                for s, n in [('Physics', per_sub), ('Chemistry', per_sub), ('Maths', rem)]:
                    cur.execute(f"SELECT * FROM questions WHERE subject = ? ORDER BY RANDOM() LIMIT {n}", (s,))
                    pool.extend([dict(r) for r in cur.fetchall()])
            else:
                norm_chap = chap.strip()
                if norm_chap and norm_chap.lower() != 'all' and 'mixed' not in norm_chap.lower():
                    cur.execute(f"""
                        SELECT * FROM questions
                        WHERE subject = ? AND (chapter LIKE ? OR topic LIKE ?)
                        ORDER BY RANDOM() LIMIT {count}
                    """, (sub, f"%{norm_chap}%", f"%{norm_chap}%"))
                    pool = [dict(r) for r in cur.fetchall()]

                # If chapter pool is smaller than required, fill from same subject
                if len(pool) < count:
                    needed = count - len(pool)
                    cur.execute(f"SELECT * FROM questions WHERE subject = ? ORDER BY RANDOM() LIMIT {needed}", (sub,))
                    pool.extend([dict(r) for r in cur.fetchall()])

            conn.close()

            # Format for CBT exam runner
            formatted = []
            for idx, q in enumerate(pool[:count]):
                q['num'] = idx + 1
                q['options'] = json.loads(q.get('options_json') or '[]')
                try:
                    q['correct'] = int(q['correct_answer'])
                except (ValueError, TypeError):
                    try:
                        q['correctNum'] = float(q['correct_answer'])
                    except Exception:
                        q['correct'] = 0
                formatted.append(q)

            return handler.send_json(200, {
                "subject": sub,
                "chapter": chap,
                "count": len(formatted),
                "questions": formatted
            })

        # 4.3 Chapter List with Question Counts
        if path == '/api/questions/chapters' and method == 'GET':
            conn = get_db()
            cur = conn.cursor()
            cur.execute("""
                SELECT subject, chapter, COUNT(*) as count
                FROM questions
                GROUP BY subject, chapter
                ORDER BY subject ASC, count DESC
            """)
            rows = cur.fetchall()
            conn.close()

            grouped = {"Physics": [], "Chemistry": [], "Maths": []}
            for r in rows:
                sub = r['subject']
                if sub in grouped:
                    grouped[sub].append({ "chapter": r['chapter'], "count": r['count'] })

            return handler.send_json(200, grouped)

        # ── 5. QUESTION LOGS & SPRINT CADENCE API ──
        if path == '/api/logs':
            if method == 'GET':
                uid = get_auth_user_id(handler) or 'user_alpha'
                sub = qs.get('subject', [None])[0]
                limit = int(qs.get('limit', [50])[0])

                conn = get_db()
                cur = conn.cursor()
                if sub:
                    cur.execute("SELECT * FROM question_logs WHERE user_id = ? AND subject = ? ORDER BY created_at DESC LIMIT ?", (uid, sub, limit))
                else:
                    cur.execute("SELECT * FROM question_logs WHERE user_id = ? ORDER BY created_at DESC LIMIT ?", (uid, limit))
                rows = cur.fetchall()
                conn.close()

                return handler.send_json(200, {"logs": [dict(r) for r in rows]})

            elif method == 'POST':
                req = parse_body(handler)
                uid = req.get('user_id') or get_auth_user_id(handler) or 'user_alpha'
                lid = req.get('id') or f"log_{secrets.token_hex(6)}"
                sub = req.get('subject', 'Physics')
                chap = req.get('chapter', 'General')
                qnum = req.get('qNum', 1)
                dur = float(req.get('duration', 0.0))
                correct = 1 if req.get('correct') else 0
                mistake = req.get('mistake', '')
                score_delta = req.get('scoreDelta', 4 if correct else -1)
                notes = req.get('notes', '')

                conn = get_db()
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO question_logs (id, user_id, subject, chapter, question_num, duration_seconds, is_correct, mistake_tag, score_delta, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (lid, uid, sub, chap, qnum, dur, correct, mistake, score_delta, notes))
                conn.commit()
                conn.close()

                return handler.send_json(200, {"success": True, "id": lid})

        # ── 6. TASKS & KANBAN MATRIX API ──
        if path == '/api/tasks':
            if method == 'GET':
                uid = get_auth_user_id(handler) or 'user_alpha'
                conn = get_db()
                cur = conn.cursor()
                cur.execute("SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC", (uid,))
                rows = cur.fetchall()
                conn.close()
                return handler.send_json(200, {"tasks": [dict(r) for r in rows]})

            elif method == 'POST':
                req = parse_body(handler)
                uid = req.get('user_id') or get_auth_user_id(handler) or 'user_alpha'
                tid = req.get('id') or f"task_{secrets.token_hex(6)}"
                title = req.get('title', '').strip()
                sub = req.get('subject', 'General')
                priority = req.get('priority', 'medium')
                due = req.get('due_date', '')

                if not title:
                    return handler.send_json(400, {"error": "Task title is required"})

                conn = get_db()
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO tasks (id, user_id, title, subject, priority, completed, due_date)
                    VALUES (?, ?, ?, ?, ?, 0, ?)
                """, (tid, uid, title, sub, priority, due))
                conn.commit()
                conn.close()

                return handler.send_json(200, {"success": True, "id": tid})

        if path.startswith('/api/tasks/') and method in ('PUT', 'PATCH', 'DELETE'):
            tid = path.split('/api/tasks/')[1]
            conn = get_db()
            cur = conn.cursor()

            if method == 'DELETE':
                cur.execute("DELETE FROM tasks WHERE id = ?", (tid,))
                conn.commit()
                conn.close()
                return handler.send_json(200, {"success": True, "deleted_id": tid})

            elif method in ('PUT', 'PATCH'):
                req = parse_body(handler)
                if 'completed' in req:
                    cur.execute("UPDATE tasks SET completed = ? WHERE id = ?", (1 if req['completed'] else 0, tid))
                if 'priority' in req:
                    cur.execute("UPDATE tasks SET priority = ? WHERE id = ?", (req['priority'], tid))
                if 'title' in req:
                    cur.execute("UPDATE tasks SET title = ? WHERE id = ?", (req['title'], tid))
                conn.commit()
                conn.close()
                return handler.send_json(200, {"success": True, "id": tid})

        # ── 7. CBT EXAM SESSION & CRASH-PROOF RECOVERY API ──
        if path == '/api/cbt/crash-save' and method == 'POST':
            req = parse_body(handler)
            uid = req.get('user_id') or get_auth_user_id(handler) or 'user_alpha'
            tid = req.get('test_id')
            if not tid:
                return handler.send_json(400, {"error": "test_id is required"})

            session_id = f"{uid}_{tid}"
            test_data = json.dumps(req.get('test_data', {}))
            responses = json.dumps(req.get('responses', {}))
            palette = json.dumps(req.get('palette', {}))
            curr_q = req.get('current_question', 1)
            rem_sec = req.get('remaining_seconds', 3600)

            conn = get_db()
            cur = conn.cursor()
            cur.execute("""
                INSERT OR REPLACE INTO cbt_active_sessions (
                    id, user_id, test_id, test_data_json, responses_json, palette_state_json, current_question, remaining_seconds, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (session_id, uid, tid, test_data, responses, palette, curr_q, rem_sec))
            conn.commit()
            conn.close()

            return handler.send_json(200, {"success": True, "checkpoint": session_id})

        if path == '/api/cbt/crash-resume' and method == 'GET':
            uid = qs.get('user_id', [None])[0] or get_auth_user_id(handler) or 'user_alpha'
            tid = qs.get('test_id', [None])[0]
            if not tid:
                return handler.send_json(400, {"error": "test_id is required"})

            session_id = f"{uid}_{tid}"
            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM cbt_active_sessions WHERE id = ?", (session_id,))
            row = cur.fetchone()
            conn.close()

            if not row:
                return handler.send_json(404, {"error": "No active crash recovery session found"})

            return handler.send_json(200, {
                "test_data": json.loads(row['test_data_json'] or '{}'),
                "responses": json.loads(row['responses_json'] or '{}'),
                "palette": json.loads(row['palette_state_json'] or '{}'),
                "current_question": row['current_question'],
                "remaining_seconds": row['remaining_seconds'],
                "updated_at": row['updated_at']
            })

        if path == '/api/cbt/exams':
            if method == 'GET':
                uid = qs.get('user_id', [None])[0] or get_auth_user_id(handler) or 'user_alpha'
                conn = get_db()
                cur = conn.cursor()
                cur.execute("SELECT * FROM cbt_exams WHERE user_id = ? ORDER BY created_at DESC", (uid,))
                rows = cur.fetchall()
                conn.close()
                return handler.send_json(200, {"exams": [dict(r) for r in rows]})

            elif method == 'POST':
                req = parse_body(handler)
                uid = req.get('user_id') or get_auth_user_id(handler) or 'user_alpha'
                eid = req.get('id') or f"exam_{secrets.token_hex(6)}"
                tid = req.get('test_id') or f"test_{int(datetime.now().timestamp())}"
                title = req.get('title', 'CBT Test')
                mode = req.get('mode', 'mains')
                sub = req.get('subject', 'Full')
                chap = req.get('chapter', '')
                tot_q = req.get('total_questions', 25)
                time_s = req.get('time_spent_seconds', 0)
                score = req.get('score', 0)
                max_score = req.get('max_score', 100)
                acc = float(req.get('accuracy', 0.0))
                resp_json = json.dumps(req.get('responses', []))
                ana_json = json.dumps(req.get('analytics', {}))

                conn = get_db()
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO cbt_exams (
                        id, user_id, test_id, title, mode, subject, chapter, total_questions,
                        time_spent_seconds, score, max_score, accuracy, status, responses_json, analytics_json, completed_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'completed', ?, ?, CURRENT_TIMESTAMP)
                """, (eid, uid, tid, title, mode, sub, chap, tot_q, time_s, score, max_score, acc, resp_json, ana_json))

                # Clean up active crash session
                cur.execute("DELETE FROM cbt_active_sessions WHERE id = ?", (f"{uid}_{tid}",))

                conn.commit()
                conn.close()
                return handler.send_json(200, {"success": True, "exam_id": eid})

        # ── 7.5 SIMULATION TELEMETRY & ERROR AUTOPSY TO MAIN CONTROL ──
        if path == '/api/simulations/report':
            if method == 'POST':
                req = parse_body(handler)
                uid = req.get('user_id') or get_auth_user_id(handler) or 'user_alpha'
                sim_id = req.get('test_id') or f"sim_{secrets.token_hex(6)}"
                title = req.get('title', 'JEE Exam Simulation')
                sub = req.get('subject', 'Full')
                score = req.get('score', 0)
                max_score = req.get('max_score', 300)
                acc = float(req.get('accuracy', 0.0))
                tot_q = req.get('total_questions', 75)
                mistakes = req.get('mistakes', [])
                ana = req.get('analytics', {})

                conn = get_db()
                cur = conn.cursor()

                # 1. Store in cbt_exams
                cur.execute("""
                    INSERT INTO cbt_exams (
                        id, user_id, test_id, title, mode, subject, chapter, total_questions,
                        time_spent_seconds, score, max_score, accuracy, status, responses_json, analytics_json, completed_at
                    ) VALUES (?, ?, ?, ?, 'simulation', ?, 'Main Control Simulation', ?, ?, ?, ?, ?, 'completed', ?, ?, CURRENT_TIMESTAMP)
                """, (
                    f"sim_exam_{secrets.token_hex(4)}", uid, sim_id, title, sub, tot_q,
                    int(ana.get('avgLatencySec', 75) * tot_q), score, max_score, acc,
                    json.dumps(mistakes), json.dumps(ana)
                ))

                # 2. Store question error logs and tasks for each mistake
                tasks_created = 0
                for m in mistakes:
                    q_num = m.get('qNum', 1)
                    m_sub = m.get('subject', sub)
                    m_cat = m.get('errorCategory', 'Calculation Mistake')
                    m_topic = m.get('topic') or m.get('chapter') or 'Concept Problem'
                    
                    cur.execute("""
                        INSERT INTO question_logs (
                            id, user_id, subject, chapter, question_num, duration_seconds,
                            is_correct, mistake_tag, score_delta, notes
                        ) VALUES (?, ?, ?, ?, ?, ?, 0, ?, -1, ?)
                    """, (
                        f"qlog_{secrets.token_hex(6)}", uid, m_sub, m.get('chapter', 'Simulation Autopsy'),
                        q_num, float(m.get('timeSpentSec', 75)), m_cat, m.get('reasonDetail', '')
                    ))

                    # Create actionable task in tasks table
                    task_id = f"task_autopsy_{secrets.token_hex(4)}"
                    task_title = f"[Autopsy] Master Error Q#{q_num}: {m_topic}"
                    cur.execute("""
                        INSERT INTO tasks (id, user_id, title, subject, priority, completed, due_date)
                        VALUES (?, ?, ?, ?, 'high', 0, CURRENT_DATE)
                    """, (task_id, uid, task_title, m_sub))
                    tasks_created += 1

                # 3. Update student_states snapshot if exists
                cur.execute("SELECT state_json FROM student_states WHERE user_id = ?", (uid,))
                row = cur.fetchone()
                if row:
                    try:
                        st = json.loads(row['state_json'] or '{}')
                        st['mistakeVault'] = st.get('mistakeVault', [])
                        st['simulations'] = st.get('simulations', [])
                        st['simulations'].insert(0, {
                            'id': sim_id, 'title': title, 'subject': sub, 'score': score,
                            'maxScore': max_score, 'accuracy': acc, 'errorsCount': len(mistakes),
                            'timestamp': int(datetime.now().timestamp() * 1000)
                        })
                        for m in mistakes:
                            if not any(x.get('id') == m.get('id') for x in st['mistakeVault']):
                                st['mistakeVault'].insert(0, m)
                        cur.execute("UPDATE student_states SET state_json = ?, updated_at = CURRENT_TIMESTAMP WHERE user_id = ?", (json.dumps(st), uid))
                    except Exception as e:
                        pass

                conn.commit()
                conn.close()

                return handler.send_json(200, {
                    "success": True,
                    "simulation_id": sim_id,
                    "errors_logged": len(mistakes),
                    "tasks_created": tasks_created,
                    "message": f"Successfully processed simulation & forwarded {len(mistakes)} errors to Main Control"
                })

            elif method == 'GET':
                uid = qs.get('user_id', [None])[0] or get_auth_user_id(handler) or 'user_alpha'
                conn = get_db()
                cur = conn.cursor()
                cur.execute("SELECT * FROM cbt_exams WHERE user_id = ? AND mode = 'simulation' ORDER BY created_at DESC LIMIT 20", (uid,))
                sims = [dict(r) for r in cur.fetchall()]
                cur.execute("SELECT * FROM question_logs WHERE user_id = ? AND is_correct = 0 ORDER BY created_at DESC LIMIT 30", (uid,))
                errors = [dict(r) for r in cur.fetchall()]
                conn.close()
                return handler.send_json(200, {"simulations": sims, "recent_errors": errors})

        # ── 8. ADMIN ACTIONS (Re-seed & Backup Export) ──
        if path == '/api/admin/seed' and method == 'POST':
            seed_database(force_questions=True)
            return handler.send_json(200, {"success": True, "message": "Database successfully re-seeded!"})

        if path == '/api/admin/export' and method == 'GET':
            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT id, email, name, role, is_admin, data_json FROM users")
            users = [dict(r) for r in cur.fetchall()]
            cur.execute("SELECT * FROM question_logs ORDER BY created_at DESC LIMIT 100")
            logs = [dict(r) for r in cur.fetchall()]
            cur.execute("SELECT * FROM tasks")
            tasks = [dict(r) for r in cur.fetchall()]
            cur.execute("SELECT * FROM cbt_exams")
            exams = [dict(r) for r in cur.fetchall()]
            conn.close()

            return handler.send_json(200, {
                "backup_date": datetime.now().isoformat(),
                "users": users,
                "logs": logs,
                "tasks": tasks,
                "exams": exams
            })

        # Endpoint not recognized by API router
        return False
