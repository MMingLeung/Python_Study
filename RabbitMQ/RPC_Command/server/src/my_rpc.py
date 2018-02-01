#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
The class which including create RPC connection ,push message 
and asynchronous wait for the message.
'''
import pika
import uuid


class MyRPCCommand:
    def __init__(self, host):
        '''
        Initializing connection
        :param host: 
        '''
        credential = pika.PlainCredentials('matt', '123')
        parameters = pika.ConnectionParameters(host=host, credentials=credential)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        # 1、声明一个接收结果的队列
        result = self.channel.queue_declare(exclusive=True)
        # 2、获取接收结果的队列
        self.callback_queue = result.method.queue
        self.command = None
        # 3、声明开始消费接收结果的队列
        self.channel.basic_consume(
            self.on_request,
            queue=self.callback_queue,
        )


    def call(self, cmd):
        '''
        push message to queue and waiting for message
        :param cmd: 
        :return: 
        '''
        self.command = cmd
        command = cmd.encode('utf-8')
        self.corr_id = str(uuid.uuid4())
        self.response = None
        # 4、放消息入队列
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue2',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id = self.corr_id,
            ),
            body=command,
        )
        while self.response is None:
            # 检测监听的队列有无新消息
            self.connection.process_data_events()
        return self.response


    def on_request(self, ch, method, props, body):
        '''
        Callback method for receving message 
        :param ch: 
        :param method: 
        :param props: 
        :param body: 
        :return: 
        '''
        if self.corr_id == props.correlation_id:
            result = {
                'command':self.command,
                'task_id':self.corr_id,
                'content':body.decode('utf-8')
            }
            self.response = result






