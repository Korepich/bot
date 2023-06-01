from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

open_door_btn = KeyboardButton('Открыть дверь')
close_door_btn = KeyboardButton('Закрыть дверь')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)

kb_client.row(open_door_btn, close_door_btn)
