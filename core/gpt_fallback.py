# core/gpt_fallback.py

import os
import traceback
from datetime import datetime

# ✅ Setup OpenAI client for openai>=1.0.0
try:
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    GPT_ENABLED = True
except ImportError:
    GPT_ENABLED = False
    client = None

LOG_FILE = "logs/gpt_fallback_errors.log"
DEFAULT_SYSTEM_PROMPT = (
    "You are a senior AI engineer helping NOVARIS self-build safely."
)


def log_gpt_error(error_msg: str):
    os.makedirs("logs", exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] GPT Fallback Error:\n{error_msg}\n\n")


def call_gpt(
    prompt: str,
    system: str = DEFAULT_SYSTEM_PROMPT,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.5,
) -> str:
    if not GPT_ENABLED:
        msg = "⚠️ GPT fallback unavailable: openai package not installed."
        log_gpt_error(msg)
        return msg

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        tb = traceback.format_exc()
        log_gpt_error(f"{e}\n{tb}")
        print(f"[GPT Fallback Error] {e}")
        print(tb)
        return "❗ GPT fallback failed. Check logs for error trace."


# ✅ Generate Dev Day task list from a topic
def generate_tasks_from_topic(topic: str) -> str:
    prompt = f"Generate a realistic, detailed Dev Day task list for the AI OS NOVARIS to learn: {topic}"
    return call_gpt(prompt)


# ✅ Generate agent code based on a topic
def generate_agent_code(topic: str) -> str:
    agent_name = topic.replace(" ", "") + "Agent"
    prompt = f"""
Write a Python class named `{agent_name}` that implements an AI agent.

Include methods:
- can_handle(task: str): returns True if the agent is responsible
- handle_task(task: str): executes the task and returns a result

The agent's responsibility is: {topic}
Only output the code.
"""
    return call_gpt(prompt)


# ✅ Suggest a fix from an error trace
def suggest_fix_from_error(error_trace: str) -> str:
    prompt = f"""
You are debugging a Python program. Here's the traceback:

{error_trace}

Please analyze the issue and respond with the updated and corrected code only.
"""
    return call_gpt(prompt)


# ✅ Direct GPT code generator
def gpt_generate_code(prompt: str) -> str:
    return call_gpt(prompt)
