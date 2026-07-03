from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from picnic_adapter import optimize_picnic_basket


ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "app" / "static"


DEFAULT_ITEMS = [
    {"id": "sandwiches", "name": "Sandwiches", "weight": 3, "happiness": 8, "heat_penalty": 1, "rain_penalty": 0},
    {"id": "lemonade", "name": "Lemonade", "weight": 2, "happiness": 5, "heat_penalty": 0, "rain_penalty": 1},
    {"id": "blanket", "name": "Blanket", "weight": 4, "happiness": 6, "heat_penalty": 0, "rain_penalty": 0},
    {"id": "ice_cream", "name": "Ice cream", "weight": 2, "happiness": 10, "heat_penalty": 9, "rain_penalty": 0},
    {"id": "fruit", "name": "Fruit", "weight": 2, "happiness": 6, "heat_penalty": 0, "rain_penalty": 0},
    {"id": "cards", "name": "Cards", "weight": 1, "happiness": 7, "heat_penalty": 0, "rain_penalty": 6},
    {"id": "thermos", "name": "Thermos", "weight": 3, "happiness": 7, "heat_penalty": 0, "rain_penalty": 0},
    {"id": "poncho", "name": "Poncho", "weight": 2, "happiness": 4, "heat_penalty": 0, "rain_penalty": 0},
]


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self._send_file(STATIC / "index.html", "text/html; charset=utf-8")
            return
        if self.path == "/api/items":
            self._json({"items": DEFAULT_ITEMS})
            return
        if self.path == "/app.js":
            self._send_file(STATIC / "app.js", "application/javascript")
            return
        if self.path == "/style.css":
            self._send_file(STATIC / "style.css", "text/css")
            return
        self.send_error(404)

    def do_POST(self):
        if self.path != "/api/optimize":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("content-length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            result = optimize_picnic_basket(
                payload.get("items", DEFAULT_ITEMS),
                payload.get("constraints", {}),
            )
            self._json({"ok": True, "result": result})
        except Exception as exc:
            self._json({"ok": False, "error": str(exc)}, status=500)

    def _send_file(self, path: Path, content_type: str):
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("content-type", content_type)
        self.send_header("content-length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _json(self, value: dict, status: int = 200):
        data = json.dumps(value).encode()
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        return


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 8789), Handler)
    print("Picnic optimizer running at http://127.0.0.1:8789")
    server.serve_forever()


if __name__ == "__main__":
    main()
