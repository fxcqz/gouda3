import random


def run_schema():
    pass


def main(*args, **kwargs):
    writer = kwargs.pop('writer')
    line = kwargs.pop('line')
    offset = 0
    if len(line[0]) > 1:
        if line[0][:-1] == kwargs.get('name', 'Gouda'):
            if len(line) < 2:
                return
            offset = 1
        if line[offset] == "rate":
            writer("%d/8" % random.randint(0, 8))
        elif line[offset][0] == 'r' and line[offset][1:].isdigit():
            try:
                base = int(line[offset][1:])
                rating = random.randint(0, base)
                writer("%d/%d" % (rating, base))
            except ValueError:
                # naughty input
                pass
