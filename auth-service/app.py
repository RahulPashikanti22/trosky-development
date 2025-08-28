from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import stripe

app = Flask(__name__)
CORS(app)

# Config
PORT = int(os.getenv("PORT", 5001))
COMM_URL = os.getenv("COMM_SERVICE_URL", "http://localhost:8002")
stripe.api_key = os.getenv("STRIPE_API_KEY", "")

# ------------------- Health -------------------
@app.route("/auth/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "auth-service"}), 200


# ------------------- Signup -------------------
@app.route("/auth/signup", methods=["POST"])
def signup():
    data = request.get_json(force=True, silent=True) or {}

    if not data.get("email") or not data.get("name"):
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    user = {
        "id": "usr_123",
        "email": data.get("email"),
        "name": data.get("name")
    }

    # Example: notify via communication-service
    try:
        requests.post(
            f"{COMM_URL}/comm/email",
            json={
                "to": user["email"],
                "subject": "Welcome to Trosky",
                "body": f"Hi {user['name']}, your account has been created."
            },
            timeout=5
        )
    except Exception as e:
        app.logger.warning(f"comm email failed: {e}")

    return jsonify({"success": True, "user": user}), 201


# ------------------- Login -------------------
@app.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json(force=True, silent=True) or {}

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "Missing credentials"}), 400

    # Dummy token for now
    return jsonify({"success": True, "token": "jwt_dummy_token"}), 200


# ------------------- Stripe Checkout Session -------------------
@app.route("/auth/stripe/session", methods=["POST"])
def create_stripe_session():
    if not stripe.api_key:
        return jsonify({"success": False, "message": "Stripe not configured"}), 500

    data = request.get_json(force=True, silent=True) or {}
    price_id = data.get("price_id")

    if not price_id:
        return jsonify({"success": False, "message": "Missing price_id"}), 400

    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            line_items=[{"price": price_id, "quantity": 1}],
            success_url=data.get("success_url", "https://example.com/success"),
            cancel_url=data.get("cancel_url", "https://example.com/cancel"),
        )
        return jsonify({
            "success": True,
            "session_id": session.id,
            "url": session.url
        }), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


# ------------------- Run App -------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
