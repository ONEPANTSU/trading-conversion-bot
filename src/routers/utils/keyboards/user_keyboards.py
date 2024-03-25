from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.routers.utils.callbacks.user_callback_data import USER_START_DATA


def get_user_start_inline(buttons: dict[str, str]) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=buttons["user-start"], callback_data=USER_START_DATA
            ),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
