from aiogram.dispatcher import FSMContext
from aiogram.types import (LabeledPrice, ContentType)
from aiogram import types


import bot
from keyboards.inline.choice_buttons import main, main_admin
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


@dp.message_handler(text='Каталог', state=Get_Goods_Page.page)
async def catalog(callback: types.CallbackQuery, state: FSMContext):
    keyboards = await get_all_goods_keyboard("get")

    await callback.message.edit_text("<b>Каталог товаров: </b>")
    await callback.message.edit_reply_markup(reply_markup=keyboards[1])

    async with state.proxy() as data:
        data["keyboards"] = keyboards
        data["page"] = 1


@dp.callback_query_handler(text="next_page", state=Get_Goods_Page.page)
async def send_next_page(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["page"] += 1

    state_data = await state.get_data()
    keyboards = state_data["keyboards"]
    page = state_data["page"]

    await callback.message.edit_text("<b>Каталог товаров:</b>")
    await callback.message.edit_reply_markup(reply_markup=keyboards[page])


@dp.callback_query_handler(text="previous_page", state=Get_Goods_Page.page)
async def send_previous_page(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["page"] -= 1

    state_data = await state.get_data()
    keyboards = state_data["keyboards"]
    page = state_data["page"]

    await callback.message.edit_text("<b>Каталог товаров:</b>")
    await callback.message.edit_reply_markup(reply_markup=keyboards[page])


@dp.callback_query_handler(text_contains="get_good", state=Get_Goods_Page.page)
async def send_good(callback: types.CallbackQuery, state: FSMContext):
    callback_data = callback.data.strip().split(":")[1:]
    good_id = int(callback_data[0])
    good_information = await get_good_from_db(good_id)
    good_name, good_description, good_price, good_image = good_information
    price = [LabeledPrice(label=f"{good_name} | {good_description}", amount=good_price)]

    await bot.send_invoice(callback.message.chat.id,
                           title=f"Книга \"{good_name}\"",
                           description=f"Описание - {good_description}",
                           currency="rub",
                           photo_url=good_image,
                           photo_width=220,
                           photo_height=344,
                           photo_size=344,
                           is_flexible=True,
                           prices=price,
                           start_parameter="buy_book",
                           payload="book",
                           need_phone_number=True)

    await callback.message.delete()
    await state.reset_state()




@dp.pre_checkout_query_handler(lambda query: True)
async def checkout_process(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    await message.answer("<b>Вы успешно оплатили покупку! В скором времени вы "
                         "получите свой заказ.</b>")


@dp.callback_query_handler(text="back_to_shop_menu", state=Get_Goods_Page.page)
async def back_to_shop_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.reset_state()

    await main(callback.message)


@dp.callback_query_handler(text="exit_from_shop", state=Get_Goods_Page.page)
async def exit_from_shop(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.reset_state()


@dp.message_handler(text='Контакты')
async def contacts(message: types.Message):
    await message.answer(f'Покупать товар у него: @123456')


@dp.message_handler(text='Корзина')
async def cart(message: types.Message):
    await message.answer(f'Корзина пуста')


@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Я тебя не понимаю')



