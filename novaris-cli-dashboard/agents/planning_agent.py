from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# agents/planning_agent.py


class PlanningAgent:
    """Handles planning-related tasks."""

    def handle(self, task: str) -> tuple:
        """
        Generate a planning response.

        Parameters:
            task (str): The user’s planning request.

        Returns:
            tuple: (response text, confidence score)
        """
        response = f"Planned detailed steps for: '{task}'"
        confidence = 0.92
        return response, confidence
