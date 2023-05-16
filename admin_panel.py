import os
from asyncio import sleep
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db import item
from sqlalchemy.orm import state

from database import Item
from keyboards.inline.choice_buttons import admin_panel
from loader import dp
from states import NewItem

@dp.message_handler(text="Админ-панель")
async def contacts(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы вошли в админ-панель', reply_markup=admin_panel)

    else:
        await message.reply('Я тебя не понимаю')

@dp.message_handler(commands=["cancel"], state=NewItem)
async def cancel(message: types.Message, state: FSMContext):
    await message.answer("Вы отменили создание товара")
    await state.reset_state()

@dp.message_handler(text="Добавить товар")
async def add_items(message: types.Message):
    await message.answer("Введите название товара или нажмите /cancel")
    await NewItem.Name.set()

@dp.message_handler(state = NewItem.Name)
async def enter_name(message: types.Message, state: FSMContext):
    name = message.text
    item = Item()
    item.name = name
    await message.answer("Название: {name}"
                         "\nПришлите мне фотографию товара или нажмите /cancel".format(name=name))
    await NewItem.Photo.set()
    await state.update_data(item=item)

@dp.message_handler(state=NewItem.Photo, content_types=types.ContentType.PHOTO)
async def add_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    data = await state.get_data()
    item: Item = data.get("item")
    item.photo = photo
    await message.answer_photo(
        photo=photo,
        caption="Название: {name}"
            "\nПришлите мне цену товара или нажмите /cancel".format(name=item.name)
    )
    await NewItem.Price.set()
    await state.update_data(item=item)

@dp.message_handler(state=NewItem.Price)
async def enter_price(message: types.Message, state:FSMContext):
    data = await state.get_data()
    item: Item = data.get("item")
    try:
        price = int(message.text)
    except ValueError:
        await message.answer("Неверное значение, введите число")
        return

    item.price = price
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text="Да", callback_data="confirm")],
            [InlineKeyboardButton(text="Ввести заново", callback_data="change")]
        ]
    )
    await message.answer(("Цена: {price}:,\n"
                         "Подтверждаете? Нажмите /cancel , чтобы отменить"), reply_markup = markup)

    await state.update_data(item=item)
    await NewItem.Confirm.set()

@dp.callback_query_handler(text_contains="change", state=NewItem.Confirm)
async def change_price(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer("Ввелите заново цену товара")
    await NewItem.Price.set()

@dp.callback_query_handler(text_contains="confirm", state=NewItem.Confirm)
async def confirm(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    item: Item = data.get("item")
    await item.create()
    await call.message.answer("Товар удачно создан")
    await state.reset_state()




