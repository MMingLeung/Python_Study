#!/usr/bin/env python
#! -*- coding: utf-8 -*-
'''
Handlers for chating both one to one and group
'''
import json
import tornado.websocket


class OneToOneHandler(tornado.websocket.WebSocketHandler):
    # 存放用户连接对象
    connections = []

    # 用户发送的消息
    message = []

    def open(self, *args, **kwargs):
        '''
        :param nid: 对方 id
        :param my_nid: 当前用户 id
        :param my_name: 当前用户名
        :return: 
        '''
        nid = self.get_argument('nid')
        self.my_nid = self.get_argument('mynid')
        my_name = self.get_argument('myname')
        self.write_message(self.my_nid+','+my_name)

        # 封装连接对象和当前用户 id
        my_data_dict = {
            'id': self.my_nid,
            'obj':self,
        }

        OneToOneHandler.connections.append(my_data_dict)

        for item in OneToOneHandler.message:
            data = json.loads(item)
            if not data:
                continue
            # 缓存数据中用户 id 以及接收方 id 与获取的值匹配，进行消息推送
            elif data['uid'] == self.my_nid \
                    and data['to_user_or_group'] == nid \
                        or data['uid'] == nid \
                    and data['to_user_or_group'] == self.my_nid:
                content = self.render_string('message.html', **data)
                self.write_message(content)


    def on_message(self, message):
        '''
        收到消息时执行
        :param message: 用户发送的消息
        :return: 
        '''
        msg = json.loads(message)
        OneToOneHandler.message.append(message)

        for client in OneToOneHandler.connections:
            if self == client['obj'] or msg['to_user_or_group'] == client['id']:
                content = client['obj'].render_string('message.html', **msg)
                client['obj'].write_message(content)

    def on_close(self):
        '''
        关闭连接时执行
        :return: 
        '''
        for item in OneToOneHandler.connections:
            if item['id'] == self.my_nid:
                OneToOneHandler.connections.remove(item)


class GroupHandler(tornado.websocket.WebSocketHandler):

    connections = []

    message = []

    def open(self, *args, **kwargs):
        '''
        
        :param gid: 用户组 id
        :param gname: 用户组名
        :param current_id: 当前用户 id
        :param current_name: 当前用户名
        :return: 
        '''
        self.gid = self.get_argument('gid')
        gname = self.get_argument('gname')
        self.current_id = self.get_argument('mynid')
        current_name = self.get_argument('myname')
        self.write_message(self.current_id+','+ current_name)

        # 封装连接对象、用户 id 、用户组 id
        my_data_dict = {
            'id': self.current_id,
            'obj': self,
            'gid': self.gid,
        }

        GroupHandler.connections.append(my_data_dict)
        for item in GroupHandler.message:
            data = json.loads(item)
            if not data:
                continue
            elif data['to_user_or_group'] == self.gid:
                content = self.render_string('message.html', **data)
                self.write_message(content)

    def on_message(self, message):
        msg = json.loads(message)
        GroupHandler.message.append(message)
        for client in GroupHandler.connections:
            if msg['to_user_or_group'] == client['gid']:
                content = client['obj'].render_string('message.html', **msg)
                client['obj'].write_message(content)

    def on_close(self):
        for item in GroupHandler.connections:
            if item['gid'] == self.gid:
                GroupHandler.connections.remove(item)
