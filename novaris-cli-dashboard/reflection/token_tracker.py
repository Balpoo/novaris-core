from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# reflection/token_tracker.py


class TokenTracker:
    def __init__(self):
        self.total_tokens = 0
        self.total_retries = 0

    def log_tokens(self, tokens: int):
        self.total_tokens += tokens

    def log_retry(self):
        self.total_retries += 1

    def stats(self) -> str:
        return f"Tokens: {self.total_tokens} | Retries: {self.total_retries}"
