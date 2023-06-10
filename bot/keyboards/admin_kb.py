from aiogram.types import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
)

from .common_btns import open_door_btn, close_door_btn
from storage import redis

# Bottom keyboard
show_actions_btn = KeyboardButton("Посмотреть историю")

kb_admin = (
    ReplyKeyboardMarkup(resize_keyboard=True)
    .row(open_door_btn, close_door_btn)
    .add(show_actions_btn)
)


# Inline keyboard
def get_inline_admin_kb():
    pages_quantity = int(redis.get("history_pages_quantity") or '1')

    current_page = int(redis.get("history_pages_current") or '1')

    prev_btn = InlineKeyboardButton("←", callback_data="history_prev")
    pages_counter = InlineKeyboardButton(
        f"{current_page}/{pages_quantity}", callback_data="None"
    )
    next_btn = InlineKeyboardButton("→", callback_data="history_next")

    if current_page == 1:
        return InlineKeyboardMarkup().row(pages_counter, next_btn)
    
    if current_page == pages_quantity:
        return InlineKeyboardMarkup().row(prev_btn, pages_counter)

    return InlineKeyboardMarkup().row(prev_btn, pages_counter, next_btn)
