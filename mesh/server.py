import http.server
import socketserver
import os
import json
import sys
import threading
import time

WORKSPACE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(WORKSPACE)

sys.path.append(os.path.join(WORKSPACE, "mesh"))
import harvest_mesh

PORT = 5500

# Thread-safe in-memory state cache to eliminate Windows file-locking collisions
STATE_LOCK = threading.Lock()
LATEST_STATE = None

def background_harvester():
    """Continuously harvests agent transcripts every 3 seconds in memory and atomic disk write."""
    global LATEST_STATE
    print("🛰️ Continuous Harvester Thread active. Updating every 3s in memory...")
    while True:
        try:
            new_state = harvest_mesh.build_full_tracker_state()
            with STATE_LOCK:
                LATEST_STATE = new_state
        except Exception as e:
            print(f"Harvester warning: {e}")
        time.sleep(3)

class MeshRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_GET(self):
        global LATEST_STATE
        try:
            # Health check endpoint
            if self.path.startswith('/api/health'):
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "healthy", "service": "chitti-mesh", "port": PORT}).encode('utf-8'))
                return

            # Live tracker telemetry endpoint (served from RAM lock)
            if self.path.startswith('/api/tracker'):
                with STATE_LOCK:
                    state = LATEST_STATE
                
                if not state:
                    state_path = os.path.join(WORKSPACE, "mesh", "mesh_tracker_state.json")
                    if os.path.exists(state_path):
                        with open(state_path, "r", encoding="utf-8") as f:
                            state = json.load(f)
                    else:
                        state = harvest_mesh.build_full_tracker_state()
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(state, ensure_ascii=False).encode('utf-8'))
                return
            
            # Route shortcuts
            if self.path == '/' or self.path == '/tracker':
                self.path = '/live_tracker.html'
            elif self.path == '/syllabus':
                self.path = '/tracker.html'
            elif self.path == '/cbt':
                self.path = '/cbt_exam.html'
            
            super().do_GET()
        except (ConnectionResetError, BrokenPipeError):
            pass
        except Exception as e:
            try:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            except:
                pass

    def log_message(self, format, *args):
        # Suppress noisy repetitive polling logs
        if len(args) > 0 and ("/api/tracker" in str(args[0]) or "/api/health" in str(args[0])):
            return
        super().log_message(format, *args)

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

def run_server():
    # Initial synchronous hydration so LATEST_STATE is populated immediately
    global LATEST_STATE
    try:
        with STATE_LOCK:
            LATEST_STATE = harvest_mesh.build_full_tracker_state()
    except Exception as e:
        print(f"Initial hydration note: {e}")

    # Launch background continuous harvester
    harvester_thread = threading.Thread(target=background_harvester, daemon=True)
    harvester_thread.start()

    # Self-healing server loop that never exits on client disconnect
    while True:
        try:
            with ReusableTCPServer(("", PORT), MeshRequestHandler) as httpd:
                print(f"⚡ Resilient Mesh Server running continuously at http://localhost:{PORT}")
                httpd.serve_forever()
        except Exception as e:
            print(f"Server loop recovered from error: {e}. Restarting listener in 1s...")
            time.sleep(1)

if __name__ == "__main__":
    run_server()
