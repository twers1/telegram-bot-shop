from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, inline_keyboard
from aiogram.utils.callback_data import CallbackData
from aiogram.types import Message

from loader import bot

from loader import dp
from states import BankCardState
from utils.db_functions import get_all_goods, get_categories_from_db, get_goods_by_category_from_db, \
    get_cart_items_count

get_category_callback = CallbackData("get_category", "category_id")
remove_category_callback = CallbackData("remove_category", "category_id")
get_good_callback = CallbackData("get_good", "id")
remove_good_callback = CallbackData("remove_good", "id")


async def get_all_categories_keyboard(mode):
    all_categories_keyboards = {}
    all_buttons = []
    categories = await get_categories_from_db()

    page = 1

    if mode == "get":
        callback = get_category_callback

    elif mode == "remove":
        callback = remove_category_callback

    for category_name, category_id in categories:
        print(all_categories_keyboards)
        all_buttons.append(InlineKeyboardButton(text=f"{category_name}", callback_data=callback.new(category_id)))

    while len(all_buttons) > 0:
        keyboard = InlineKeyboardMarkup()
        counter = 1

        try:
            while counter < 5:
                keyboard.add(all_buttons[0])
                all_buttons.remove(all_buttons[0])
                counter += 1

        except:
            if page != 1:
                keyboard.add(InlineKeyboardButton(text="Назад", callback_data="previous_page"))

            else:
                keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_to_shop_menu"))

            break

        else:
            if page == 1:
                keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_to_shop_menu"))

            else:
                keyboard.add(InlineKeyboardButton(text="Назад", callback_data="previous_page"))

            if len(all_buttons) > 0:
                keyboard.insert(InlineKeyboardButton(text="Вперёд", callback_data="next_page"))

        finally:
            all_categories_keyboards[page] = keyboard
            page += 1

    return all_categories_keyboards


async def get_all_goods_keyboard(mode, category_id):
    all_goods_keyboards = {}
    all_buttons = []
    goods = await get_goods_by_category_from_db(category_id)
    callback = None
    page = 1

    if mode == "get":
        callback = get_good_callback

    elif mode == "remove":
        callback = remove_good_callback

    for name, description, id in goods:
        print(f'Товары: {all_goods_keyboards}')
        all_buttons.append(InlineKeyboardButton(text=f"{name} | {description}", callback_data=callback.new(id)))

    while len(all_buttons) > 0:
        keyboard = InlineKeyboardMarkup()
        counter = 1

        try:
            while counter < 5 and all_buttons:
                keyboard.add(all_buttons[0])
                all_buttons.remove(all_buttons[0])
                counter += 1

        except:
            if page != 1:
                keyboard.add(InlineKeyboardButton(text="Назад", callback_data="previous_page"))

            else:
                keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_to_shop_menu"))

            break

        else:
            if page == 1:
                keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_to_shop_menu"))

            else:
                keyboard.add(InlineKeyboardButton(text="Назад", callback_data="previous_page"))

            if len(all_buttons) > 0:
                keyboard.insert(InlineKeyboardButton(text="Вперёд", callback_data="next_page"))

        finally:
            all_goods_keyboards[page] = keyboard
            page += 1

    return all_goods_keyboards


async def update_good_card(message, good_name, good_description, good_price, good_image, user_id, good_id):
    # получаем информацию о количестве товаров в корзине пользователя
    cart_count = await get_cart_items_count(user_id, good_id)

    # обновляем карточку товара с новой клавиатурой и информацией
    await bot.send_message(chat_id=message.chat.id, text=f'<b>Вы добавили еще один экземпляр товара: </b>\n{good_name} | {good_description}') #\nТаких товаров в корзине: {cart_count}',


# async def add_good_to_cart(message: Message):
#     # Проверяем, есть ли аргументы в сообщении пользователя
#     if not message.get_args():
#         await message.answer("Вы не указали идентификатор товара и количество.")
#         return
#
#     # Получаем идентификатор товара и количество из сообщения пользователя
#     args = message.get_args().split()
#     good_id = int(args[0])
#     quantity = int(args[1])
#
#     # Получаем текущее содержимое корзины пользователя из контекста бота
#     cart = await dp.current_state(user=message.from_user.id).get_data()
#
#     # Проверяем, есть ли уже такой товар в корзине
#     if good_id in cart:
#         # Если товар уже есть, увеличиваем его количество на указанную величину
#         cart[good_id] += quantity
#     else:
#         # Если товара еще нет в корзине, добавляем его
#         cart[good_id] = quantity
#
#     # Обновляем данные о содержимом корзины пользователя в контексте бота
#     await dp.current_state(user=message.from_user.id).set_data(cart)
#
#     # Отправляем сообщение пользователю об успешном добавлении товара в корзину
#     await message.answer(f"Товар {good_id} добавлен в корзину в количестве {quantity} шт.")


