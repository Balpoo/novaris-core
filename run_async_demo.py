from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# run_async_demo.py

import asyncio
from tasks.task_tree_node import TaskTreeNode
from agents.execution_engine_async import AsyncExecutionEngine
from agents.agent_registry import AgentRegistry
from agents.knowledge_agent import KnowledgeAgent
from utils.pretty_tree import print_task_tree  # ✅ Tree visualizer


async def main():
    print("🚀 Starting NOVARIS Async Execution Demo...\n")

    # 🧠 Step 1: Load documents into knowledge base
    k_agent = KnowledgeAgent()
    k_agent.ingest_file("docs/company_profile.txt")
    k_agent.ingest_file("docs/financials.xlsx")
    k_agent.ingest_file("docs/vision_slide.pptx")

    print("\n📚 Documents Ingested:")
    for doc in k_agent.list_documents():
        print(f"   • {doc}")

    # 🔁 Step 2: Setup Agent Registry + Async Execution Engine
    registry = AgentRegistry(knowledge_agent=k_agent)
    engine = AsyncExecutionEngine(registry)

    # 🌳 Step 3: Build async task tree
    root = TaskTreeNode("T1", "Plan Corporate Launch Event")

    vision = TaskTreeNode("T2", "Summarize company vision", parent=root)
    finance = TaskTreeNode("T3", "Analyze financials report", parent=root)
    branding = TaskTreeNode("T4", "Design brand identity", parent=root)  # Fallback test

    root.add_child(vision)
    root.add_child(finance)
    root.add_child(branding)

    # 🚀 Step 4: Execute tree asynchronously
    tree_result = await engine.execute_tree(root)

    # 📄 Step 5: Print tree results
    print("\n✅ Async Task Tree Execution Completed.\n")
    print_task_tree(tree_result)  # ✅ Bonus: Pretty print


if __name__ == "__main__":
    asyncio.run(main())
