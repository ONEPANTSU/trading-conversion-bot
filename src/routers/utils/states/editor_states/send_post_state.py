from aiogram.fsm.state import State, StatesGroup


class SendPostState(StatesGroup):
    send_post = State()
    submit_sending = State()
