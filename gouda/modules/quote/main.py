from peewee import *

from gouda.bot import DATABASE as db
from gouda.models import Message, Quote

def run_schema():
    Quote.create_table(True)

# main

def main(*args, **kwargs):
    """
    quote stuff

    qsave [tag] quote   save quote
    qsave [tag] ^num    save quote chat backref
    qload [tag]         load random quote from tag
    qfind [pattern]     find a random quote based on a pattern
    """
    # since this module has special syntax we use a main func
    writer = kwargs.pop('writer')
    line = kwargs.pop('line')
    if line[0] == "qsave" and len(line) > 2:
        # saving a new quote
        tag = line[1]
        saved = False
        if line[2].startswith("^") and len(line[2]) > 1:
            last_id = Message.select().order_by(Message.id.desc()).get().id
            try:
                num = int(line[2][1:])
                if num >= 0:
                    try:
                        message = Message.select().where(Message.id==last_id-num).get()
                        Quote.create(tag=tag, user=message.name, message=message.message)
                        saved = True
                    except Message.DoesNotExist:
                        # just in case
                        pass
            except ValueError as e:
                # naughty user input
                print(e)
        else:
            message = ' '.join(line[2:])
            Quote.create(tag=tag, user=kwargs.pop('nick', '~'), message=message)
            saved = True
        if saved:
            writer("Saved your quote, pal")
    elif line[0] == "qload" and len(line) > 1:
        # retrieving a quote
        tag = line[1]
        try:
            quote = Quote.select().where(Quote.tag==tag).order_by(fn.Random()).get()
            writer('<%s> %s' % (quote.user, quote.message))
        except:
            # probably no quotes in this tag
            print("Could not load quote with tag %s" % tag)
    elif line[0] == "qfind" and len(line) > 1:
        # search records
        try:
            quote = Quote.select().where(Quote.message.contains(' '.join(line[1:]))).order_by(fn.Random()).get()
            writer('<%s> %s' % (quote.user, quote.message))
        except:
            # probably no quotes in this tag
            print("Could not find quote with pattern %s" % ' '.join(line[1:]))
    elif line[0] == "qtags":
        try:
            tags = Quote.select(Quote.tag).distinct()
            writer('Tags: %s.' % ', '.join(t.tag for t in tags))
        except:
            print("Cannot load tags")
