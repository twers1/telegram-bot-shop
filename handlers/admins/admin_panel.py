import os
import re

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.user_panel import cmd_start
from keyboards.inline.choice_buttons import admin_panel, keyboard
from loader import dp, bot
from states import NewItem, Get_Goods_Page, BankCardState, NewCategory
from utils.db_functions import add_good_to_db, remove_good_from_db, save_bank_card, get_bank_card, set_category, \
    generate_categories_keyboard, get_all_orders
from utils.inline_keyboards import get_all_goods_keyboard


@dp.message_handler(text="Админ-панель", state=Get_Goods_Page.page)
async def contacts(message: types.Message, state: FSMContext):
    print("Бот запущен(админ-панель)")
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        bot_message = await bot.send_message(message.from_user.id, f'Вы вошли в админ-панель', reply_markup=admin_panel)
        async with state.proxy() as data:
            data["key"] = bot_message.message_id

        await Get_Goods_Page.page.set()


@dp.message_handler(text="Добавить категорию", state=Get_Goods_Page.page)
async def add_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await bot.delete_message(message_id=data["key"], chat_id=message.from_user.id)
        await bot.send_message(message.from_user.id, "<b>Введите название категории: </b>")

    await state.reset_state()
    await NewCategory.first()


@dp.message_handler(state=NewCategory.name)
async def get_category_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text

    state_data = await state.get_data()
    name = state_data["name"]

    await message.answer("<b>Категория успешно добавлена!</b>", reply_markup=admin_panel)

    await set_category(name)
    await state.reset_state()

    await Get_Goods_Page.first()


@dp.message_handler(text="Добавить товар", state=Get_Goods_Page.page)
async def add_good(message: types.Message, state: FSMContext):
    print('Нажата кнопка "Добавить товар". Категории')
    category_keyboard = await generate_categories_keyboard()

    await bot.send_message(message.from_user.id, "<b>Выберите категорию:</b>", reply_markup=category_keyboard)

    await NewItem.category.set()


@dp.callback_query_handler(state=NewItem.category)
async def get_category(callback: types.CallbackQuery, state: FSMContext):
    print('Категория выбрана')
    await callback.message.answer("<b>Введите название товара:</b>")

    async with state.proxy() as data:
        print(callback.data)
        data["category_id"] = callback.data.split(':')[1]

    await NewItem.name.set()


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
        data["price"] = int(message.text)
    await NewItem.next()


@dp.message_handler(state=NewItem.photo)
async def get_photo(message: types.Message, state: FSMContext):
    await message.answer("<b>Введите количество товара в наличии: </b>")
    async with state.proxy() as data:
        data["photo"] = message.text
    await NewItem.next()


@dp.message_handler(state=NewItem.availability)
async def get_availability(message:types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["availability"] = int(message.text)

    state_data = await state.get_data()
    category_id = int(state_data["category_id"])
    name = state_data["name"]
    description = state_data["description"]
    price = state_data["price"]
    photo = state_data["photo"]
    availability = state_data["availability"]

    await message.answer("<b>Товар успешно добавлен!</b>", reply_markup=admin_panel)

    await add_good_to_db(name, description, price, photo, category_id, availability)

    await state.reset_state()
    await Get_Goods_Page.first()


@dp.message_handler(text="Удалить товар")
async def send_remove_goods(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        # print(type(data["key"]))
        await bot.delete_message(message_id=data["key"], chat_id=message.from_user.id)
        await bot.send_message(message.from_user.id, "<b>Нажмите на товар чтобы удалить его:</b>", reply_markup=None)
        await bot.edit_reply_markup(reply_markup=await get_all_goods_keyboard("remove"))


@dp.message_handler(text="Удалить товар", state=Get_Goods_Page.page)
async def send_remove_goods(message: types.Message, state: FSMContext):
    keyboards = await get_all_goods_keyboard("remove")

    async with state.proxy() as data:
        await bot.delete_message(message_id=data["key"], chat_id=message.from_user.id)
        await bot.send_message(message.from_user.id, text="<b>Нажмите на товар чтобы удалить его:</b>", reply_markup=None)
        await bot.send_message(chat_id=message.from_user.id,reply_markup=keyboards[1], text="Все доступные товары: ")
        data["keyboards"] = keyboards
        data["page"] = 1
    await Get_Goods_Page.first()


@dp.callback_query_handler(text_contains="remove_good", state=Get_Goods_Page.page)
async def remove_good(callback: types.CallbackQuery, state: FSMContext):
    callback_data = callback.data.strip().split(":")[1:]
    good_id = callback_data[0]

    await callback.message.edit_text("<b>Товар был успешно удалён!</b>")
    await remove_good_from_db(good_id)

    await state.reset_state()
    await Get_Goods_Page.first()
    await Get_Goods_Page.page.set()


@dp.message_handler(text='Реквизиты банковской карты', state=Get_Goods_Page.page)
async def bank_card_details(message: types.Message, state:FSMContext):
    # Отправляем сообщение с запросом номера банковской карты и кнопкой
    await message.answer('Вы нажали на кнопку "Реквизиты банковской карты".\nНажмите на кнопку, чтобы ввести номер банковской карты.', reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data == 'bank_card_number', state=Get_Goods_Page.page)
async def process_bank_card_button(callback_query: types.CallbackQuery, state:FSMContext):
    # Отправляем запрос на ввод номера банковской карты
    await bot.send_message(callback_query.from_user.id, 'Введите номер банковской карты:')


@dp.message_handler(regexp=r'^\d{4}\s\d{4}\s\d{4}\s\d{4}$', state=Get_Goods_Page.page)
async def process_bank_card_number(message: types.Message, state:FSMContext):
    # Проверяем, что пользователь ввел 16 цифр, разделенных пробелами
    card_number = message.text

    # Удаляем пробелы из номера карты
    card_number = card_number.replace(' ','')

    await save_bank_card(user_id=message.from_user.id, card_number=card_number)

    # Отправляем сообщение с подтверждением ввода номера банковской карты
    await bot.send_message(message.chat.id, f'Вы успешно ввели номер банковской карты: {card_number}', reply_markup=admin_panel)


@dp.message_handler(text="Размер предоплаты", state=Get_Goods_Page.page)
async def prepayment_amount(message: types.Message, state:FSMContext):
    user_id = message.from_user.id
    # Получаем номер карты из базы данных
    card_number = await get_bank_card(user_id)
    if card_number:
        await message.answer(f"Номер вашей банковской карты: <b>{card_number[0]}</b>", reply_markup=admin_panel)
    else:
        await message.answer("Номер вашей банковской карты не найден.", reply_markup=admin_panel)


@dp.message_handler(text="Заказы", state=Get_Goods_Page.page)
async def get_user_order(message: types.Message, state: FSMContext):
    orders = await get_all_orders()

    orders_text = "Список заказов:\n\n"
    for order in orders:
        orders_text += f"ФИО: {order[0]}\nНомер телефона: {order[1]}\nСпособ доставки: {order[2]}\nСпособ оплаты: {order[3]}\nНомер заказа: {order[4]}\n\n"
    await message.answer(orders_text)


@dp.message_handler(text="Выйти", state=Get_Goods_Page.page)
async def return_to_lobby(message: types.Message, state: FSMContext):
    await cmd_start(message)



