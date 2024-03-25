from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from routers.utils.keyboards.buttons.editor_buttons import get_editor_buttons


def get_editor_keyboard(buttons: dict[str, str]) -> ReplyKeyboardMarkup:
    keyboard = []
    for button in get_editor_buttons():
        keyboard.append([KeyboardButton(text=buttons[button])])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_language_inline(
    callback_data, buttons: dict[str, str]
) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=buttons["ru"], callback_data=f"{callback_data}ru"
            ),
            InlineKeyboardButton(
                text=buttons["en"], callback_data=f"{callback_data}en"
            ),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
