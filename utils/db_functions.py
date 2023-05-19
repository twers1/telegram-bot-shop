from utils.connect_db import con, cursor_obj


async def create_table():
    cursor_obj.execute("""CREATE TABLE IF NOT EXISTS goods (
    name VARCHAR(200) NOT NULL PRIMARY KEY,
    price INT NOT NULL,
    image VARCHAR(300) NOT NULL,
    id INT GENERATED ALWAYS AS IDENTITY);""")

    con.commit()


async def add_good_to_db(name, price, photo):
    cursor_obj.execute(f"""INSERT INTO goods VALUES ('{name}', {price}, '{photo}') 
    ON CONFLICT DO NOTHING;""")

    con.commit()


async def get_all_goods():
    cursor_obj.execute("""SELECT name id FROM goods;""")

    return cursor_obj.fetchall()


async def get_good_from_db(id):
    cursor_obj.execute(f"""SELECT name, price, photo FROM goods WHERE id = {id};""")

    return cursor_obj.fetchone()


async def remove_good_from_db(id):
    cursor_obj.execute(f"""DELETE FROM goods WHERE id = {id};""")

    con.commit()