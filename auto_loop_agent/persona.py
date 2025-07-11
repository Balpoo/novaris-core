from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# agents/persona.py


class AgentPersona:
    def __init__(self, name, role, tone="neutral", voice_id=None):
        self.name = name
        self.role = role
        self.tone = tone
        self.voice_id = voice_id  # Optional: TTS integration
        self.emotion_state = "calm"

    def describe(self):
        return f"{self.name} the {self.role}, tone: {self.tone}, emotion: {self.emotion_state}"

    def adjust_emotion(self, event: str):
        if "error" in event.lower():
            self.emotion_state = "frustrated"
        elif "success" in event.lower():
            self.emotion_state = "happy"
        elif "fail" in event.lower():
            self.emotion_state = "concerned"
        else:
            self.emotion_state = "calm"
