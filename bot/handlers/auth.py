from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from helpers.request import create_post_request
import json
from os import environ

from keyboards import kb_client, auth_client
from storage import redis
from helpers import base64_decode


class FSMAuth(StatesGroup):
    login = State()
    password = State()


async def start(message: types.Message):
    await FSMAuth.login.set()
    await message.answer("Введите логин")


async def set_login(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["login"] = message.text
    await FSMAuth.next()
    await message.answer("Введите пароль")


async def set_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["password"] = message.text

    async with state.proxy() as data:
        response = create_post_request(
            "token", {"username": data["login"], "password": data["password"]}
        )

        if response.status_code == 200:
            base64_token = response.json()["access"].split(".")
            user_id = json.loads(base64_decode(base64_token[1]))["user_id"]
            redis.set("user_id", user_id)

            redis.set(
                "jwt_token",
                environ.get("JWT_SECRET_WORD") + " " + response.json()["access"],
            )

            await message.answer("Авторизация прошла успешно", reply_markup=kb_client)
            redis.set("is_auth", "True")
        else:
            await message.answer("Ошибка при авторизации!", reply_markup=auth_client)
            redis.set("is_auth", "False")

    await state.finish()


def register_handlers_auth(dp: Dispatcher):
    dp.register_message_handler(
        start, lambda msg: msg.text == "Авторизоваться", state=None
    )
    dp.register_message_handler(set_login, state=FSMAuth.login)
    dp.register_message_handler(set_password, state=FSMAuth.password)
