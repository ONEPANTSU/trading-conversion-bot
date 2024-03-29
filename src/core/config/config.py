import os

from dotenv import load_dotenv
from loguru import logger
from yaml import safe_load

from src.core.config.bot_config import BotConfig, ParseMode
from src.core.config.db_config import DataBaseConfig
from src.core.config.parsers.mexc_config import MEXCConfig
from src.core.config.parsers.parser_config import ParserConfig


class Config:
    database: DataBaseConfig
    bot: BotConfig
    parser: ParserConfig

    def __init__(self) -> None:
        self.load()

    def load(self) -> None:
        load_dotenv()
        with open("config.yml", "r") as config_file:
            configs = safe_load(config_file)
        self.set_bot(configs["bot"])
        self.set_database(configs["database"])
        self.set_logger(configs["logger"])
        self.set_parser()

    def set_bot(self, bot_config) -> None:
        self.bot = BotConfig(
            token=os.environ.get("BOT_TOKEN"),
            parse_mode=ParseMode(bot_config["parse_mode"]),
        )

    def set_database(self, db_config: dict) -> None:
        self.database = DataBaseConfig(
            driver=db_config["driver"],
            host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT"),
            name=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
        )

    @staticmethod
    def set_logger(logger_config: dict) -> None:
        logger.remove()
        logger.add(
            sink=logger_config["sink"],
            format=logger_config["format"],
            level=logger_config["level"],
            rotation=logger_config["rotation"],
            compression=logger_config["compression"],
        )

    def set_parser(self) -> None:
        self.parser = ParserConfig(
            mexc_config=MEXCConfig(
                api_key=os.environ.get("MEXC_API_KEY"),
                secret_key=os.environ.get("MEXC_SECRET_KEY"),
            )
        )
