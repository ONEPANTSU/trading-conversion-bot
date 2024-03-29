from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_submit_inline(
    callback_data: str, buttons: dict[str, str]
) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=buttons["yes"], callback_data=f"{callback_data}yes"
            ),
            InlineKeyboardButton(
                text=buttons["no"], callback_data=f"{callback_data}no"
            ),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_language_inline(
    callback_data, buttons: dict[str, str]
) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=buttons["ru"], callback_data=f"{callback_data}ru"
            ),
            InlineKeyboardButton(
                text=buttons["en"], callback_data=f"{callback_data}en"
            ),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
