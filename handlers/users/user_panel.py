from aiogram.dispatcher import FSMContext
from aiogram.types import (LabeledPrice, InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram import types

from loader import  bot
from keyboards.inline.choice_buttons import main, main_admin, show_cart_all, cart_markup, delivery_keyboard, \
    payment_keyboard
from loader import dp
import os

from states import Get_Goods_Page, YourForm
from utils.db_functions import get_good_from_db, delete_cart, save_order, generate_order_number, get_category_id_by_name
from utils.inline_keyboards import get_all_goods_keyboard, get_all_categories_keyboard
from utils.db_functions import get_cart, add_good_to_cart

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(f'Добро пожаловать в магазин!', reply_markup=main)

    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы авторизовались как администратор', reply_markup=main_admin)

    await Get_Goods_Page.first()

# @dp.message_handler()
# async def ggggg(message: types.Message):
#     print(message.text)
#
# @dp.message_handler(state='*')
# async def ggggg_state(message: types.Message, state: FSMContext):
#     print(message.text, await state.get_state())


@dp.message_handler(text='Каталог', state=Get_Goods_Page.page)
async def send_catalog_start(message: types.Message, state: FSMContext):
    keyboards_category = await get_all_categories_keyboard("get")
    print(keyboards_category.keys())

    await bot.send_message(text="<b>🎉 Добро пожаловать в каталог товаров!</b>", chat_id=message.from_user.id)
    await bot.send_message(text="Категории товаров", reply_markup=keyboards_category[1], chat_id=message.from_user.id)

    async with state.proxy() as data:
        data["keyboards"] = keyboards_category
        data["page"] = 1


@dp.message_handler(text="next_page", state=Get_Goods_Page.page)
async def send_next_page(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["page"] += 1

    state_data = await state.get_data()
    keyboards = state_data["keyboards"]
    page = state_data["page"]

    await message.edit_text(text="<b>Каталог товаров:</b>")
    await message.edit_reply_markup(reply_markup=keyboards[page])


@dp.callback_query_handler(text="previous_page", state=Get_Goods_Page.page)
async def send_previous_page(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["page"] -= 1

    state_data = await state.get_data()
    keyboards = state_data["keyboards"]
    page = state_data["page"]

    await bot.message.edit_text("<b>Каталог товаров:</b>")
    await bot.message.edit_reply_markup(reply_markup=keyboards[page])


@dp.callback_query_handler(text_contains="get_category", state=Get_Goods_Page.page)
async def send_cart_good(message: types.Message, state: FSMContext):
    category_name = message.data.split(":")[1]
    category_id = get_category_id_by_name(category_name)
    keyboards_goods = await get_all_goods_keyboard("get", category_id)
    print('Получаем ключ от товаров')
    print(keyboards_goods.keys())

    await bot.send_message(text="<b>Товары в категории </b>", chat_id=message.from_user.id)
    await bot.send_message(text="Выберите товар", reply_markup=keyboards_goods[1], chat_id=message.from_user.id)

    async with state.proxy() as data:
        data["keyboards"] = keyboards_goods
        data["page"] = 1


@dp.callback_query_handler(text_contains="get_good", state=Get_Goods_Page.page)
async def send_good(callback: types.CallbackQuery, state: FSMContext):
    callback_data = callback.data.strip().split(":")[1:]
    good_id = int(callback_data[0])
    good_information = await get_good_from_db(good_id)

    if good_information is None:
        await callback.answer(text="Извините, запрашиваемый товар в данный момент недоступен.",
                               ) # chat_id=callback.message.from_user.id
        return

    good_name, good_description, good_price, good_image = good_information
    price = [LabeledPrice(label=f"{good_name} | {good_description}", amount=good_price)]

    add_to_cart = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text='Добавить в корзину', callback_data=f'add_to_cart:{good_id}'))
    add_to_cart.add(InlineKeyboardButton(text='Вернуться в меню', callback_data='return_to_menu'))

    await bot.send_photo(callback.message.chat.id, photo=good_image,caption=f"Имя товара - {good_name}\n"
                                                          f"Описание - {good_description}\n"
                                                          f"Цена - {good_price}", reply_markup=add_to_cart)

    await callback.message.delete()
    await state.reset_state()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('add_to_cart'), state="*")
async def process_add_to_cart(callback_query: types.CallbackQuery, state: FSMContext):
    good_id = int(callback_query.data.split(':')[1])
    user_id = callback_query.from_user.id

    await add_good_to_cart(user_id, good_id)

    await bot.send_message(callback_query.from_user.id, text='Товар добавлен в корзину.', reply_markup=show_cart_all)


