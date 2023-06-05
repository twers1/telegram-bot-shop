from aiogram.dispatcher import FSMContext
from aiogram.types import (LabeledPrice, InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram import types

from loader import  bot
from keyboards.inline.choice_buttons import main, main_admin, cart_markup, delivery_keyboard, \
    payment_keyboard, generate_cart_all
from loader import dp
import os

from states import Get_Goods_Page, YourForm
from utils.db_functions import get_good_from_db, delete_cart, save_order, generate_order_number, \
    get_category_id_by_name, get_cart_items_count, get_cart_items, update_good_quantity
from utils.inline_keyboards import get_all_goods_keyboard, get_all_categories_keyboard, update_good_card, \
    subtract_good_from_cart
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
async def send_cart_good(callback: types.CallbackQuery, state: FSMContext):
    category_id = callback.data.split(":")[1]  # Извлекаем значение category_id из коллбэк-данных
    keyboards_goods = await get_all_goods_keyboard("get", category_id=category_id)
    print('Получаем ключ от товаров')
    print(keyboards_goods.keys())

    await bot.send_message(text="<b>Товары в категории </b>", chat_id=callback.message.chat.id)
    if len(keyboards_goods) > 0:
        await bot.send_message(text="Выберите товар", reply_markup=keyboards_goods[list(keyboards_goods.keys())[0]],
                               chat_id=callback.message.chat.id)

        async with state.proxy() as data:
            data["keyboards"] = keyboards_goods
            data["page"] = 1
    else:
        await bot.send_message(text="В данной категории нет товаров.", chat_id=callback.message.chat.id)
        await state.reset_state()


@dp.callback_query_handler(text_contains="get_good", state=Get_Goods_Page.page)
async def send_good(callback: types.CallbackQuery, state: FSMContext):
    callback_data = callback.data.strip().split(":")[1:]
    good_id = int(callback_data[0])
    good_information = await get_good_from_db(good_id)

    if good_information is None:
        await callback.answer(text="Извините, запрашиваемый товар в данный момент недоступен.",) # chat_id=callback.message.from_user.id
        return

    good_name, good_description, good_price, good_image, good_quantity = good_information
    price = [LabeledPrice(label=f"{good_name} | {good_description}", amount=good_price)]

    add_to_cart = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text='Добавить в корзину', callback_data=f'add_to_cart:{good_id}'))
    add_to_cart.add(InlineKeyboardButton(text='Вернуться в меню', callback_data='return_to_menu'))

    await bot.send_photo(callback.message.chat.id, photo=good_image,caption=f"Имя товара - {good_name}\n"
                                                          f"Описание - {good_description}\n"
                                                          f"Цена - {good_price}", reply_markup=add_to_cart)

    await callback.message.delete()
    await state.reset_state()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('add_to_cart'))
async def process_add_to_cart(callback_query: types.CallbackQuery, state: FSMContext):
    good_id = int(callback_query.data.split(':')[1])
    user_id = callback_query.from_user.id

    # Получаем информацию о товаре из базы данных
    good_information = await get_good_from_db(good_id)

    if good_information is None:
        await callback_query.answer(text="Извините, запрашиваемый товар в данный момент недоступен.")
        return

    good_name, good_description, good_price, good_image, good_quantity = good_information

    # Добавляем товар в корзину с помощью функции add_good_to_cart
    await add_good_to_cart(user_id, good_id, good_name, good_description, good_price, good_quantity)

    await bot.send_message(
        callback_query.from_user.id,
        text=f'🎉Товар {good_name} добавлен в корзину.\nВы тут можете добавить еще один экземпляр товара или же убрать его',
        reply_markup=generate_cart_all(good_id)
    )
    print(good_name, good_description)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith(f'good:plus:'), state="*")
