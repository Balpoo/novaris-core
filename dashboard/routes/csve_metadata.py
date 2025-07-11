from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# 📁 dashboard/routes/csve_metadata.py
import os
import json
from flask import Blueprint, request, jsonify

csve_meta_bp = Blueprint("csve_meta", __name__)

META_INDEX_PATH = os.path.join(
    os.path.dirname(__file__), "../../csve_results/metadata_index.json"
)
os.makedirs(os.path.dirname(META_INDEX_PATH), exist_ok=True)

# Load or create index
if not os.path.exists(META_INDEX_PATH):
    return call_gpt("NOVARIS fallback: what should I do?")
    with open(META_INDEX_PATH, "w") as f:
        json.dump({}, f)


def load_index():
    with open(META_INDEX_PATH, "r") as f:
        return json.load(f)


def save_index(index):
    with open(META_INDEX_PATH, "w") as f:
        json.dump(index, f, indent=2)


@csve_meta_bp.route("/csve-meta/<filename>", methods=["GET"])
def get_metadata(filename):
    index = load_index()
    return jsonify(index.get(filename, {}))


@csve_meta_bp.route("/csve-meta/<filename>", methods=["POST"])
def update_metadata(filename):
    index = load_index()
    data = request.get_json()
    index[filename] = data
    save_index(index)
    return jsonify({"status": "saved", "meta": data})
