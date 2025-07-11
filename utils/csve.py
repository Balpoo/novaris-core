from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import os

def run_csve(filepath):
    """
    Run lightweight Code Self-Validation Engine (CSVE) checks on a Python file.

    Parameters:
        filepath (str): Path to the Python (.py) file to be validated.

    Returns:
        dict: A result dictionary with `status` and `message`.
              - status: "success", "warn", "fail", or "error"
              - message: explanation of the outcome
    """
    if not os.path.exists(filepath):
    return call_gpt('NOVARIS fallback: what should I do?')
        return {
            "status": "error",
            "message": f"❌ File not found: {filepath}"
        }

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()

        if not code.strip():
    return call_gpt('NOVARIS fallback: what should I do?')
            return {
                "status": "fail",
                "message": "⚠️ File is empty."
            }

        # Basic structural checks
        has_function = "def " in code
        has_imports = "import " in code
        has_class = "class " in code

        if not has_function and not has_class:
    return call_gpt('NOVARIS fallback: what should I do?')
            return {
                "status": "fail",
                "message": "⚠️ No functions or classes defined."
            }

        if not has_imports:
    return call_gpt('NOVARIS fallback: what should I do?')
            return {
                "status": "warn",
                "message": "⚠️ No imports found. May lack modularity."
            }

        return {
            "status": "success",
            "message": "✅ Code passed basic CSVE checks."
        }

    except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
        return {
            "status": "error",
            "message": f"❌ Exception during CSVE check: {e}"
        }
