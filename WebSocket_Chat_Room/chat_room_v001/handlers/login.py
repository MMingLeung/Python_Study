#!/usr/bin/env python
#! -*- coding: utf-8 -*-
'''
Handler for login
'''
import tornado.web
from lib.db_controller import DBController
from lib.CUSTOMIZED_SESSION.my_session import SessionFactory


class LoginHandler(tornado.web.RequestHandler):
    def initialize(self):
        # 钩子函数 首先执行
        class_ = SessionFactory.get_session()
        # 实例化 session 类的对象
        self.session = class_(self)

    def get(self, *args, **kwargs):
        self.render('login.html', msg='')

    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')

        db_obj = DBController()
        db_obj.search('SELECT * from userinfo WHERE username=(%s) AND password=(%s)', (username, password,))
        data = db_obj.get_one()
        # sq = db_obj.search('SELECT * from user2user, userinfo where user2user.user_2=userinfo.uid')
        if data:
            # 好友
            db_obj.search(
                'select user_2, username from user2user left join userinfo on userinfo.uid=user2user.user_2 where user_1=(%s)',
                (data[0],))
            friends = db_obj.get_all()
            # 1、查询数据库中，friend_application 表的 user_recv 等于当前 my_nid的数据
            # 2、查询出发送申请的人信息
            # 3、推送到客户端中显示

            # 申请信息
            # SELECT * from friend_application left join userinfo on userinfo.uid = friend_application.user_apply where user_recv = my_nid
            db_obj.db_dict_cur()
            db_obj.search(
                'SELECT * from friend_application '
                    'left join userinfo on userinfo.uid = friend_application.user_apply '
                        'WHERE user_recv=%s AND confirm!=1',
                (data[0],))
            apply_data = db_obj.get_all()

            # 组
            # SELECT * FROM user2group LEFT JOIN user_group ON group_id=user_group.gid WHERE user_id=%s
            db_obj.search(
                'SELECT * FROM user2group LEFT JOIN user_group ON group_id=user_group.gid WHERE user_id=%s',
                (data[0],))
            group_data = db_obj.get_all()

            # 组成员
            # SELECT * FROM user2group LEFT JOIN user_group ON group_id=user_group.gid WHERE user_id=%s',
            db_obj.search(
                '''
                SELECT admin, block, group_id,user_id, userinfo.username FROM user2group 
                  LEFT JOIN userinfo ON userinfo.uid = user2group.user_id 
                    WHERE group_id in (
                      SELECT group_id FROM user2group 
                        LEFT JOIN user_group ON group_id=user_group.gid 
                          WHERE user_id=%s)
                ''',
                (data[0],))

            # 处理组信息
            group_member = db_obj.get_all()
            group_fix_data = {}
            for member in group_member:
                temp_dict = {
                    'user_id': member['user_id'],
                    'username': member['username'],
                    'block': member['block'],
                }
                if member['group_id'] not in group_fix_data.keys():
                    group_fix_data[member['group_id']] = {}
                    group_fix_data[member['group_id']]['admin'] = member['admin']
                    group_fix_data[member['group_id']]['mems'] = []
                    group_fix_data[member['group_id']]['mems'].append(temp_dict)
                else:
                    group_fix_data[member['group_id']]['mems'].append(temp_dict)
            db_obj.db_close()

            self.session['user_data'] = {'data': data, 'friends': friends, 'group': group_data, 'group_member': group_fix_data}
            self.render('index.html',
                        friends=self.session['user_data']['friends'],
                        my_data=self.session['user_data']['data'],
                        add_error="",
                        apply_data=apply_data,
                        group_data=group_data,
                        group_member=group_fix_data,
                        )
        else:
            self.render('login.html', msg='账号或密码错误')
