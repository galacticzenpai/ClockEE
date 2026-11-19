import http.server
import socketserver
import os
import json
import sys
import threading
import time

# Ensure workspace root is working directory
WORKSPACE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(WORKSPACE)

sys.path.append(os.path.join(WORKSPACE, "mesh"))
import harvest_mesh

PORT = 5500

def background_harvester():
    """Continuously harvests agent transcripts every 3 seconds in the background."""
    print("🛰️ Continuous Harvester Thread active. Updating every 3s...")
    while True:
        try:
            harvest_mesh.build_full_tracker_state()
        except Exception as e:
            print(f"Harvester error: {e}")
        time.sleep(3)

class MeshRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_GET(self):
        if self.path.startswith('/api/tracker'):
            try:
                # Read latest pre-compiled state from disk or build on the fly
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
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            return
        
        # Route root or /tracker to live_tracker.html
        if self.path == '/' or self.path == '/tracker':
            self.path = '/live_tracker.html'
        
        super().do_GET()

def run_server():
    # Start continuous background harvester thread
    harvester_thread = threading.Thread(target=background_harvester, daemon=True)
    harvester_thread.start()

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), MeshRequestHandler) as httpd:
        print(f"⚡ Mesh Server running continuously at http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
