#!/usr/bin/env python3
"""
MIFECO Dashboard Server
  - Port 5540: HTTP redirect -> HTTPS (for users typing http://)
  - Port 5543: HTTPS serving the dashboard content + API endpoints
"""
import http.server
import ssl
import json
import os
import sys
import threading
from urllib.parse import urlparse

HTTPS_PORT = 5543
HTTP_PORT = 5540
CERT_DIR = os.path.expanduser("~/.hermes/ssl")
DASHBOARD_DIR = os.path.expanduser("~/.hermes/pipeline-engine/dashboard")

# Import the data API
sys.path.insert(0, os.path.expanduser("~/.hermes/pipeline-engine/scripts"))
from pipeline_data_api import handle_request

# ---- HTTPS content + API server ----
class DashboardHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # Serve static files from DASHBOARD_DIR
        if path.startswith("/api/"):
            self._send_json(404, {"error": "GET not supported on API endpoints"})
            return

        # Map / to index.html
        if path == "/":
            path = "/index.html"

        file_path = os.path.join(DASHBOARD_DIR, path.lstrip("/"))

        # Security: no directory traversal
        real_path = os.path.realpath(file_path)
        if not real_path.startswith(os.path.realpath(DASHBOARD_DIR)):
            self._send_json(403, {"error": "Forbidden"})
            return

        if not os.path.isfile(real_path):
            self._send_json(404, {"error": "File not found"})
            return

        # Serve the file
        ext = os.path.splitext(real_path)[1].lower()
        mime_types = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".json": "application/json",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".svg": "image/svg+xml",
            ".ico": "image/x-icon",
        }
        content_type = mime_types.get(ext, "application/octet-stream")

        try:
            with open(real_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(content)
        except IOError:
            self._send_json(500, {"error": "Error reading file"})

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if not path.startswith("/api/"):
            self._send_json(404, {"error": "Not found"})
            return

        # Read request body
        content_length = int(self.headers.get("Content-Length", 0))
        body_bytes = self.rfile.read(content_length) if content_length > 0 else b"{}"
        try:
            body = json.loads(body_bytes)
        except json.JSONDecodeError:
            body = {}

        status, response = handle_request("POST", path, body)
        self._send_json(status, response)

    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _send_json(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        sys.stderr.write("[%s:%d] %s - %s\n" % (
            "HTTPS" if HTTPS_PORT else "HTTP", HTTPS_PORT or HTTP_PORT,
            self.client_address[0], format % args
        ))

# ---- HTTP redirect server ----
class RedirectHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        host = self.headers.get("Host", "192.168.1.77").split(":")[0]
        new_url = "https://%s:%d%s" % (host, HTTPS_PORT, self.path)
        self.send_response(301)
        self.send_header("Location", new_url)
        self.send_header("Connection", "close")
        self.end_headers()

    do_POST = do_GET
    do_PUT = do_GET
    do_DELETE = do_GET
    do_HEAD = do_GET
    do_OPTIONS = do_GET

    def log_message(self, format, *args):
        sys.stderr.write("[REDIR:%d] %s - HTTP->HTTPS\n" % (HTTP_PORT, self.client_address[0]))

# ---- Run functions ----
def run_https():
    os.chdir(DASHBOARD_DIR)
    httpd = http.server.HTTPServer(("0.0.0.0", HTTPS_PORT), DashboardHandler)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(
        certfile=os.path.join(CERT_DIR, "server.crt"),
        keyfile=os.path.join(CERT_DIR, "server.key")
    )
    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)
    httpd.timeout = 60
    print("✅ HTTPS serving on https://0.0.0.0:%d" % HTTPS_PORT, flush=True)
    print("   Dashboard: https://192.168.1.77:%d/pipeline-dashboard.html" % HTTPS_PORT, flush=True)
    httpd.serve_forever()

def run_http_redirect():
    httpd = http.server.HTTPServer(("0.0.0.0", HTTP_PORT), RedirectHandler)
    httpd.timeout = 60
    print("✅ HTTP redirect on http://0.0.0.0:%d -> https://...:%d" % (HTTP_PORT, HTTPS_PORT), flush=True)
    httpd.serve_forever()

if __name__ == "__main__":
    print("═══ MIFECO Dashboard Server ═══", flush=True)
    t = threading.Thread(target=run_http_redirect, daemon=True)
    t.start()
    run_https()