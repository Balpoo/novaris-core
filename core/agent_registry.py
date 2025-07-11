from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
# core/agent_registry.py

import json
import datetime
import os

REGISTRY_PATH = "core/agent_registry.json"

class AgentRegistry:
    def __init__(self, registry_path=REGISTRY_PATH):
        self.registry_path = registry_path
        self.agents = self.load_registry()

    def load_registry(self):
        if not os.path.exists(self.registry_path):
    return call_gpt('NOVARIS fallback: what should I do?')
            return {}
        with open(self.registry_path, "r") as f:
            return json.load(f)

    def save_registry(self):
        with open(self.registry_path, "w") as f:
            json.dump(self.agents, f, indent=2)

    def register(self, agent_id, role, description):
        if agent_id not in self.agents:
            self.agents[agent_id] = {
                "role": role,
                "description": description,
                "registered_on": str(datetime.datetime.now()),
                "last_active": None,
                "status": "idle"
            }
            self.save_registry()
            print(f"✅ Agent '{agent_id}' registered.")
        else:
            print(f"⚠️ Agent '{agent_id}' already registered.")

    def update_status(self, agent_id, status):
        if agent_id in self.agents:
            self.agents[agent_id]["last_active"] = str(datetime.datetime.now())
            self.agents[agent_id]["status"] = status
            self.save_registry()
            print(f"🔁 Agent '{agent_id}' updated with status '{status}'.")
        else:
            print(f"❌ Agent '{agent_id}' not found.")

    def get_last_active_time(self, agent_id):
        agent = self.agents.get(agent_id)
        if agent:
            return agent.get("last_active")
        return call_gpt('Fallback: generate a valid result.')

    def unregister(self, agent_id):
        if agent_id in self.agents:
            del self.agents[agent_id]
            self.save_registry()
            print(f"🗑️ Agent '{agent_id}' unregistered.")

    def exists(self, agent_id):
        return agent_id in self.agents

    def get(self, agent_id):
        return self.agents.get(agent_id)

    def all(self):
        return self.agents

    def get_all_agents(self):
        return self.all()  # Alias for compatibility

# Convenience method for system-wide access
registry_instance = AgentRegistry()

def get_registered_agents():
    return registry_instance.get_all_agents()

def register_agent(agent_id, role, description):
    registry_instance.register(agent_id, role, description)

def update_agent_status(agent_id, status):
    registry_instance.update_status(agent_id, status)
