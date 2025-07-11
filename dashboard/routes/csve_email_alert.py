from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# 📁 dashboard/routes/csve_email_alert.py
import os
from flask import Blueprint, request, jsonify
import smtplib
from email.message import EmailMessage

csve_email_bp = Blueprint("csve_email", __name__)

ADMIN_EMAIL = "admin@example.com"  # 🔧 Change this to your actual email

@csve_email_bp.route("/csve-email-alert", methods=["POST"])
def send_alert():
    try:
        data = request.get_json()
        spike_date = data.get("spike_date")

        msg = EmailMessage()
        msg["Subject"] = f"📊 Spike Alert on {spike_date}"
        msg["From"] = ADMIN_EMAIL
        msg["To"] = ADMIN_EMAIL
        msg.set_content(f"A spike in CSVE validation was detected on {spike_date}. Please review the insights dashboard.")

        with smtplib.SMTP("localhost") as server:
            server.send_message(msg)

        return jsonify({"sent": True})
    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        return jsonify({"error": str(e)}), 500
