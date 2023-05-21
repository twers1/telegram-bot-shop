import os

from aiogram import types
from aiogram.dispatcher import FSMContext




from keyboards.inline.choice_buttons import admin_panel
from loader import dp
from states import NewItem, Get_Goods_Page
from utils.db_functions import add_good_to_db


@dp.message_handler(text="Админ-панель")
async def contacts(message: types.Message):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        await message.answer(f'Вы вошли в админ-панель', reply_markup=admin_panel)

        await Get_Goods_Page.first()




@dp.message_handler(text="Добавить товар", state=Get_Goods_Page.page)
async def add_good(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите название товара:")

    await state.reset_state()
    await NewItem.first()
@dp.message_handler(state = NewItem.name)
async def get_name(message: types.Message, state: FSMContext):
    await message.answer("<b>Введите описание товара:</b>")

    async with state.proxy() as data:
        data["name"] = message.text

    await NewItem.next()
    # FSMContextname = message.text
    # item = Item()
    # item.name = name
    # await message.answer("Название: {name}"
    #                      "\nПришлите мне фотографию товара или нажмите /cancel".format(name=name))
    # await NewItem.photo.set()
    # await state.update_data(item=item)


@dp.message_handler(state=NewItem.price) # content_types=types.ContentType.PHOTO
async def get_name(message: types.Message, state: FSMContext):
    await message.answer("<b>Отправьте фото товара: </b>")

    async with state.proxy() as data:
        data["price"] = int(message.text) * 100

    await NewItem.next()
    # photo = message.photo[-1].file_id
    # data = await state.get_data()
    # item: Item = data.get("item")
    # item.photo = photo
    # await message.answer_photo(
    #     photo=photo,
    #     caption="Название: {name}"
    #         "\nПришлите мне цену товара или нажмите /cancel".format(name=item.name)
    # )
    # await NewItem.price.set()
    # await state.update_data(item=item)

@dp.message_handler(state=NewItem.photo)
async def get_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["photo"] = message.text

    state_data = await state.get_data()
    name = state_data["name"]
    price = state_data["price"]
    photo = state_data["photo"]

    await message.answer("<b>Товар успешно добавлен!</b>", reply_markup=admin_panel)

    await add_good_to_db(name, price, photo)
    await state.reset_state()

    await Get_Goods_Page.first()
    # data = await state.get_data()
    # item: Item = data.get("item")
    # try:
    #     price = int(message.text)
    # except ValueError:
    #     await message.answer("Неверное значение, введите число")
    #     return
    #
    # item.price = price
    # markup = InlineKeyboardMarkup(
    #     inline_keyboard=
    #     [
    #         [InlineKeyboardButton(text="Да", callback_data="confirm")],
    #         [InlineKeyboardButton(text="Ввести заново", callback_data="change")]
    #     ]
    # )
    # await message.answer(("Цена: {price}:,\n"
    #                      "Подтверждаете? Нажмите /cancel , чтобы отменить"), reply_markup = markup)
    #
    # await state.update_data(item=item)
    # await NewItem.Confirm.set()

@dp.message_handler(commands=["cancel"], state=NewItem)
async def cancel(message: types.Message, state: FSMContext):
    await message.answer("Вы отменили создание товара")
    await state.reset_state()

@dp.message_handler(text="Реквизиты банковской карты")
async def bank_card_details(message: types.Message):
    await message.answer("Пусто")

@dp.message_handler(text="Размер предоплаты")
async def prepayment_amount(message: types.Message):
    await message.answer("Пусто")

@dp.callback_query_handler(text_contains="change", state=NewItem.confirm)
async def change_price(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer("Ввелите заново цену товара")
    await NewItem.price.set()

@dp.callback_query_handler(text_contains="confirm", state=NewItem.confirm)
async def confirm(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    await call.message.answer("Товар удачно создан")
    await state.reset_state()




