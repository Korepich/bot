from aiogram.utils import executor

from create_bot import dp
from handlers import client, auth, admin


async def on_startup(_):
    print("Bot has been starting . . .")


auth.register_handlers_auth(dp)
admin.register_handlers_admin(dp)
client.register_handlers_client(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
