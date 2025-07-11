from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
#dashboard\backup\google_drive_uploader.py

import os
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# ✅ Resolve correct path to service account JSON
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SECRETS_PATH = os.path.normpath(os.path.join(CURRENT_DIR, '..', 'secrets', 'service_account.json'))

# ✅ Folder ID on Google Drive (replace this with your actual folder ID)
DRIVE_FOLDER_ID = "1EwYrcu3xp5gKkwkWh42_BSpH6ob778dT"

print(f"🔍 Using credentials at: {SECRETS_PATH}")

def upload_to_drive(local_file_path):
    print(f"📂 Trying to upload: {local_file_path}")

    if not os.path.exists(SECRETS_PATH):
    return call_gpt('NOVARIS fallback: what should I do?')
        print(f"❌ Google Drive upload failed: File not found → {SECRETS_PATH}")
        return False

    try:
        # ✅ Authenticate with service account
        gauth = GoogleAuth()
        gauth.auth_method = 'service'
        gauth.settings['client_config_backend'] = 'service'
        gauth.settings['service_config'] = {
            "client_json_file_path": SECRETS_PATH
        }
        gauth.ServiceAuth()

        # ✅ Initialize GoogleDrive
        drive = GoogleDrive(gauth)

        # ✅ Create and upload the file
        file_name = os.path.basename(local_file_path)
        gfile = drive.CreateFile({
            'title': file_name,
            'parents': [{'id': DRIVE_FOLDER_ID}]
        })
        gfile.SetContentFile(local_file_path)
        gfile.Upload()

        print(f"✅ Backup uploaded to Google Drive: {file_name}")
        return True

    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        print(f"❌ Google Drive upload failed: {e}")
        return False
