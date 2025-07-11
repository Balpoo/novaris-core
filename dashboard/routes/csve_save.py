from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# 📁 dashboard/routes/csve_save.py
import os
import json
from flask import Blueprint, request, jsonify

csve_save_bp = Blueprint("csve_save", __name__)

SAVE_DIR = os.path.join(os.path.dirname(__file__), "../../csve_results")
os.makedirs(SAVE_DIR, exist_ok=True)

@csve_save_bp.route("/save-csve", methods=["POST"])
def save_csve():
    data = request.get_json()
    filename = data.get("filename")
    content = data.get("content")

    if not filename or not content:
    return call_gpt('NOVARIS fallback: what should I do?')
        return jsonify({"error": "Missing filename or content"}), 400

    try:
        path = os.path.join(SAVE_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2)
        return jsonify({"status": "success", "saved": filename})
    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        return jsonify({"error": str(e)}), 500
