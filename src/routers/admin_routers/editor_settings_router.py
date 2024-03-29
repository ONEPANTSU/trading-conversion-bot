from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.core.dto.user import User
from src.core.utils.default_roles import DEFAULT_ROLES_ID
from src.routers.utils.callbacks.admin_callback_data import (
    ADD_EDITOR_DATA,
    REMOVE_EDITOR_DATA,
    SUBMIT_ADD_EDITOR_DATA,
    SUBMIT_REMOVE_EDITOR_DATA,
)
from src.routers.utils.checkers.admin_checker import (
    admin_check,
    callback_admin_check,
)
from src.routers.utils.filters.buttons_filter import ButtonsFilter
from src.routers.utils.keyboards.admin_keyboards import (
    get_editor_settings_inline,
)
from src.routers.utils.keyboards.buttons.admin_buttons import get_admin_buttons
from src.routers.utils.keyboards.common_keyboards import get_submit_inline
from src.routers.utils.states.admin_states.add_editor_state import (
    AddEditorState,
)
from src.services.users.admin_service import AdminService
from src.services.users.editor_service import EditorService
from src.utils.language_handler import get_language


class EditorSettingsRouter(Router):
    def __init__(
        self, editor_service: EditorService, admin_service: AdminService
    ):
        super().__init__(name="editor-settings-router")

        self.editor_service = editor_service
        self.admin_service = admin_service

        admin_buttons = get_admin_buttons()

        self.message(ButtonsFilter(admin_buttons["editors-settings"]))(
            self.editor_settings
        )
        self.callback_query(F.data.startswith(REMOVE_EDITOR_DATA))(
            self.remove_editor
        )
        self.callback_query(F.data.startswith(SUBMIT_REMOVE_EDITOR_DATA))(
            self.remove_editor_submit
        )
        self.callback_query(F.data == ADD_EDITOR_DATA)(self.add_editor)
        self.message(AddEditorState.set_editor)(self.add_editor_forward)
        self.callback_query(F.data.startswith(SUBMIT_ADD_EDITOR_DATA))(
            self.add_editor_submit
        )

    @admin_check
    async def editor_settings(self, message: Message, state: FSMContext):
        await state.clear()
        editors = await self.editor_service.get_users()
        lang_text = await self.get_lang_text(message.from_user.id)
        await message.answer(
            text=lang_text.messages["editors-list"],
            reply_markup=get_editor_settings_inline(
                editors, lang_text.buttons
            ),
        )

    @callback_admin_check
    async def remove_editor(self, callback: CallbackQuery):
        lang_text = await self.get_lang_text(callback.from_user.id)
        editor_id = callback.data.replace(REMOVE_EDITOR_DATA, "")
        editor = await self.editor_service.get_user(int(editor_id))
        callback_data = SUBMIT_REMOVE_EDITOR_DATA + editor_id + "-"
        await callback.message.answer(
            text=lang_text.messages["remove-editor-submit"].format(
                username=editor.username
            ),
            reply_markup=get_submit_inline(
                callback_data=callback_data,
                buttons=lang_text.buttons,
            ),
        )
        await callback.message.delete()

    @callback_admin_check
    async def remove_editor_submit(self, callback: CallbackQuery):
        lang_text = await self.get_lang_text(callback.from_user.id)
        editor_id, submit = callback.data.replace(
            SUBMIT_REMOVE_EDITOR_DATA, ""
        ).split("-")
        editor = await self.editor_service.get_user(int(editor_id))
        if submit == "yes":
            editor.role_id = DEFAULT_ROLES_ID["user"]
            await self.editor_service.update_user(editor)
            await callback.message.edit_text(
                text=lang_text.messages["editor-removed"].format(
                    username=editor.username
                )
            )
        else:
            await callback.message.edit_text(
                text=lang_text.messages["cancelled"]
            )

    @callback_admin_check
    async def add_editor(self, callback: CallbackQuery, state: FSMContext):
        lang_text = await self.get_lang_text(callback.from_user.id)
        await callback.message.answer(text=lang_text.messages["add-editor"])
        await callback.message.delete()
        await state.set_state(AddEditorState.set_editor)

    @admin_check
    async def add_editor_forward(self, message: Message, state: FSMContext):
        lang_text = await self.get_lang_text(message.from_user.id)
        if message.forward_from:
            user = User(
                id=message.forward_from.id,
                username=message.forward_from.username,
                role_id=DEFAULT_ROLES_ID["editor"],
            )
            await state.update_data(user=user)
            await message.answer(
                text=lang_text.messages["add-editor-submit"].format(
                    username=user.username
                ),
                reply_markup=get_submit_inline(
                    callback_data=SUBMIT_ADD_EDITOR_DATA,
                    buttons=lang_text.buttons,
                ),
            )
        else:
            await message.answer(text=lang_text.messages["cancelled"])
            await state.clear()

    @callback_admin_check
    async def add_editor_submit(
        self, callback: CallbackQuery, state: FSMContext
    ):
        lang_text = await self.get_lang_text(callback.from_user.id)
        submit = callback.data.replace(SUBMIT_ADD_EDITOR_DATA, "")
        if submit == "yes":
            state_data = await state.get_data()
            user = state_data["user"]
            await self.editor_service.create_user(user)
            await callback.message.edit_text(
                text=lang_text.messages["editor-added"].format(
                    username=user.username
                )
            )
        else:
            await callback.message.edit_text(
                text=lang_text.messages["cancelled"]
            )
        await state.clear()

    async def get_lang_text(self, user_id: int):
        lang_code = await self.admin_service.get_user_lang_code(user_id)
        return get_language(lang_code)
