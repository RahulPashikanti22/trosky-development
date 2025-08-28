from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
PORT = int(os.getenv("PORT", 5007))

@app.get("/notify/health")
def health():
    return {"status": "ok", "service": "notification-service"}, 200

@app.post("/notify/sms")
def sms():
    data = request.json or {}
    if not data.get("to") or not data.get("message"):
        return jsonify({"success": False, "message": "Missing to/message"}), 400
    return jsonify({"success": True, "message": "SMS queued", "details": data}), 202

@app.post("/notify/push")
def push():
    data = request.json or {}
    if not data.get("device_id") or not data.get("message"):
        return jsonify({"success": False, "message": "Missing device_id/message"}), 400
    return jsonify({"success": True, "message": "Push notification queued", "details": data}), 202

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)