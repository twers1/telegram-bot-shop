# from aiogram.dispatcher import FSMContext
# from aiogram.types import (LabeledPrice, InlineKeyboardMarkup, InlineKeyboardButton)
# from aiogram import types
#
# from handlers.users.user_panel import show_cart, cmd_start
# from loader import  bot
# from keyboards.inline.choice_buttons import main, main_admin, show_cart_all, cart_markup
# from loader import dp
# import os
#
# from states import Get_Goods_Page
# from utils.db_functions import get_good_from_db, delete_cart
# from utils.inline_keyboards import get_all_goods_keyboard
# from utils.db_functions import get_cart, add_good_to_cart
#
#
# @dp.message_handler(text="next_page", state=Get_Goods_Page.page)
# async def send_next_page(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data["page"] += 1
#
#     state_data = await state.get_data()
#     keyboards = state_data["keyboards"]
#     page = state_data["page"]
#
#     await message.edit_text(text="<b>Каталог товаров:</b>")
#     await message.edit_reply_markup(reply_markup=keyboards[page])
#
#
# @dp.callback_query_handler(text="previous_page", state=Get_Goods_Page.page)
# async def send_previous_page(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data["page"] -= 1
#
#     state_data = await state.get_data()
#     keyboards = state_data["keyboards"]
#     page = state_data["page"]
#
#     await bot.message.edit_text("<b>Каталог товаров:</b>")
#     await bot.message.edit_reply_markup(reply_markup=keyboards[page])
#
#
# @dp.callback_query_handler(text_contains="get_good", state=Get_Goods_Page.page)
# async def send_good(callback: types.CallbackQuery, state: FSMContext):
#     callback_data = callback.data.strip().split(":")[1:]
#     good_id = int(callback_data[0])
#     good_information = await get_good_from_db(good_id)
#     good_name, good_description, good_price, good_image = good_information
#     price = [LabeledPrice(label=f"{good_name} | {good_description}", amount=good_price)]
#
#     add_to_cart = InlineKeyboardMarkup().add(
#         InlineKeyboardButton(text='Добавить в корзину', callback_data=f'add_to_cart:{good_id}'))
#     add_to_cart.add(InlineKeyboardButton(text='Вернуться в меню', callback_data='return_to_menu'))
#
#     await bot.send_photo(callback.message.chat.id, photo=good_image,caption=f"Имя товара - {good_name}\n"
#                                                           f"Описание - {good_description}\n"
#                                                           f"Цена - {good_price}", reply_markup=add_to_cart)
#
#     await callback.message.delete()
#     await state.reset_state()
#
#
# @dp.callback_query_handler(lambda c: c.data and c.data.startswith('add_to_cart'), state="*")
# async def process_add_to_cart(callback_query: types.CallbackQuery, state: FSMContext):
#     good_id = int(callback_query.data.split(':')[1])
#     user_id = callback_query.from_user.id
#
#     await add_good_to_cart(user_id, good_id)
#
#     await bot.send_message(callback_query.from_user.id, text='Товар добавлен в корзину.', reply_markup=show_cart_all)
#
# @dp.message_handler(text="Перейти в корзину")
# async def go_to_cart(message: types.Message):
#     await show_cart(message)
#
#
# @dp.message_handler(text="Вернуться в меню")
# async def return_to_catalog(message: types.Message, state: FSMContext):
#     await cmd_start(message)
#
#
# @dp.callback_query_handler(lambda c: c.data == 'clear_cart')
# async def process_clear_cart(callback_query: types.CallbackQuery):
#     user_id = callback_query.from_user.id
#     await clear_cart(user_id)
#     await bot.answer_callback_query(callback_query.id, text="Корзина очищена")
#
#
# async def clear_cart(user_id):
#     await delete_cart(user_id)