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

commands = ['log']

def run_schema():
    Message.create_table(True)

def log(*args, **kwargs):
    writer = kwargs.pop('writer')
    user = kwargs.pop('message', ['log'])[0]
    if user == 'log':
        log = random.choice([msg for msg in Message.select()])
        user = log.name
    else:
        log = random.choice([msg for msg in Message.select().where(Message.name == user)])
    writer("<%s> %s" % (user, log.message))

def main(*args, **kwargs):
    writer = kwargs.pop('writer')
    if kwargs.pop('log', True):
        # log message
        Message.create(
            name=kwargs.pop('nick', '***'),
            message=' '.join(kwargs.pop('line', ['blank']))
        )
