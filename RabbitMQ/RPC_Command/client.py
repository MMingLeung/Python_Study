#!/usr/bin/python
# -*- coding: utf-8 -*-
import subprocess
import pika
import time


credentials = pika.PlainCredentials('matt', '123')
parameters = pika.ConnectionParameters(host='127.0.0.1',credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='rpc_queue2')

def run_cmd(cmd):
    cmd_obj = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    result = cmd_obj.stdout.read() + cmd_obj.stderr.read()
    return result


def on_request(ch, method, props, body):
    cmd = body.decode("utf-8")

    print(" [.] run (%s)" % cmd)
    response = run_cmd(cmd)

    # 3、把监听到的消息处理后，放入存放结果的队列
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to, #队列
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=response)

    ch.basic_ack(delivery_tag = method.delivery_tag)

# 1、声明监听消息队列
channel.basic_consume(on_request, queue='rpc_queue2')
print("Waiting RPC requests")
# 2、开始监听
channel.start_consuming()