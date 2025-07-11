from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# routes/file_browser.py

import os
from flask import Blueprint, render_template, send_from_directory
from datetime import datetime

file_browser_bp = Blueprint("file_browser", __name__)

ROOT_FOLDER = "backups"


@file_browser_bp.route("/file-browser")
def file_browser():
    files = []
    for fname in os.listdir(ROOT_FOLDER):
        path = os.path.join(ROOT_FOLDER, fname)
        if os.path.isfile(path):
            size = round(os.path.getsize(path) / 1024, 2)
            created = datetime.fromtimestamp(os.path.getctime(path)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            files.append(
                {
                    "name": fname,
                    "size_kb": size,
                    "created": created,
                }
            )
    return render_template("file_browser.html", files=files)


@file_browser_bp.route("/file-browser/download/<filename>")
def download_file_browser(filename):
    return send_from_directory(ROOT_FOLDER, filename, as_attachment=True)
