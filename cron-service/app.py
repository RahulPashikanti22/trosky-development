from flask import Flask, jsonify
from flask_cors import CORS
import os
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
CORS(app)
PORT = int(os.getenv("PORT", 8009))
scheduler = BackgroundScheduler()
scheduler.start()

def sample_job():
    app.logger.info("Cron job executed")

scheduler.add_job(sample_job, "interval", minutes=5)

@app.get("/cron/health")
def health():
    return {"status": "ok", "service": "cron-service"}, 200

@app.get("/cron/run")
def run_now():
    sample_job()
    return jsonify({"success": True, "message": "Cron executed"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)