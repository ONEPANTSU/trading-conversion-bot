from enum import Enum


class ParseMode(Enum):
    MARKDOWN_V2 = "MarkdownV2"
    MARKDOWN = "Markdown"
    HTML = "HTML"


class BotConfig:
    def __init__(self, token: str, parse_mode: ParseMode):
        self.token = token
        self.parse_mode = parse_mode.value
