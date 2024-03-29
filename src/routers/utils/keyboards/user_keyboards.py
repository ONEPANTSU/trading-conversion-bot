from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from src.routers.utils.callbacks.user_callback_data import USER_START_DATA


def get_user_settings_keyboard(buttons: dict[str, str]) -> ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton(text=buttons["user-lang-settings"]),
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_user_start_inline(buttons: dict[str, str]) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=buttons["user-start"], callback_data=USER_START_DATA
            ),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
