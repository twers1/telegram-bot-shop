import psycopg2
import os
import src.config

from aiogram import Bot,Dispatcher, types

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from src import config

bot = Bot(config.TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
