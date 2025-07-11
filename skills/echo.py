from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods


def run(input_text):
    return f"ECHO: {input_text}"
