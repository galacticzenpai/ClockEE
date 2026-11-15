#!/usr/bin/env python3
"""
⚡ ClockEE — Master Full-Stack Tactical Cockpit Server & Backend Engine
Autonomous JEE Advanced OS & Cognitive CBT Simulation Platform
"""

import os
import sys
import json
import sqlite3
import mimetypes
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import urllib.parse

# Setup paths
WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(WORKSPACE_DIR, "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from backend.db import DB_PATH, init_db, get_db
from backend.seed import seed_database
from backend.api import ClockEEBackendRouter

# Ensure standard MIME types are loaded
mimetypes.init()
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("application/json", ".json")
mimetypes.add_type("image/svg+xml", ".svg")
mimetypes.add_type("image/png", ".png")
mimetypes.add_type("image/jpeg", ".jpg")
mimetypes.add_type("text/html", ".html")

class ClockEEServerHandler(SimpleHTTPRequestHandler):
    """
    High-performance multi-threaded request handler for ClockEE.
    Serves static assets and routes REST API, Cloud Sync, and CBT endpoints.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WORKSPACE_DIR, **kwargs)

    def send_json(self, status_code, data):
        body = json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With, Cache-Control')
        self.send_header('Access-Control-Max-Age', '86400')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        return True

    def do_OPTIONS(self):
        """Handle CORS pre-flight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With, Cache-Control')
        self.send_header('Access-Control-Max-Age', '86400')
        self.send_header('Content-Length', '0')
        self.end_headers()
        return True

    def do_GET(self):
        # 1. Check if routed by API or Firebase Cloud Sync
        if ClockEEBackendRouter.handle_request(self, 'GET'):
            return

        # 2. Default to static file serving
        return super().do_GET()

    def do_POST(self):
        if ClockEEBackendRouter.handle_request(self, 'POST'):
            return
        self.send_json(404, {"error": "Endpoint not found", "path": self.path, "method": "POST"})

    def do_PUT(self):
        if ClockEEBackendRouter.handle_request(self, 'PUT'):
            return
        self.send_json(404, {"error": "Endpoint not found", "path": self.path, "method": "PUT"})

    def do_PATCH(self):
        if ClockEEBackendRouter.handle_request(self, 'PATCH'):
            return
        self.send_json(404, {"error": "Endpoint not found", "path": self.path, "method": "PATCH"})

    def do_DELETE(self):
        if ClockEEBackendRouter.handle_request(self, 'DELETE'):
            return
        self.send_json(404, {"error": "Endpoint not found", "path": self.path, "method": "DELETE"})

    def log_message(self, format, *args):
        # Clean terminal output formatting
        try:
            msg = format % args
            sys.stderr.write(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        except Exception:
            pass

def print_banner(port):
    print("=" * 68)
    print("  ⚡ ClockEE Master Tactical Cockpit Engine & Backend Server")
    print("=" * 68)
    print(f"  🌐 Local Server:        http://127.0.0.1:{port}/")
    print(f"  🏆 Hackathon Showcase:  http://127.0.0.1:{port}/hackathon.html")
    print(f"  🐻 Interactive Login:   http://127.0.0.1:{port}/login.html")
    print(f"  🎯 Tactical Sprint:     http://127.0.0.1:{port}/timer.html")
    print(f"  📝 CBT Exam Arena:      http://127.0.0.1:{port}/cbt_home.html")
    print(f"  🛡️ Master Admin Panel:  http://127.0.0.1:{port}/admin.html")
    print(f"  💾 SQLite Database:     {DB_PATH}")
    print("-" * 68)
    print("  🔑 Pre-Seeded Evaluation Credentials:")
    print("     • Student Alpha:     alpha@clockee.app  /  password123")
    print("     • Student Beta:      beta@clockee.app   /  password456")
    print("     • Master Admin:      admin@clockee.app  /  admin123")
    print("-" * 68)
    print("  🚀 Endpoints Active:")
    print("     • Auth API:          POST /api/signin, POST /api/signup, POST /api/check-email")
    print("     • Cloud Sync API:    GET/PUT /students/<id>/state.json, GET /students.json")
    print("     • Question Bank:     GET /api/questions, GET /api/questions/random (5,775 Qs)")
    print("     • Sprints & Logs:    GET/POST /api/logs")
    print("     • Tasks Kanban:      GET/POST/PUT/DELETE /api/tasks")
    print("     • CBT Crash Engine:  POST /api/cbt/crash-save, GET /api/cbt/crash-resume")
    print("     • Diagnostics:       GET /clockee.json, GET /api/health")
    print("=" * 68)
    print("  Ready for incoming connections. Press Ctrl+C to terminate.\n")

def run_server(port=8000):
    init_db()

    # Ensure pre-seeded accounts exist
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    user_count = cur.fetchone()[0]
    conn.close()

    if user_count == 0:
        print("[*] Database empty. Running initial database seed...")
        seed_database()

    # Attempt binding to port with fallback
    server = None
    for p in [port, 8080, 8008, 8888, 5000]:
        try:
            server = ThreadingHTTPServer(('127.0.0.1', p), ClockEEServerHandler)
            port = p
            break
        except OSError as e:
            if "address already in use" in str(e).lower() or e.errno == 10048:
                continue
            raise

    if not server:
        print(f"[!] Could not bind to ports {port}, 8080, 8008, 8888.")
        sys.exit(1)

    print_banner(port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down ClockEE Server cleanly...")
        server.server_close()

if __name__ == '__main__':
    run_server()
