from aiogram import types, Bot
from gino import Gino
from sqlalchemy import (Column, Integer, BigInteger, String, Sequence, TIMESTAMP, Boolean, JSON)
from sqlalchemy import sql
from gino.schema import GinoSchemaVisitor

db = Gino()

class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    user_id = Column(BigInteger)
    language = Column(String(2))
    full_name = Column(String(100))
    username = Column(String(50))
    referral = Column(Integer)
    query: sql.Select


class Item(db.Model):
    __tablename__ = "items"
    name = Column(String(50))
    photo = Column(String(250))
    price = Column(Integer)


class Purchase(db.Model):
    __tablename__ = "purchases"
    query: sql.Select
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    buyer = Column(BigInteger)
    item_id = Column(Integer)
    amount = Column(Integer)
    quantity = Column(Integer)
    purchase_time = Column(TIMESTAMP)
    shipping_address = Column(JSON)
    phone_number = Column(String(50))
    email = Column(String(200))
    receiver = Column(String(100))
    successful = Column(Boolean, default=False)

class DBCommands:
    async def get_user(self, user_id) -> User:
        user = await User.query.where(User.user_id == user_id).gino().first()
        return user

    async def add_new_user(self, referral=None) -> User:
        user = types.User.get_current()
        old_user = await self.get_user(user_id)
        if old_user:
            return old_user
        new_user = User()
        new_user.user_id = user_id
        new_user.username = user.username
        new_user.full_name = user.full_name
        if referral:
            new_user.referral = int(referral)
        await new_user.create()
        return new_user

    async def show_items(self):
        items = await Item.query.gino.all()
        return items

async def create_db():
    await db.set_bind(f"postgresql://{DB_USER}:{db_pass}@{host}/telegramShopTest")
    db.gino = GinoSchemaVisitor
    await db.gino.drop_all()
    await db.gino.create_all()