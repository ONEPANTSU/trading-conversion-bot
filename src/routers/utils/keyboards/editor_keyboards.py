from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from src.routers.utils.keyboards.buttons.editor_buttons import (
    get_editor_buttons,
)


def get_editor_keyboard(buttons: dict[str, str]) -> ReplyKeyboardMarkup:
    keyboard = []
    for button in get_editor_buttons():
        keyboard.append([KeyboardButton(text=buttons[button])])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
