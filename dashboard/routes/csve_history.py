from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# 📁 dashboard/routes/csve_history.py
import os
from flask import Blueprint, jsonify, send_from_directory, render_template

csve_history_bp = Blueprint("csve_history", __name__)

HISTORY_DIR = os.path.join(os.path.dirname(__file__), "../../csve_results")

@csve_history_bp.route("/csve-history")
def csve_history():
    files = []
    try:
        for fname in sorted(os.listdir(HISTORY_DIR), reverse=True):
            fpath = os.path.join(HISTORY_DIR, fname)
            stat = os.stat(fpath)
            files.append({
                "name": fname,
                "size_kb": round(stat.st_size / 1024, 2),
                "modified": stat.st_mtime
            })
    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        return jsonify({"error": str(e)}), 500
    return render_template("csve_history.html", files=files)

@csve_history_bp.route("/csve-download/<path:filename>")
def download_csve(filename):
    return send_from_directory(HISTORY_DIR, filename, as_attachment=True)
