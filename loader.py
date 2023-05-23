import psycopg2

from aiogram import Bot,Dispatcher, types
import os

from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config

bot = Bot(config.TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
