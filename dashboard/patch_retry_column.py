from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
from retry_logger import initialize_retry_column

initialize_retry_column()
print("✅ Retry column ensured in task_logs table.")
