from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.core.config.config import Config
from src.core.database import DataBase
from src.middleware.scheduler_middleware import SchedulerMiddleware
from src.repositories.repository_registry import RepositoryRegistry
from src.routers.router_registry import RouterRegistry
from src.services.service_registry import ServiceRegistry
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
    register_middlewares(dp)
    include_routers(dp, config)
    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands(bot)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


def register_middlewares(dp: Dispatcher):
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.start()
    dp.update.middleware.register(SchedulerMiddleware(scheduler))


def include_routers(dp: Dispatcher, config: Config):
    database = DataBase(config.database)
    repositories = RepositoryRegistry(database)
    services = ServiceRegistry(repositories, config.parser)
    routers = RouterRegistry(services)

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
