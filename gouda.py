#!/usr/bin/python
"""
Cheesebot of love. xo
"""
import os
import sqlite3

from gouda.bot import Gouda
from gouda.connection import Connection, ConnectionManager
from gouda.settings import Settings


if __name__ == '__main__':
    gouda = Gouda()

    # create db if it doesnt exist
    if not os.path.exists(gouda.settings.db['name']):
        with sqlite3.connect(gouda.settings.db['name']) as db:
            print("Database created.")

    connection = Connection(gouda.settings.startup)
    with ConnectionManager(connection, gouda.db) as conn:
        gouda.run(conn)
