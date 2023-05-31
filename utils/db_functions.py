import uuid

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


async def add_good_to_db(name, description, price, photo):
    cursor_obj.execute(f"""INSERT INTO goods VALUES ('{name}', '{description}', {price}, '{photo}') 
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
    cursor_obj.execute(f"""INSERT INTO orders (user_id, fio, phone_number, delivery_method, payment_method, order_number) VALUES ({fio}, {phone_number},
    {delivery_method}, {payment_method}, {order_number}
""")

    con.commit()


async def get_order(user_id):
    cursor_obj.execute(f"""SELECT fio, phone_number, delivery_method, payment_method, order_number FROM orders WHERE user_id={user_id}""")

    return cursor_obj.fetchone()


def generate_order_number():
    """Генерирует уникальный номер для заказа"""
    return str(uuid.uuid4())
