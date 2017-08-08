#! -*- coding:utf8 -*-
#! /usr/bin/Python
from lib import db_handler

class User:
    'handler all the users interactions'
    def run(self):
        while True:
            self.db_handler_obj  = db_handler.OperatrDB()
            self.db_handler_obj.print_person_info()
            print("User Management:1、add_user 2、del_user 3、mod_user")
            user_input = input("Please input :>> ")
            if user_input == '1':
                user_input = "add_user"
            elif user_input == '2':
                user_input = "del_user"
            elif user_input == '3':
                user_input = "mod_user"
            elif user_input == "exit":
                break
            if hasattr(self,user_input):
                func = getattr(self, user_input)
                func()
            else:
                print("Please input correct choice.")

    def user_input(self):
        user_name = input("Please input username  :")
        user_password = input("Please input password : ")
        user_email = input("Please input email: ")
        return user_name,user_password,user_email

    def add_user(self):
        user_name, user_password, user_email = self.user_input()
        self.db_handler_obj.add_usr_handler(user_name, user_password, user_email)

    def del_user(self):
        user_name = input("Please input username to delete: ")
        self.db_handler_obj.del_usr_handler(user_name)

    def mod_user(self):
        user_name = input("Please input username to update: ")
        self.db_handler_obj.mod_usr_handler(user_name)