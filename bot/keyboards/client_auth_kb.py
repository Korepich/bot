from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

auth_btn = KeyboardButton('Авторизоваться')

auth_client = ReplyKeyboardMarkup(resize_keyboard=True)

auth_client.row(auth_btn)
