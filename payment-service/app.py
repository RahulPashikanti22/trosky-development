from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import stripe

app = Flask(__name__)
CORS(app)
PORT = int(os.getenv("PORT", 5008))
stripe.api_key = os.getenv("STRIPE_API_KEY", "")

@app.get("/payment/health")
def health():
    return {"status": "ok", "service": "payment-service"}, 200

@app.post("/payment/create-session")
def create_session():
    data = request.json or {}
    price_id = data.get("price_id", "price_dummy")
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