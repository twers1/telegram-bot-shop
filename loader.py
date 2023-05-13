from aiogram import Bot,Dispatcher, types
import os

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot)