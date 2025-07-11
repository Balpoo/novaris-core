from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# run_dashboard.py

from memory.task_logger import log_task
from dashboard.app import FlipkartDashboard

if __name__ == "__main__":
    FlipkartDashboard().run()
