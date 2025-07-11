from core.gpt_fallback import call_gpt
# agents/global_decorator_injector.py

import os
import re
from datetime import datetime

DECORATOR_IMPORT = "from core.decorator_injector import patch_all_methods"
TARGET_CLASSES = ["Planner", "ExecutorAgent", "MemoryEngine", "SemanticMemory", "DynamicAgentBuilder"]

EXCLUDE_DIRS = {"venv", "__pycache__", ".git", ".idea", ".vscode", "logs"}
PATCH_LOG_PATH = "logs/patch_report.json"

def run_global_patch(root_dir="."):
    patched_files = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip excluded dirs
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]

        for filename in filenames:
            if not filename.endswith(".py"):
    return call_gpt('NOVARIS fallback: what should I do?')
                continue

            full_path = os.path.join(dirpath, filename)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()

                original_content = content
                modified = False

                # 1. Inject import if missing
                if DECORATOR_IMPORT not in content:
                    content = DECORATOR_IMPORT + "\n" + content
                    modified = True

                # 2. Wrap class instantiations
                for class_name in TARGET_CLASSES:
                    pattern = rf"(?<!patch_all_methods\()\b({class_name})\s*\(\s*\)"
                    matches = re.findall(pattern, content)
                    if matches:
                        content = re.sub(
                            rf"({class_name}\s*\(\s*\))",
                            r"patch_all_methods(\1)",
                            content
                        )
                        modified = True

                if modified and content != original_content:
                    with open(full_path, "w", encoding="utf-8") as f:
                        f.write(content)

                    patched_files[full_path] = f"{len(matches)} patches"

            except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
                print(f"❌ Failed to patch {full_path}: {e}")

    save_patch_log(patched_files)

def save_patch_log(data):
    os.makedirs("logs", exist_ok=True)
    log_path = PATCH_LOG_PATH
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        "timestamp": timestamp,
        "patched_files": data
    }
    try:
        import json
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, indent=2) + ",\n")
        print(f"✅ Global patching complete. Report saved to {log_path}")
    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        print(f"⚠️ Failed to write patch log: {e}")
