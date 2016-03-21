from peewee import *

from gouda.bot import DATABASE as db
from gouda.models import Message, Quote

def run_schema():
    Quote.create_table(True)

# main

def main(*args, **kwargs):
    """ since this module has special syntax we use a main func """
    writer = kwargs.pop('writer')
    line = kwargs.pop('line')
    if line[0].startswith("qs#") and len(line) > 1:
        # saving a new quote
        if len(line[0]) > 2:
            tag = line[0][2:]
        else:
            tag = "none"
        if line[1].startswith("CHAT@") and len(line[1]) > 5:
            last_id = Message.select().order_by(Message.id.desc()).get().id
            try:
                num = int(line[1][5:]) - 1
                if num >= 0:
                    message = Message.select().where(Message.id==last_id-num).get()
                    Quote.create(tag=tag, user=message.name, message=message.message)
            except ValueError:
                # naughty user input
                pass
        else:
            message = ' '.join(line[1:])
            Quote.create(tag=tag, user=kwargs.pop('nick', '~'), message=message)
    elif line[0].startswith("qr#"):
        # retrieving a quote
        if len(line[0]) <= 2:
            tag = "none"
        else:
            tag = line[0][2:]
        try:
            quote = Quote.select().where(Quote.tag==tag).order_by(fn.Random()).get()
            writer('<%s> %s' % (quote.user, quote.message))
        except:
            # probably no quotes in this tag
            pass
    elif line[0].startswith("qf#") and len(line[0]) > 2:
        # search records
        try:
            quote = Quote.select().where(Quote.message.contains(' '.join(line)[2:])).order_by(fn.Random()).get()
            writer('<%s> %s' % (quote.user, quote.message))
        except:
            # probably no quotes in this tag
            pass
