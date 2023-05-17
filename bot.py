from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv


import os

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot=bot,storage=storage)






if __name__ == '__main__':
    from admin_panel import dp
    from handlers import dp
    executor.start_polling(dp)

