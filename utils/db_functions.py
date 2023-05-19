from utils.db_suff.connect_db import connect, cursor


async def create_table():
    cursor.execute("""CREATE TABLE IF NOT EXISTS goods (
    name VARCHAR(200) NOT NULL PRIMARY KEY,
    price INT NOT NULL,
    image VARCHAR(300) NOT NULL,
    id INT GENERATED ALWAYS AS IDENTITY);""")

    connect.commit()


async def add_good_to_db(name, author, price, image):
    cursor.execute(f"""INSERT INTO goods VALUES ('{name}', '{author}', {price}, '{image}') 
    ON CONFLICT DO NOTHING;""")

    connect.commit()


async def get_all_goods():
    cursor.execute("""SELECT name, author, id FROM goods;""")

    return cursor.fetchall()


async def get_good_from_db(id):
    cursor.execute(f"""SELECT name, author, price, image FROM goods WHERE id = {id};""")

    return cursor.fetchone()


async def remove_good_from_db(id):
    cursor.execute(f"""DELETE FROM goods WHERE id = {id};""")

    connect.commit()