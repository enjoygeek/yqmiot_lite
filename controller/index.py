# -*- encoding: utf-8 -*-
from bottle import template, view, request
from model.node import findNodes, loadNode

@view("index.html")
def app():
    account = request.get("account")
    nodes = []
    if account:
        nodes = findNodes(account.id)
        nodes = map(loadNode, nodes)
    return {"account":account, "nodes": nodes}