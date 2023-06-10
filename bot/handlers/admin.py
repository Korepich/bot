from aiogram import types, Dispatcher
from aiogram.types.callback_query import CallbackQuery

from storage import redis
from keyboards import get_inline_admin_kb
from helpers import read_history


async def see_history(message: types.Message):
    history = read_history()

    await message.answer(history, reply_markup=get_inline_admin_kb())


async def history_step(cb: CallbackQuery):
    current_page = int(redis.get("history_pages_current"))
    current_page += 1 if cb.data.find("next") != -1 else -1

    redis.set("history_pages_current", current_page)

    history = read_history()

    await cb.message.edit_text(text=history, reply_markup=get_inline_admin_kb())


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(
        see_history, lambda msg: msg.text == "Посмотреть историю"
    )
    dp.register_callback_query_handler(
        history_step, lambda cb: cb.data.startswith("history")
    )
