from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from routers.utils.keyboards.buttons.editor_buttons import get_editor_buttons
from src.routers.utils.checkers.editor_checker import editor_check
from src.routers.utils.escape_markdown import escape_markdown
from src.routers.utils.filters.buttons_filter import ButtonsFilter
from src.routers.utils.states.editor_states.media_id_state import MediaIDState
from src.services.editor_service import EditorService
from src.utils.language_handler import get_language


class GetMediaIDRouter(Router):
    def __init__(
        self,
        editor_service: EditorService,
    ):

        super().__init__(name="get-media-id-router")

        self.editor_service = editor_service

        editor_buttons = get_editor_buttons()

        self.message(ButtonsFilter(editor_buttons["get-media-id"]))(
            self.get_media_id
        )
        self.message(MediaIDState.send_media)(self.send_media)

    @editor_check
    async def get_media_id(self, message: Message, state: FSMContext):
        lang_text = get_language(message.from_user.language_code)
        await message.answer(
            text=lang_text.messages["send-media"],
        )
        await state.set_state(MediaIDState.send_media)

    @editor_check
    async def send_media(self, message: Message, state: FSMContext):
        media_id = self.__get_media_id_from_message(message)
        if media_id:
            await message.answer(
                text=escape_markdown(media_id),
            )
        else:
            lang_text = get_language(message.from_user.language_code)
            await message.answer(text=lang_text.messages["media-type-error"])
        await state.clear()

    @staticmethod
    def __get_media_id_from_message(message: Message):
        media_id = ""
        if message.video:
            media_id = message.video.file_id
        elif message.document:
            media_id = message.document.file_id
        elif message.photo:
            media_id = message.photo[-1].file_id
        elif message.sticker:
            media_id = message.sticker.file_id
        elif message.animation:
            media_id = message.animation.file_id
        return media_id
