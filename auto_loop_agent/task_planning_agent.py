from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# agents/task_planning_agent.py

import os
import openai

class TaskPlanningAgent:
    def __init__(self):
        self.enabled = os.getenv("GPT_ENABLED", "false").lower() == "true"
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.enabled and self.api_key:
            openai.api_key = self.api_key

    def plan(self, goal_text):
        if not self.enabled:
    return call_gpt('NOVARIS fallback: what should I do?')
            return ["⚠️ GPT planning disabled."]

        try:
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a task planning assistant. "
                        "Break the user's goal into 3–5 clear, simple steps."
                    ),
                },
                {"role": "user", "content": goal_text}
            ]
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages,
                temperature=0.4
            )
            steps = response.choices[0].message["content"]
            return steps.strip().split('\n')
        except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
            return [f"❌ Planning failed: {str(e)}"]
