# 网络编程与线、进程

## 一、套接字 SOCKET 简介

基本概念：起始是用于两个不同进程间的通信，后来发展到网络通信。核心是基于文件类型或者网络类型通信。

<br>

地址家族：

1. AF_UNIX：基于文件通信
2. AF_INET：基于网络通信



## 二、TCP/IP 架构中的 SOCKET

### 基本概念：位于传输层与应用层之间的虚拟层，向用户提供一组接口，向下封装全部网络协议。

<br>

### 基于 TCP 协议的套接字简单应用

````Python
# ####################### server #######################
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket


# AF_INET: 基于网络
# SOCK_STREAM: 基于"流"，即 TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ip 重用
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(('127.0.0.1', 8080))

# 连接池，暂存连接
s.listen(5)

while True:
    # 连接对象和地址
    conn, addr = s.accept()

    while True:
        try:
        	# 异常处理
            # 收1024个字节
            data = conn.recv(1024)
            # linux 系统需要加此操作
            if not data:
                break
            print(data)
       	    # 发
            inp = input('>>: ')
            if not inp:
                continue
            conn.send(inp.encode('utf-8'))
        except Exception as e:
            break
    # 关
    conn.close()
s.close()
````

<br>

````Python
# ####################### client #######################
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('127.0.0.1', 8080))

while True:
    inp = input('>>: ')
    if not inp:
        continue
    s.send(inp.encode('utf-8'))
    data = s.recv(1024)
    print(data)
s.close()
````

<br>

### 收发过程

#### 发送

客户端程序 ——> 发送消息  ——> 系统（缓存）  

（用户态 ——> 发送系统调用  ——> 内核态 ）

​	——> 

系统通过 TCP/IP 协议把数据封包并转换成电信号  ——> 网卡 ——> 目标服务器           

<br>

#### 接收

服务器程序 ——> 接收消息 ——> 系统（缓存）

（用户态 ——> 发送系统调用  ——> 内核态 )

​    ——>

阻塞等待缓存中的数据 ——> 系统通过 TCP/IP 协议把电信号转换成数据包 ——> 交给服务端程序

（内核态 ——> 发送系统调用  ——> 用户态 )

<br>

### TCP 粘包问题

TCP 协议是面向连接、面向流的，内部针对数据量少且间隔时间短的消息会进行打包发送，造成粘包情况。

<br>

#### 解决方法：自定义报头

````python
# ####################### server #######################
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
import subprocess
import struct
import json

# AF_INET: 基于网络
# SOCK_STREAM: 基于"流"，即 TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ip 重用
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind(('127.0.0.1', 8080))

# 连接池，暂存连接
s.listen(5)

while True:
    # 连接对象和地址
    conn, addr = s.accept()

    while True:
        try:
        # 异常处理
            # 收1024个字节
            command = conn.recv(1024).decode('utf-8')
            # linux 系统需要加此操作
            if not command:
                break
            print(command)
            res = subprocess.run(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        # 发
            data_len = len(res.stdout) + len(res.stderr)

            data_dict = {'data_size': data_len}
            data_json_dict = json.dumps(data_dict)
            data_json_dict_b = data_json_dict.encode('utf-8')


            # 发报头长度
            pack_len = len(data_json_dict_b)
            data_len_pack = struct.pack('i', pack_len)
            conn.send(data_len_pack)

            # 发报头
            conn.send(data_json_dict_b)

            # 发数据
            conn.send(data_len_pack)

            conn.send(res.stdout)
            conn.send(res.stderr)
        except Exception as e:
            break
    # 关
    conn.close()
s.close()
````

<br>

````python
# ####################### client #######################
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket
import struct
import json


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('127.0.0.1', 8080))

while True:
    inp = input('>>: ')
    if not inp:
        continue
    s.send(inp.encode('utf-8'))
    # 收报头长度
    data_len_pack = s.recv(4)
    pack_len = struct.unpack('i', data_len_pack)

    # 收报头
    data_json_dict_b = s.recv(pack_len[0])

    # 解码、反序列化
    data_json_dict = data_json_dict_b.decode('utf-8')
    data_dict = json.loads(data_json_dict)

    # 获取字典中的数据长度
    data_len = data_dict['data_size']

    recv_data = b''
    recv_len = 0
    while recv_len < data_len:
        data = s.recv(1024)
        recv_len += len(data)
        recv_data += data
    print(recv_data.decode('utf-8'))

    # 异常处理


