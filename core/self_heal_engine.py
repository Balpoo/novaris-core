# core/self_heal_engine.py

import os
import ast
import traceback
from core.gpt_fallback import call_gpt

METHOD_PATCHES = {
    "MemoryEngine": {
        "add": """
    def add(self, message: str, tags: list = []):
        import datetime, uuid
        entry = {
            "id": str(uuid.uuid4()),
            "summary": message,
            "tags": tags,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }
        self.thoughts.append(entry)
        self._save()
        print(f"\U0001f9e0 Memory added: {message[:50]}...")
        return entry
        """
    }
}

LOG_PATH = "logs/auto_heal_log.json"


def log_patch(target_file, class_name, method):
    os.makedirs("logs", exist_ok=True)
    with open(LOG_PATH, "a") as log:
        log.write(f"Patched: {target_file} | Class: {class_name} | Method: {method}\n")


def inject_method(file_path, class_name, method_name, method_code):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        new_lines = []
        injected = False
        inside_target_class = False

        for i, line in enumerate(lines):
            new_lines.append(line)
            if line.strip().startswith(f"class {class_name}"):
                inside_target_class = True
            elif inside_target_class and line.strip().startswith("def "):
                pass
            elif inside_target_class and line.strip() == "":
                if not injected:
                    new_lines.append("\n" + method_code.strip("\n") + "\n")
                    injected = True
                    inside_target_class = False

        if injected:
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            log_patch(file_path, class_name, method_name)
            print(f"✅ Injected missing method: {method_name} into {class_name}")

    except Exception as e:
        print(f"❌ Failed to inject method {method_name} in {file_path}: {e}")
        traceback.print_exc()


def run_self_diagnosis():
    print("🧪 Running Self-Heal Diagnostics...")
    for root, _, files in os.walk("core"):
        for file in files:
            if not file.endswith(".py"):
                continue

            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read(), filename=path)

                for node in tree.body:
                    if isinstance(node, ast.ClassDef):
                        cls = node.name
                        methods = [
                            n.name for n in node.body if isinstance(n, ast.FunctionDef)
                        ]
                        if cls in METHOD_PATCHES:
                            for method_name, method_code in METHOD_PATCHES[cls].items():
                                if method_name not in methods:
                                    inject_method(path, cls, method_name, method_code)

            except Exception as e:
                print(f"❌ Error scanning {path}: {e}")
                try:
                    return call_gpt("NOVARIS fallback: what should I do?")
                except Exception as e:
                    print(f"[Self-Heal GPT Error] {e}")
                    return "❗ Self-heal fallback failed."


if __name__ == "__main__":
    run_self_diagnosis()
