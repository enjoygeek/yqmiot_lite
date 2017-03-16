# -*- encoding: utf-8 -*-
from bottle import template, view, request, response, redirect
from model.account import checkAccount2

def app():
    if request.method == "GET":
        account = request.get("account")
        if account:
            redirect("/")

        return template("login.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        if len(username) == 0:
            return "无效账号"
        if len(password) == 0:
            return "无效密码"
        account = checkAccount2(username)
        if account:
            if account.validPassword(password):
                print dir(response)
                response.set_cookie("userid", str(account.id), path="/") # 坑！path 必须指定
                redirect("/")
            else:
                return "密码错误"
        else:
            return "账号不存在"