from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher

from keyboards import kb_client, auth_client, kb_admin
from storage import redis
from authentication import authentication


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
    redis.set("tg_user_id", message["from"]["id"])

    async with state.proxy() as data:
        data["password"] = message.text

    async with state.proxy() as data:
        is_auth = authentication(data)

        if is_auth == True:
            keyboard = kb_admin if int(redis.get("user_id")) == 1 else kb_client

            await message.answer("Авторизация прошла успешно", reply_markup=keyboard)

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
