from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# dashboard/widgets/theme_toggle.py

from textual.widgets import Button


class ThemeToggle(Button):
    def __init__(self):
        super().__init__(label="Toggle Theme", id="toggle-theme")

    async def on_button_pressed(self, event: Button.Pressed):
        from textual.app import get_app

        app = get_app()
        current = app.stylesheet_path.name
        if "dark" in current:
            app.stylesheet_path = "dashboard/themes/light.css"
        else:
            app.stylesheet_path = "dashboard/themes/dark.css"
