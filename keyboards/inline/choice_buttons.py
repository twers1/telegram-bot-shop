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
admin_panel.add(KeyboardButton('Заказы'))
admin_panel.add(KeyboardButton(text="Выйти"))

button = InlineKeyboardButton('Введите номер карты: ', callback_data='bank_card_number')
keyboard = InlineKeyboardMarkup().add(button)


delivery_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
delivery_keyboard.add(KeyboardButton('СДЭК'))
delivery_keyboard.add(KeyboardButton('Почта России'))

payment_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
payment_keyboard.add(KeyboardButton('Полная оплата'))
payment_keyboard.add(KeyboardButton('Частичная оплата'))

cart_markup = ReplyKeyboardMarkup(resize_keyboard=True)
cart_markup.add(KeyboardButton(text='Очистить корзину'))
cart_markup.add(KeyboardButton('Заказать'))
cart_markup.add(KeyboardButton('Выйти'))


def generate_cart_all(good_id: int) -> InlineKeyboardMarkup:
    cart_all = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text='➕', callback_data=f'good:plus:{good_id}')
    ).add(
        InlineKeyboardButton(text='➖', callback_data=f'good:minus:{good_id}')
    )

    return cart_all


return_to_new_state = ReplyKeyboardMarkup(resize_keyboard=True)
return_to_new_state.add(KeyboardButton(text="Выйти в главное меню"))



