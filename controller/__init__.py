# -*- encoding: utf-8 -*-
# import gevent
import time
import bottle
import json

from bottle import run, request, response, route

from model.account import Account
from model.node import add as addNode
from model.account import checkAccount2

from index import app as index
from login import app as login
import model.account
from model.node import findNodes, loadNode



@bottle.hook("before_request")
def hookRequest(*args, **kargs):
    userid = bottle.request.get_cookie("userid")
    if userid:
        # try:
        bottle.request["account"] = Account(userid)
        # except:
            # pass

@bottle.route('/static/<subpath:path>')
def server_static(subpath):
    print subpath
    return bottle.static_file(subpath, root='views')

@bottle.route("/addnode", method="POST")
def addnode():
    name = bottle.request.forms.getunicode("name")
    model = bottle.request.forms.getunicode("model")
    account = bottle.request.get("account")

    if not account:
        return bottle.redirect("/login")

    if name and len(name) > 0 \
        and model and len(model) > 0:
        addNode({"userid": account.id, "name": name, "model": model})
        return bottle.redirect("/")
    else:
        return "参数错误"

# 创建新账号
@route("/v1/accounts", method="POST")
def createAccount():
    forms = request.json
    # username = request.forms.getunicode("username")
    # password = request.forms.getunicode("password")
    username = forms.get("username")
    password = forms.get("password")

    result = {}
    result["error"] = 0
    result["errmsg"] = ""

    if username and len(username) >= 4 \
        and password and len(password) >= 4:

        # 检查账号是否已经存在
        if not checkAccount2(username):
            try:
                account = model.account.add({"username": username, "password": password})
                if account:
                    result["error"] = 0
                    result["errmsg"] = "ok"
                    result["accountid"] = account.id
                    result["username"] = account.username
                else:
                    result["error"] = -1
                    result["errmsg"] = "unknown error1"
            except:
                raise
                result["error"] = -1
                result["errmsg"] = "unknown error2"
        else:
            result["error"] = -1
            result["errmsg"] = "account exist"
    else:
        result["error"] = -1
        result["errmsg"] = "params error"

    return json.dumps(result)

# 创建认证
@route("/v1/auth", method="POST")
def createAuth():
    forms = request.json
    username = forms.get("username")
    password = forms.get("password")

    result = {}
    result["error"] = 0
    result["errmsg"] = ""

    if username and len(username) >= 4 \
        and password and len(password) >= 4:

        # 检查账号是否已经存在
        account = checkAccount2(username)
        if account:
            if account.validPassword(password):
                response.set_cookie("userid", str(account.id), path="/") # 坑！path 必须指定
                result["error"] = 0
                result["errmsg"] = "ok"
            else:
                result["error"] = -1
                result["errmsg"] = "password erorr"
        else:
            result["error"] = -1
            result["errmsg"] = "account not exist"
    else:
        result["error"] = -1
        result["errmsg"] = "params error"

    return json.dumps(result)

# 检查认证
@route("/v1/auth", method="GET")
def getAuth():
    account = request.get("account")

    result = {}
    result["error"] = 0
    result["errmsg"] = ""

    if account:
        result["error"] = 0
        result["errmsg"] = "ok"
    else:
        result["error"] = -1
        result["errmsg"] = "not login"

    return json.dumps(result)

# 创建新设备
@route("/v1/nodes", method="POST")
def createNode():
    # TODO auth 检查

    result = {}
    result["error"] = 0
    result["errmsg"] = ""

    forms = request.json
    name = forms.get("name")
    model = forms.get("model")
    # userid = forms.get("userid")

    if name:
        addNode({"userid": 1, "name": name, "model": model})
        result["error"] = 0
        result["errmsg"] = "ok"
    else:
        result["error"] = -1
        result["errmsg"] = "params error"

    return json.dumps(result)

# 获得所有设备
@route("/v1/nodes", method="GET")
def listNodes():
    result = {}
    result["error"] = 0
    result["errmsg"] = "ok"

    nodes = findNodes(1) # 获得所有id
    nodes = map(loadNode, nodes)

    result["nodes"] = {node.id: {"id": node.id, "name": node.name, "model": node.model or "", "accountid": node.userid} for node in nodes}

    return json.dumps(result)

def web():

    bottle.route("/", callback=index)
    bottle.route("/login", method=["GET", "POST"], callback=login)
    bottle.run(host="0.0.0.0", port=8003, reloader=True)

# def mqtt():
#     while True:
#         time.sleep(1)
#         # print 2

def run():
    web()
    # gevent.joinall([
    #     gevent.spawn(web),
    #     gevent.spawn(mqtt),
    # ])
