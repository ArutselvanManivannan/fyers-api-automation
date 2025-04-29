from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class AuthCodeHandler(BaseHTTPRequestHandler):
    auth_code = None

    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        AuthCodeHandler.auth_code = query.get("auth_code", [None])[0]

        # Respond to browser
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"<h1> Login successful. You can close this tab now.</h1>")

def start_callback_server(port=5000):
    server = HTTPServer(("127.0.0.1", port), AuthCodeHandler)
    print(f"Waiting for auth code on http://127.0.0.1:{port}/ ...")
    while AuthCodeHandler.auth_code is None:
        server.handle_request()
    return AuthCodeHandler.auth_code