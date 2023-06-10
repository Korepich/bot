from aiogram.utils import executor
import asyncio
from threading import Thread

from create_bot import dp, bot
from handlers import client, auth, admin
from helpers import ws_connect
from storage import redis


async def on_startup(_):
    me = await bot.get_me()
    event_loop = asyncio.get_event_loop()
    redis.set("bot_id", me["id"])

    ws_thread = Thread(target=ws_connect, args=([event_loop]), daemon=True)
    ws_thread.start()

    print("Bot has been started . . .")


auth.register_handlers_auth(dp)
admin.register_handlers_admin(dp)
client.register_handlers_client(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
