from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import stripe

app = Flask(__name__)
CORS(app)

PORT = int(os.getenv("PORT", 8001))
COMM_URL = os.getenv("COMM_SERVICE_URL", "http://localhost:8002")
stripe.api_key = os.getenv("STRIPE_API_KEY", "")

@app.get("/auth/health")
def health():
    return {"status": "ok", "service": "auth-service"}, 200

@app.post("/auth/signup")
def signup():
    data = request.json or {}
    # TODO: Paste logic from src/modules/Authentication/Signup.py here
    user = {
        "id": "usr_123",
        "email": data.get("email"),
        "name": data.get("name")
    }
    # Example: notify via communication-service
    try:
        requests.post(f"{COMM_URL}/comm/email", json={
            "to": user["email"],
            "subject": "Welcome to Trosky",
            "body": f"Hi {user['name']}, your account has been created."
        }, timeout=5)
    except Exception as e:
        app.logger.warning(f"comm email failed: {e}")
    return jsonify({"success": True, "user": user}), 201

@app.post("/auth/login")
def login():
    data = request.json or {}
    # TODO: Paste logic from src/modules/Authentication/Login.py here
    ok = data.get("username") and data.get("password")
    if not ok:
        return jsonify({"success": False, "message": "Missing credentials"}), 400
    # Dummy token
    return jsonify({"success": True, "token": "jwt_dummy_token"}), 200

@app.post("/auth/stripe/session")
def create_stripe_session():
    data = request.json or {}
    price_id = data.get("price_id", "price_dummy")
    # TODO: Map to logic in src/modules/Authentication/Stripe.py
    if not stripe.api_key:
        return jsonify({"success": False, "message": "Stripe not configured"}), 500
    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            line_items=[{"price": price_id, "quantity": 1}],
            success_url=data.get("success_url", "https://example.com/success"),
            cancel_url=data.get("cancel_url", "https://example.com/cancel"),
        )
        return jsonify({"success": True, "session_id": session.id, "url": session.url}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)