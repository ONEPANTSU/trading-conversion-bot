from collections import defaultdict

from src.routers.utils.keyboards.buttons.common_buttons import COMMON_BUTTONS
from src.utils.language_handler import LANGUAGES

USER_BUTTONS = [] + COMMON_BUTTONS


def get_user_buttons():
    user_buttons = defaultdict(list)
    for _, text in LANGUAGES.items():
        for button in USER_BUTTONS:
            user_buttons[button].append(text.buttons[button])
    return user_buttons
