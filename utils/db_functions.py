import uuid

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.connect_db import con, cursor_obj


async def create_table():
    cursor_obj.execute("""CREATE TABLE IF NOT EXISTS goods (
    name VARCHAR(200) NOT NULL PRIMARY KEY,
    description VARCHAR(200) NOT NULL,
    price INT NOT NULL,
    photo VARCHAR(300) NOT NULL,
    id INT GENERATED ALWAYS AS IDENTITY);""")

    con.commit()


async def create_table():
    cursor_obj.execute("""CREATE TABLE IF NOT EXISTS carts (
           user_id INT NOT NULL,
           good_id INT NOT NULL,
           id INT GENERATED ALWAYS AS IDENTITY);""")

    con.commit()


async def create_table():
    cursor_obj.execute("""CREATE TABLE IF NOT EXISTS bank_card (
           user_id INT NOT NULL,
           card_number VARCHAR(16) NOT NULL,
           id INT GENERATED ALWAYS AS IDENTITY);""")

    con.commit()


async def create_table():
    cursor_obj.execute("""CREATE TABLE IF NOT EXISTS orders (
           user_id INT NOT NULL,
           fio VARCHAR(200) NOT NULL,
           phone_number INT NOT NULL,
           delivery_method TEXT NOT NULL,
           payment_method TEXT NOT NULL, 
           order_number INT NOT NULL,
           id INT GENERATED ALWAYS AS IDENTITY);""")

    con.commit()


async def create_table():
    cursor_obj.execute("""CREATE TABLE IF NOT EXISTS categories (
           category_name VARCHAR(200) NOT NULL,
           category_id INT GENERATED ALWAYS AS IDENTITY);""")

    con.commit()


async def add_good_to_db(name, description, price, photo, category_id):
    cursor_obj.execute(f"""INSERT INTO goods VALUES ('{name}', '{description}', {price}, '{photo}', {category_id}) 
    ON CONFLICT DO NOTHING;""")

    con.commit()


async def get_all_goods():
    cursor_obj.execute("""SELECT name, description, id FROM goods;""")

    return cursor_obj.fetchall()


async def get_good_from_db(id):
    cursor_obj.execute(f"""SELECT name, description, price, photo FROM goods WHERE id = {id};""")

    return cursor_obj.fetchone()


async def remove_good_from_db(id):
    cursor_obj.execute(f"""DELETE FROM goods WHERE id = {id};""")

    con.commit()


async def add_good_to_cart(user_id, good_id):
    cursor_obj.execute(f"""INSERT INTO carts (user_id, good_id) VALUES ({user_id}, {good_id});""")

    con.commit()


async def get_cart(user_id):
    cursor_obj.execute(f"""SELECT name, description, price, photo 
    FROM goods
    JOIN carts ON goods.id = carts.good_id WHERE carts.user_id = {user_id};""")

    return cursor_obj.fetchall()


async def delete_cart(user_id):
    cursor_obj.execute(f"""DELETE FROM carts WHERE user_id = {user_id} """)

    con.commit()


async def save_bank_card(user_id, card_number):
    cursor_obj.execute(f"""INSERT INTO bank_card (user_id, card_number) VALUES ({user_id}, {card_number})""")

    con.commit()


async def get_bank_card(user_id):
    cursor_obj.execute(f"""SELECT card_number FROM bank_card WHERE user_id={user_id}""")

    return cursor_obj.fetchone()


async def save_order(user_id, fio, phone_number, delivery_method, payment_method, order_number):
    cursor_obj.execute(f"""INSERT INTO orders (user_id, fio, phone_number, delivery_method, payment_method, order_number) VALUES ('{fio}', {phone_number},
    '{delivery_method}', '{payment_method}', {order_number}
""")

    con.commit()


async def get_order(user_id):
    cursor_obj.execute(f"""SELECT fio, phone_number, delivery_method, payment_method, order_number FROM orders WHERE user_id={user_id}""")

    return cursor_obj.fetchone()


async def set_category(category_name):
    cursor_obj.execute(f"""INSERT INTO categories VALUES ('{category_name}') 
        ON CONFLICT DO NOTHING;""")

    con.commit()


async def get_categories_from_db():
    cursor_obj.execute("""SELECT category_name, category_id FROM categories;""")

    return cursor_obj.fetchall()


async def generate_categories_keyboard():
    categories = await get_categories_from_db()  # получаем список категорий из базы данных
    categories_keyboard = InlineKeyboardMarkup()

    for category in categories:
        category_name = category[0]  # получаем имя категории из кортежа
        categories_keyboard.add(InlineKeyboardButton(category_name, callback_data=f"category:{category_name}"))

    return categories_keyboard


async def update_good_card(message, good_name, good_description, good_price, good_image, user_id):
    # получаем информацию о количестве товаров в корзине пользователя
    cart_count = await get_cart_count(user_id)

    # обновляем карточку товара с новой клавиатурой и информацией
    await bot.edit_message_media(media=types.InputMediaPhoto(good_image, caption=f"{good_name}\n{good_description}\n{good_price} руб."), chat_id=message.chat.id, message_id=message.message_id, reply_markup=inline_keyboard)


def generate_order_number():
    """Генерирует уникальный номер для заказа"""
    return str(uuid.uuid4())
