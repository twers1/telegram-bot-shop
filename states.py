from aiogram.dispatcher.filters.state import StatesGroup, State


class Puchase(StatesGroup):
    EnterQuantity: State()
    Approval = State()
    Payment = State()


class NewItem(StatesGroup):
    name = State()
    description = State()
    price = State()
    photo = State()


class Get_Goods_Page(StatesGroup):
    page = State()


class BankCardState(StatesGroup):
    waiting_for_bank_card = State()


class YourForm(StatesGroup):
    name = State()
    phone = State()
    delivery = State()
    payment = State()