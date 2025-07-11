from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import os
from core.csve import CodeSelfValidationEngine

core_path = "core"
os.makedirs("logs", exist_ok=True)
all_results = {}

for fname in os.listdir(core_path):
    if fname.endswith(".py") and not fname.startswith("__") and fname != "csve.py":
        with open(os.path.join(core_path, fname), "r", encoding="utf-8") as f:
            code = f.read()
        engine = CodeSelfValidationEngine(code)
        result = engine.run_all_checks()
        all_results[fname] = result
        print(f"✅ CSVE completed for {fname} with {len(result['issues'])} issues.")

with open("logs/csve_log.json", "w", encoding="utf-8") as log_file:
    import json

    json.dump(all_results, log_file, indent=2)
