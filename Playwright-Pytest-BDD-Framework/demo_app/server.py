"""Fictional, in-memory local service. No employer assets or external services."""

import argparse, json, secrets, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

PRODUCTS = [
    {"sku": "notebook", "name": "Demo Notebook", "price_cents": 1250},
    {"sku": "mug", "name": "Demo Mug", "price_cents": 900},
]
USERS = {f"sample{i:02}": f"DemoOnly{i:02}!" for i in range(1, 21)}


class Server(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address):
        self.lock = threading.RLock()
        self.sessions = {}
        self.orders = {}
        super().__init__(address, Handler)

    def user(self, token):
        with self.lock:
            now = time.monotonic()
            self.sessions = {k: v for k, v in self.sessions.items() if v[1] > now}
            return self.sessions.get(token, (None, 0))[0]


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):
        pass

    def send(self, status, payload=None, content_type="application/json"):
        raw = (
            (
                json.dumps(payload).encode()
                if content_type == "application/json"
                else payload
            )
            if payload is not None
            else b""
        )
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Request-ID", secrets.token_hex(8))
        self.end_headers()
        if raw:
            self.wfile.write(raw)

    def body(self):
        size = int(self.headers.get("Content-Length", "0"))
        if not 0 <= size <= 16384:
            raise ValueError("body too large")
        value = json.loads(self.rfile.read(size))
        if not isinstance(value, dict):
            raise ValueError("JSON object required")
        return value

    def do_GET(self):
        self.dispatch("GET")

    def do_POST(self):
        self.dispatch("POST")

    def do_DELETE(self):
        self.dispatch("DELETE")

    def dispatch(self, method):
        path = urlsplit(self.path).path
        s = self.server
        if method == "GET" and path in ["/", "/login", "/shop"]:
            return self.send(
                200,
                Path(__file__).with_name("index.html").read_bytes(),
                "text/html; charset=utf-8",
            )
        if method == "GET" and path == "/health":
            return self.send(200, {"status": "ok", "service": "fictional-sample-store"})
        try:
            data = self.body() if method == "POST" else {}
        except (ValueError, UnicodeError):
            return self.send(400, {"error": "invalid_json"})
        if method == "POST" and path == "/api/login":
            name = data.get("username")
            password = data.get("password")
            if (
                not isinstance(name, str)
                or not isinstance(password, str)
                or USERS.get(name) != password
            ):
                return self.send(401, {"error": "invalid_credentials"})
            token = secrets.token_urlsafe(24)
            with s.lock:
                s.sessions[token] = (name, time.monotonic() + 300)
            return self.send(200, {"token": token, "username": name, "expires_in": 300})
        token = self.headers.get("Authorization", "").removeprefix("Bearer ")
        user = s.user(token)
        if not user:
            return self.send(401, {"error": "unauthorized"})
        if method == "POST" and path == "/api/logout":
            with s.lock:
                s.sessions.pop(token, None)
            return self.send(204)
        if method == "GET" and path == "/api/products":
            return self.send(200, {"products": PRODUCTS})
        if method == "POST" and path == "/api/orders":
            sku = data.get("sku")
            qty = data.get("quantity")
            product = next((p for p in PRODUCTS if p["sku"] == sku), None)
            if not product:
                return self.send(400, {"error": "unknown_product"})
            if type(qty) is not int or not 1 <= qty <= 10:
                return self.send(400, {"error": "invalid_quantity"})
            order = {
                "id": secrets.token_hex(8),
                "owner": user,
                "sku": sku,
                "quantity": qty,
                "unit_price_cents": product["price_cents"],
                "total_cents": product["price_cents"] * qty,
                "status": "created",
            }
            with s.lock:
                s.orders[order["id"]] = order
            return self.send(201, order)
        if path.startswith("/api/orders/"):
            oid = path.rsplit("/", 1)[1]
            with s.lock:
                order = s.orders.get(oid)
                if order is None:
                    return self.send(404, {"error": "not_found"})
                if order["owner"] != user:
                    return self.send(403, {"error": "forbidden"})
                if method == "GET":
                    return self.send(200, order)
                if method == "DELETE":
                    del s.orders[oid]
                    return self.send(204)
        return self.send(404, {"error": "not_found"})


def start_server(port=0):
    s = Server(("127.0.0.1", port))
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=8765)
    a = p.parse_args()
    s = Server(("127.0.0.1", a.port))
    print(f"Sample Store ready at http://127.0.0.1:{s.server_port}", flush=True)
    try:
        s.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        s.server_close()
