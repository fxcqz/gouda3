import random


def run_schema():
    pass


def main(*args, **kwargs):
    writer = kwargs.pop('writer')
    line = kwargs.pop('line')
    offset = 0
    if line[0][:-1] == kwargs.get('name', 'Gouda'):
        offset = 1
    if line[offset] == "rate":
        writer("%d/8" % random.randint(0, 8))
    elif line[offset][0] == 'r' and line[offset][1:].isdigit():
        base = int(line[offset][1:])
        rating = random.randint(0, base)
        writer("%d/%d" % (rating, base))
