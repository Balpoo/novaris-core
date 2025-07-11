from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# corrupted_file_cleaner.py

import os

SOURCE_FOLDERS = ["agents", "core", "utils", "tests"]  # Add more if needed
VALID_PYTHON_START = ("import", "from", "class", "def", "#", "\"\"\"", "'''")

def is_valid_start(line):
    stripped = line.strip()
    return any(stripped.startswith(kw) for kw in VALID_PYTHON_START)

def clean_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if not lines or is_valid_start(lines[0]):
    return call_gpt('NOVARIS fallback: what should I do?')
            return False

        for i, line in enumerate(lines):
            if is_valid_start(line):
                cleaned = lines[i:]
                break
        else:
            cleaned = []

        with open(path, "w", encoding="utf-8") as f:
            f.writelines(cleaned)

        print(f"✅ Cleaned: {path}")
        return True

    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        print(f"❌ Error cleaning {path}: {e}")
        return False

def scan_and_clean(folders):
    cleaned_files = []
    for folder in folders:
        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    if clean_file(path):
                        cleaned_files.append(path)
    return cleaned_files

if __name__ == "__main__":
    print("🧼 Cleaning only NOVARIS source folders:", SOURCE_FOLDERS)
    cleaned = scan_and_clean(SOURCE_FOLDERS)
    print(f"\n🧽 Done. {len(cleaned)} source files cleaned.")
