import os

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.choice_buttons import admin_panel
from loader import dp
from states import NewItem, Get_Goods_Page
from utils.db_functions import add_good_to_db


@dp.message_handler(text="Админ-панель")
async def contacts(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы вошли в админ-панель', reply_markup=admin_panel)
        await Get_Goods_Page.first()

@dp.callback_query_handler(text="add_goods", state=Get_Goods_Page.page)
async def add_good(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("<b>Введите название товара: </b>")

    await state.reset_state()
    await NewItem.first()

@dp.message_handler(state = NewItem.name)
async def get_name(message: types.Message, state: FSMContext):
    await message.answer("<b>Введите описание товара:</b>")

    async with state.proxy() as data:
        data["name"] = message.text

    await NewItem.next()


@dp.message_handler(state=NewItem.description) # content_types=types.ContentType.PHOTO
async def get_name(message: types.Message, state: FSMContext):
    await message.answer("<b>Введите цену книги: </b>")

    async with state.proxy() as data:
        data["description"] = message.text
    await NewItem.next()


@dp.message_handler(state=NewItem.price)
async def get_name(message: types.Message, state: FSMContext):
    await message.answer("<b>Отправьте фотографию товара: </b>")
    async with state.proxy() as data:
        data["price"] = int(message.text) * 100
    await NewItem.next()


@dp.message_handler(state=NewItem.photo)
async def get_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["photo"] = message.text

    state_data = await state.get_data()
    name = state_data["name"]
    description = state_data["description"]
    price = state_data["price"]
    photo = state_data["photo"]

    await message.answer("<b>Товар успешно добавлен!</b>", reply_markup=admin_panel)

    await add_good_to_db(name, description, price, photo)
    await state.reset_state()

    await Get_Goods_Page.first()


@dp.message_handler(commands=["cancel"], state=NewItem)
async def cancel(message: types.Message, state: FSMContext):
    await message.answer("Вы отменили создание товара")
    await state.reset_state()

@dp.message_handler(text="Реквизиты банковской карты")
async def bank_card_details(message: types.Message):
    await message.answer("Пусто")


@dp.message_handler(text="Размер предоплаты")
async def prepayment_amount(message: types.Message):
    await message.answer("Пусто")


@dp.callback_query_handler(text_contains="change", state=NewItem.confirm)
async def change_price(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer("Ввелите заново цену товара")
    await NewItem.price.set()


@dp.callback_query_handler(text_contains="confirm", state=NewItem.confirm)
async def confirm(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    await call.message.answer("Товар удачно создан")
    await state.reset_state()




