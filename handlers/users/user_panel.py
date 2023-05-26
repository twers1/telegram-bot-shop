from aiogram.dispatcher import FSMContext
from aiogram.types import (LabeledPrice, ContentType)
from aiogram import types

from config import PAYMENTS_TOKEN
from loader import dp, bot
from keyboards.inline.choice_buttons import main, main_admin, add_to_cart
from loader import dp
import os

from states import Get_Goods_Page
from utils.db_functions import get_good_from_db
from utils.inline_keyboards import get_all_goods_keyboard


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(f'Добро пожаловать в магазин!', reply_markup=main)

    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы авторизовались как администратор', reply_markup=main_admin)

    await Get_Goods_Page.first()


@dp.message_handler(text='Каталог', state=Get_Goods_Page.page)
async def send_catalog_start(message: types.Message, state: FSMContext):
    keyboards = await get_all_goods_keyboard("get")

    await bot.send_message(text="<b>Каталог товаров: </b>", chat_id=message.from_user.id)
    await bot.send_message(text="Доступные товары представлены тут", reply_markup=keyboards[1], chat_id=message.from_user.id)

    async with state.proxy() as data:
        data["keyboards"] = keyboards
        data["page"] = 1


@dp.callback_query_handler(text="next_page", state=Get_Goods_Page.page)
async def send_next_page(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["page"] += 1

    state_data = await state.get_data()
    keyboards = state_data["keyboards"]
    page = state_data["page"]

    await bot.message.edit_text(text="<b>Каталог товаров:</b>")
    await bot.message.edit_reply_markup(reply_markup=keyboards[page])


@dp.callback_query_handler(text="previous_page", state=Get_Goods_Page.page)
async def send_previous_page(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["page"] -= 1

    state_data = await state.get_data()
    keyboards = state_data["keyboards"]
    page = state_data["page"]

    await bot.message.edit_text("<b>Каталог товаров:</b>")
    await bot.message.edit_reply_markup(reply_markup=keyboards[page])


@dp.callback_query_handler(text_contains="get_good", state=Get_Goods_Page.page)
async def send_good(callback: types.CallbackQuery, state: FSMContext):
    callback_data = callback.data.strip().split(":")[1:]
    good_id = int(callback_data[0])
    good_information = await get_good_from_db(good_id)
    good_name, good_description, good_price, good_image = good_information
    price = [LabeledPrice(label=f"{good_name} | {good_description}", amount=good_price)]

    await bot.send_photo(callback.message.chat.id, photo=good_image,caption=f"Имя товара - {good_name}\n"
                                                          f"Описание - {good_description}\n"
                                                          f"Цена - {good_price}", reply_markup=add_to_cart)

    # await callback.message.delete()
    await state.reset_state()


@dp.message_handler(text="Добавить в корзину")
async def add_cart(message: types.Message):
    await message.answer("Здрасте")


@dp.callback_query_handler(text="Вернуться в каталог", state=Get_Goods_Page.page)
async def back_to_shop_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.reset_state()

    await main(callback.message)


@dp.message_handler(text='Корзина')
async def cart(message: types.Message):
    await message.answer(f'Корзина пуста')


@dp.message_handler(text='Контакты')
async def contacts(message: types.Message):
    await message.answer(f'Покупать товар у него: @123456')


@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Я тебя не понимаю')



