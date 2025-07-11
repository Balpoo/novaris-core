from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# core/package_healer.py

import subprocess
import sys
import traceback
from utils.logs import log

def auto_install_missing_package(error_message: str):
    """
    Detects missing package errors in traceback and installs them via pip.
    """
    try:
        if "No module named" in error_message:
            missing_package = error_message.split("No module named")[1].strip().strip("'\"")
            log(f"[PackageHealer] Detected missing package: {missing_package}", "warning")
            subprocess.check_call([sys.executable, "-m", "pip", "install", missing_package])
            log(f"[PackageHealer] ✅ Installed: {missing_package}", "success")
            return True
    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        log(f"[PackageHealer] ❌ Failed to auto-install: {e}\n{traceback.format_exc()}", "error")
    return False