s.close()

````

<br>

### socketserver 模块实现并发

````Python
# ####################### server #######################
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socketserver


class MyServer(socketserver.BaseRequestHandler):
    def handle(self):
        # 通信循环
        while True:
            print(self.request.recv(1024))


if __name__ == '__main__':
    # 多线程 TCPServer
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 9000), MyServer)
    # 链接循环，循环提供服务
    server.serve_forever()
````

<br>

> 源码跟踪：
>
> 1. server = socketserver.ThreadingTCPServer(('127.0.0.1', 9000), MyServer) 实例化一个ThreadingTCPServer 的对象，该类继承 ThreadingMixIn, TCPServer，本质调用 TCPServer 的构造方法。
>
> 2. 在 TCPServer 构造方法中调用 BaseServer 的构造方法，把传入的 ip 端口号已经自定义的类传入对象的变量中。
>
> 3. ```
>    self.server_bind()
>    self.server_activate()
>    # 绑定 ip 端口号以及监听
>    ```
>
> 4. 执行 serve_forever 方法，内部是调用 IO 多路复用相关的方法，然后执行 _handle_request_noblock
>
> 5. 获取客户端的 conn 和 address
>
> 6. 执行 process_request 方法，内部其实是执行 finish_request 方法
>
> 7. 最后实例化自己定义的类（继承 BaseRequestHandler）
>
> 8. 执行 BaseRequestHandler 的构造方法，在其中执行 handle 方法

<br>

## 三、线程与进程

进程：一个程序在一个数据集上的一次动态执行过程

````
multiprocessing 模块与 threading 公用一套 API
````

<br>

线程：最小执行单位

````python
# ################## threading ##################
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import threading
import time


def listen():
    print('开始听')
    time.sleep(3)
    print('结束听')


def play():
    print('开始玩')
    time.sleep(3)
    print('结束玩')

t = time.time()
t1 = threading.Thread(target=listen, args=())
t2 = threading.Thread(target=play, args=())

t1.start()
t2.start()

# 等待 t1 t2 完成执行
t1.join()
t2.join()

print(time.time() - t)

# 主线程开线程
# 两个子线程
# 并发执行两个子线程
````

<br>

协程：轻量级的线程，由用户自己决定程序何时进行切换，没有操作系统级别的切换更加节省资源

````PYTHON
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time

def producer(c):
    next(c)
    num = 0
    while num < 4:
        num += 1
        print('produce %s' % num)
        time.sleep(1)
        cr = c.send(num)
        print(cr)
    print('produce finished')
    c.close()

def consumer():
    r = ''
    while True:
        data = yield r
        if not data:
            print('no data')
            return
        print('consume %s' % data)
        time.sleep(1)
        r = '200 OK'


c = consumer()
producer(c)
````



<br>

并发：单个进程执行多项任务，同一时刻只有一个任务在执行

<br>

并行：多个进程同时执行多项任务

<br>

同步：线/进程涉及 IO 操作时，直到收到数据才往下执行程序

<br>

异步：线/进程涉及 IO 操作时，不管是否收到数据都往下执行程序，直到收到系统通知，才回头处理数据

<br>

## 四、GIL 锁

全局解释器锁：在 cpython 的解释器中有一把锁，作用是只允许同一个进程在同一时刻只能有一个线程在运行



## 五、互斥锁、死锁、递归锁

#### 互斥锁：多线程执行时，通过加锁行为保护数据的安全问题

<br>

````Python
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import threading
import time


def subnum():
    global num
    # 加锁
    lock.acquire()
    temp = num
    time.sleep(0.01)
    num = temp - 1
    # 释放锁
    lock.release()

num = 100

now_time = time.time()
print(now_time)

lock = threading.Lock()

for i in range(100):
    t = threading.Thread(target=subnum)
    t.run()

print(num)
print(time.time() - now_time)
````

<br>

#### 死锁：当多个线程运行中，锁的增加与释放产生冲突，使得程序卡死

````python
#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
执行流程: 
线程1: 执行 fun1 获取 A 锁、B 锁
	  执行 fun2 获取 B 锁，通过 sleep 模拟发生 I/O 操作
