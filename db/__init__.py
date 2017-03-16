# -*- encoding: utf-8 -*-
import sqlite3

from const import DATABASE

class DB(object):
    def __init__(self, db):
        self.conn = sqlite3.connect(db)

    def close(self):
        self.conn.close()

    def query(self, sql, *args):
        return self.conn.execute(sql, *args)

    def execute(self, sql, *args):
        self.conn.execute(sql, *args)

    def commit(self):
        self.conn.commit()

db = DB(DATABASE)