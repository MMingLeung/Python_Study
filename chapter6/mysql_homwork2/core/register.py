#! -*- coding:utf8 -*-
#! /usr/bin/Python


from lib import db_handler

def register():
    'register interation'
    username = input("Please input username: ")
    password = input("Please input password: ")
    email = input("Please input email: ")
    obj = db_handler.OperatrDB()
    obj.register(username, password, email)