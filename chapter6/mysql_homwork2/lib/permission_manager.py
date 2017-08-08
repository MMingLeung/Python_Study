#! -*- coding:utf8 -*-
#! /usr/bin/Python
from core import login
from lib import db_handler



class Permission:
    'handler all the permission interactions'
    def run(self):
        while True:
            self.db_handler_obj = db_handler.OperatrDB()
            self.db_handler_obj.print_permission()
            print("Permission Management:1、add_per 2、del_per 3、mod_per")
            user_input = input("Please input :>> ")
            if user_input == '1':
                user_input = "add_per"
            elif user_input == '2':
                user_input = "del_per"
            elif user_input == '3':
                user_input = "mod_per"
            elif user_input == "exit":
                break
            if hasattr(self,user_input):
                func = getattr(self, user_input)
                func()
            else:
                print("Please input correct choice.")

    def user_input(self):
        user_input = input("Please input username  :")
        per = input("Please input permission :")
        return user_input,per

    def add_per(self):
        user_input, add_per = self.user_input()
        self.db_handler_obj.add_per_handler(user_input, add_per)

    def del_per(self):
        user_input, del_per = self.user_input()
        self.db_handler_obj.del_per_handler(user_input, del_per)

    def mod_per(self):
        user_input, mod_per = self.user_input()
        self.db_handler_obj.mod_per_handler(user_input, mod_per)