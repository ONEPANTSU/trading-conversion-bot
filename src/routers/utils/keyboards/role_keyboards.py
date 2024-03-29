from aiogram.types import ReplyKeyboardMarkup

from src.core.utils.default_roles import DEFAULT_ROLES_ID
from src.routers.utils.keyboards.admin_keyboards import get_admin_keyboard
from src.routers.utils.keyboards.editor_keyboards import get_editor_keyboard
from src.routers.utils.keyboards.user_keyboards import (
    get_user_settings_keyboard,
)


def get_main_keyboard(
    role_id: int, buttons: dict[str, str]
) -> ReplyKeyboardMarkup:
    if role_id == DEFAULT_ROLES_ID["user"]:
        return get_user_settings_keyboard(buttons)
    elif role_id == DEFAULT_ROLES_ID["admin"]:
        return get_admin_keyboard(buttons)
    elif role_id == DEFAULT_ROLES_ID["editor"]:
        return get_editor_keyboard(buttons)
