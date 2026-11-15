import os
import json
import sqlite3
import hashlib
import secrets
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(WORKSPACE_DIR, "clockee_auth.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_json TEXT DEFAULT '{}'
        )
    """)
    conn.commit()
    conn.close()

init_db()

def hash_password(password, salt=None):
    if not salt:
        salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
    return dk.hex(), salt

class ClockEEAuthHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WORKSPACE_DIR, **kwargs)

    def send_json(self, status_code, data):
        body = json.dumps(data).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Content-Length', '0')
        self.end_headers()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b'{}'
        try:
            req = json.loads(post_data.decode('utf-8') or '{}')
        except Exception:
            req = {}

        if parsed.path == '/api/check-email':
            email = req.get('email', '').strip().lower()
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT id, name FROM users WHERE email = ?", (email,))
            row = cur.fetchone()
            conn.close()
            return self.send_json(200, {"exists": bool(row), "name": row[1] if row else ""})

        elif parsed.path == '/api/signup':
            email = req.get('email', '').strip().lower()
            password = req.get('password', '')
            name = req.get('name', '').strip()
            role = req.get('role', 'JEE 2028 Aspirant')
            
            if not email or len(email) < 5 or '@' not in email:
                return self.send_json(400, {"error": "Invalid email address format."})
            if not password or len(password) < 8:
                return self.send_json(400, {"error": "Password must be at least 8 characters."})
            if not name or len(name) < 2:
                return self.send_json(400, {"error": "Name must be at least 2 characters."})
                
            pwd_hash, salt = hash_password(password)
            user_id = "user_" + secrets.token_hex(8)
            
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            try:
                cur.execute(
                    "INSERT INTO users (id, email, name, role, password_hash, salt, data_json) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (user_id, email, name, role, pwd_hash, salt, json.dumps({}))
                )
                conn.commit()
            except sqlite3.IntegrityError:
                conn.close()
                return self.send_json(409, {"error": "An account with this email already exists."})
            conn.close()
            
            return self.send_json(200, {
                "success": True,
                "user": {
                    "uid": user_id,
                    "email": email,
                    "name": name,
                    "role": role,
                    "pfp": f"https://api.dicebear.com/7.x/bottts-neutral/svg?seed={urllib.parse.quote(name)}"
                }
            })

        elif parsed.path == '/api/signin':
            email = req.get('email', '').strip().lower()
            password = req.get('password', '')
            
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT id, name, role, password_hash, salt, data_json FROM users WHERE email = ?", (email,))
            row = cur.fetchone()
            conn.close()
            
            if not row:
                return self.send_json(404, {"error": "Account not found. Please register first."})
                
            user_id, name, role, stored_hash, salt, data_json = row
            check_hash, _ = hash_password(password, salt)
            
            if check_hash != stored_hash:
                return self.send_json(401, {"error": "Invalid email or password. Please verify credentials."})
                
            return self.send_json(200, {
                "success": True,
                "user": {
                    "uid": user_id,
                    "email": email,
                    "name": name,
                    "role": role,
                    "pfp": f"https://api.dicebear.com/7.x/bottts-neutral/svg?seed={urllib.parse.quote(name)}"
                },
                "userData": json.loads(data_json or '{}')
            })

        elif parsed.path == '/api/userdata':
            email = req.get('email', '').strip().lower()
            user_data = req.get('data', {})
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("UPDATE users SET data_json = ? WHERE email = ?", (json.dumps(user_data), email))
            conn.commit()
            conn.close()
            return self.send_json(200, {"success": True})

        else:
            self.send_error(404, "Endpoint not found")

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path.startswith('/api/userdata'):
            qs = urllib.parse.parse_qs(parsed.query)
            email = qs.get('email', [''])[0].strip().lower()
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("SELECT data_json FROM users WHERE email = ?", (email,))
            row = cur.fetchone()
            conn.close()
            if row:
                return self.send_json(200, {"success": True, "data": json.loads(row[0] or '{}')})
            else:
                return self.send_json(404, {"error": "User not found"})
        return super().do_GET()

if __name__ == '__main__':
    port = 8000
    server = HTTPServer(('127.0.0.1', port), ClockEEAuthHandler)
    print(f"ClockEE Full Stack Server running at http://127.0.0.1:{port}/")
    server.serve_forever()
