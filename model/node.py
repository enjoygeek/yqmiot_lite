# -*- encoding: utf-8 -*-
from db import db

class InvalidNode(Exception):
    pass

class InvalidUser(Exception):
    pass

node = {} # 内存cache

def add(args):
    name = args.get("name")
    model = args.get("model", "normal")
    userid = args.get("userid")
    if not userid:
        raise InvalidUser
    id = maxid() + 1
    if not name:
        name = str(id)
    sql = "INSERT INTO node(id, name, model, userid)VALUES(?, ?, ?, ?)"
    db.execute(sql, (id, name, model, userid))
    db.commit()

def loadNode(id):
    n = node.get(id)
    if not n:
        n = Node(id)
        node[id] = n
    return n

def findNodes(userid):
    sql = "SELECT id FROM node WHERE userid=?"
    r = db.query(sql, (userid, )).fetchall()
    return [col[0] for col in r]

def maxid():
    sql = "SELECT id from node ORDER BY id DESC"
    r = db.query(sql).fetchone()
    if r:
        return r[0]
    else:
        return 0


class Node(object):
    def __init__(self, id):
        self.id = None
        self.name = None
        self.model = None
        self.userid = None
        self.props = {}
        self.loadFromDb(id)

    def loadFromDb(self, id):
        sql = "SELECT id, name, model, userid FROM node WHERE id=?"
        r = db.query(sql, (id, )).fetchone()
        if r:
            self.id, self.name, self.model, self.userid = r
            
        else:
            raise InvalidNode

    

'''
    events, property, method

    node = Node(1)
    node.
'''