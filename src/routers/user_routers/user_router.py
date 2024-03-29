from datetime import datetime, timedelta

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.routers.utils.callbacks.user_callback_data import USER_START_DATA
from src.routers.utils.states.user_states.register_confirm_state import (
    RegisterConfirmState,
)
from src.services.parsers.parsing_service import ParsingService
from src.services.users.user_service import UserService
from src.utils.language_handler import get_language


class UserRouter(Router):
    def __init__(
        self, user_service: UserService, parsing_service: ParsingService
    ):
        super().__init__(name="user-router")
        self.user_service = user_service
        self.parsing_service = parsing_service

        self.callback_query(F.data == USER_START_DATA)(self.user_start)
        self.message(RegisterConfirmState.send_uuid)(self.check_registration)

    async def user_start(
        self,
        callback: CallbackQuery,
        scheduler: AsyncIOScheduler,
        state: FSMContext,
    ):
        lang_text = get_language(callback.from_user.language_code)
        await callback.message.answer(lang_text.messages["mexc-register"])
        jobs = []
        for minutes in [10, 30, 60, 120, 1440, 2880]:
            jobs.append(
                self.__start_interval_reminder(
                    message=callback.message,
                    scheduler=scheduler,
                    minutes=minutes,
                    message_to_send=lang_text.messages["remind"],
                )
            )
        await state.update_data(reminding_jobs=jobs)
        await state.set_state(RegisterConfirmState.send_uuid)

    def __start_interval_reminder(
        self,
        message: Message,
        scheduler: AsyncIOScheduler,
        minutes: int,
        message_to_send: str,
    ) -> str:
        job = scheduler.add_job(
            self.remind,
            trigger="interval",
            minutes=minutes,
            end_date=datetime.now() + timedelta(minutes=minutes + 1),
            kwargs={"message": message, "message_to_send": message_to_send},
        )
        return job.id

    @staticmethod
    async def remind(message: Message, message_to_send: str):
        await message.answer(message_to_send)

    async def check_registration(
        self, message: Message, scheduler: AsyncIOScheduler, state: FSMContext
    ):
        uuid = message.text
        if self.parsing_service.mexc_parser.check_registration(uuid):
            data = await state.get_data()
            await self.__registration_success(message)
            [scheduler.remove_job(job_id) for job_id in data["reminding_jobs"]]
            await state.clear()
        else:
            await self.__registration_failed(message)
            await state.set_state(RegisterConfirmState.send_uuid)

    async def __registration_success(self, message: Message):
        user = await self.user_service.get_user(message.from_user.id)
        user.privacy = True
        await self.user_service.update_user(user)

        lang_text = get_language(message.from_user.language_code)
        await message.answer(lang_text.messages["mexc-success"])

    @staticmethod
    async def __registration_failed(message: Message):
        lang_text = get_language(message.from_user.language_code)
        await message.answer(lang_text.messages["mexc-error"])
