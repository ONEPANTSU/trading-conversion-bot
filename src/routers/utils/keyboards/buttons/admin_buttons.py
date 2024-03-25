from collections import defaultdict

from src.routers.utils.keyboards.buttons.editor_buttons import EDITOR_BUTTONS
from src.utils.language_handler import LANGUAGES

ADMIN_BUTTONS = ["admins-settings", "editors-settings"] + EDITOR_BUTTONS


def get_admin_buttons():
    admin_buttons = defaultdict(list)
    for _, text in LANGUAGES.items():
        for button in ADMIN_BUTTONS:
            admin_buttons[button].append(text.buttons[button])
    return admin_buttons
