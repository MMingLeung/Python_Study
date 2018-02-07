#!/usr/bin/env python
#! -*- coding: utf-8 -*-
'''
Handlers for operating which friends and groups
'''
import json
import tornado.escape
from lib.db_controller import DBController
from lib.CUSTOMIZED_SESSION.my_session import SessionFactory


class SearchHandler(tornado.web.RequestHandler):
    '''
    处理搜索请求
    '''
    def post(self, *args, **kwargs):
        '''
        :param username: 用户名
        :return: 
        '''
        username = self.get_argument('username')
        db_obj = DBController()
        db_obj.search('SELECT uid, username FROM userinfo WHERE username=(%s)', (username,))
        user_data = db_obj.get_one()
        db_obj.db_close()
        self.write(json.dumps(user_data))


class AddHandler(tornado.web.RequestHandler):
    '''
    处理好友添加请求
    '''
    def initialize(self):
        # 钩子函数 首先执行
        class_ = SessionFactory.get_session()
        # 实例化 session 类的对象
        self.session = class_(self)

    def get(self, *args, **kwargs):
        '''
        查询用户是否存在
        :param apply_id: 添加好友 id
        :param current_id: 当前用户 id
        :return: 
        '''
        apply_id = self.get_argument('id')
        current_id = self.session['user_data']['data'][0]
        db_obj = DBController()
        result = db_obj.search('INSERT INTO friend_application(user_apply, user_recv, confirm) VALUE (%s, %s, 0)',
                               (current_id, apply_id))
        db_obj.db_save()
        db_obj.db_close()
        if result:
            self.render('index.html',
                        friends=self.session['user_data']['friends'],
                        my_data=self.session['user_data']['data'],
                        add_error='',
                        apply_data='',
                        group_data=self.session['user_data']['group'],
                        group_member=self.session['user_data']['group_member'],
                        )
        else:
            self.render('index.html',
                        friends=self.session['user_data']['friends'],
                        my_data=self.session['user_data']['data'],
                        add_error='添加失败',
                        apply_data='',
                        group_data=self.session['user_data']['group'],
                        group_member=self.session['user_data']['group_member'],
                        )

    def post(self, *args, **kwargs):
        '''
        添加好友
        :param apply_id: 添加好友 id
        :param current_id: 当前用户 id
        :return: 
        '''
        apply_id = self.get_argument('user_apply')
        current_id = self.session['user_data']['data'][0]
        db_obj = DBController()
        try:
            sql = "UPDATE friend_application set confirm=1 WHERE user_apply=%s AND user_recv=%s"
            result1 = db_obj.search(sql, (apply_id, current_id))
            sql_2 = "INSERT INTO user2user(user_1, user_2) VALUES (%s, %s), (%s, %s)"
            result2 = db_obj.search(sql_2, (apply_id, current_id, current_id, apply_id))
            db_obj.db_save()
        except Exception as e:
            result1 = None
            result2 = None

        db_obj.search(
            'select user_2, username from user2user left join userinfo on userinfo.uid=user2user.user_2 where user_1=(%s)',
            (current_id,))
        # sq = db_obj.search('SELECT * from user2user, userinfo where user2user.user_2=userinfo.uid')
        friends = db_obj.get_all()
        self.session['user_data']['friends'] = friends

        db_obj.db_close()

        if result1 and result2:
            self.render('index.html',
                        friends=self.session['user_data']['friends'],
                        my_data=self.session['user_data']['data'],
                        add_error='添加成功',
                        apply_data='',
                        group_data=self.session['user_data']['group'],
                        group_member=self.session['user_data']['group_member'],
                        )
        else:
            self.render('index.html',
                        friends=self.session['user_data']['friends'],
                        my_data=self.session['user_data']['data'],
                        add_error='添加失败',
                        apply_data='',
                        group_data=self.session['user_data']['group'],
                        group_member=self.session['user_data']['group_member'],
                        )


class BlockHandler(tornado.web.RequestHandler):
    '''
    处理屏蔽组成员发言权
    '''
    def initialize(self):
        # 钩子函数 首先执行
        class_ = SessionFactory.get_session()
        # 实例化 session 类的对象
        self.session = class_(self)

    def get(self, *args, **kwargs):
        '''
        :param group_id: 组 id
        :param block_id: 被屏蔽者 id
        :param block_status: 当前状态（0：正常，1：屏蔽）
        :return: 
        '''
        group_id = self.get_argument('group_id')
        block_id = self.get_argument('id')
        block_status = self.get_argument('block')
        db_obj = DBController()
        status = 0
        if block_status == '1':
            sql = "UPDATE user2group SET block=0 WHERE user_id=%s"
        else:
            sql = "UPDATE user2group SET block=1 WHERE user_id=%s"
            status = 1
        db_obj.search(sql, (block_id,))
        db_obj.db_save()
        db_obj.db_close()

        # session 中 group_member 需要修改
        if not self.session['user_data']:
            self.render('login.html', msg='请登录')
            return
        for user in self.session['user_data']['group_member'][int(group_id)]['mems']:
            if user['user_id'] == int(block_id):
                user['block'] = status
        self.redirect('/index')


class DelGroupMemHandler(tornado.web.RequestHandler):
    '''
    处理删除组成员
    '''
    def initialize(self):
        # 钩子函数 首先执行
        class_ = SessionFactory.get_session()
        # 实例化 session 类的对象
        self.session = class_(self)

    def get(self, *args, **kwargs):
        user_id = self.get_argument('id')
        group_id = self.get_argument('group_id')

        sql = 'DELETE FROM user2group WHERE user_id=%s AND group_id=%s'
        db_obj = DBController()
        db_obj.search(sql, (user_id, group_id))
        db_obj.db_save()
        db_obj.db_close()

        if not self.session['user_data']:
            self.render('login.html', msg='请登录')
            return
        for user in self.session['user_data']['group_member'][int(group_id)]['mems']:
            if user['user_id'] == int(user_id):
                self.session['user_data']['group_member'][int(group_id)]['mems'].remove(user)
        self.redirect('/index')


class AddGroupMemHandler(tornado.web.RequestHandler):
    '''
    处理添加组成员
    '''
    def initialize(self):
        # 钩子函数 首先执行
        class_ = SessionFactory.get_session()
        # 实例化 session 类的对象
        self.session = class_(self)

    def post(self, *args, **kwargs):

        data = {'status':True, 'msg':'添加成功'}
        gid = self.get_argument('gid')
        username = self.get_argument('username')

        db_obj = DBController()
        sql_1 = 'SELECT uid FROM userinfo WHERE username=%s'
        sql_2 = 'INSERT INTO user2group (user_id, group_id) VALUE (%s, %s)'
        db_obj.search(sql_1, username)
        uid = db_obj.get_one()
        if not uid[0]:
            data = {'status': False, 'msg': '添加失败'}
            self.write(json.dumps(data))
            return
        result = db_obj.search(sql_2, (uid, gid))
        db_obj.db_save()
        db_obj.db_close()
        new_mem_dict  = {
            'block': 0,
            'user_id': uid[0],
            'username': username
        }
        self.session['user_data']['group_member'][int(gid)]['mems'].append(new_mem_dict)
        self.write(json.dumps(data))
