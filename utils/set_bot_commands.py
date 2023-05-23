from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота."),
            types.BotCommand("help", "Вывести справку о доступных командах."),
            types.BotCommand("shop", "Открыть меню магазина.")
        ]
    )