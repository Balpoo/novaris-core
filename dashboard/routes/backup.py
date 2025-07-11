from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# ✅ Final version with correct path to service_account.json inside 'dashboard/secrets'

import os
import shutil
import py7zr
import csv
import io
import sqlite3
import json

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from flask import Blueprint, render_template, send_from_directory, flash, redirect, url_for, request
from datetime import datetime
from dotenv import load_dotenv

# 🔐 Load admin password securely
load_dotenv()
ADMIN_PASSWORD = os.getenv("ADMIN_RESTORE_PASSWORD", "novaris2047secure")

# 🧠 Folder Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_FOLDER = os.path.abspath(os.path.join(BASE_DIR, "..", "db"))
BACKUP_FOLDER = os.path.abspath(os.path.join(BASE_DIR, "..", "backups"))
SECRETS_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "secrets", "service_account.json"))

backup_bp = Blueprint("backup", __name__)

@backup_bp.route("/backups")
def list_backups():
    try:
        files = []
        for file in os.listdir(BACKUP_FOLDER):
            if file.endswith(".7z"):
                path = os.path.join(BACKUP_FOLDER, file)
                size_kb = round(os.path.getsize(path) / 1024, 2)
                mtime = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M:%S")
                tag = "Manual"
                if "auto" in file.lower():
                    tag = "Auto"
                elif "drive" in file.lower():
                    tag = "Drive"
                files.append({
                    "name": file,
                    "size_kb": size_kb,
                    "mtime": mtime,
                    "tag": tag
                })
        files.sort(key=lambda x: x["mtime"], reverse=True)
        return render_template("backups.html", backups=files)
    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        flash(f"Error loading backups: {e}", "danger")
        return render_template("backups.html", backups=[])

@backup_bp.route("/backups/download/<filename>")
def download_backup(filename):
    return send_from_directory(BACKUP_FOLDER, filename, as_attachment=True)

@backup_bp.route("/backups/restore/<filename>", methods=["GET", "POST"])
def restore_backup(filename):
    if request.method == "GET":
        return render_template("confirm_restore.html", filename=filename)

    password = request.form.get("password")
    if password != ADMIN_PASSWORD:
        flash("❌ Incorrect admin password. Access denied.", "danger")
        return redirect(url_for("backup.restore_backup", filename=filename))

    try:
        backup_path = os.path.join(BACKUP_FOLDER, filename)
        extract_path = "temp_restore"
        os.makedirs(extract_path, exist_ok=True)

        with py7zr.SevenZipFile(backup_path, mode='r') as archive:
            archive.extractall(path=extract_path)

        extracted_db = os.path.join(extract_path, "db", "task_logs.db")
        current_db = os.path.join(SOURCE_FOLDER, "task_logs.db")

        if os.path.exists(extracted_db):
            if os.path.exists(current_db):
                shutil.copy2(current_db, current_db + ".bak")
                print("🛡️ Existing DB backed up before restore.")

            shutil.copy2(extracted_db, current_db)
            flash("✅ Restore completed successfully. Please restart the app.", "success")
        else:
            flash("❌ Extracted DB not found. Restore failed.", "danger")

        shutil.rmtree(extract_path)

    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        flash(f"❌ Restore failed: {e}", "danger")

    return redirect(url_for("backup.list_backups"))

@backup_bp.route("/manual-backup")
def manual_backup():
    os.makedirs(BACKUP_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_FOLDER, f"backup_{timestamp}.7z")

    try:
        with py7zr.SevenZipFile(backup_file, 'w') as archive:
            archive.writeall(SOURCE_FOLDER, arcname="db")

        flash(f"✅ Manual backup created: {os.path.basename(backup_file)}", "success")
        upload_backup_to_drive(backup_file)

    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        flash(f"❌ Backup failed: {e}", "danger")

    return redirect(url_for("backup.list_backups"))

def upload_backup_to_drive(file_path):
    try:
        SCOPES = ["https://www.googleapis.com/auth/drive.file"]
        print(f"🔍 Using service account credentials from: {SECRETS_PATH}")
        print(f"📂 Uploading: {file_path}")

        credentials = service_account.Credentials.from_service_account_file(SECRETS_PATH, scopes=SCOPES)
        service = build("drive", "v3", credentials=credentials)

        folder_id = "1EwYrcu3xp5gKkwkWh42_BSpH6ob778dT"
        file_metadata = {
            "name": os.path.basename(file_path),
            "parents": [folder_id]
        }

        media = MediaFileUpload(file_path, mimetype="application/x-7z-compressed")
        uploaded = service.files().create(body=file_metadata, media_body=media, fields="id").execute()

        flash("☁️ Backup uploaded to Google Drive successfully.", "info")

    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        flash(f"❌ Google Drive upload failed: {e}", "danger")

@backup_bp.route("/upload-csv", methods=["GET", "POST"])
def upload_csv():
    if request.method == "POST":
        file = request.files["csvfile"]
        if not file or not file.filename.endswith(".csv"):
    return call_gpt('NOVARIS fallback: what should I do?')
            flash("⚠️ Invalid file format. Upload a .csv file.", "warning")
            return redirect(url_for("backup.upload_csv"))

        try:
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            reader = csv.DictReader(stream)

            conn = sqlite3.connect(os.path.join(SOURCE_FOLDER, "task_logs.db"))
            cursor = conn.cursor()

            rows_inserted = 0
            for row in reader:
                if all(k in row for k in ["timestamp", "task", "status", "task_type", "agent"]):
                    cursor.execute(
                        "INSERT INTO logs (timestamp, task, status, task_type, agent) VALUES (?, ?, ?, ?, ?)",
                        (row["timestamp"], row["task"], row["status"], row["task_type"], row["agent"])
                    )
                    rows_inserted += 1

            conn.commit()
            conn.close()
            flash(f"✅ CSV uploaded. {rows_inserted} rows inserted into logs.", "success")

        except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
            flash(f"❌ CSV upload failed: {e}", "danger")

        return redirect(url_for("backup.upload_csv"))

    return render_template("upload_csv.html")
