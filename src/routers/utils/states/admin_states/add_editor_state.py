from aiogram.fsm.state import State, StatesGroup


class AddEditorState(StatesGroup):
    set_editor = State()
