from src.core.config.parsers.parser_config import ParserConfig
from src.services.parsers.mexc_parser import MexcParser


class ParsingService:

    def __init__(self, config: ParserConfig):
        self.mexc_parser = MexcParser(config.mexc_config)
