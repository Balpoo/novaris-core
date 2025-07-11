# main.py

import os
import time
import threading
from datetime import datetime
import traceback


# ✅ Self-wiring at boot
try:
    from core.self_wiring_engine import run_self_wiring

    run_self_wiring()
except Exception:
    print("❌ Self-wiring failed:")
    traceback.print_exc()

# ✅ Background loop to monitor self-wiring
try:
    from core.boot_checker import loop_self_wiring

    threading.Thread(target=loop_self_wiring, daemon=True).start()
except Exception:
    print("⚠️ Boot checker thread failed.")

# ✅ Observe chat messages for learning
try:
    from core.chat_observer import observe_chat_message
except Exception:

    def observe_chat_message(message, **kwargs):
        print("⚠️ Chat observer unavailable.")


# ✅ Auto-clean corrupted files
EXCLUDE_FOLDERS = {"venv", ".git", "__pycache__", ".idea", ".vscode", ".mypy_cache"}
SAFE_FILE_TYPES = {
    ".py": ("import", "from", "class", "def", "#", '"""', "'''"),
    ".html": ("<!DOCTYPE", "<html", "<!—", "<!doctype"),
    ".css": ("*", ".", "#", "@import", ":root", "body", "html"),
    ".js": ("function", "var", "const", "let", "import", "export"),
    ".json": ("{", "["),
    ".yml": ("#", "---"),
    ".yaml": ("#", "---"),
    ".md": ("#", "---"),
    ".txt": ("#", "-", "•"),
    ".j2": ("{%", "{{", "#"),
    ".jinja": ("{%", "{{", "#"),
    ".tpl": ("{%", "{{", "#"),
}


def is_valid_start(line, extension):
    stripped = line.strip()
    valid_starts = SAFE_FILE_TYPES.get(extension, [])
    return any(stripped.startswith(start) for start in valid_starts)


def clean_file(path):
    _, ext = os.path.splitext(path)
    if ext not in SAFE_FILE_TYPES:
        return False
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if not lines or is_valid_start(lines[0], ext):
            return False

        for i, line in enumerate(lines):
            if is_valid_start(line, ext):
                cleaned = lines[i:]
                break
        else:
            cleaned = []

        with open(path, "w", encoding="utf-8") as f:
            f.writelines(cleaned)

        print(f"✅ Cleaned: {path}")
        return True

    except Exception as e:
        print(f"❌ Error cleaning {path}: {e}")
        return False


def scan_and_clean(root):
    cleaned_files = []
    for folder in os.listdir(root):
        path = os.path.join(root, folder)
        if os.path.isdir(path) and folder not in EXCLUDE_FOLDERS:
            for sub_root, _, files in os.walk(path):
                for file in files:
                    if os.path.splitext(file)[1].lower() in SAFE_FILE_TYPES:
                        file_path = os.path.join(sub_root, file)
                        if clean_file(file_path):
                            cleaned_files.append(file_path)
    return cleaned_files


print("🧼 Cleaning corrupted project files...")
scan_and_clean(".")

# ✅ Core Engine Imports (Fail-safe)
try:
    from core.web_learning_engine import WebLearningEngine
    from core.planner import Planner
    from core.memory_engine import MemoryEngine
    from core.reflection_engine import reflect_on_day
    from core.retry_engine import start_retry_engine
    from core.auto_skill_registrar import auto_register_skills
    from core.skill_router import suggest_skills
except ImportError as e:
    print(f"❌ Core module import failed: {e}")
    raise

# ✅ Agents & Utils
from config.config_loader import load_config
from agents.code_patcher_agent import run_code_patcher
from agents.planning_agent import PlanningAgent
from agents.memory_agent import MemoryAgent
from agents.multi_agent_orchestrator import MultiAgentOrchestrator
from agents.dynamic_agent_builder import DynamicAgentBuilder
from agents.agent_chain_executor import AgentChainExecutor
from agents.fallback_agent import GPTFallbackAgent
from agents.skill_chain_executor import SkillChainExecutor
from memory.semantic_memory import SemanticMemory
from utils.task_feedback import show_task_feedback, complete_task_feedback
from utils.voice import speak


@auto_debug_wrap
def boot_novaris():
    try:
        config = load_config()
        skills = auto_register_skills()
        memory = SemanticMemory()
        fallback_agent = GPTFallbackAgent()
        executor = SkillChainExecutor(list(skills.values()))
        planner_agent = Planner()
        start_retry_engine()
        print("🧠 NOVARIS Core Booted ✅")
        print("🔧 Loaded Skills:", list(skills.keys()))
        return config, skills, memory, fallback_agent, executor, planner_agent
    except Exception:
        print("❌ Error during boot:")
        traceback.print_exc()
        raise


