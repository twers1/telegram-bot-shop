import os

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline.choice_buttons import admin_panel, return_to_admin_panel
from loader import dp, bot
from states import NewItem, Get_Goods_Page
from utils.db_functions import add_good_to_db, remove_good_from_db
from utils.inline_keyboards import get_all_goods_keyboard


@dp.message_handler(text="Админ-панель")
async def contacts(message: types.Message, state: FSMContext):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):

        bot_message = await bot.send_message(message.from_user.id, f'Вы вошли в админ-панель', reply_markup=admin_panel)
        async with state.proxy() as data:
            data["key"] = bot_message.message_id

        await Get_Goods_Page.page.set()


@dp.message_handler(text="Добавить товар", state=Get_Goods_Page.page)
async def add_good(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        print(type(data["key"]))
        await bot.delete_message(message_id=data["key"], chat_id=message.from_user.id)
        await bot.send_message(message.from_user.id, "<b>Введите название товара: </b>", reply_markup=None)

    await state.reset_state()
    await NewItem.first()


@dp.message_handler(state=NewItem.name)
async def get_name(message: types.Message, state: FSMContext):
    await message.answer("<b>Введите описание товара:</b>")

    async with state.proxy() as data:
        data["name"] = message.text

    await NewItem.next()


@dp.message_handler(state=NewItem.description)
async def get_name(message: types.Message, state: FSMContext):
    await message.answer("<b>Введите цену товара: </b>")

    async with state.proxy() as data:
        data["description"] = message.text

    await NewItem.next()


@dp.message_handler(state=NewItem.price)
async def get_name(message: types.Message, state: FSMContext):
    await message.answer("<b>Отправьте фотографию товара(ссылку): </b>")
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


@dp.message_handler(text="Удалить товар")
async def send_remove_goods(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        print(type(data["key"]))
        await bot.delete_message(message_id=data["key"], chat_id=message.from_user.id)
        await bot.send_message(message.from_user.id, "<b>Нажмите на товар чтобы удалить его:</b>", reply_markup=None)
        await bot.edit_reply_markup(reply_markup=await get_all_goods_keyboard("remove"))




@dp.message_handler(text="Удалить товар", state=Get_Goods_Page.page)
async def send_remove_goods(message: types.Message, state: FSMContext):
    keyboards = await get_all_goods_keyboard("remove")

    await bot.message.edit_text("<b>Нажмите на товар чтобы удалить его:</b>")
    await bot.message.edit_reply_markup(reply_markup=keyboards[1])

    async with state.proxy() as data:
        data["keyboards"] = keyboards
        data["page"] = 1


@dp.message_handler(text_contains="remove_good", state=Get_Goods_Page.page)
async def remove_good(message: types.Message, state: FSMContext):
    callback_data = bot.data.strip().split(":")[1:]
    good_id = callback_data[0]

    await bot.message.edit_text("<b>Товар был успешно удалён!</b>")
    await bot.message.edit_reply_markup(reply_markup=return_to_admin_panel)
    await remove_good_from_db(good_id)

    await state.reset_state()


# @dp.message_handler(commands=["cancel"], state=NewItem)
# async def cancel(message: types.Message, state: FSMContext):
#     await message.answer("Вы отменили создание товара")
#     await state.reset_state()

@dp.message_handler(text="Реквизиты банковской карты")
async def bank_card_details(message: types.Message):
    await message.answer("Пусто")


@dp.message_handler(text="Размер предоплаты")
async def prepayment_amount(message: types.Message):
    await message.answer("Пусто")


@dp.callback_query_handler(text="return_to_admin_panel")
async def return_to_admin_menu(callback: types.CallbackQuery):
    await callback.message.delete()
    await contacts(callback.message)


@dp.callback_query_handler(text="exit_from_admin_panel", state=Get_Goods_Page.page)
async def exit_from_admin_panel(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()

    await state.reset_state()
