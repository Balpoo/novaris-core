# agents/gpt_fallback_injector.py

import os
import re
import json
from datetime import datetime

FALLBACK_IMPORT = "from core.gpt_fallback import call_gpt"
EXCLUDE_DIRS = {"venv", "__pycache__", ".git", ".idea", ".vscode", "logs"}
TARGET_EXT = ".py"
PATCH_LOG_PATH = "logs/gpt_patch_log.json"


def auto_inject_gpt_fallback(root_dir="."):
    patched_files = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for filename in filenames:
            if not filename.endswith(TARGET_EXT):
                continue

            full_path = os.path.join(dirpath, filename)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                original = list(lines)
                modified = False

                # Inject import if missing
                if FALLBACK_IMPORT not in "".join(lines):
                    lines.insert(0, FALLBACK_IMPORT + "\n")
                    modified = True

                i = 0
                while i < len(lines):
                    line = lines[i]
                    stripped = line.strip()

                    # Skip already patched logic
                    if "call_gpt(" in stripped or "# GPT-SAFE INJECTED" in stripped:
                        i += 1
                        continue

                    indent = line[: len(line) - len(stripped)]

                    # Inject fallback for: if not X / if X is None
                    if re.match(r"(if\s+not\s+\w+|if\s+\w+\s+is\s+None)", stripped):
                        inject = (
                            indent
                            + "    return call_gpt('NOVARIS fallback: what should I do?')  # GPT-SAFE INJECTED\n"
                        )
                        lines.insert(i + 1, inject)
                        modified = True
                        i += 1  # skip injected line

                    # Inject fallback for: return None
                    elif re.match(r"return\s+None", stripped):
                        lines[i] = line.replace(
                            "return None",
                            "return call_gpt('Fallback: generate a valid result.')  # GPT-SAFE INJECTED\n",
                        )
                        modified = True

                    # Inject fallback in except blocks
                    elif (
                        stripped.startswith("except")
                        and (i + 1 < len(lines))
                        and "call_gpt" not in lines[i + 1]
                    ):
                        inject = (
                            indent
                            + "    return call_gpt('Exception occurred. Suggest a solution.')  # GPT-SAFE INJECTED\n"
                        )
                        lines.insert(i + 1, inject)
                        modified = True
                        i += 1

                    i += 1

                if modified and lines != original:
                    with open(full_path, "w", encoding="utf-8") as f:
                        f.writelines(lines)

                    patched_files[full_path] = (
                        f"{len(lines) - len(original)} lines changed"
                    )

            except Exception as e:
                print(f"❌ Failed to patch {full_path}: {e}")

    save_patch_log(patched_files)


def save_patch_log(data):
    os.makedirs("logs", exist_ok=True)
    entry = {"timestamp": datetime.now().isoformat(), "patched_files": data}
    try:
        with open(PATCH_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, indent=2) + ",\n")
        print(f"✅ GPT fallback patching complete. Log saved to {PATCH_LOG_PATH}")
    except Exception as e:
        print(f"⚠️ Failed to write GPT patch log: {e}")


if __name__ == "__main__":
    auto_inject_gpt_fallback(".")
