import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from auth import create_jwt, decode_jwt, hash_password, verify_password
from data_store import filter_by_region, load_data, next_id, save_data
from matching import build_matches
from reports import build_dashboard, export_excel, export_pdf


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"


def json_response(handler: BaseHTTPRequestHandler, status: int, payload: dict) -> None:
    body = json.dumps(payload, ensure_ascii=True).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def file_response(handler: BaseHTTPRequestHandler, path: Path, content_type: str) -> None:
    if not path.exists():
        json_response(handler, 404, {"error": "Arquivo nao encontrado."})
        return
    content = path.read_bytes()
    handler.send_response(200)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Content-Length", str(len(content)))
    handler.end_headers()
    handler.wfile.write(content)


class SolidarioHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:
        return

    def _parse_body(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def _require_auth(self):
        auth_header = self.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return None
        token = auth_header.split(" ", 1)[1]
        return decode_jwt(token)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS")
        self.end_headers()

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS")
        super().end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/":
            return file_response(self, FRONTEND_DIR / "index.html", "text/html; charset=utf-8")
        if path == "/styles.css":
            return file_response(self, FRONTEND_DIR / "styles.css", "text/css; charset=utf-8")
        if path == "/app.js":
            return file_response(self, FRONTEND_DIR / "app.js", "application/javascript; charset=utf-8")
        if path == "/api/health":
            return json_response(self, 200, {"status": "ok", "service": "Sistema Solidario API"})

        data = load_data()
        matches = build_matches(data["items"], data["requests"], _float_query(query.get("max_distance", [None])[0]))
        region = query.get("region", [""])[0]

        if path == "/api/users":
            users = [_public_user(user) for user in filter_by_region(data["users"], region)]
            return json_response(self, 200, {"data": users})
        if path == "/api/items":
            return json_response(self, 200, {"data": filter_by_region(data["items"], region)})
        if path == "/api/requests":
            return json_response(self, 200, {"data": filter_by_region(data["requests"], region)})
        if path == "/api/matches":
            return json_response(self, 200, {"data": matches})
        if path == "/api/dashboard":
            return json_response(self, 200, {"data": build_dashboard(data, matches)})
        if path == "/api/reports/export.xlsx":
            dashboard = build_dashboard(data, matches)
            report = export_excel(BASE_DIR / "data" / "relatorio-impacto.xlsx", dashboard, data["items"], data["requests"], matches)
            return file_response(
                self,
                report,
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        if path == "/api/reports/export.pdf":
            dashboard = build_dashboard(data, matches)
            report = export_pdf(BASE_DIR / "data" / "relatorio-impacto.pdf", dashboard, matches)
            return file_response(self, report, "application/pdf")

        return json_response(self, 404, {"error": "Rota nao encontrada."})

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        payload = self._parse_body()
        data = load_data()

        if path == "/api/auth/register":
            try:
                new_user = {
                    "id": next_id(data, "users"),
                    "name": payload["name"],
                    "email": payload["email"],
                    "password_hash": hash_password(payload["password"]),
                    "role": payload["role"],
                    "region": payload["region"],
                    "x": float(payload["x"]),
                    "y": float(payload["y"]),
                }
            except (KeyError, TypeError, ValueError):
                return json_response(self, 400, {"error": "Dados invalidos para cadastro de usuario."})
            data["users"].append(new_user)
            save_data(data)
            return json_response(self, HTTPStatus.CREATED, {"message": "Usuario cadastrado com sucesso.", "user": _public_user(new_user)})

        if path == "/api/auth/login":
            user = next((u for u in data["users"] if u["email"] == payload.get("email")), None)
            if not user or not verify_password(payload.get("password", ""), user.get("password_hash", "")):
                return json_response(self, 401, {"error": "Credenciais invalidas."})
            token = create_jwt({"sub": user["id"], "role": user["role"], "email": user["email"]})
            return json_response(self, 200, {"token": token, "user": _public_user(user)})

        auth = self._require_auth()
        if auth is None:
            return json_response(self, 401, {"error": "Token JWT obrigatorio."})

        if path == "/api/items":
            try:
                item = {
                    "id": next_id(data, "items"),
                    "title": payload["title"],
                    "category": payload["category"],
                    "quantity": int(payload["quantity"]),
                    "status": "disponivel",
                    "donor_id": int(payload["donor_id"]),
                    "region": payload["region"],
                    "x": float(payload["x"]),
                    "y": float(payload["y"]),
                }
            except (KeyError, TypeError, ValueError):
                return json_response(self, 400, {"error": "Dados invalidos para cadastro do item."})
            data["items"].append(item)
            save_data(data)
            return json_response(self, HTTPStatus.CREATED, {"message": "Item cadastrado.", "item": item})

        if path == "/api/requests":
            try:
                request = {
                    "id": next_id(data, "requests"),
                    "beneficiary_id": int(payload["beneficiary_id"]),
                    "category": payload["category"],
                    "description": payload["description"],
                    "needed_quantity": int(payload["needed_quantity"]),
                    "status": "aberta",
                    "region": payload["region"],
                    "x": float(payload["x"]),
                    "y": float(payload["y"]),
                }
            except (KeyError, TypeError, ValueError):
                return json_response(self, 400, {"error": "Dados invalidos para cadastro da solicitacao."})
            data["requests"].append(request)
            save_data(data)
            return json_response(self, HTTPStatus.CREATED, {"message": "Solicitacao cadastrada.", "request": request})

        return json_response(self, 404, {"error": "Rota nao encontrada."})

    def do_PATCH(self):
        parsed = urlparse(self.path)
        path = parsed.path
        payload = self._parse_body()
        data = load_data()

        auth = self._require_auth()
        if auth is None:
            return json_response(self, 401, {"error": "Token JWT obrigatorio."})

        if path.startswith("/api/items/") and path.endswith("/status"):
            try:
                item_id = int(path.split("/")[3])
            except (ValueError, IndexError):
                return json_response(self, 400, {"error": "ID invalido."})

            item = next((item for item in data["items"] if item["id"] == item_id), None)
            if item is None:
                return json_response(self, 404, {"error": "Item nao encontrado."})
            item["status"] = payload.get("status", item["status"])
            save_data(data)
            return json_response(self, 200, {"message": "Status atualizado.", "item": item})

        return json_response(self, 404, {"error": "Rota nao encontrada."})


def _public_user(user: dict) -> dict:
    return {key: value for key, value in user.items() if key != "password_hash"}


def _float_query(value):
    if value in (None, ""):
        return None
    try:
        return float(value)
    except ValueError:
        return None


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8000), SolidarioHandler)
    print("Sistema Solidario rodando em http://127.0.0.1:8000")
    server.serve_forever()
