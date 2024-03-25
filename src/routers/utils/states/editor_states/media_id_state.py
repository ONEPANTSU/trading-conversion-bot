from aiogram.fsm.state import State, StatesGroup


class MediaIDState(StatesGroup):
    send_media = State()
