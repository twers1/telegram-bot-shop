
from aiogram.dispatcher.filters.state import StatesGroup, State

class Puchase(StatesGroup):
    EnterQuantity: State()
    Approval = State()
    Payment = State()

class NewItem(StatesGroup):
    default = State()
    name = State()
    photo = State()
    price = State()
    confirm = State()
    cost = State()
    code = State()
    category = State()
    description = State()
    end = State()
    apply = State()

class DeleteItem(StatesGroup):
    Delete_Item = State()


class Get_Goods_Page(StatesGroup):
    page = State()

