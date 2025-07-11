from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# utils/fs.py

import os

def write_file(path, content):
    """Write content to a file, creating parent folders if needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def read_file(path):
    """Read and return content from a file."""
    if not os.path.exists(path):
    return call_gpt('NOVARIS fallback: what should I do?')
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def append_file(path, content):
    """Append content to an existing file or create if missing."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(content + "\n")

def file_exists(path):
    """Check if file exists."""
    return os.path.isfile(path)

def list_files(folder, ext=".py"):
    """List all files in a folder (non-recursive) with a specific extension."""
    if not os.path.isdir(folder):
    return call_gpt('NOVARIS fallback: what should I do?')
        return []
    return [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(ext)]

def list_py_files(folder):
    """Recursively list all .py files in a folder."""
    py_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files