线程2: 执行 fun1 获取 A 锁
线程1: fun2 无法获取 A 锁
线程2: fun1 无法获取 B 锁
程序无法继续执行
'''
import threading
import time


lock_A = threading.Lock()
lock_B = threading.Lock()

class MyTH(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.fun1()
        self.fun2()

    def fun1(self):
        lock_A.acquire()
        print('A', self.name, time.time())
        lock_B.acquire()
        print('B', self.name, time.time())

        lock_B.release()

        lock_A.release()

    def fun2(self):
        lock_B.acquire()
        print('B', self.name, time.time())
        time.sleep(0.2)
        lock_A.acquire()
        print('A', self.name, time.time())
        lock_A.release()
        lock_B.release()

if __name__ == '__main__':
    for i in range(0, 10):
        tmp = MyTH()
        tmp.start()
````

<br>

#### 递归锁 Rlock

<br>

#### Event 对象：锁的标志位，set 方法让线程阻塞， isSet 方法让程序继续运行

````Python
#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
通过线程3把 event 对象设置成 true,让其他线程继续执行
可用于访问数据库的程序中
'''
import threading

def connect(event):
    print('begin to connect..')
    while not event.isSet():
        print('waiting..')
    print('finish')

lock_event = threading.Event()

def connect_signal(event):
    event.set()
    print('connect success')

if __name__ == '__main__':
    t1 = threading.Thread(target=connect, args=(lock_event,))
    t2 = threading.Thread(target=connect, args=(lock_event,))
    t1.start()
    t2.start()
    t3 = threading.Thread(target=connect_signal, args=(lock_event,))
    t3.start()
````

<br>

## 六、I/O 模型

#### 1、阻塞 IO

全程阻塞

![](http://hi.csdn.net/attachment/201007/31/0_1280550787I2K8.gif)

> 过程：
>
> 1、用户态的应用程序发起系统调用，需要获取某些数据
>
> 2、系统从用户态切换到内核态，等待数据到来
>
> 3、数据从硬件设备获取，复制到内核态的内存空间
>
> 4、把数据返回给应用程序，此时系统从内核态切换到用户态

<br>

#### 2、非阻塞 IO

等待数据过程不阻塞，复制数据过程阻塞

![](http://hi.csdn.net/attachment/201007/31/0_128055089469yL.gif)

>过程：
>
>1、用户态的应用程序发起系统调用，需要获取某些数据
>2、系统从用户态切换到内核态，发现数据未到来，立即返回，又切换到用户态
>
>3、用户态应用程序继续往下执行
>
>4、用户态的应用程序继续发起系统调用，需要获取某些数据，系统从用户态切换到内核态，发现数据到来
>
>6、数据从硬件设备获取，复制到内核态的内存空间
>
>7、把数据返回给应用程序，此时系统从内核态切换到用户态

<br>

#### 3、IO多路复用

进程全程阻塞，通过 select 对象监听链接的变化，通知系统获取数据

![](http://hi.csdn.net/attachment/201007/31/0_1280551028YEeQ.gif)

>过程：
>
>1、通过 select 对象发起系统调用，监听数据是否到来。此时是用户态切换到内核态。
>
>2、内核从硬件中获取到数据，返回信号给 select 对象
>
>3、应用程序从 select 对象中获取数据以到来的信号，就发起系统调用
>
>4、系统把数据复制到内核态的内存空间
>
>5、返回给用户态的应用程序

<br>

````Python
# ################## select ##################
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import select 
import socket


s = socket.socket()
s.setblocking(False)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 8080))
s.listen(5)
while True:
    r, w, e = select.select([s,], [], [])
    while True:
        for i in r:
            conn, addr = i.accept()
            data = conn.recv(1024)
            if data:
                print(data)
            conn.send(b'hello')

````

<br>

````Python
# ################## selectors ##################
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import selectors 
import socket


s = socket.socket()
s.setblocking(False)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 8080))
s.listen(5)

sel = selectors.DefaultSelector()

def accept(sock, mask):
    print('accept func')
    print(sock, mask)
    conn, addr = sock.accept()
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    data = conn.recv(1024)
    print(data)
    print('send msg')
    conn.send(b'hello')

sel.register(s, selectors.EVENT_READ, accept)

while True:
    events = sel.select()

    for key, mask in events:
        print(key.fileobj, type(key.fileobj))
        if key.fileobj == s:
            key.data(key.fileobj, mask)
        else:
            key.data(key.fileobj, mask)
            break
````



