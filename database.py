from aiogram import types, Bot
from dotenv import load_dotenv
from gino import Gino
from sqlalchemy import (Column, Integer, BigInteger, String, Sequence, TIMESTAMP, Boolean, JSON)
from sqlalchemy import sql
from gino.schema import GinoSchemaVisitor

import os

from config import db_user, db_pass, host

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
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
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

    async def count_user(self):
        total = await db.func.count(User.id).gino.scalar()
        return total
    async def check_referral(self):
        bot = Bot.get_current()
        user_id = types.User.get_current().id
        user = await self.get_user(user_id)
        referrals = await User.query.where(User.referral == user.id).gino.all()
        return ", ".join([
            f"{num+1}. " + (await bot.get_chat(referral.user_id)).get_mention(as_html=True)
            for num, referral in enumerate(referrals)
        ])
    async def show_items(self):
        items = await Item.query.gino.all()
        return items
async def create_db():
    await db.set_bind(f"postgresql://{db_user}:{db_pass}@{host}/telegramShopTest")
    db.gino = GinoSchemaVisitor
    await db.gino.drop_all()
    await db.gino.create_all()