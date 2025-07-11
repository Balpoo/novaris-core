from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# plugins/ecommerce_platform_plugin.py


class PluginAgent:
    def can_handle(self, task: str) -> bool:
        keywords = ["ecommerce", "platform", "flipkart", "amazon"]
        return any(word in task.lower() for word in keywords)

    def handle(self, task: str) -> tuple:
        response = (
            "🛒 Building Flipkart-like eCommerce system:\n"
            "- 📦 Modules: Product, Cart, Orders, Payments, Auth\n"
            "- 🛠 Stack: React + Node + MongoDB (or Supabase)\n"
            "- 🔒 Auth: Firebase or OAuth (Google/Phone)\n"
            "- ☁️ Hosting: Vercel + Railway\n"
            "- 📁 DevOps ready. GitHub Actions + Auto deploy\n"
            "- 📄 Docs & roadmap auto-generatable.\n\n"
            "✅ Ready to scaffold project now?"
        )
        return response, 0.98


# Optional direct call (CommandTab test shortcut)
def handle_ecommerce_task(task: str) -> str:
    return "🛒 eCommerce plugin triggered for: " + task
