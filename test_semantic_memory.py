from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# test_semantic_memory.py

from memory.semantic_memory import SemanticMemory


def test_semantic_memory():
    print("🧠 Initializing Semantic Memory...")
    mem = patch_all_methods(SemanticMemory())

    # Add entries
    mem.add("Schedule team meeting on Monday")
    mem.add("Fix broken login functionality in app")
    mem.add("Draft blog post on AI agents and memory")
    mem.add("Prepare roadmap for Q4 AI module")
    mem.add("Send follow-up email to the client")

    # Query test
    print("\n🔍 Query: 'meeting'")
    results = mem.query("meeting")
    for i, result in enumerate(results, 1):
        print(f" {i}. {result}")


if __name__ == "__main__":
    test_semantic_memory()
