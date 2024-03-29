from abc import ABC, abstractmethod

from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InputMediaAnimation,
    InputMediaDocument,
    InputMediaPhoto,
    InputMediaVideo,
    Message,
)

from src.services.users.user_service import UserService


class PostSender(ABC):
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def resend_content(self, message: Message, state: FSMContext):
        if message.content_type == ContentType.VIDEO_NOTE:
            await self.__get_video_note_to_send(message, state)
        elif message.content_type == ContentType.VOICE:
            await self.__get_voice_to_send(message, state)
        else:
            await self.__get_media_to_send(message, state)

    @staticmethod
    async def __get_video_note_to_send(message: Message, state: FSMContext):
        await state.update_data(video_note=message.video_note.file_id)
        await message.answer_video_note(message.video_note.file_id)

    @staticmethod
    async def __get_voice_to_send(message: Message, state: FSMContext):
        await state.update_data(voice=message.voice.file_id)
        await message.answer_voice(message.voice.file_id)

    async def __get_media_to_send(self, message: Message, state: FSMContext):
        media, text = self.__get_media_from_message(message)
        if len(media) > 0:
            await message.answer_media_group(media=media)
        else:
            await message.answer(text=text)

        await state.update_data(text=text, media=media)

    @staticmethod
    def __get_media_from_message(message: Message):
        media = []
        text = message.md_text
        if message.photo:
            media.append(
                InputMediaPhoto(media=message.photo[-1].file_id, caption=text)
            )
        if message.video:
            media.append(
                InputMediaVideo(media=message.video.file_id, caption=text)
            )
        if message.audio:
            media.append(
                InputMediaVideo(media=message.audio.file_id, caption=text)
            )
        if message.document:
            media.append(
                InputMediaDocument(
                    media=message.document.file_id, caption=text
                )
            )
        if message.animation:
            media.append(
                InputMediaAnimation(
                    media=message.animation.file_id, caption=text
                )
            )
        return media, text

    async def send_post(self, callback: CallbackQuery, state_data: dict[str,]):
        if state_data.get("voice", None):
            await self.__send_voice(callback, state_data)

        elif state_data.get("video_note", None):
            await self.__send_video_note(callback, state_data)

        elif state_data.get("media", None):
            await self.__send_media(callback, state_data)

    async def __send_video_note(
        self, callback: CallbackQuery, state_data: dict[str,]
    ):
        language_code = state_data["language_code"]
        file_id = state_data["video_note"]
        users = await self._get_users(language_code)
        for user in users:
            await callback.bot.send_video_note(
                chat_id=user.id,
                video_note=file_id,
            )

    async def __send_voice(
        self, callback: CallbackQuery, state_data: dict[str,]
    ):
        language_code = state_data["language_code"]
        file_id = state_data["voice"]
        users = await self._get_users(language_code)
        for user in users:
            await callback.bot.send_voice(
                chat_id=user.id,
                voice=file_id,
            )

    async def __send_media(
        self, callback: CallbackQuery, state_data: dict[str,]
    ):
        media = state_data["media"]
        text = state_data["text"]
        language_code = state_data["language_code"]
        users = await self._get_users(language_code)
        for user in users:
            if len(media) > 0:
                await callback.bot.send_media_group(
                    chat_id=user.id, media=media
                )
            else:
                await callback.bot.send_message(chat_id=user.id, text=text)

    @abstractmethod
    async def _get_users(self, language_code: str):
        raise NotImplementedError
