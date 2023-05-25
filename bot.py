
from aiogram import Bot, Dispatcher, executor

from dotenv import load_dotenv

import os

from utils import notify_admins, set_bot_commands
from utils.connect_db import con
from utils.db_functions import create_table
from loader import dp

load_dotenv()
bot = Bot(os.getenv('TOKEN'))


async def on_startup(dispatcher):
    # await notify_admins.on_startup_notify(dispatcher)
    # await set_bot_commands.set_default_commands(dispatcher)
    await create_table()


async def on_shutdown(dispatcher):
    con.close()

if __name__ == '__main__':
    from handlers.admins import admin_panel
    from handlers.users import user_panel
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)

