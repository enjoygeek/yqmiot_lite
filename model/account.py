# -*- encoding: utf-8 -*-
import const

from db import db

class InvalidArgument(Exception):
    pass

class AccountExist(Exception):
    pass

class AccountNotFound(Exception):
    pass

class InvalidAccount(Exception):
    pass

def checkAccount(func):
    def check(self, *args, **kargs):
        if not self.id:
            raise InvalidAccount
        return func(self, *args, **kargs)
    return check

def fetchMaxId():
    r = db.query("SELECT id FROM account ORDER BY id DESC LIMIT 1")
    row = r.fetchone()
    if row:
        return row[0]
    else:
        return 0

def checkExist(username):
    r = db.query("SELECT * FROM account WHERE username=?", (username, ))
    return r.fetchone() != None

def checkAccount2(username):
    r = db.query("SELECT id FROM account WHERE username=?", (username, ))
    row = r.fetchone()
    if row:
        return Account(row[0])

def add(args):
    username = args.get("username", None)
    password = args.get("password", None)

    if username and len(username)>0 and password and len(password)>0:
        if checkExist(username):
            raise AccountExist
        maxId = fetchMaxId() + 1
        sql = "INSERT INTO account (id, username, password)VALUES(?, ?, ?)"
        db.execute(sql, (maxId, username, password))
        db.commit()
        return Account(maxId)
    else:
        raise InvalidArgument

class Account(object):

    def __init__(self, id):
        self.id = None
        self.username = None
        self.password = None
        self.authkey = None
        self.nodes = [] # did
        self._loadFromDb(id)
        
    def _loadFromDb(self, id):
        sql = "SELECT id, username, password, authkey FROM account WHERE id=?"
        r = db.query(sql, (id, )).fetchone()
        if r:
            self.id = r[0]
            self.username = r[1]
            self.password = r[2]
            self.authkey = r[3]
        else:
            raise AccountNotFound

    @checkAccount
    def validPassword(self, password):
        return self.password != None \
            and len(self.password) > 0 \
            and self.password == password

    @checkAccount
    def validAuthkey(self, authkey):
        return self.authkey != None \
            and len(self.authkey) > 0 \
            and self.authkey == authkey

    

