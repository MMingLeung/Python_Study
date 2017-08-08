#!-*- coding:utf-8 -*-
#!/usr/bin/pyhton

from conf import settings
from lib import db_handle

def auth(func):
    '''
    用户认证装饰器
    :param:func
    :return func,匹配到正确密码的用户的username,data[num]["quota"]用户配额
    '''
    def wrapper(*args, **kwargs):
        username = input("Please input your username: ")
        password = input("Please input your password: ")
        data = db_handle.load_db()
        # print(username,password)
        for num in range(len(data)):
            # print('num:', num, 'len(data)',len(data))
            # print('data: ',data[num]["username"], data[num]["password"])
            if username == data[num]["username"] and password == data[num]["password"]:
                res = func(*args, **kwargs)
                return res,username,data[num]["quota"]
        else:
            print("Username or password is incorret! ")

    return wrapper()
