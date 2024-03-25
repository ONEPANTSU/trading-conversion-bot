from dataclasses import dataclass

from static.text.en import EN_BUTTONS, EN_COMMANDS, EN_MESSAGES
from static.text.ru import RU_BUTTONS, RU_COMMANDS, RU_MESSAGES


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
