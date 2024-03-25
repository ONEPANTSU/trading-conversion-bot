from dataclasses import dataclass

from static.text.en import EN_BUTTONS, EN_MESSAGES, EN_COMMANDS
from static.text.ru import RU_BUTTONS, RU_MESSAGES, RU_COMMANDS


@dataclass
class Text:
    buttons: dict[str, str]
    messages: dict[str, str]
    commands: dict[str, str]


LANGUAGES = {
    "ru": Text(buttons=RU_BUTTONS, messages=RU_MESSAGES, commands=RU_COMMANDS),
    "en": Text(buttons=EN_BUTTONS, messages=EN_MESSAGES, commands=EN_COMMANDS),
}


def get_language(code: str):
    return LANGUAGES.get(code, LANGUAGES["en"])
