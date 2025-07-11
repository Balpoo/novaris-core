from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# reflection/reflection_engine.py

from agents.adaptive_agent import AdaptiveAgent
from retry_engine import RetryEngine
from memory.reflective_memory import ReflectiveMemory
from task_logger.logger import log_task  # 🆕 Import Task Logger


class ReflectionEngine:
    def __init__(self, memory: ReflectiveMemory):
        self.memory = memory
        self.agent = AdaptiveAgent()

    def reflect_on_task(self, task: str):
        print(f"\n🧠 Reflecting on task: '{task}'")

        # 🔄 Step 1: Run task through AdaptiveAgent
        result, confidence, agent_type = self.agent.handle_task(task)

        # 🤔 Step 2: Retry if confidence < threshold
        retry_engine = RetryEngine(
            agent_pool=[
                self.agent.content_agent,
                self.agent.code_agent,
                self.agent.research_agent,
                self.agent.planning_agent,
                self.agent.web_agent,
            ]
        )

        result, confidence, final_agent, retry_log = retry_engine.try_agents(
            task, (result, confidence, agent_type)
        )

        # 💾 Step 3: Save to reflective memory
        reflection_entry = {
            "task": task,
            "final_result": result,
            "agent": final_agent,
            "confidence": confidence,
        }
        self.memory.add(reflection_entry)

        # 🧠 Step 4: Log to persistent task log (JSONL)
        log_task(
            {
                **reflection_entry,
                "retry_log": retry_log,  # 🧾 Optional, for traceability
            }
        )

        # 🪞 Step 5: Print retry log (optional)
        print(f"\n🔁 Retry Log:")
        for name, conf in retry_log:
            print(f" - {name}: {conf}")

        print(f"\n✅ Final Result [{final_agent}] → Confidence: {confidence}")
        print(result)

        # 🎯 Step 6: Return structured result
        return reflection_entry
