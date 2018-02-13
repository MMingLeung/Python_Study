#! -*- coding:utf8 -*-
#! /usr/bin/Python

'handle all the database interactions'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Index

Base = declarative_base()

class Users(Base):
    'create database module of Users'
    __tablename__ = 'users'
    uid = Column (Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False, index = True)
    password = Column(String(32), nullable=False)
    email = Column(String(16), unique=True)

    __tablename__args__  = (
    UniqueConstraint("id", "name", name="unique_id_name" ),
        Index("ix_name_email", "name", "email"),
    )

class Permissions(Base):
    'create database module of Permissions'
    __tablename__ = 'permissions'
    pid = Column(Integer, primary_key=True, autoincrement=True)
    permission = Column(String(32), nullable=False)


class UserPerRelation(Base):
    'create database module of Users_Permissions_Relation'
    __tablename__ = "user_per"
    rid = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.uid"))
    per_id = Column(Integer, ForeignKey("permissions.pid"))

    user_re = relationship("Users", backref="u_back")
    per_re = relationship("Permissions", backref="p_back")

class OperatrDB:
    'Operate Database'
    def __init__(self):
        'initialize and connect to db'
        self.engine = create_engine(
        "mysql+pymysql://root:qwert@localhost:3306/mysql_p?charset=utf8",
        max_overflow=5)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_db(self):
        Base.metadata.create_all(self.engine)

    def login_user(self, username, password):
        '''
        sql query
        :param username, password: sql query params set in settings
        :return:user_list
        '''
        user_list = self.session.query(Users).filter(Users.name==username,Users.password==password)
        self.session.close()
        return user_list

    def login_manager(self,userid):
        '''
        sql query
        :param username, password: sql query params set in settings
        :return:user_list
        '''
        user_list = self.session.query(UserPerRelation).filter(UserPerRelation.user_id==userid)
        self.session.close()
        return user_list

    def output_name_permission(self,username, password):
        '''
        sql query
        :param username, password, per: sql query params set in settings, for login module to get arguments
        :return:user_id,user_name,per
        '''
        odb = OperatrDB()
        res = odb.login_user(username, password)
        for row in res:
            user_id = row.uid
            user_name = row.name
        res1 = odb.login_manager(user_id)
        for row in res1:
            per = row.per_re.permission
        return user_id,user_name,per

    def add_mod_del_handler(self, username, permission):
        '''
        :param username, permission: input username and permission to get user_id,per_id for db operator
        :return: user_id,per_id
        '''
        res1 = self.session.query(Users.uid).filter(Users.name == username).all()
        if res1:
            for row in res1:
                user_id = row.uid
            res2 = self.session.query(Permissions.pid).filter(Permissions.permission == permission).all()
            if res2:
                for row in res2:
                    per_id = row.pid
                return user_id,per_id
            else:
                print("Permission is not existed")
        else:
            print("User is not existed")

    def add_per_handler(self, username, permission):
        '''
        :param username, permission: 
        add permission
        '''
        user_id, per_id = self.add_mod_del_handler(username, permission)
        modify_per = UserPerRelation(user_id=user_id, per_id=per_id)
        self.session.add(modify_per)
        self.session.commit()
        self.session.close()
        print("Add success.")

    def del_per_handler(self, username, permission):
        '''
        :param username, permission: 
        del permission
        '''
        user_id, per_id = self.add_mod_del_handler(username, permission)
        users_list = self.session.query(UserPerRelation).filter(
            UserPerRelation.user_id==user_id,
            UserPerRelation.per_id==per_id).delete()
        self.session.commit()
        self.session.close()
        print("Delete success.")

    def mod_per_handler(self, username, permission):
        '''
        :param username, permission: 
        modify permission
        '''
        user_id, per_id = self.add_mod_del_handler(username, permission)
        new_per = input("Please input the new permission: ")
        if new_per == 'manager':
            new_per = 2
        elif new_per == 'guest':
            new_per = 3
        mod = self.session.query(UserPerRelation).filter(UserPerRelation.user_id==user_id
                                                         ).update({UserPerRelation.per_id:new_per},synchronize_session="evaluate")
        self.session.commit()
        self.session.close()
        print("Update success.")

    def add_usr_handler(self,user_name, user_password, user_email):
        '''
        :param user_name, user_password, user_email: 
        add user info
        '''
        add_user = Users(name=user_name, password=user_password, email=user_email)
        self.session.add(add_user)
        self.session.commit()
        self.session.close()
        print("Add user success.")

    def del_usr_handler(self, user_name):
        '''
        :param user_name: 
        del user info
        '''
        del_user = self.session.query(Users).filter(Users.name==user_name).delete()
        self.session.commit()
        self.session.close()
        print("Delete success.")


    def mod_usr_handler(self, user_name):
        '''
        :param user_name: 
        modify user info
        '''
        ipt =  input("change : 1、user_name  2、password 3、email")
        if ipt == '1':
            new_name = input("Please input the new name: ")
            mod = self.session.query(Users).filter(Users.name == user_name
                                                   ).update({Users.name: new_name}, synchronize_session=False)
            self.session.commit()
            self.session.close()
            print("Update username success.")
        elif ipt == '2':
            new_password = input("Please input the new password: ")
            mod = self.session.query(Users).filter(Users.name == user_name
                                                   ).update({Users.password: new_password}, synchronize_session=False)
            self.session.commit()
            self.session.close()
            print("Update password success.")

        elif ipt == '3':
            new_email = input("Please input the new email: ")
            mod = self.session.query(Users).filter(Users.name == user_name
                                                   ).update({Users.email: new_email}, synchronize_session=False)
            self.session.commit()
            self.session.close()
            print("Update email success.")

    def register(self,user_name, user_password, user_email):
        'register interface'
        add_user = Users(name=user_name, password=user_password, email=user_email)
        self.session.add(add_user)
        self.session.commit()
        self.session.close()
        print("Register success.")

    def print_permission(self):
        'print premission info on database'
        user_list = self.session.execute("select users.uid, users.name, permissions.permission from users left join user_per on users.uid=user_per.user_id left join permissions on permissions.pid=user_per.per_id")
        for row in user_list:
            print(row)
        self.session.close()

    def print_person_info(self):
        'print user info on database'
        user_list = self.session.query(Users)
        for row in user_list:
            print(row.uid, row.name, row.password, row.email)
        self.session.close()

# select user_id,permissions.permission from user_per left join permissions
#  on permissions.pid=user_per.per_id where user_id in (select uid from users wher
# e name="Noah");

# #SELECT * FROM (select * from tb) as B;
# users_list = session.query(Users).filter(Users.id > 2).subquery()
# res = session.query(users_list).all()

# odb = OperatrDB()
# res = odb.login_user("Noah","123")
# for row in res:
#     use_id =row.uid
# res1 = odb.login_manager(use_id)
# for row in res1:
#     print(row.rid,row.per_re.permission)
# user_id,user_name,per = odb.output_name_permission("Noah","123")
# print(user_id,user_name,per)
# odb.mod_per_handler("Mason", "guest")



