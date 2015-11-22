from peewee import *

from gouda.bot import DATABASE as db


class Message(Model):
    name = CharField()
    message = CharField()

    class Meta:
        database = db
