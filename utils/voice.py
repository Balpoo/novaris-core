from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# utils/voice.py

import pyttsx3


def speak(text: str, voice_id=None):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    if voice_id:
        engine.setProperty("voice", voice_id)
    engine.say(text)
    engine.runAndWait()
