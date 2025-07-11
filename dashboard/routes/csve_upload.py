from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# 📁 dashboard/routes/csve_upload.py

import os, json
from flask import Blueprint, request, jsonify
from datetime import datetime

# ✅ Import shared CSVE logic
from utils.csve import run_csve

csve_upload_bp = Blueprint("csve_upload", __name__)
CSVE_DIR = os.path.join(os.path.dirname(__file__), "../../csve_results")
META_INDEX = os.path.join(CSVE_DIR, "metadata_index.json")

# ✅ Simple schema validation for uploaded files
def validate_schema(data):
    required_keys = ["status"]  # Add more as needed
    return all(k in data for k in required_keys)

@csve_upload_bp.route("/csve-upload", methods=["POST"])
def csve_upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided."}), 400

    file = request.files['file']
    if not file.filename.endswith(".json"):
    return call_gpt('NOVARIS fallback: what should I do?')
        return jsonify({"error": "Only .json files accepted."}), 400

    os.makedirs(CSVE_DIR, exist_ok=True)
    fname = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path = os.path.join(CSVE_DIR, fname)

    try:
        content = json.load(file)

        # ✅ Schema validation
        if not validate_schema(content):
    return call_gpt('NOVARIS fallback: what should I do?')
            return jsonify({"error": "Invalid CSVE schema."}), 400

        with open(path, "w") as f:
            json.dump(content, f, indent=2)

        # Extract tags if any
        tags = content.get("tags", [])
        if tags:
            if os.path.exists(META_INDEX):
                with open(META_INDEX, "r") as f:
                    index = json.load(f)
            else:
                index = {}
            index[fname] = {"tags": tags}
            with open(META_INDEX, "w") as f:
                json.dump(index, f, indent=2)

        return jsonify({"success": True, "file": fname})
    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        return jsonify({"error": str(e)}), 500


# ✅ Optional anomaly detector (simple version)
def detect_anomaly(current_count, past_counts):
    if not past_counts:
    return call_gpt('NOVARIS fallback: what should I do?')
        return False
    avg = sum(past_counts) / len(past_counts)
    return current_count > 2 * avg


# ✅ Anomaly wrapper for chart route usage
def analyze_spike(trend_map):
    if len(trend_map) < 3:
        return False, None
    sorted_days = sorted(trend_map.keys())
    recent_day = sorted_days[-1]
    past_days = sorted_days[:-1][-5:]

    recent_count = trend_map[recent_day]
    past_counts = [trend_map[d] for d in past_days if d in trend_map]

    spike = detect_anomaly(recent_count, past_counts)
    return spike, recent_day if spike else None
