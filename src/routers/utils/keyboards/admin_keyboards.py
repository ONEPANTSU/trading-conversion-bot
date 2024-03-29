from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from src.core.models import User
from src.routers.utils.callbacks.admin_callback_data import (
    ADD_ADMIN_DATA,
    ADD_EDITOR_DATA,
    REMOVE_ADMIN_DATA,
    REMOVE_EDITOR_DATA,
    SELECT_ADMIN_DATA,
    SELECT_EDITOR_DATA,
)
from src.routers.utils.keyboards.buttons.admin_buttons import get_admin_buttons


def get_admin_keyboard(buttons: dict[str, str]) -> ReplyKeyboardMarkup:
    keyboard = []
    for button in get_admin_buttons():
        keyboard.append([KeyboardButton(text=buttons[button])])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_admin_settings_inline(
    admins: list[User], buttons: dict[str, str]
) -> InlineKeyboardMarkup:
    keyboard = list()
    for admin in admins:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=admin.username,
                    callback_data=f"{SELECT_ADMIN_DATA}{admin.id}",
                ),
                InlineKeyboardButton(
                    text="️❌", callback_data=f"{REMOVE_ADMIN_DATA}{admin.id}"
                ),
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text=buttons["add-admin"], callback_data=ADD_ADMIN_DATA
            ),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_editor_settings_inline(
    editors: list[User], buttons: dict[str, str]
) -> InlineKeyboardMarkup:
    keyboard = list()
    for editor in editors:
        keyboard.append(
            [
                InlineKeyboardButton(
                    text=editor.username,
                    callback_data=f"{SELECT_EDITOR_DATA}{editor.id}",
                ),
                InlineKeyboardButton(
                    text="️❌", callback_data=f"{REMOVE_EDITOR_DATA}{editor.id}"
                ),
            ]
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                text=buttons["add-editor"], callback_data=ADD_EDITOR_DATA
            ),
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