@auto_debug_wrap
def main():
    print("🮩 Auto-patching all agents...")
    try:
        patched_files = run_code_patcher()
        print(f"✅ Patched: {patched_files}")
    except Exception as e:
        print(f"⚠️ Agent patching failed: {e}")

    config, skills, memory, fallback_agent, executor, planner_agent = boot_novaris()
    web_learner = WebLearningEngine()
    builder = DynamicAgentBuilder()

    agents = [PlanningAgent(), MemoryAgent()]
    orchestrator = MultiAgentOrchestrator(agents)
    chain_executor = AgentChainExecutor(orchestrator)

    while True:
        try:
            user_input = input("You > ").strip()

            if not user_input:
                continue

            observe_chat_message(user_input)

            if user_input.lower() in ["exit", "quit"]:
                print("👋 Exiting NOVARIS. Goodbye, Karan.")
                break

            elif user_input.lower().startswith("learn:"):
                topic = user_input.split("learn:", 1)[1].strip()
                result = web_learner.learn_from_web(topic)
                print("\n📚 Web Learning Result:", result)

            elif user_input.lower() == "reflect":
                print("🪞 Reflective Memory:")
                print("\n".join(memory.query("task")))

            elif user_input.lower().startswith("agent-profile:"):
                agent_name = user_input.split("agent-profile:")[1].strip()
                for agent in agents:
                    if agent.name.lower() == agent_name.lower():
                        print(f"🧠 Persona for {agent.name}:")
                        print(agent.persona.describe())
                        break
                else:
                    print(f"❌ No agent named '{agent_name}' found.")

            elif user_input.lower().startswith("agent-reflect:"):
                agent_name = user_input.split("agent-reflect:")[1].strip()
                for agent in agents:
                    if (
                        hasattr(agent, "memory")
                        and agent.name.lower() == agent_name.lower()
                    ):
                        print(f"\n📜 Reflection from {agent.name}:")
                        print(agent.memory.reflect())
                        break
                else:
                    print(f"❌ No agent named '{agent_name}' found.")

            elif user_input.lower().startswith("plan:"):
                goal = user_input[5:].strip()
                plan = planner_agent.plan(goal)
                print("\n📋 Task Plan:")
                for step in plan:
                    print("✅", step)

            elif user_input.lower().startswith("create-agent:"):
                goal = user_input.split("create-agent:")[1].strip()
                agent = builder.create_agent(goal)
                agents.append(agent)
                print(f"🧠 New agent for '{goal}' registered.")

            elif user_input.lower().startswith("chain:"):
                raw = user_input.split("chain:")[1].strip()
                subtasks = [t.strip() for t in raw.split("->")]
                results = chain_executor.execute_chain(subtasks)
                print("\n🔗 Chained Agent Results:")
                for task, result in results:
                    print(f"🧹 {task} → {result}")
                    speak(result)

            else:
                print("🧠 Running NOVARIS Planner for today...")
                tasks = planner_agent.plan_day()
                planner_agent.validate_day()
                summary = f"Completed {len(tasks)} tasks via planner."
                next_steps = [t["task"] for t in tasks]
                reflect_on_day(planner_agent.current_day, summary, next_steps)
                memory.add(summary, tags=["planner", "daily_summary"])
                memory.add(user_input)

                past_matches = memory.query(user_input)
                if past_matches:
                    print("🧠 Memory Matches:")
                    for match in past_matches:
                        print(f" - {match}")

                matches = suggest_skills(skills, user_input)
                if not matches:
                    print("⚠️ No skills matched. Trying GPT fallback...")
                    fallback_context = " | ".join(past_matches)
                    gpt_response = fallback_agent.run(
                        user_input, context=fallback_context
                    )
                    print("🧠 GPT Fallback:", gpt_response)
                    speak(gpt_response)
                else:
                    print("✅ Tool Responses:")
                    for name, response in matches:
                        show_task_feedback(name)
                        time.sleep(1)
                        complete_task_feedback(response)
                        speak(response)

                agent_result = orchestrator.assign_and_execute(user_input)
                print(f"🌟 Agent Execution Result: {agent_result}")
                speak(agent_result)

        except Exception:
            print("❌ Critical error during user interaction:")
            traceback.print_exc()


if __name__ == "__main__":
    main()
