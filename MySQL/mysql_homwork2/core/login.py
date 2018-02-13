#! -*- coding:utf8 -*-
#! /usr/bin/Python
from lib import db_handler
from lib import permission_manager, user_manager


def login():
    'Login module'
    while True:
        username = input("Please input your username: ")
        password = input("Please input your password: ")
        db_handler_obj = db_handler.OperatrDB()
        user_id, user_name, per = db_handler_obj.output_name_permission(username, password)
        if user_id :
            print("login success!, your permission is %s" % per)
            if per == "admin":
                admin()
        else :
            print("username or password is incorrect!")

def admin():
    'Admin interface'
    while True:
        msg = """
                ===========功能选择===========
                1、权限管理
                2、用户管理
            """
        print(msg)
        ipt = input(">> :")
        if ipt == "1":
            p_m = permission_manager.Permission()
            p_m.run()
        elif ipt == "2":
            u_m = user_manager.User()
            u_m.run()
        elif ipt == 'exit':
            break