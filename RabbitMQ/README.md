# RabbitMQ 

## 一、简介

作用：1、存储消息

​	    2、保证消息的顺序

 	    3、保证数据的交付

<br>

解决：1、解耦

​            2、异步（排队问题、不能确保任务被及时执行）

<br>

## 二、安装

mac：brew install rabbitmq

<br>

添加环境变量：~/.bash_profile

<br>

## 三、命令

#### 启动：rabbitmq-server

<br>

#### 查看队列：rabbitmqctl listqueue

<br>

#### 添加用户：rabbitmqctl add_user username password

<br>

#### 授权：rabbitmqctl set_permission -p / username ".\*"  ".\*" ".\*"



## 四、生产者/消费者

#### 1、简单使用

````python
# ############################### producer ##############################
import pika


# 授权
credentials = pika.PlainCredentials('matt', '123')
# 绑定 IP、PORT 等参数
parameters = pika.ConnectionParameters(host='127.0.0.1', credentials=credentials)
# 创建连接
connection = pika.BlockingConnection(parameters)
# 创建频道
channel = connection.channel()
# 声明队列
channel.queue_declare(queue='q1')

channel.basic_publish(
    exchange='', # 过滤
    routing_key='q1', # 路由: 告诉 exchange 把 body 转到 q1 队列
    body='Hello World!' # 消息
)
channel.close()
````

<br>

````python
# ############################### consumer ##############################
import pika


# 授权
credentials = pika.PlainCredentials('matt', '123')
# IP、PORT 等参数
parameters = pika.ConnectionParameters(host='127.0.0.1', credentials=credentials)
# 创建连接的对象
connection = pika.BlockingConnection(parameters)
# 创建频道
channel = connection.channel()

# 获取消息时调用的回调函数
def callback(ch, method, properties, body):
    print('c1 Recevied %s' % body)
    print('method: %s' % method )
    channel.basic_ack(delivery_tag=method.delivery_tag)

# 公平分发：消费完再取消息
channel.basic_qos(prefetch_count=1)

channel.basic_consume(
    callback,
    queue='q2',
)
print('wating for message c1')
channel.start_consuming() # 阻塞
````

<br>

#### 2、消息持久化

解决消费者获取消息后，在处理时故障，导致消息丢失情况

````python
# ############################### producer ##############################
import pika


credentials = pika.PlainCredentials('matt', '123')
parameters = pika.ConnectionParameters(host='127.0.0.1', credentials=credentials)
connect = pika.BlockingConnection(parameters)
channel = connect.channel()
channel.queue_declare(queue='q1')

channel.basic_publish(
    exchange='', 
    routing_key='q1',
    body='Hello World!',
    properties=pika.BasicProperties(
        delivery_mode=2, # 消息持久化
    ),
)
channel.close()
````

<br>

````python
# ############################### consumer ##############################
import pika
import time


credentials = pika.PlainCredentials('matt', '123')
parameters = pika.ConnectionParameters(host='127.0.0.1', credentials=credentials)
connect = pika.BlockingConnection(parameters)
channel = connect.channel()


def callback(ch, method, properties, body):
   	# 通知生产者消息已处理
    channel.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)

channel.basic_consume(
    callback,
    queue='q2',
    # no_ack=True # 注释了代表消息处理完毕需要和服务器确认
)
channel.start_consuming() # 阻塞
````

<br>

#### 3、队列持久化

解决生产者发生故障导致队列中消息丢失（需配合消息持久化使用）

````python
# ############################### producer ##############################
import pika


credentials = pika.PlainCredentials('matt', '123')
parameters = pika.ConnectionParameters(host='127.0.0.1', credentials=credentials)
connect = pika.BlockingConnection(parameters)
channel = connect.channel()

channel.queue_declare(queue='q2', durable=True) # 队列持久化，必须队列初识时声明

channel.basic_publish(
    exchange='', 
    routing_key='q2', 
    properties=pika.BasicProperties(
        delivery_mode=2, # 消息持久化
    ),
    body='Hello World!', # 消息
)

channel.close()
````



#### 4、消息广播

exchange: 

fanout 广播

direct 组播

topic 话题

rpc 

<br>

##### 广播：>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

