
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import socket

HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", "8080"))


class SecurityAppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "healthy"
            }).encode())
            return

        if self.path == "/api/status":
            response = {
                "application": "Kubernetes Secure Web App",
                "status": "running",
                "hostname": socket.gethostname()
            }
            body = json.dumps(response).encode()

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if self.path == "/":
            try:
                with open("/app/index.html", "rb") as page:
                    body = page.read()

                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            except OSError:
                self.send_error(500, "Web page unavailable")
            return

        self.send_error(404, "Not found")

    def log_message(self, format_string, *args):
        print(f"{self.client_address[0]} - {format_string % args}")


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), SecurityAppHandler)
    print(f"Security Web App listening on port {PORT}")
    server.serve_forever()
