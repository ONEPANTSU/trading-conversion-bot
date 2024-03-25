from aiogram.filters import BaseFilter
from aiogram.types import Message


class ButtonsFilter(BaseFilter):
    def __init__(self, buttons: list[str]):
        self.buttons = buttons

    async def __call__(self, message: Message) -> bool:
        return message.text in self.buttons
