#!/usr/bin/env python
#! -*- coding: utf-8 -*-
'''
Handlers for index page
'''
import tornado.web
from lib.CUSTOMIZED_SESSION.my_session import SessionFactory


class IndexHandler(tornado.web.RequestHandler):
    def initialize(self):
        # 钩子函数 首先执行
        class_ = SessionFactory.get_session()
        # 实例化 session 类的对象
        self.session = class_(self)


    def get(self, *args, **kwargs):
        if not self.session['user_data']:
            self.render('login.html', msg='请登录')
            return
        self.render('index.html',
                    friends=self.session['user_data']['friends'],
                    my_data=self.session['user_data']['data'],
                    add_error='',
                    apply_data='',
                    group_data=self.session['user_data']['group'],
                    group_member=self.session['user_data']['group_member'],
                    )
