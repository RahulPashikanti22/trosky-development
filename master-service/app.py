from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
PORT = int(os.getenv("PORT", 5000))

@app.get("/master/health")
def health():
    return {"status": "ok", "service": "master-service"}, 200

@app.get("/master/templates")
def templates():
    # TODO: Move/serve from modules/MasterScreens/Master.py and MailTemplate.json
    templates = [
        {"id": "welcome", "subject": "Welcome", "body": "Welcome to Trosky!"},
        {"id": "reset", "subject": "Reset Password", "body": "Click link to reset."}
    ]
    return jsonify({"success": True, "templates": templates}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)