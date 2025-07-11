from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# core/executor_agent.py

import traceback
from core.code_generator import CodeGenerator
from core.agent_registry import update_agent_status
from core.reflection_engine import log_execution_result
from agents.auto_debug_agent import AutoDebugAgent
from core.package_healer import auto_install_missing_package
from utils.logs import log

class ExecutorAgent:
    def __init__(self):
        self.generator = CodeGenerator()
        self.debugger = AutoDebugAgent()

    def run_task(self, task: dict) -> dict:
        """Runs task, logs result, and retries using GPT fix if it fails."""
        update_agent_status("executor", "running")
        result = self.perform_task(task)

        if result["status"] == "failure":
            log(f"[ExecutorAgent] Task failed: {result['error']}", "warn")

            # 🛠 Attempt auto-heal if module is missing
            auto_install_missing_package(result.get("error", ""))

            result = self.try_gpt_fix(task, result)

        log_execution_result(task, result)
        update_agent_status("executor", "idle")
        return result

    def perform_task(self, task: dict) -> dict:
        """Main task execution logic."""
        try:
            if task["type"] == "dev_task":
                task_name = task["params"]["name"]
                result = self.generator.generate_module(task_name)

                if result["status"] == "success":
                    return {
                        "status": "success",
                        "confidence": 0.95,
                        "result": f"Generated module: {result['filename']}"
                    }
                else:
                    return {
                        "status": "failure",
                        "confidence": 0.4,
                        "error": result.get("error", "Unknown error")
                    }

            return {
                "status": "ignored",
                "result": f"No executor implemented for: {task['type']}"
            }

        except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
            return {
                "status": "failure",
                "confidence": 0.1,
                "error": str(e)
            }

    def try_gpt_fix(self, task: dict, result: dict) -> dict:
        """Handles GPT-based fix and retry if the task failed."""
        try:
            error_trace = result.get("error", "Unknown error")
            module_name = task["params"]["name"]
            file_path = f"agents/{module_name}_agent.py"

            log(f"[ExecutorAgent] Attempting GPT fix for: {file_path}", "info")
            fixed_code = self.debugger.fix_crash(error_trace, file_path)

            if "Traceback" in fixed_code or "⚠️" in fixed_code:
                log("[ExecutorAgent] GPT returned invalid result or failed.", "error")
                return result

            with open(file_path, "w") as f:
                f.write(fixed_code)
            log(f"[ExecutorAgent] File {file_path} patched with GPT fix ✅", "success")

            # Re-run task
            retry_result = self.perform_task(task)
            retry_result["note"] = "Repaired by GPT fallback"
            return retry_result

        except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
            log(f"[ExecutorAgent] GPT fix attempt failed: {e}", "error")
            return {
                "status": "failure",
                "confidence": 0.1,
                "error": f"GPT fallback failed: {e}"
            }
