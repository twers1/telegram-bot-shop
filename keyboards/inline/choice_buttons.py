from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from keyboards.inline.callback_datas import buy_callback
from aiogram.utils.callback_data import CallbackData

import os



main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add(KeyboardButton('Каталог'))
main.add(KeyboardButton('Корзина'))
main.add(KeyboardButton('Контакты'))

main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('Каталог').add('Корзина').add('Контакты').add('Админ-панель')

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add(KeyboardButton('Добавить товар'))
admin_panel.add(KeyboardButton('Удалить товар'))
admin_panel.add(KeyboardButton('Реквизиты банковской карты'))
admin_panel.add(KeyboardButton('Размер предоплаты'))
admin_panel.add(KeyboardButton(text="Выйти"))

button = InlineKeyboardButton('Введите номер карты: ', callback_data='bank_card_number')
keyboard = InlineKeyboardMarkup().add(button)

return_to_admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
return_to_admin_panel.add(InlineKeyboardButton(text="Вернуться в меню", callback_data="return_to_admin_panel"))

product_design = ReplyKeyboardMarkup(resize_keyboard=True)
product_design.add(KeyboardButton('СДЭК'))
product_design.add(KeyboardButton('Почта России'))

type_of_payment = ReplyKeyboardMarkup(resize_keyboard=True)
type_of_payment.add(KeyboardButton('Полная оплата'))
type_of_payment.add(KeyboardButton('Частичная оплата'))

add_to_cart = ReplyKeyboardMarkup(resize_keyboard=True)
add_to_cart.add(InlineKeyboardButton(text='Добавить в корзину', callback_data='add_to_cart'))
add_to_cart.add(KeyboardButton('Вернуться в меню'))

cart_markup = ReplyKeyboardMarkup(resize_keyboard=True)
cart_markup.add(KeyboardButton(text='Очистить корзину', callback_data='clear_cart'))
cart_markup.add(KeyboardButton('Заказать'))

show_cart_all = ReplyKeyboardMarkup(resize_keyboard=True)
show_cart_all.add(KeyboardButton('Перейти в корзину'))

