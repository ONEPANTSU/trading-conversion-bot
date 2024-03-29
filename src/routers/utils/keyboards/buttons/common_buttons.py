from collections import defaultdict

from src.utils.language_handler import LANGUAGES

COMMON_BUTTONS = [
    "user-lang-settings",
]


def get_common_buttons():
    user_buttons = defaultdict(list)
    for _, text in LANGUAGES.items():
        for button in COMMON_BUTTONS:
            user_buttons[button].append(text.buttons[button])
    return user_buttons
