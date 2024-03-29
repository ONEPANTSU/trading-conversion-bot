from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.routers.utils.callbacks.user_callback_data import (
    USER_LANG_SETTINGS_DATA,
)
from src.routers.utils.filters.buttons_filter import ButtonsFilter
from src.routers.utils.keyboards.buttons.user_buttons import get_user_buttons
from src.routers.utils.keyboards.common_keyboards import get_language_inline
from src.routers.utils.keyboards.role_keyboards import get_main_keyboard
from src.services.users.user_service import UserService
from src.utils.language_handler import get_language


class LanguageRouter(Router):
    def __init__(self, user_service: UserService):
        super().__init__(name="user-language-router")
        self.user_service = user_service

        user_buttons = get_user_buttons()

        self.message(ButtonsFilter(user_buttons["user-lang-settings"]))(
            self.language_settings
        )
        self.callback_query(F.data.startswith(USER_LANG_SETTINGS_DATA))(
            self.set_language
        )

    async def language_settings(self, message: Message, state: FSMContext):
        await state.clear()
        lang_text = await self.get_lang_text(message.from_user.id)
        await message.answer(
            text=lang_text.messages["user-lang-settings"],
            reply_markup=get_language_inline(
                callback_data=USER_LANG_SETTINGS_DATA,
                buttons=lang_text.buttons,
            ),
        )

    async def set_language(self, callback: CallbackQuery):
        user = await self.user_service.get_user(callback.from_user.id)
        user.language_code = callback.data.replace(USER_LANG_SETTINGS_DATA, "")
        await self.user_service.update_user(user)
        lang_text = get_language(user.language_code)
        keyboard = get_main_keyboard(user.role_id, lang_text.buttons)
        await callback.message.answer(
            text=lang_text.messages["user-lang-changed"],
            reply_markup=keyboard,
        )
        await callback.message.delete()

    async def get_lang_text(self, user_id: int):
        lang_code = await self.user_service.get_user_lang_code(user_id)
        return get_language(lang_code)
