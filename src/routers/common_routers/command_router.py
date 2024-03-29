from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.core.dto.user import User
from src.core.utils.default_roles import DEFAULT_ROLES_ID
from src.routers.utils.keyboards.admin_keyboards import get_admin_keyboard
from src.routers.utils.keyboards.editor_keyboards import get_editor_keyboard
from src.routers.utils.keyboards.user_keyboards import (
    get_user_settings_keyboard,
    get_user_start_inline,
)
from src.services.users.admin_service import AdminService
from src.services.users.editor_service import EditorService
from src.services.users.user_service import UserService
from src.utils.language_handler import get_language
from static.video import get_videos


class CommandRouter(Router):
    def __init__(
        self,
        admin_service: AdminService,
        editor_service: EditorService,
        user_service: UserService,
    ):
        super().__init__(name="start-router")
        self.admin_service = admin_service
        self.editor_service = editor_service
        self.user_service = user_service
        self.message(Command("start"))(self.start)

    async def start(self, message: Message, state: FSMContext):
        await state.clear()
        user_id = int(message.from_user.id)
        if await self.admin_service.check_is_admin(user_id):
            await self.__send_admin_start_message(message)
        elif await self.editor_service.check_is_editor(user_id):
            await self.__send_editor_start_message(message)
        else:
            await self.__create_user(message)
            await self.__send_user_start_message(message)

    async def __send_admin_start_message(self, message: Message):
        lang_code = await self.admin_service.get_user_lang_code(
            message.from_user.id
        )
        lang_text = get_language(lang_code)

        await self.admin_service.update_user(
            User(
                id=message.from_user.id,
                username=message.from_user.username,
                language_code=message.from_user.language_code,
                role_id=DEFAULT_ROLES_ID["admin"],
            )
        )
        await message.answer(
            text=lang_text.messages["admin-start"],
            reply_markup=get_admin_keyboard(buttons=lang_text.buttons),
        )

    async def __send_editor_start_message(self, message: Message):
        lang_code = await self.editor_service.get_user_lang_code(
            message.from_user.id
        )
        lang_text = get_language(lang_code)

        await self.editor_service.update_user(
            User(
                id=message.from_user.id,
                username=message.from_user.username,
                language_code=message.from_user.language_code,
                role_id=DEFAULT_ROLES_ID["editor"],
            )
        )
        await message.answer(
            text=lang_text.messages["editor-start"],
            reply_markup=get_editor_keyboard(buttons=lang_text.buttons),
        )

    async def __create_user(self, message: Message):
        await self.user_service.create_user_if_not_exist(
            User(
                id=message.from_user.id,
                username=message.from_user.username,
                language_code=message.from_user.language_code,
                role_id=DEFAULT_ROLES_ID["user"],
            )
        )

    async def __send_user_start_message(self, message: Message):
        lang_code = await self.user_service.get_user_lang_code(
            message.from_user.id
        )
        lang_text = get_language(lang_code)

        await message.answer_video(
            video=get_videos(lang_code)["start"],
            reply_markup=get_user_settings_keyboard(lang_text.buttons),
        )
        await message.answer(
            text=lang_text.messages["user-start"],
            reply_markup=get_user_start_inline(buttons=lang_text.buttons),
        )
