
from aiogram.dispatcher.filters.state import StatesGroup, State

class Puchase(StatesGroup):
    EnterQuantity: State()
    Approval = State()
    Payment = State()

class NewItem(StatesGroup):
    name = State()
    photo = State()
    price = State()
    description = State()

class DeleteItem(StatesGroup):
    Delete_Item = State()


class Get_Goods_Page(StatesGroup):
    page = State()

