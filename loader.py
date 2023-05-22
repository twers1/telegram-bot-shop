from aiogram import Bot,Dispatcher, types
import os

from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(os.getenv('TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
