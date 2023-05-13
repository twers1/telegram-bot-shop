from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

from keyboards.inline.callback_datas import buy_callback

import os

choice = InlineKeyboardMarkup(
    inline_keyboard=[
    [
        InlineKeyboardButton(text="Купить ...", callback_data=buy_callback.new(
            item_name="pear", quantity = 1
        )),
        InlineKeyboardButton(text="Купить...", callback_data="buy:apple:5")
    ],
    [

        InlineKeyboardButton(text="Отмена", callback_data="cancel")

    ]
]
)


choice2 = InlineKeyboardMarkup(row_width=2)

buy_pear = InlineKeyboardButton(text="Купить грушу",
                                callback_data=buy_callback.new(item_name="pear", quantity=1))
choice2.insert(buy_pear)

buy_apples = InlineKeyboardButton(text="Купить..", callback_data="buy:apple:5")
choice2.insert(buy_apples )

cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel")
choice2.insert(cancel_button)


pear_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Купи тут", url="https://t.me/testShopTeg_bot")
        ]
    ]
)

apples_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Купи тут", url="https://t.me/testShopTeg_bot")
        ]
    ]
)

main = ReplyKeyboardMarkup(resize_keyboard=True)
main.add('Каталог').add('Корзина').add('Контакты')

main_admin = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin.add('Каталог').add('Корзина').add('Контакты').add('Админ-панель')

admin_panel = ReplyKeyboardMarkup(resize_keyboard=True)
admin_panel.add('Добавить товар').add('Удалить товар').add('Сделать рассылку')