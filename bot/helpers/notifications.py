import websocket
from os import environ
import asyncio
import json

from storage import redis
from create_bot import dp, bot

event_loop = {}


def on_message(ws, msg):
    message = json.loads(msg)
    if message["message"] != True:
        return

    global event_loop
    user_id = int(redis.get("tg_user_id"))

    bot_message = "Внимание! Кто-то пытается проникнуть"

    async def send_message(id, message):
        await bot.send_message(id, message)

    coro = send_message(user_id, bot_message)
    asyncio.run_coroutine_threadsafe(coro, event_loop)


def ws_connect(main_thread_event_loop):
    global event_loop
    event_loop = main_thread_event_loop

    ws = websocket.WebSocketApp(
        f"ws://{environ.get('LOCAL_IP')}:8000/api/v1/notifications/breaking/",
        on_message=on_message,
    )

    ws.run_forever()
