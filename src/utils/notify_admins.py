# import logging
# from aiogram import Dispatcher
# from config import admin_id
#
#
# async def on_startup_notify(dp: Dispatcher):
#     bot_name = await dp.bot.get_me()
#
#     for admin in admin_id:
#         try:
#             await dp.bot.send_message(admin, f"<b>Бот запущен</b>")
#
#         except Exception as err:
#             logging.exception(err)