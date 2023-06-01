from aiogram.dispatcher import Dispatcher
from aiogram import Bot
from os import environ
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token=environ.get('BOT_TOKEN'))
dp = Dispatcher(bot, storage=storage)