`````python
# ############################### producer ##############################
import sys
import pika


credentials = pika.PlainCredentials('matt', '123')
parameters = pika.ConnectionParameters(host='127.0.0.1', credentials=credentials)
connect = pika.BlockingConnection(parameters)
channel = connect.channel()

# 广播模式
# 1、队列绑定 exchange
channel.exchange_declare(
    exchange='logs',
    exchange_type='fanout',
)
# 2、可接受参数，参数作为消息内容
message = ' '.join(sys.argv[1:]) or 'Hello !'

# 3、exchange='logs'
#   routing_key 不需要填写
channel.basic_publish(
    exchange='logs', 
    routing_key='',
    properties=pika.BasicProperties(
        delivery_mode=2,
    ),
    body=message,
)

channel.close()
`````

<br>

````python
# ############################### consumer ##############################
import pika
import time


credentials = pika.PlainCredentials('matt', '123')
parameters = pika.ConnectionParameters(host='127.0.0.1', credentials=credentials)
connect = pika.BlockingConnection(parameters)
channel = connect.channel()


def callback(ch, method, properties, body):
    # time.sleep(20)
    print('c1 Recevied %s' % body)
    print('method: %s' % method )
    channel.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)

# 声明队列，防止服务器没有启动时的报错
channel.exchange_declare(
    exchange='logs',
    exchange_type='fanout'
)

# 1、不指定队列
result = channel.queue_declare(exclusive=True) 
# 2、获取队列名
queue_name = result.method.queue
# 3、绑定广播和队列的名称
channel.queue_bind(
    exchange='logs',
    queue=queue_name
)
# 4、声明回调函数和队列
channel.basic_consume(
    callback,
    queue=queue_name,
)
# 5、开始消费（阻塞）
channel.start_consuming() 
````

<br>

#####  组播：>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

````python
# ############################### producer ##############################
import pika
import sys


credentials = pika.PlainCredentials('matt', '123')
parameters = pika.ConnectionParameters(host='127.0.0.1', credentials=credentials)
connect = pika.BlockingConnection(parameters)
channel = connect.channel()

channel.exchange_declare(
    exchange='direct_logs',
    exchange_type='direct',
)

serverity = sys.argv[1] if len(sys.argv) > 1 else 'warning'

channel.basic_publish(
    exchange='direct_logs', 
    routing_key=serverity,
    properties=pika.BasicProperties(
        delivery_mode=2, 
    ),
    body='Hello World direct!', 
)
channel.close()
````

<br>

`````python
# ############################### consumer ##############################
import pika
import time
import sys


credentials = pika.PlainCredentials('matt', '123')
parameters = pika.ConnectionParameters(host='127.0.0.1', credentials=credentials)
connect = pika.BlockingConnection(parameters)
channel = connect.channel()


def callback(ch, method, properties, body):
    print('c1 Recevied %s' % body)
    print('method: %s' % method )
    channel.basic_ack(delivery_tag=method.delivery_tag)

# 公平分发 消费完再取
channel.basic_qos(prefetch_count=1)

# 防止生产者没有启动而报错
channel.exchange_declare(
    exchange='direct_logs',
    exchange_type='direct'
)

# 1、不指定队列
result = channel.queue_declare(exclusive=True) 
# 2、获取队列名
queue_name = result.method.queue
# 3、接收参数，代表不同的组
log_level = sys.argv[1:] # info warning error
if not log_level:
    log_level = ['info', 'warning']

# 绑定组
for level in log_level:
    channel.queue_bind(
        exchange='direct_logs',
        routing_key=level,
        queue=queue_name,
    )

channel.basic_consume(
    callback,
    queue=queue_name,
)
channel.start_consuming() 
`````

<br>

#### 话题：>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

`````python
# ############################### producer ##############################
import pika
import sys


credentials = pika.PlainCredentials('matt', '123')
parameters = pika.ConnectionParameters(host='127.0.0.1', credentials=credentials)
connect = pika.BlockingConnection(parameters)
channel = connect.channel()

# 1、声明队列
channel.exchange_declare(
    exchange='topic_logs',
    exchange_type='topic',
)

# 2、接收参数，以'.'分割，识别话题
# '#' 代表接收全部
serverity = sys.argv[1] if len(sys.argv) > 1 else 'aaaaa.info'

# 3、放入消息
channel.basic_publish(
    exchange='topic_logs', # 过滤
    routing_key=serverity,
    properties=pika.BasicProperties(
        delivery_mode=2, # 持久化
    ),
    body='Hello World direct!', # 消息
)

channel.close()
`````

