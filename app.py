from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from urllib.parse import urlparse, parse_qs

DATA_FILE = os.environ.get(
    "DATA_FILE",
    "/var/lib/backend_data/messages.json"
)


def load_messages():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_messages(messages):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(messages, file, ensure_ascii=False, indent=2)


class APIHandler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/health":
            self.send_json(200, {"status": "active", "service": "python-crud-api"})
        elif path == "/messages":
            self.send_json(200, {"messages": load_messages()})
        else:
            self.send_json(404, {"error": "Endpoint tidak ditemukan"})

    def do_POST(self):
        if urlparse(self.path).path != "/messages":
            self.send_json(404, {"error": "Endpoint tidak ditemukan"})
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, json.JSONDecodeError):
            self.send_json(400, {"error": "Format JSON tidak valid"})
            return

        message = data.get("message")
        if not message:
            self.send_json(400, {"error": "Field 'message' wajib diisi"})
            return

        messages = load_messages()
        messages.append({"message": message})
        save_messages(messages)
        self.send_json(201, {"message": "Data berhasil ditambahkan"})

    def do_DELETE(self):
        parsed = urlparse(self.path)
        if parsed.path != "/messages":
            self.send_json(404, {"error": "Endpoint tidak ditemukan"})
            return

        try:
            index = int(parse_qs(parsed.query).get("index", [""])[0])
            messages = load_messages()
            if index < 0 or index >= len(messages):
                self.send_json(404, {"error": "Data tidak ditemukan"})
                return

            deleted = messages.pop(index)
            save_messages(messages)
            self.send_json(200, {"message": "Data berhasil dihapus", "deleted": deleted})
        except ValueError:
            self.send_json(400, {"error": "Gunakan format /messages?index=0"})

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 5000), APIHandler)
    print("API berjalan pada port 5000")
    server.serve_forever()