from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from keyboards.inline.callback_datas import buy_callback
from aiogram.utils.callback_data import CallbackData

import os

# choice = InlineKeyboardMarkup(
#     inline_keyboard=[
#     [
#         InlineKeyboardButton(text="Купить ...", callback_data=buy_callback.new(
#             item_name="pear", quantity = 1
#         )),
#         InlineKeyboardButton(text="Купить...", callback_data="buy:apple:5")
#     ],
#     [
#
#         InlineKeyboardButton(text="Отмена", callback_data="cancel")
#
#     ]
# ]
# )
#
#
# choice2 = InlineKeyboardMarkup(row_width=2)
#
# buy_pear = InlineKeyboardButton(text="Купить грушу",
#                                 callback_data=buy_callback.new(item_name="pear", quantity=1))
# choice2.insert(buy_pear)
#
# buy_apples = InlineKeyboardButton(text="Купить..", callback_data="buy:apple:5")
# choice2.insert(buy_apples )
#
# cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel")
# choice2.insert(cancel_button)
#
#
# pear_keyboard = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text="Купи тут", url="https://t.me/testShopTeg_bot")
#         ]
#     ]
# )
#
# apples_keyboard = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text="Купи тут", url="https://t.me/testShopTeg_bot")
#         ]
#     ]
# )

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add(KeyboardButton('Каталог'))
main.add(KeyboardButton('Корзина'))
main.add(KeyboardButton('Контакты'))


main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('Каталог').add('Корзина').add('Контакты').add('Админ-панель')

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add(KeyboardButton('Добавить товар'))
admin_panel.add(KeyboardButton('Удалить товар', ))
admin_panel.add(KeyboardButton('Реквизиты банковской карты'))
admin_panel.add(KeyboardButton('Размер предоплаты'))
admin_panel.add(KeyboardButton(text="Выйти"))

return_to_admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
return_to_admin_panel.add(InlineKeyboardButton(text="Вернуться в меню", callback_data="return_to_admin_panel"))

