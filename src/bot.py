from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from src.core.config.config import Config
from src.core.database import DataBase
from src.repositories.repositories import Repositories
from src.routers.routers import Routers
from src.services.services import Services
from src.utils.language_handler import LANGUAGES, get_language


async def start_bot():
    config = Config()
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(
            parse_mode=config.bot.parse_mode,
            link_preview_is_disabled=True,
        ),
    )
    dp = Dispatcher(storage=MemoryStorage())

    include_routers(dp, config)
    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands(bot)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


def include_routers(dp: Dispatcher, config: Config):
    database = DataBase(config.database)
    repositories = Repositories(database)
    services = Services(repositories)
    routers = Routers(services)

    for router in routers.get_list():
        dp.include_router(router)


async def set_commands(bot: Bot):
    for lang_code in LANGUAGES:
        commands = [
            BotCommand(command=command, description=description)
            for command, description in get_language(
                lang_code
            ).commands.items()
        ]
        await bot.set_my_commands(commands=commands, language_code=lang_code)