async def add_item_to_cart(callback_query: types.CallbackQuery, state: FSMContext):
    print('Я в плюсике')
    print(await state.get_state())
    good_id = int(callback_query.data.split(":")[2])
    print(callback_query.data)
    good_information = await get_good_from_db(good_id)
    good_name, good_description, good_price, good_image, good_quantity = good_information

    # Добавляем товар в корзину
    await add_good_to_cart(callback_query.from_user.id, good_id, good_name, good_description, good_price, good_quantity)

    # Получаем количество товаров в корзине и обновляем карточку товара
    cart_items_count = await get_cart_items_count(callback_query.from_user.id, good_id)
    await update_good_card(callback_query.message, good_name, good_description, good_price, good_image,
                           cart_items_count, good_id)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith(f'good:minus:'), state="*")
async def remove_item_from_cart(callback_query: types.CallbackQuery):
    # Получаем информацию о товаре из базы данных
    good_id = int(callback_query.data.split(":")[2])
    good_information = await get_good_from_db(good_id)
    good_name, good_description, good_price, good_image, good_quantity = good_information

    # Вычитаем 1 единицу товара из корзины
    await subtract_good_from_cart(
        message=callback_query.message,
        user_id=callback_query.from_user.id,
        good_id=good_id,
        good_name=good_name,
        good_description=good_description
    )

    return
    # Получаем количество выбранного товара в корзине и обновляем карточку товара
    cart_items_count = await get_cart_items_count(good_id, callback_query.from_user.id)
    await update_good_card(
        message=callback_query.message,
        good_name=good_name,
        good_description=good_description,
        good_price=good_price,
        good_image=good_image,
        user_id=callback_query.from_user.id,
        good_id=good_id,
    )

                         
    # # Если количество выбранного товара в корзине равно 0, то удаляем товар из корзины полностью
    # if cart_items_count == 0:
    #     await remove_good_from_cart(callback_query.from_user.id, good_id)


# @dp.callback_query_handler(lambda c: c.data and c.data.startswith(f'good:return_to_menu'), state="*")
# async def return_to_catalog(callback: types.CallbackQuery, state: FSMContext):
#     await send_cart_good(callback, state)


@dp.message_handler(text="Выйти в главное меню")
async def return_to_menu_new_state(message: types.Message):
    await cmd_start(message)


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


@dp.message_handler(text="Очистить корзину", state=Get_Goods_Page.page)
async def process_clear_cart(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await delete_cart(user_id)
    await bot.send_message(message.chat.id, text='Корзина пуста!')
    await return_to_main_menu(message, state)


@dp.message_handler(text='Заказать', state=Get_Goods_Page.page)
async def order_start(message: types.Message, state: FSMContext):
    await message.answer('Введите свое ФИО:')
    await YourForm.name.set()


@dp.message_handler(text='Выйти', state=Get_Goods_Page.page)
async def quit_carts(message: types.Message, state: FSMContext):
    await cmd_start(message)


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
    fio = state_data['fio']
    phone_number = state_data['phone_number']
    delivery_method = state_data['delivery_method']
    payment_method = state_data['payment_method']
    user_id = message.from_user.id

    # Get cart items
    cart_items = await get_cart_items(user_id)
    goods_amount = {}
    goods_quantity = {}
    for good in cart_items:
        good_id = good[0]
        goods_quantity[good_id] = good[4]
        if good_id not in goods_amount.keys():
            goods_amount[good_id] = 0
        goods_amount[good_id] += 1

    for good_id, quantity in goods_quantity.items():
        amount = goods_amount[good_id]
        new_quantity = quantity - amount
        await update_good_quantity(good_id, new_quantity)

    await save_order(message.from_user.id, fio, phone_number, delivery_method, payment_method, order_number, goods_quantity)
    await delete_cart(user_id)
    await message.answer("<b>Заказ успешно создан!</b>")
    await state.finish()
    await return_to_main_menu(message, state)


@dp.message_handler(text='Контакты', state=Get_Goods_Page.page)
async def contacts(message: types.Message, state: FSMContext):
    await message.answer('Контакт для связи [Алексей](https://t.me/pal1maaaa)', parse_mode='Markdown')


@dp.message_handler(text='Выйти в главное меню', state=Get_Goods_Page.page)
async def return_to_main_menu(message: types.Message, state: FSMContext):
    await cmd_start(message)


@dp.message_handler()
async def answer(message: types.Message):
    await message.reply('Я тебя не понимаю')



