#!/usr/bin/env python
#! -*- coding: utf-8 -*-
import uuid
import json
import tornado.websocket


class ChatHandler(tornado.websocket.WebSocketHandler):

    # 存放客户端连接对象
    connectors = set()
    # 存放消息
    message = []

    def open(self):
        '''
        成功连接时执行
        :return: 
        '''
        ChatHandler.connectors.add(self)
        # 为每一个客户端赋予 uuid 作为识别符
        uid = str(uuid.uuid4())
        # 发送 uuid
        self.write_message(uid)

        # 为刚连接的客户端发送之前的消息
        for item in ChatHandler.message:
            if not item:
                continue
            content = self.render_string('message.html', **item)
            self.write_message(content)

    def on_message(self, message):
        '''
        收到消息时执行
        :param message: 
        :return: 
        '''
        msg = json.loads(message)
        ChatHandler.message.append(message)

        for client in ChatHandler.connectors:
            content = client.render_string('message.html', **msg)
            client.write_message(content)

    def on_close(self):
        '''
        关闭连接时执行
        :return: 
        '''
        ChatHandler.connectors.remove(self)