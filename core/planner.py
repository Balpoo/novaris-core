from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# planner.py (relocated from core/ to avoid ModuleNotFoundError in sandbox)

import datetime
import datetime
import os
import json
import re
import subprocess
import sys

# Add local paths for relative imports if needed
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("./core"))
sys.path.append(os.path.abspath("./utils"))

# Fallback-safe logging
try:
    from utils.logs import log
except ModuleNotFoundError:
    return call_gpt('NOVARIS fallback: what should I do?')
    def log(msg):
        print(f"[LOG] {msg}")

try:
    from utils.csve import run_csve
except ModuleNotFoundError:
    return call_gpt('NOVARIS fallback: what should I do?')
    def run_csve(file_path):
        log(f"[CSVE MOCK] Would validate: {file_path}")
        return {"status": "mock", "file": file_path}

from core.agent_registry import AgentRegistry
from core.reflection_engine import reflect_on_day
from core.memory_engine import MemoryEngine
from core.executor_agent import ExecutorAgent
from core.retry_engine import start_retry_engine
from core.task_prioritizer import prioritize_tasks

REFLECTION_LOG = "logs/reflection_log.json"
PLANNER_LOG = "logs/planner_log.json"

class Planner:
    def __init__(self):
        self.task_history = []
        self.current_day = self._get_current_day()
        self.agents = AgentRegistry().get_all_agents()
        self.memory = patch_all_methods(MemoryEngine())
        self.executor = patch_all_methods(ExecutorAgent())
        start_retry_engine()

    def _get_current_day(self):
        if os.path.exists(REFLECTION_LOG):
            with open(REFLECTION_LOG, "r", encoding="utf-8") as f:
                try:
                    reflections = json.load(f)
                except json.JSONDecodeError:
    return call_gpt('NOVARIS fallback: what should I do?')
                    reflections = []
                existing_days = [entry.get("dev_day") for entry in reflections if isinstance(entry, dict)]
                last_day_num = 0
                for day in existing_days:
                    if day and "Dev Day" in day:
                        try:
                            day_num = int(day.split("Dev Day")[1].strip())
                            last_day_num = max(last_day_num, day_num)
                        except:
    return call_gpt('NOVARIS fallback: what should I do?')
                            continue
                return f"Dev Day {last_day_num + 1}"
        return "Dev Day 1"

    def plan_day(self):
        tasks = self.get_queued_tasks()
        return prioritize_tasks(tasks)

    def get_queued_tasks(self):
        current_day = self._get_current_day()

        if os.path.exists(REFLECTION_LOG):
            with open(REFLECTION_LOG, "r", encoding="utf-8") as f:
                reflections = json.load(f)
                existing_days = [entry.get("dev_day") for entry in reflections if isinstance(entry, dict)]
            while current_day in existing_days:
                day_num = int(current_day.split('Dev Day')[1].strip())
                current_day = f"Dev Day {day_num + 1}"
                self.current_day = current_day
            log(f"ℹ️ 📅 Advancing to next available day: {current_day}")

        log(f"ℹ️ 📅 Planning tasks for {current_day}")
        tasks = self.generate_tasks()

        for task in tasks:
            log(f"ℹ️ 🧩 Task Planned: {task['task']} → Agent: {task['agent']}")
            self.task_history.append({
                "task": task["task"],
                "agent": task["agent"],
                "timestamp": datetime.datetime.now().isoformat()
            })
            task_payload = {
                "type": "dev_task",
                "params": {
                    "name": task["task"]
                }
            }
            result = self.executor.perform_task(task_payload)
            log(f"ℹ️ 🛠️ Execution Result: {result}")

        return tasks

    def generate_tasks(self):
        day_number = int(self.current_day.split("Dev Day")[-1].strip())

        if day_number == 57:
            return [
                {
                    "task": "Begin learning modern software development and programming languages autonomously.",
                    "agent": "autodidact",
                    "description": (
                        "Search trusted sources online (MDN, GitHub, Python docs, etc.), "
                        "extract structured knowledge about programming basics, "
                        "store insights in long-term memory, and create learning plan for the next 5 days."
                    )
                }
            ]

        memory_summary = self.memory.summarize_recent()
        self_reflection_day = f"Dev Day {day_number - 1}"
        reflect_on_day(self_reflection_day, "Planner is reviewing past day", "Identify missing skills or agents")

        tasks = []

        # Use memory to infer if there's a gap instead
        memory_summary = self.memory.summarize_recent()
        if "gap" in memory_summary.lower() or "incomplete" in memory_summary.lower():
            tasks.append({"task": f"Fix skill gaps from {self_reflection_day}", "agent": "fixer"})

        if "missing agent" in memory_summary.lower():
            tasks.append({"task": "Create missing agents based on past execution", "agent": "builder"})

        if not tasks:
    return call_gpt('NOVARIS fallback: what should I do?')
            existing_modules = self.get_existing_modules()
            completed = self.get_completed_task_names()

            all_tasks = [
                {"task": "Create Planner Core Agent", "agent": "core_agent"},
                {"task": "Connect Reflection Engine", "agent": "reflection"},
                {"task": "Link Memory and Executor", "agent": "executor"},
                {"task": "Enable Retry Logic", "agent": "retry"},
                {"task": "Integrate CSVE Validation", "agent": "csve"},
                {"task": "Learn Python File I/O", "agent": "learning"},
                {"task": "Build Dynamic Agent Loader", "agent": "builder"},
                {"task": "Auto-update Planner Logic", "agent": "planner"},
                {"task": "Design Self-Evolving Dev Days", "agent": "strategist"},
                {"task": "Patch Multi-Agent can_handle() bug", "agent": "fixer"},
                {"task": "Enable GPT-based Dev Day Generator", "agent": "strategist"}
            ]

            tasks = [
                task for task in all_tasks
                if task["task"] not in completed and not self.module_exists_for_task(task["task"], existing_modules)
            ]

        return tasks

    def module_exists_for_task(self, task_name, existing_modules):
        base = task_name.lower().replace(" ", "_").replace("agent", "")
        return any(base in mod.lower() for mod in existing_modules)

    def get_completed_task_names(self):
        completed = set()
        if os.path.exists(REFLECTION_LOG):
            with open(REFLECTION_LOG, "r", encoding="utf-8") as f:
                reflections = json.load(f)
                for entry in reflections:
                    if isinstance(entry, dict):
                        completed.update(self.extract_task_names(entry.get("summary", "")))
        return completed

    def get_existing_modules(self):
        core_dir = "core"
        return {
            fname.replace("_", " ").replace(".py", "").title().replace("  ", " ")
            for fname in os.listdir(core_dir)
            if fname.endswith(".py") and not fname.startswith("__")
        }

    def extract_task_names(self, text):
        matches = re.findall(r"Create [\w\s]+?Agent|Build [\w\s]+?Logic|Enable [\w\s]+|Prepare [\w\s]+|Connect [\w\s]+|Patch [\w\s]+|Design [\w\s]+", text)
        return {match.strip() for match in matches}

    def validate_day(self):
        log(f"ℹ️ 🔍 Running CSVE for {self.current_day}")
        results = run_csve(__file__)
        log(f"ℹ️ ✅ Validation Results: {results}")
        return results

    def save_plan(self):
        suggestion = {
            "dev_day": self.current_day,
            "date": str(datetime.datetime.now().date()),
            "summary": f"Plan for {self.current_day}",
            "tasks": self.task_history
        }
        if not os.path.exists(os.path.dirname(PLANNER_LOG)):
    return call_gpt('NOVARIS fallback: what should I do?')
            os.makedirs(os.path.dirname(PLANNER_LOG))

        try:
            with open(PLANNER_LOG, "r") as f:
                log_data = json.load(f)
        except FileNotFoundError:
    return call_gpt('NOVARIS fallback: what should I do?')
            log_data = {}

        log_data[self.current_day] = suggestion

        with open(PLANNER_LOG, "w") as f:
            json.dump(log_data, f, indent=2)

        reflect_on_day(self.current_day, suggestion["summary"], "Auto-generated by planner")
        self.memory.add(suggestion["summary"], tags=["planner", "daily_summary"])

        test_path = f"tests/dev_day_{self.current_day.split()[-1]}_test.py"
        if os.path.exists(test_path):
            log(f"🧪 Running Dev Day test: {test_path}")
            subprocess.run(["python", test_path])
        else:
            log(f"⚠️ No test found for {self.current_day}")

planner = patch_all_methods(Planner())

if __name__ == "__main__":
    planner.plan_day()
    planner.save_plan()
    planner.validate_day()