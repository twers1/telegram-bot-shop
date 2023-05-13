import logging

from aiogram.types import Message, CallbackQuery
from aiogram import types

from aiogram.dispatcher.filters import Command

from keyboards.inline.callback_datas import buy_callback
from keyboards.inline.choice_buttons import choice, pear_keyboard, apples_keyboard, main, main_admin
from loader import dp
import os

@dp.message_handler(Command("items"))
async def show_items(message: Message):
    await message.answer(text="На продажу у нас есть: ..\n"
                         "Если вам ничего не нужно - ждите отмену",
                         reply_markup=choice)

@dp.callback_query_handler(text_contains="pear")
async def buying_pear(call: CallbackQuery):
    await call.answer(cache_time=60)
    callback_data = call.data
    logging.info(f"call = {callback_data}")

    await call.message.answer("Вы выбрали купить грушу. Груша всего одна. Спаасибо",
                              reply_markup=pear_keyboard)

@dp.callback_query_handler(buy_callback.filter(item_name="apple"))
async def buying_apples(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)
    logging.info(f"call = {callback_data}")
    quantity = callback_data.get("quantity")
    await call.message.answer(f"Вы выбрали купить яблоки. Яблок всего {quantity}. Спасибо!",
                              reply_markup=apples_keyboard)

@dp.callback_query_handler(text="cancel")
async def cancel_buying(call: CallbackQuery):
    await call.answer("Вы отменили эту покупку",
                      show_alert=True)
    await call.message.edit_reply_markup()

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(f'Добро пожаловать в магазин!', reply_markup=main)

    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы авторизовались как администратор', reply_markup=main_admin)

@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Я тебя не понимаю')
