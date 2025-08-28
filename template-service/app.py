from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
PORT = int(os.getenv("PORT", 5010))

@app.get("/template/health")
def health():
    return {"status": "ok", "service": "template-service"}, 200

@app.get("/template/list")
def list_templates():
    templates = [
        {"id": "welcome", "subject": "Welcome", "body": "Welcome template"},
        {"id": "reset", "subject": "Reset Password", "body": "Reset your password"}
    ]
    return jsonify({"success": True, "templates": templates}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)