@dp.callback_query_handler(lambda callback_query: 'add_one_more' in callback_query.data)
async def add_one_more_to_cart(callback_query: types.CallbackQuery):
    # Получаем информацию о товаре из базы данных
    good_id = int(callback_query.data.split(":")[1])
    good_information = await get_good_from_db(good_id)
    good_name, good_description, good_price, good_image = good_information

    # Добавляем товар в корзину
    await add_good_to_cart(callback_query.from_user.id, good_id)

    # Отправляем сообщение об успешном добавлении и обновляем карточку товара с новым количеством товаров в корзине
    await bot.answer_callback_query(callback_query.id, text=f"Товар '{good_name}' успешно добавлен в корзину!")
    await update_good_card(callback_query.message, good_name, good_description, good_price, good_image, callback_query.from_user.id)

@dp.callback_query_handler(lambda callback_query: 'remove_from_cart' in callback_query.data)
async def remove_from_cart(callback_query: types.CallbackQuery):
    # Получаем информацию о товаре из базы данных
    good_id = int(callback_query.data.split(":")[1])
    good_information = await get_good_from_db(good_id)
    good_name, good_description, good_price, good_image = good_information

    # Удаляем товар из корзины
    await remove_good_from_cart(callback_query.from_user.id, good_id)

    # Отправляем сообщение об успешном удалении и обновляем карточку товара с новым количеством товаров в корзине
    await bot.answer_callback_query(callback_query.id, text=f"Товар '{good_name}' успешно удален из корзины!")
    await update_good_card(callback_query.message, good_name, good_description, good_price, good_image, callback_query.from_user.id)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('return_to_menu'))
async def return_to_catalog(message: types.Message, state: FSMContext):
    await send_catalog_start(message, state)


@dp.message_handler(text="Перейти в корзину")
async def go_to_cart(message: types.Message, state: FSMContext):
    await show_cart(message, state)


@dp.message_handler(text='Корзина', state=Get_Goods_Page.page)
async def show_cart(message: types.Message, state: FSMContext):
    # Этот метод вызывается, когда пользователь нажимает на кнопку 'Корзина'.
    # message = callback_query.message
    print('Я в корзине')
    user_id = message.from_user.id
    cart = await get_cart(user_id)

    if not cart:
        await message.answer("Корзина пуста!")
    else:
        total_price = 0
        cart_text = "<b>Товары в корзине:</b>\n\n"
        for good_information in cart:
            good_name, good_description, good_price, good_image = good_information
            cart_text += f"{good_name} | {good_description}\nЦена - {good_price}\n\n"
            total_price += good_price

        # Выводим итоговую сумму в конце списка товаров
        cart_text += f"<b>Итого: {total_price}</b>"

        # Отправляем все товары и итоговую сумму в одном сообщении
        await bot.send_message(message.chat.id, text=cart_text, reply_markup=cart_markup, parse_mode="HTML")


@dp.message_handler(text="Очистить корзину")
async def process_clear_cart(message: types.Message):
    user_id = message.from_user.id
    await delete_cart(user_id)
    await bot.send_message(message.chat.id, text='Корзина пуста!', reply_markup=main)


@dp.message_handler(text='Заказать', state=Get_Goods_Page.page)
async def order_start(message: types.Message, state: FSMContext):
    await message.answer('Введите свое ФИО:')
    await YourForm.name.set()


@dp.message_handler(state=YourForm.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fio'] = message.text
    await message.answer('Введите номер телефона:')
    await YourForm.next()


@dp.message_handler(state=YourForm.phone)
async def process_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text
    await message.answer('Выберите метод доставки:', reply_markup=delivery_keyboard)
    await YourForm.next()


@dp.message_handler(state=YourForm.delivery)
async def process_delivery(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['delivery_method'] = message.text
    await message.answer('Выберите метод оплаты:', reply_markup=payment_keyboard)
    await YourForm.next()


@dp.message_handler(state=YourForm.payment)
async def process_payment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['payment_method'] = message.text

    state_data = await state.get_data()
    order_number = generate_order_number()
    await save_order(message.from_user.id, state_data['fio'], state_data['phone_number'], state_data['delivery_method'], state_data['payment_method'], order_number)
    await state.finish()


@dp.message_handler(text='Контакты', state=Get_Goods_Page.page)
async def contacts(message: types.Message, state: FSMContext):
    await message.answer('Контакт для связи [Алексей](https://t.me/pal1maaaa)', parse_mode='Markdown')


@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Я тебя не понимаю')



