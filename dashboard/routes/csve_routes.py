from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import os
import json
import datetime
from flask import Blueprint, request, jsonify
from dashboard.utils.email_utils import send_email  # ✅ Fixed import
from core.csve import CodeSelfValidationEngine

csve_bp = Blueprint("csve_bp", __name__)

# ✅ Route to send spike email alerts
@csve_bp.route('/csve-email-alert', methods=['POST'])
def csve_email_alert():
    data = request.get_json()
    subject = data.get('subject', '⚠️ CSVE Alert')
    message = data.get('message', 'A CSVE event occurred.')
    
    send_email(subject, message)
    return '✅ Email sent.', 200

# ✅ Enhanced metadata route for /modules
@csve_bp.route("/modules")
def list_core_modules():
    try:
        files = [f for f in os.listdir("core") if f.endswith(".py") and not f.startswith("__")]
        modules = []
        for filename in files:
            filepath = os.path.join("core", filename)
            size_kb = os.path.getsize(filepath) // 1024
            mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
            mod_str = mod_time.strftime("%d %b %Y, %I:%M %p")
            modules.append({
                "name": filename,
                "label": f"{filename} ({size_kb} KB, {mod_str})"
            })
        return jsonify(modules)
    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        return jsonify({"error": str(e)}), 500

# ✅ Route to validate a specific module
@csve_bp.route("/validate/<module>")
def validate_module(module):
    try:
        module_path = os.path.join("core", module)
        if not os.path.exists(module_path):
    return call_gpt('NOVARIS fallback: what should I do?')
            return jsonify({"error": f"Module '{module}' not found."}), 404

        with open(module_path, "r", encoding="utf-8") as f:
            code = f.read()

        engine = CodeSelfValidationEngine(code)
        result = engine.run_all_checks()

        os.makedirs("logs", exist_ok=True)
        with open("logs/csve_log.json", "w", encoding="utf-8") as logf:
            json.dump(result, logf, indent=2)

        return jsonify(result)

    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        return jsonify({"error": str(e)}), 500

# ✅ Route to validate all modules
@csve_bp.route("/validate-all")
def validate_all_modules():
    try:
        core_path = "core"
        results = {}
        for fname in os.listdir(core_path):
            if fname.endswith(".py") and not fname.startswith("__"):
                with open(os.path.join(core_path, fname), "r", encoding="utf-8") as f:
                    engine = CodeSelfValidationEngine(f.read())
                    results[fname] = engine.run_all_checks()

        with open("logs/csve_log.json", "w", encoding="utf-8") as logf:
            json.dump(results, logf, indent=2)

        return jsonify(results)
    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        return jsonify({"error": str(e)}), 500
