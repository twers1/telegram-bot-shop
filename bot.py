
from aiogram import Bot, executor

from dotenv import load_dotenv

import os

from utils.connect_db import con
from utils.db_functions import create_table
from loader import dp

load_dotenv()
bot = Bot(os.getenv('TOKEN'))


async def on_startup(dispatcher):
    await create_table()


async def on_shutdown(dispatcher):
    con.close()

if __name__ == '__main__':
    from handlers.admins import admin_panel
    from handlers.users import user_panel
    print("                                                      ████ \n ░░███                                               ░░███ \n ███████   █████ ███ █████  ██████  ████████   █████  ░███ \n░░░███░   ░░███ ░███░░███  ███░░███░░███░░███ ███░░   ░███ \n  ░███     ░███ ░███ ░███ ░███████  ░███ ░░░ ░░█████  ░███ \n  ░███ ███ ░░███████████  ░███░░░   ░███      ░░░░███ ░███ \n  ░░█████   ░░████░████   ░░██████  ░███████  ██████  █████\n   ░░░░░     ░░░░ ░░░░     ░░░░░░  ░░░░░     ░░░░░░  ░░░░░ \n                                                           \n                                                           \n                                                           \nBot started successfully")
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
    print("Bot stopped")
