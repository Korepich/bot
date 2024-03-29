from aiogram import types, Dispatcher

from keyboards import auth_client
from storage import redis
from helpers.request import create_post_request

from helpers import ws_send_message


async def send_welcome(message: types.Message):
    await message.answer("Привет, авторизуйся!", reply_markup=auth_client)


async def send_door_action(message: types.Message):
    if redis.get("is_auth") != "True":
        await message.answer("Ты должен быть авторизован!")

    door_action = {"user": redis.get("user_id"), "door": 1, "is_open": True}

    match message["text"]:
        case "Открыть дверь":
            door_action.update({"is_open": True})
            ws_send_message("door_open")
            # create_post_request("action", door_action, True)

            await message.answer('Ждем подтверждения . . .')
        case "Закрыть дверь":
            door_action.update({"is_open": False})
            ws_send_message("door_close")
            # create_post_request("action", door_action, True) 

            await message.answer('Ждем подтверждения . . .')
        case _:
            print(f"no action specified! {message['text']}")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=["start"])
    dp.register_message_handler(
        send_door_action, lambda msg: msg.text == "Открыть дверь" or "Закрыть дверь"
    )
