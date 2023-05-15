import os
from asyncio import sleep
from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.choice_buttons import admin_panel
from loader import dp
from states import NewItem

@dp.message_handler(text="Админ-панель")
async def contacts(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы вошли в админ-панель', reply_markup=admin_panel)

    else:
        await message.reply('Я тебя не понимаю')

@dp.message_handler(text="Добавить товар")
async def add_items(message: types.Message):
    await message.answer("Введите название товара или нажмите /cancel")
    await NewItem.Name.set()

@dp.message_handler(state = NewItem.Name)
async def enter_name(message: types.Message, state: FSMContext):
    name = message.text
    item.name = name
