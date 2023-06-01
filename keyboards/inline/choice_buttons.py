from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from keyboards.inline.callback_datas import buy_callback
from aiogram.utils.callback_data import CallbackData

import os


main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add(KeyboardButton('Каталог'))
main.add(KeyboardButton('Корзина'))
main.add(KeyboardButton('Контакты'))

main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add(KeyboardButton('Каталог'))
main_admin.add(KeyboardButton('Корзина'))
main_admin.add('Контакты')
main_admin.add('Админ-панель')

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add(KeyboardButton('Добавить категорию'))
admin_panel.add(KeyboardButton('Добавить товар'))
admin_panel.add(KeyboardButton('Удалить товар'))
admin_panel.add(KeyboardButton('Реквизиты банковской карты'))
admin_panel.add(KeyboardButton('Размер предоплаты'))
# admin_panel.add(KeyboardButton(text="Выйти"))

button = InlineKeyboardButton('Введите номер карты: ', callback_data='bank_card_number')
keyboard = InlineKeyboardMarkup().add(button)

# return_to_admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
# return_to_admin_panel.add(InlineKeyboardButton(text="Вернуться в меню", callback_data="return_to_admin_panel"))

delivery_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
delivery_keyboard.add(KeyboardButton('СДЭК'))
delivery_keyboard.add(KeyboardButton('Почта России'))

payment_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
payment_keyboard.add(KeyboardButton('Полная оплата'))
payment_keyboard.add(KeyboardButton('Частичная оплата'))

# add_to_cart = InlineKeyboardButton(text='Добавить в корзину', callback_data=f'add_to_cart')
# add_to_cart.add = (InlineKeyboardButton(text='Вернуться в меню', callback_data='return_to_menu'))


cart_markup = ReplyKeyboardMarkup(resize_keyboard=True)
cart_markup.add(KeyboardButton(text='Очистить корзину'))
cart_markup.add(KeyboardButton('Заказать'))

show_cart_all = ReplyKeyboardMarkup(resize_keyboard=True)
show_cart_all.add(KeyboardButton(text='Перейти в корзину'))

# exit_to_admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
# exit_to_admin_panel.add(KeyboardButton(text="Вернуться в админ-панель"))

