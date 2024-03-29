from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.core.dto.user import User
from src.core.utils.default_roles import DEFAULT_ROLES_ID
from src.routers.utils.callbacks.admin_callback_data import (
    ADD_ADMIN_DATA,
    REMOVE_ADMIN_DATA,
    SUBMIT_ADD_ADMIN_DATA,
    SUBMIT_REMOVE_ADMIN_DATA,
)
from src.routers.utils.checkers.admin_checker import (
    admin_check,
    callback_admin_check,
)
from src.routers.utils.filters.buttons_filter import ButtonsFilter
from src.routers.utils.keyboards.admin_keyboards import (
    get_admin_settings_inline,
)
from src.routers.utils.keyboards.buttons.admin_buttons import get_admin_buttons
from src.routers.utils.keyboards.common_keyboards import get_submit_inline
from src.routers.utils.states.admin_states.add_admin_state import AddAdminState
from src.services.users.admin_service import AdminService
from src.utils.language_handler import get_language


class AdminSettingsRouter(Router):
    def __init__(self, admin_service: AdminService):
        super().__init__(name="admin-settings-router")

        self.admin_service = admin_service

        admin_buttons = get_admin_buttons()

        self.message(ButtonsFilter(admin_buttons["admins-settings"]))(
            self.admin_settings
        )
        self.callback_query(F.data.startswith(REMOVE_ADMIN_DATA))(
            self.remove_admin
        )
        self.callback_query(F.data.startswith(SUBMIT_REMOVE_ADMIN_DATA))(
            self.remove_admin_submit
        )
        self.callback_query(F.data == ADD_ADMIN_DATA)(self.add_admin)
        self.message(AddAdminState.set_admin)(self.add_admin_forward)
        self.callback_query(F.data.startswith(SUBMIT_ADD_ADMIN_DATA))(
            self.add_admin_submit
        )

    @admin_check
    async def admin_settings(self, message: Message):
        admins = await self.admin_service.get_users()
        lang_text = get_language(message.from_user.language_code)
        await message.answer(
            text=lang_text.messages["admins-list"],
            reply_markup=get_admin_settings_inline(admins, lang_text.buttons),
        )

    @callback_admin_check
    async def remove_admin(self, callback: CallbackQuery):
        lang_text = get_language(callback.from_user.language_code)
        admin_id = callback.data.replace(REMOVE_ADMIN_DATA, "")
        admin = await self.admin_service.get_user(int(admin_id))
        callback_data = SUBMIT_REMOVE_ADMIN_DATA + admin_id + "-"
        await callback.message.answer(
            text=lang_text.messages["remove-admin-submit"].format(
                username=admin.username
            ),
            reply_markup=get_submit_inline(
                callback_data=callback_data,
                buttons=lang_text.buttons,
            ),
        )
        await callback.message.delete()

    @callback_admin_check
    async def remove_admin_submit(self, callback: CallbackQuery):
        lang_text = get_language(callback.from_user.language_code)
        admin_id, submit = callback.data.replace(
            SUBMIT_REMOVE_ADMIN_DATA, ""
        ).split("-")
        admin = await self.admin_service.get_user(int(admin_id))
        if submit == "yes":
            await self.admin_service.delete_user(int(admin_id))
            await callback.message.edit_text(
                text=lang_text.messages["admin-removed"].format(
                    username=admin.username
                )
            )
        else:
            await callback.message.edit_text(
                text=lang_text.messages["cancelled"]
            )

    @callback_admin_check
    async def add_admin(self, callback: CallbackQuery, state: FSMContext):
        lang_text = get_language(callback.from_user.language_code)
        await callback.message.answer(text=lang_text.messages["add-admin"])
        await callback.message.delete()
        await state.set_state(AddAdminState.set_admin)

    @admin_check
    async def add_admin_forward(self, message: Message, state: FSMContext):
        lang_text = get_language(message.from_user.language_code)
        if message.forward_from:
            user = User(
                id=message.forward_from.id,
                username=message.forward_from.username,
                role_id=DEFAULT_ROLES_ID["admin"],
            )
            await state.update_data(user=user)
            await message.answer(
                text=lang_text.messages["add-admin-submit"].format(
                    username=user.username
                ),
                reply_markup=get_submit_inline(
                    callback_data=SUBMIT_ADD_ADMIN_DATA,
                    buttons=lang_text.buttons,
                ),
            )
        else:
            await message.answer(text=lang_text.messages["cancelled"])
            await state.clear()

    @callback_admin_check
    async def add_admin_submit(
        self, callback: CallbackQuery, state: FSMContext
    ):
        lang_text = get_language(callback.from_user.language_code)
        submit = callback.data.replace(SUBMIT_ADD_ADMIN_DATA, "")
        if submit == "yes":
            state_data = await state.get_data()
            user = state_data["user"]
            await self.admin_service.create_user(user)
            await callback.message.edit_text(
                text=lang_text.messages["admin-added"].format(
                    username=user.username
                )
            )
        else:
            await callback.message.edit_text(
                text=lang_text.messages["cancelled"]
            )
        await state.clear()
