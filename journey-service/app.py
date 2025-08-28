from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)
PORT = int(os.getenv("PORT", 5005))
AUTH_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
COMM_URL = os.getenv("COMM_SERVICE_URL", "http://localhost:8002")

@app.get("/journey/health")
def health():
    return {"status": "ok", "service": "journey-service"}, 200

@app.post("/journey/start")
def start():
    data = request.json or {}
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"success": False, "message": "user_id required"}), 400
    # TODO: Paste logic from modules/Journey/StudentJourney.py
    # Example: notify
    try:
        requests.post(f"{COMM_URL}/comm/email", json={
            "to": data.get("email", "user@example.com"),
            "subject": "Journey Started",
            "body": f"Journey started for {user_id}"
        }, timeout=5)
    except Exception as e:
        app.logger.warning(f"comm email failed: {e}")
    return jsonify({"success": True, "journey_id": "jny_123"}), 201

@app.get("/journey/status")
def status():
    # Pretend to return status
    return jsonify({"success": True, "status": "in_progress"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)