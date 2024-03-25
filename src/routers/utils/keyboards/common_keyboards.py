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
