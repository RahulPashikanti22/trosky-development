from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
PORT = int(os.getenv("PORT", 5009))

@app.get("/subscription/health")
def health():
    return {"status": "ok", "service": "subscription-service"}, 200

@app.post("/subscription/manage")
def manage():
    data = request.json or {}
    if not data.get("user_id"):
        return jsonify({"success": False, "message": "Missing user_id"}), 400
    return jsonify({"success": True, "message": "Subscription updated", "details": data}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)