from collections import defaultdict

from src.utils.language_handler import LANGUAGES

EDITOR_BUTTONS = ["send-post", "send-private-post", "get-media-id"]


def get_editor_buttons():
    editor_buttons = defaultdict(list)
    for _, text in LANGUAGES.items():
        for button in EDITOR_BUTTONS:
            editor_buttons[button].append(text.buttons[button])
    return editor_buttons
