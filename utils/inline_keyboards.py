from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from utils.db_functions import get_all_goods

get_good_callback = CallbackData("get_good", "id")
remove_good_callback = CallbackData("remove_good", "id")

async def get_all_goods_keyboard(mode):
    all_goods_keyboards = {}
    all_buttons = []
    goods = await get_all_goods()
    callback = None
    page = 1

    if mode == "get":
        callback = get_good_callback

    elif mode == "remove":
        callback = remove_good_callback

    for name, author, id in goods:
        all_buttons.append(InlineKeyboardButton(text=f"{name} | {author}", callback_data=callback.new(id)))

    while len(all_buttons) > 1:
        keyboard = InlineKeyboardMarkup()
        counter = 1

        try:
            while counter < 5:
                keyboard.add(all_buttons[0])
                all_buttons.remove(all_buttons[0])
                counter += 1

        except:
            if page != 1:
                keyboard.add(InlineKeyboardButton(text="Назад", callback_data="previous_page"))

            else:
                keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_to_shop_menu"))

            break

        else:
            if page == 1:
                keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_to_shop_menu"))

            else:
                keyboard.add(InlineKeyboardButton(text="Назад", callback_data="previous_page"))

            if len(all_buttons) > 0:
                keyboard.insert(InlineKeyboardButton(text="Вперёд", callback_data="next_page"))

        finally:
            all_goods_keyboards[page] = keyboard
            page += 1

    return all_goods_keyboards