from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# dashboard/routes/reflections.py

import sys
import os

# ✅ Inject project root to sys.path so core modules work
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from flask import Blueprint, render_template, jsonify
from core.memory_visualizer import MemoryVisualizer
from core.memory_engine import MemoryEngine

# ✅ Define Blueprint
reflections_bp = Blueprint("reflections", __name__)
viz = MemoryVisualizer()
memory = patch_all_methods(MemoryEngine())


# ✅ Reflections page - list all thoughts
@reflections_bp.route("/reflections")
def reflections_page():
    thoughts = memory.fetch_all_thoughts()
    thoughts = sorted(thoughts, key=lambda t: t.get("timestamp", ""), reverse=True)
    return render_template("reflections.html", thoughts=thoughts)


# ✅ Mindmap page (Vis.js frontend)
@reflections_bp.route("/mindmap")
def mindmap_page():
    return render_template("mindmap.html")


# ✅ API: Graph JSON data for memory visualization
@reflections_bp.route("/api/memory-graph")
def memory_graph_api():
    data = viz.generate_graph_data()
    return jsonify(data)
