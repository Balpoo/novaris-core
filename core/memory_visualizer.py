from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# core/memory_visualizer.py

import json
from core.memory_engine import MemoryEngine  # ✅ Absolute import for reliable execution


class MemoryVisualizer:
    def __init__(self):
        self.memory = patch_all_methods(MemoryEngine())

    def generate_graph_data(self):
        thoughts = self.memory.fetch_all_thoughts()
        nodes = []
        edges = []
        seen_ids = set()

        for idx, thought in enumerate(thoughts):
            node_id = f"node_{idx}"
            nodes.append(
                {
                    "id": node_id,
                    "label": thought.get("summary") or f"Thought {idx+1}",
                    "type": thought.get("source") or "general",
                    "timestamp": thought.get("timestamp"),
                }
            )
            seen_ids.add(node_id)

            # Draw connection if related_to exists
            related_to = thought.get("related_to")
            if related_to is not None:
                target_node = f"node_{related_to}"
                if target_node not in seen_ids:
                    target_node = "node_0"
                edges.append(
                    {"from": node_id, "to": target_node, "label": "relates to"}
                )

        return {"nodes": nodes, "edges": edges}

    def export_graph_json(self, path="exports/memory_graph.json"):
        graph_data = self.generate_graph_data()
        with open(path, "w") as f:
            json.dump(graph_data, f, indent=4)
        print(f"✅ Memory graph exported to {path}")
