from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, inline_keyboard
from utils.connect_db import con, cursor_obj

import time
import random


# Table products
async def create_table():
    cursor_obj.execute("""CREATE TABLE IF NOT EXISTS goods (
    name VARCHAR(200) NOT NULL PRIMARY KEY,
    description VARCHAR(200) NOT NULL,
    price INT NOT NULL,
    photo VARCHAR(300) NOT NULL,
    category_id INT, 
    availability INT,
    id INT GENERATED ALWAYS AS IDENTITY);""")

    con.commit()


# Table carts
async def create_table():
    cursor_obj.execute("""CREATE TABLE IF NOT EXISTS carts (
            user_id INT NOT NULL,
            good_id INT NOT NULL,
            id INT GENERATED ALWAYS AS IDENTITY);""")

    con.commit()


# Table bank_card
async def create_table():
    cursor_obj.execute("""CREATE TABLE IF NOT EXISTS bank_card (
           user_id INT NOT NULL,
           card_number VARCHAR(16) NOT NULL,
           id INT GENERATED ALWAYS AS IDENTITY);""")

    con.commit()


# Table orders
async def create_table():
    cursor_obj.execute("""CREATE TABLE IF NOT EXISTS orders (
           user_id INT NOT NULL,
           fio VARCHAR(200) NOT NULL,
           phone_number bigint NOT NULL,
           delivery_method TEXT NOT NULL,
           payment_method TEXT NOT NULL, 
           order_number INT NOT NULL,
           id INT GENERATED ALWAYS AS IDENTITY);""")

    con.commit()


# Table categories
async def create_table():
    cursor_obj.execute("""CREATE TABLE IF NOT EXISTS categories (
           category_name VARCHAR(200) NOT NULL,
           category_id INT GENERATED ALWAYS AS IDENTITY);""")

    con.commit()


# Function add category to db
async def add_category_to_db(category_name):
    # Добавляем категорию в таблицу categories
    cursor_obj.execute("INSERT INTO categories (category_name) \
                        VALUES (%s)", (category_name,))
    con.commit()


# Function
async def update_goods_category_id():
    # Обновляем столбец category_id в таблице goods на основе столбца category_name в таблице categories
    cursor_obj.execute("UPDATE goods SET category_id = categories.category_id FROM categories WHERE categories.category_name = goods.category_name")
    con.commit()


async def add_good_to_db(name, description, price, photo, category_id, availability):
    # Получаем id категории по ее названию
    cursor_obj.execute(f"""SELECT category_id FROM categories WHERE category_id='{category_id}'""")

    # Добавляем товар в таблицу goods, указывая id категории
    cursor_obj.execute("INSERT INTO goods (name, description, price, photo, category_id, availability) \
                        VALUES (%s, %s, %s, %s, %s, %s)",
                       (name, description, price, photo, category_id, availability))

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


async def save_order(user_id, fio, phone_number, delivery_method, payment_method, order_number, goods_to_order):
    cursor_obj.execute("ALTER TABLE orders ALTER COLUMN phone_number TYPE bigint;")
    cursor_obj.execute("INSERT INTO orders (user_id, fio, phone_number, delivery_method, payment_method, order_number) \
                            VALUES (%s, %s, %s, %s, %s, %s)",
                       (user_id, fio, phone_number, delivery_method, payment_method, order_number))

    for good_id, quantity in goods_to_order.items():
        # получаем информацию о товаре из базы данных
        cursor_obj.execute(f"SELECT availability FROM goods WHERE id='{good_id}'")
        result = cursor_obj.fetchone()

        if result and result[0] >= quantity:
            # уменьшаем количество товаров на заданную величину и обновляем запись в базе данных
            cursor_obj.execute(f"UPDATE goods SET availability=availability-{quantity} WHERE id={good_id}")
        else:
            # если количество товара меньше, чем запрашивается, генерируем ошибку
            raise ValueError(f"Недостаточно товара '{good_id}' на складе")

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
        category_id = category[1]
        categories_keyboard.add(InlineKeyboardButton(category_name, callback_data=f"category_id:{category_id}"))
        print(category_id, category_name)

    return categories_keyboard


async def get_category_id_by_name(category_name):
    cursor_obj.execute("SELECT category_id FROM categories WHERE category_name = %s;", (category_name,))

    return cursor_obj.fetchall()


async def get_goods_by_category_from_db(category_id):
    cursor_obj.execute("SELECT name, description, id FROM goods WHERE category_id = %s", (category_id,))
    return cursor_obj.fetchall()


async def get_cart_items_count(user_id):
    cursor_obj.execute("SELECT COUNT(*) FROM carts WHERE good_id = %s;", (user_id,))
    return cursor_obj.fetchone()


async def get_cart_items(user_id):
    cursor_obj.execute("""
        SELECT good_id
        FROM carts
        INNER JOIN goods ON carts.good_id = goods.id
        WHERE carts.user_id = %s;
    """, (user_id,))

    return cursor_obj.fetchall()


def generate_order_number():
    """Генерирует уникальный номер для заказа"""
    random_num = random.randint(0, 999)  # Generate a random number between 0 and 999
    order_number = int(f"{random_num:03d}")  # Combine timestamp and random number
    return order_number