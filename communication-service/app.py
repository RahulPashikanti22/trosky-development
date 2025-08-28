from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
PORT = int(os.getenv("PORT", 5000))

@app.get("/comm/health")
def health():
    return {"status": "ok", "service": "communication-service"}, 200

@app.post("/comm/email")
def send_email():
    data = request.json or {}
    # TODO: Replace with logic from modules/CommunicationModule/CommunicationEngine.py
    # Here we just echo the payload to simulate a send
    if not data.get("to") or not data.get("subject"):
        return jsonify({"success": False, "message": "Missing to/subject"}), 400
    return jsonify({"success": True, "message": "Email queued", "details": data}), 202

@app.post("/comm/sms")
def send_sms():
    data = request.json or {}
    # TODO: Implement SMS via provider (Twilio or similar)
    if not data.get("to") or not data.get("body"):
        return jsonify({"success": False, "message": "Missing to/body"}), 400
    return jsonify({"success": True, "message": "SMS queued", "details": data}), 202

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)