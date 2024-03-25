from aiogram.fsm.state import State, StatesGroup


class SendPrivatePostState(StatesGroup):
    send_post = State()
    submit_sending = State()
