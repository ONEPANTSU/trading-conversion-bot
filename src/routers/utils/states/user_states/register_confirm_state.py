from aiogram.fsm.state import State, StatesGroup


class RegisterConfirmState(StatesGroup):
    send_uuid = State()
