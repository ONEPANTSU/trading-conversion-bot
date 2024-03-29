from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.routers.editor_routers.post_sending.post_sender import PostSender
from src.routers.utils.checkers.editor_checker import (
    callback_editor_check,
    editor_check,
)
from src.routers.utils.filters.buttons_filter import ButtonsFilter
from src.routers.utils.keyboards.buttons.editor_buttons import (
    get_editor_buttons,
)
from src.routers.utils.keyboards.common_keyboards import (
    get_language_inline,
    get_submit_inline,
)
from src.routers.utils.states.editor_states.send_post_state import (
    SendPostState,
)
from src.routers.utils.states.editor_states.send_private_post_state import (
    SendPrivatePostState,
)
from src.services.users.editor_service import EditorService
from src.services.users.user_service import UserService
from src.utils.language_handler import get_language


class AbstractPostSendingRouter(Router):
    def __init__(
        self,
        editor_service: EditorService,
        user_service: UserService,
        name: str,
        send_post_button: str,
        choose_lang_callback_data: str,
        submit_send_callback_data: str,
        state: type[SendPostState | SendPrivatePostState],
        post_sender: type[PostSender],
    ):

        super().__init__(name=name)

        self.editor_service = editor_service
        self.user_service = user_service

        self.choose_lang_data = choose_lang_callback_data
        self.submit_send_data = submit_send_callback_data
        self.state = state

        self.post_sender = post_sender(user_service)

        editor_buttons = get_editor_buttons()

        self.message(ButtonsFilter(editor_buttons[send_post_button]))(
            self.choose_post_language
        )
        self.callback_query(F.data.startswith(self.choose_lang_data))(
            self.send_post
        )
        self.message(self.state.send_post)(self.send_post_message)
        self.callback_query(
            F.data.startswith(self.submit_send_data),
            self.state.submit_sending,
        )(self.send_post_message_submit)

    @editor_check
    async def choose_post_language(self, message: Message, state: FSMContext):
        await state.clear()
        lang_text = await self.get_lang_text(message.from_user.id)
        await message.answer(
            text=lang_text.messages["send-mailing-language"],
            reply_markup=get_language_inline(
                self.choose_lang_data, lang_text.buttons
            ),
        )

    @callback_editor_check
    async def send_post(self, callback: CallbackQuery, state: FSMContext):
        language_code = callback.data.replace(self.choose_lang_data, "")
        await state.update_data(language_code=language_code)
        lang_text = await self.get_lang_text(callback.from_user.id)
        await callback.message.answer(
            text=lang_text.messages["send-mailing-message"],
        )
        await state.set_state(self.state.send_post)

    @editor_check
    async def send_post_message(self, message: Message, state: FSMContext):
        lang_text = await self.get_lang_text(message.from_user.id)

        if message.media_group_id:
            return await message.answer(
                text=lang_text.messages["media-group-error"]
            )

        await self.post_sender.resend_content(message, state)

        await message.answer(
            text=lang_text.messages["answer-to-send"],
            reply_markup=get_submit_inline(
                self.submit_send_data, lang_text.buttons
            ),
        )
        await state.set_state(self.state.submit_sending)

    @callback_editor_check
    async def send_post_message_submit(
        self, callback: CallbackQuery, state: FSMContext
    ):
        lang_text = await self.get_lang_text(callback.from_user.id)
        submit = callback.data.replace(self.submit_send_data, "")
        if submit == "yes":
            state_data = await state.get_data()
            await self.post_sender.send_post(callback, state_data)
            await callback.message.edit_text(
                text=lang_text.messages["mailing-was-sent"]
            )
        else:
            await callback.message.edit_text(
                text=lang_text.messages["cancelled"]
            )
        await state.clear()

    async def get_lang_text(self, user_id: int):
        lang_code = await self.editor_service.get_user_lang_code(user_id)
        return get_language(lang_code)
