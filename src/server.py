"""Stdlib HTTP server for Sandbox Ops Agent. Run: python3 src/server.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from http.server import BaseHTTPRequestHandler, HTTPServer
from agents import run_task, SandboxExecutor

class Handler(BaseHTTPRequestHandler):
    def _send(self, payload, code=200):
        data = json.dumps(payload).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data))); self.end_headers()
        self.wfile.write(data)
    def do_GET(self):
        if self.path == "/api/health":
            return self._send({"status": "ok", "mode": "mock-vultr-sandbox"})
        path = "public/index.html" if self.path in ("/", "/index.html") else self.path.lstrip("/")
        if os.path.exists(path) and path.startswith("public/"):
            data = open(path, "rb").read()
            self.send_response(200); self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data)
        else:
            self._send({"error": "not found"}, 404)
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length) or b"{}")
        if self.path == "/api/run":
            try:
                return self._send(run_task(body.get("task", "")))
            except ValueError as exc:
                return self._send({"error": str(exc)}, 400)
        if self.path == "/api/containment-demo":
            # Deliberately unsafe code, to be BLOCKED by the sandbox.
            result = SandboxExecutor().run(body.get("code", "rm -rf /"))
            return self._send(result)
        return self._send({"error": "not found"}, 404)
    def log_message(self, *args):
        pass

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8001"))
    print(f"Sandbox Ops Agent on http://localhost:{port}/  (mock Vultr sandbox)")
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
