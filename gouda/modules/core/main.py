from peewee import *
import random

from gouda.bot import DATABASE as db

# models

class Message(Model):
    name = CharField()
    message = CharField()

    class Meta:
        database = db

# main

commands = ['user']

def run_schema():
    Message.create_table(True)

def user(*args, **kwargs):
    writer = kwargs.pop('writer')
    user = kwargs.pop('message', ['user'])[0]
    if user == 'user':
        return
    messages = Message.select().where(Message.name == user)
    writer("<%s> %s" % (user, random.choice([m.message for m in messages])))

def main(*args, **kwargs):
    writer = kwargs.pop('writer')
    if kwargs.pop('log', True):
        # log message
        Message.create(
            name=kwargs.pop('nick', '***'),
            message=' '.join(kwargs.pop('line', ['blank']))
        )
