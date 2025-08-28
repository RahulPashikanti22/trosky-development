from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)
PORT = int(os.getenv("PORT", 5003))
AUTH_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")

@app.get("/content/health")
def health():
    return {"status": "ok", "service": "content-service"}, 200

@app.post("/content/generate")
def generate():
    payload = request.json or {}
    # Example of inter-service auth validation (token check)
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    try:
        # In a real scenario, call auth to validate token (stubbed endpoint could be /auth/validate)
        # resp = requests.post(f"{AUTH_URL}/auth/validate", json={"token": token}, timeout=5)
        # if resp.status_code != 200: return jsonify({"success": False, "message": "Invalid token"}), 401
        pass
    except Exception as e:
        app.logger.warning(f"auth validate failed: {e}")
    # TODO: Paste logic from modules/ContenEngine/ContentEngine.py or ContentEngineLib.py
    content = {
        "title": payload.get("title", "Untitled"),
        "body": f"Generated content for: {payload.get('topic', 'general')}"
    }
    return jsonify({"success": True, "content": content}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)