#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Database Controller
'''
import pymysql
from static import settings


class DBController(object):
    def __init__(self):
        self.conn = self.connect
        self.cur = self.conn.cursor()

    @property
    def connect(self):
        try:
            conn = pymysql.connect(
                host=settings.DB_HOST,
                user=settings.DB_USER_NAME,
                password=settings.DB_PWD,
                db=settings.DB_NAME,
                charset=settings.CHARSET,
            )
        except Exception as e:
            raise Exception('数据库连接失败')
        return conn

    def search(self, sql, *args):
        result = self.cur.execute(sql, *args)
        return result

    def get_one(self):
        return self.cur.fetchone()

    def get_all(self):
        return self.cur.fetchall()

    def db_close(self):
        self.cur.close()
        self.conn.close()

    def db_save(self):
        self.conn.commit()

    def db_dict_cur(self):
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)