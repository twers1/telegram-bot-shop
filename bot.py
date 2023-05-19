from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv


import os

from utils.connect_db import con
from utils.db_functions import create_table

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot=bot,storage=storage)

async def on_startup(dispatcher):
    await create_table()

async def on_shutdown(dispatcher):
    con.close()

if __name__ == '__main__':
    from handlers.admins.admin_panel import dp
    from handlers.users.purches import dp
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)

