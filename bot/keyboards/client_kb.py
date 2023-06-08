from aiogram.types import ReplyKeyboardMarkup

from .common_btns import open_door_btn, close_door_btn

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.row(open_door_btn, close_door_btn)
