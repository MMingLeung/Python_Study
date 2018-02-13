#! -*- coding:utf8 -*-
#! /usr/bin/Python

'main program handle module , handle all the interaction stuff'

from core import login, register, retrieve_password

def run():
    msg = """
        1、登陆
        2、注册
        3、找回密码"""
    print(msg)
    userinput = input("Please input >>: ")
    if userinput == '1':
        login.login()
    elif userinput == '2':
        register.register()
    elif userinput == '3':
        retrieve_password.retrieve_password()