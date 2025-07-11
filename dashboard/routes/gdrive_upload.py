from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import os
import shutil
from flask import Blueprint, flash, redirect, url_for, request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# 🔧 Flask Blueprint
gdrive = Blueprint('gdrive', __name__)

# 🔐 Path to service account JSON
SERVICE_ACCOUNT_FILE = os.path.normpath('D:/Karan/Documents/Projects/novaris-core/dashboard/secrets/service_account.json')
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# 📁 Google Drive Folder ID (pre-created)
GDRIVE_FOLDER_ID = '1EwYrcu3xp5gKkwkWh42_BSpH6ob778dT'

# 📂 Where backup archive will be stored
BACKUP_DIR = 'backups'
ZIP_TARGET_FOLDER = 'data'  # Change this if your backup folder is something else
BACKUP_FILENAME = 'novaris_backup.zip'
BACKUP_PATH = os.path.join(BACKUP_DIR, BACKUP_FILENAME)

# 🔑 Auth & Service Builder
def get_drive_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=credentials)

# ☁️ Upload Endpoint
@gdrive.route('/upload-to-drive', methods=['POST'])
def upload_to_drive():
    try:
        # ✅ Ensure backup folder exists
        os.makedirs(BACKUP_DIR, exist_ok=True)

        # 🔁 Create fresh backup ZIP from target data
        shutil.make_archive(os.path.join(BACKUP_DIR, 'novaris_backup'), 'zip', ZIP_TARGET_FOLDER)

        # 🔌 Connect to Google Drive
        drive_service = get_drive_service()

        # 📦 Prepare upload
        file_metadata = {
            'name': BACKUP_FILENAME,
            'parents': [GDRIVE_FOLDER_ID]
        }
        media = MediaFileUpload(BACKUP_PATH, mimetype='application/zip')

        # ☁️ Upload to Drive
        uploaded_file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        flash(f"✅ Backup uploaded to Google Drive (File ID: {uploaded_file.get('id')})", 'success')
        return redirect(url_for('index'))  # ✅ This works since 'index' is root route

    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        flash(f"❌ Google Drive upload failed: {e}", 'danger')
        return redirect(url_for('index'))
