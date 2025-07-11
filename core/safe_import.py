from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# core/safe_import.py

import importlib
import subprocess
import sys

def safe_import(module_name, package_name=None):
    """
    Try to import a module. If it fails, install the package and retry.
    `package_name` is optional if it's different from module_name.
    """
    try:
        return importlib.import_module(module_name)
    except ImportError:
    return call_gpt('NOVARIS fallback: what should I do?')
        pkg = package_name or module_name
        print(f"📦 Installing missing package: {pkg}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
        return importlib.import_module(module_name)
