from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

import os

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot=bot)



catalog_list = InlineKeyboardMarkup(row_width=2)
catalog_list.add(InlineKeyboardButton(text='Какой-нибудь товар', url='https://t.me/testShopTeg_bot'),
                 InlineKeyboardButton(text='Какой-нибудь товар', url='https://t.me/testShopTeg_bot'),
                 InlineKeyboardButton(text='Какой-нибудь товар', url='https://t.me/testShopTeg_bot'))




# узнать id профиля
@dp.message_handler(commands=['id'])
async def cmd_id(message: types.Message):
    await message.answer(f'{message.from_user.id}')

@dp.message_handler(text='Контакты')
async def contacts(message: types.Message):
    await message.answer(f'Покупать товар у него: @123456')

@dp.message_handler(text='Каталог')
async def catalog(message: types.Message):
    await message.answer(f'Каталог пуст', reply_markup=catalog_list)

@dp.message_handler(text='Корзина')
async def cart(message: types.Message):
    await message.answer(f'Корзина пуста')

@dp.message_handler(text="Админ-панель")
async def contacts(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы вошли в админ-панель', reply_markup=admin_panel)
    else:
        await message.reply('Я тебя не понимаю')



if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp)

