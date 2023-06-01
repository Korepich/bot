from aiogram.utils import executor

from create_bot import dp
from handlers import client, auth

async def on_startup(_):
    print('Bot has been starting . . .')

auth.register_handlers_auth(dp)
client.register_handlers_client(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
