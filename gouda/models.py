from peewee import *

from gouda.bot import DATABASE as db


class BaseModel(Model):
    class Meta:
        database = db


class Message(BaseModel):
    name = CharField()
    message = CharField()
