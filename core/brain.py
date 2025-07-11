from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
import openai


def process_prompt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4", messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]
