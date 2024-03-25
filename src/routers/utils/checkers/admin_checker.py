import functools

from aiogram.types import CallbackQuery, Message

from utils.language_handler import get_language


def admin_check(func):
    @functools.wraps(func)
    async def wrapper(router, message: Message, *args, **kwargs):
        if await router.admin_service.check_is_admin(
            int(message.from_user.id)
        ):
            return await func(router, message, *args, **kwargs)
        else:
            await __send_access_denied_message(message)

    return wrapper


def callback_admin_check(func):
    @functools.wraps(func)
    async def wrapper(router, callback: CallbackQuery, *args, **kwargs):
        message = callback.message
        if await router.admin_service.check_is_admin(
            int(callback.from_user.id)
        ):
            return await func(router, callback, *args, **kwargs)
        else:
            await __send_access_denied_message(message)

    return wrapper


async def __send_access_denied_message(message: Message):
    lang_text = get_language(message.from_user.language_code)
    await message.answer(text=lang_text.messages["access-denied"])