<br>

````python
# ############################### consumer ##############################
import pika
import time
import sys


credentials = pika.PlainCredentials('matt', '123')
parameters = pika.ConnectionParameters(host='127.0.0.1', credentials=credentials)
connect = pika.BlockingConnection(parameters)
channel = connect.channel()


def callback(ch, method, properties, body):
    channel.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
# 1、声明
channel.exchange_declare(
    exchange='topic_logs',
    exchange_type='topic'
)
# 2、声明不指定队列
result = channel.queue_declare(exclusive=True) 
# 3、获取队列名
queue_name = result.method.queue
# 4、接收参数，作为监听的话题
log_level = sys.argv[1:] # info warning error
if not log_level:
    log_level = ['aaaaa.info']

# 5、绑定话题
channel.queue_bind(
    exchange='topic_logs',
    routing_key='*.info',
    queue=queue_name,
)
# 6、声明回调函数和队列
channel.basic_consume(
    callback,
    queue=queue_name,
)

channel.start_consuming() 
````

<br>

####  RPC：>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

&emsp;&emsp;服务端既是生产者也是消费者，通过唯一标识区分信息及其返回结果，使用 reply_to 队列返回结果给客户端

`````Python
# ############################### producer ##############################
'''
求斐波那契数列
1、定义 fib 函数
2、声明接收命令的队列
3、监听队列，收到消息后调用 fib 函数
4、fib 执行的结果发送回客户端制定的 reply_to 队列
'''
import pika
import time


credentials = pika.PlainCredentials('matt', '123')
parameters = pika.ConnectionParameters(host='127.0.0.1', credentials=credentials)
connect = pika.BlockingConnection(parameters)

channel = connect.channel()
# 1、声明队列
channel.queue_declare(queue='rpc_queue')

# 2、斐波那契函数
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

# 3、回调函数
def on_request(ch, method, props, body):
    n = int(body)
    print('开始执行 fib 函数')
    response = fib(n)
	
    ch.basic_publish(
        exchange='',
      	# 4、存放结果的队列
        routing_key=props.reply_to,
        # 5、唯一标识
        properties=pika.BasicProperties(
            correlation_id=props.correlation_id
        ),
        body=str(response)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
# 4、绑定回调函数和队列
channel.basic_consume(on_request, queue='rpc_queue')
# 5、开始消费
channel.start_consuming()
`````

<br>

````Python
# ############################### consumer ##############################
'''
1. 声明一个队列，作为reply_to返回消息结果的队列
2. 发送消息到 task 队列中，消息带有唯一标识符uid,reply_to
3. 监听 reply_to 的队列，指导有结果
'''
import pika
import uuid


class FibonacciRpcClient(object):
    def __init__(self):
        '''
        连接队列相关
        '''
        credentials = pika.PlainCredentials('matt', '123')
        parameters = pika.ConnectionParameters(host='127.0.0.1', credentials=credentials)
        self.connect = pika.BlockingConnection(parameters)
        self.channel = self.connect.channel()
        result = self.channel.queue_declare(exclusive=True)

        self.callback_queue = result.method.queue

        # 1、声明监听 callback_queue
        self.channel.basic_consume(
            self.on_response,
            no_ack=True,
            queue=self.callback_queue,
        )
	
    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        # 2、把消息放入队列
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n)
        )
        # 3、异步监听
        while self.response is None:
            # 检测监听的队列有无新消息
            self.connect.process_data_events()
        return int(self.response)

    def on_response(self, ch, method, props, body):
        '''
        收到服务器端命令结果后执行的回调函数
        :param ch: 
        :param method: 
        :param props: 
        :param body: 
        :return: 
        '''
        if self.corr_id == props.correlation_id:
            self.response = body


fibonacci_rpc = FibonacciRpcClient()
print('输入 30')
response = fibonacci_rpc.call(30)
print(response)
````

