"""
Antigravity Manager Cockpit - Local Loopback Server
Serves the private Antigravity Mesh Cockpit on 127.0.0.1:9099 with automatic routing.
"""
import http.server
import socketserver
import os
import sys

PORT = 9099
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class CockpitHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT_DIR, **kwargs)

    def do_GET(self):
        if self.path in ("/", "/cockpit", "/manager"):
            self.path = "/antigravity_manager.html"
        return super().do_GET()

def main():
    os.chdir(ROOT_DIR)
    with socketserver.TCPServer(("127.0.0.1", PORT), CockpitHandler) as httpd:
        print(f"🚀 Antigravity Manager Cockpit running at http://127.0.0.1:{PORT}")
        print("Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down cockpit server.")

if __name__ == "__main__":
    main()
