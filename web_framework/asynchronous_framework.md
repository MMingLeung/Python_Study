# Tornado 的异步非阻塞

## 一、异步非阻塞

异步：回调。当 IO 操作有返回值时，通知系统，调用预先设置的回调函数。

<br>

非阻塞：不等待。



## 二、Tornado 异步非阻塞内部运行流程

关键点：

1. @gen.coroutine 
2. Future 对象
3. yield 

<br>

&emsp;&emsp;每一个用户的每一次访问生成一个 Future 对象，封装回调函数、请求相关的操作以及其结果，当 Future 对象调用 set_result() 方法或者获取请求的响应，就会立即调用回调函数，随即返回响应。

<br>

**模拟内部运行：**

````python
import time
import tornado.web

from tornado import gen
from tornado.concurrent import Future
from concurrent.futures import ThreadPoolExecutor


fu = None

def waiting(future):
    time.sleep(5)
    future.set_result(123)

class IndexHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        # 模拟 future
        global fu
        print('开始模拟')
        fu = Future()
        # 设置回调函数
        fu.add_done_callback(self.doing)
		
		# 建立线程，模拟用户请求的操作
        pool = ThreadPoolExecutor(5)
        pool.submit(waiting, fu)
        yield fu

    def done(self, response):
        print(response)
        self.write('成功')
        self.finish()

application = tornado.web.Application([
    (r'/index', IndexHandler),
])

if __name__ == '__main__':
    # 单进程
    application.listen(8880)
    tornado.ioloop.IOLoop.instance().start()

````

<br>

**异步处理连接、查询Mysql数据库：**

````python
import tornado
import tornado_mysql
from tornado import web, gen

@gen.coroutine
def search(username, password):
    conn = yield tornado_mysql.connect(host='127.0.0.1', user='root', password='', db='db_name')
    cur = conn.cursor()
    yield cur.execute('SELECT username, password FROM user WHERE username=(%s) AND password=(%s)', (username, password,))
    data = cur.fetchone()
    cur.close()
    conn.close()
    raise gen.Return(data)

class LoginHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render('login.html')

    @gen.coroutine
    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')

        data = yield gen.Task(search, username, password)
        if data:
            print(data)
        else:
            print('username or password error')

application = web.Application([
    (r'/login', LoginHandler),
])

if __name__ == '__main__':
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

````



## 三、利用 IO 多路复用实现异步非阻塞 WEB 框架



### 流程图

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/asynchronous_non_blocking_framework.png?raw=true)

<br>

### 代码

````Python
import select
import socket
import re


class Future(object):
    '''
    Future 是异步操作中的对象，封装回调函数、状态、请求的url
    
    --------------------------------------------------------------------------------------
    
    当 _ready 为 True 时，程序立即调用 Future 对象中的回调函数，返回结果给客户端
    '''
    def __init__(self, callback, url='http://www.baidu.com'):
        self._ready = False
        self.callback = callback
        self.value = None
        self.url = url


    def set_result(self, value=None):
        self.value = value
        self._ready = True

    @property
    def ready(self):
        return self._ready


class HttpResponse(object):
    '''
    封装响应信息
    '''
    def __init__(self, content=None):
        self.content = content
        self.headers = {}
        self.cookie = {}

    def response(self):
        if isinstance(self.content, bytes):
            return self.content
        else:
            return self.content.encode('utf-8')


class HttpRequest(object):
    '''
    封装请求信息
    '''
    def __init__(self, conn):
        self.conn = conn
        self.header_bytes = bytes()
        self.header_dict = {}
        self.body_bytes = bytes()

        self.method = ""
        self.protocol = ""
        self.url = ""

        self.initial()
        self.initial_header()

    def initial(self):
        '''
        接收请求内容并分割请求头、请求体
        :return: 
        '''
        flag = False
        while True:
            try:
                receive = self.conn.recv(8096)
            except Exception as e:
                receive = None
            if not receive:
                break
            if flag:
                self.body_bytes += receive
                continue
            temp = receive.split(b'\r\n\r\n', 1)
            if len(temp) == 1:
                self.header_bytes += temp
            else:
                h, b = temp
                self.header_bytes += h
                self.body_bytes += b
                flag = True


    def initial_header(self):
        '''
        分割请求头中请求方式、url、协议版本
        :return: 
        '''
        header_list = self.headers_str.split('\r\n')
        first_line = header_list[0].split(' ')
        if len(first_line) == 3:
            self.method, self.url, self.protocol = header_list[0].split(' ')


    @property
    def headers_str(self):
        return self.header_bytes.decode('utf-8')


class HttpNotFund(HttpResponse):
    def __init__(self, content=''):
        self.content = content
        super(HttpNotFund, self).__init__(self.content)


class ClientRequest(object):
    def __init__(self, future):
        '''
        封装客户端发送的请求信息，由服务端建立 socket 对象并转发
        :param future: 
        '''
        self.sock = socket.socket()
        self.url = future.url
        self.header = 'GET / HTTP/1.1\r\nHost:{url}\r\n\r\n'

        self.connect()

    def send_request(self):
        self.msg = self.header.format(url=self.url).encode('utf-8')
        self.sock.send(self.msg)

    def connect(self):
        try:
            conn = self.sock.connect((self.url, 80))
        except Exception as e:
            raise Exception('conn is None')
        return conn


class CaroPig(object):
    def __init__(self, routes, host='127.0.0.1', port=8080):
        '''
        异步非阻塞框架主逻辑
        :param routes: 自定义路由系统
        :param host: 主机名
        :param port: 端口号
        '''
        self.host = host
        self.port = port
        self.async_dict = {}
        self.socket_list = set()
        self.routes = routes
        self.request = None
        self.client_request = None

    def run(self):
        '''
        使用 IO 多路复用监听有变化的 socket 对象，如果是客户端创建连接的 socket 加入监听集合中。
        
        ---------------------------------------------------------------------------------- 
        
        当监听到 socket 对象发送请求，使用 process() 方法处理，封装到 HttpRequest 对象中，
        进行路由匹配，返回对应对象。
        
        ----------------------------------------------------------------------------------
        
        对象有以下类型：
        1、 HttpResponse 对象：直接返回给客户端
        2、 Future 对象：从生成器中取出该对象，封装到 ClientRequest，根据 Future 对象中的 url 发送
                        请求。
                        监听 Future 对象 _ready 是否有变化（代表发送的请求是否成功接收到返回值），
                        调用回调函数。
        
        :return: 
        '''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen(5)

        self.socket_list.add(sock)

        while True:
            rlist, wlist, elist = select.select(self.socket_list, [], self.socket_list, 0.005)

            for conn in rlist:
                if conn == sock:
                    client, address = conn.accept()
                    client.setblocking(False)
                    self.socket_list.add(client)
                else:
                    gen = self.process(conn)
                    if isinstance(gen, HttpResponse):
                        conn.send(b'HTTP/1.1 200 OK\r\n\r\n')
                        conn.sendall(gen.response())
                        self.socket_list.remove(conn)
                        conn.close()
                    elif gen == 'ok':
                        if self.async_dict:
                            list(self.async_dict.values())[0].set_result('received')
                        break
                    else:
                        yield_data = next(gen)
                        self.async_dict[conn] = yield_data
                        if yield_data.url:
                            self.client_request = ClientRequest(yield_data)
                            self.socket_list.add(self.client_request.sock)
                            self.client_request.send_request()
            self.polling_callback()

    def polling_callback(self):
        for conn in list(self.async_dict.keys()):
            yield_data = self.async_dict[conn]
            if not yield_data.ready:
                continue
            if yield_data.callback:
                result = yield_data.callback(self.request, yield_data)
                conn.send(b'HTTP/1.1 200 OK\r\n\r\n')
                conn.sendall(result.response())
            self.socket_list.remove(conn)
            del self.async_dict[conn]
            conn.close()


    def process(self, conn):
        self.request = HttpRequest(conn)
        func = None

        # 判断 Future 对象发送的请求是否成功访问
        if not re.match(r'\/\w+$',self.request.url):
            return 'ok'

        # 无 url
        elif not self.request.url:
            return HttpNotFund('404 not found')

        # 路由匹配
        for route in self.routes:
            if re.match(route[0], self.request.url):
                func = route[1]
                break

        if not func:
            return HttpNotFund('404 not found')
        else:
            return func(self.request)


# ################################# 自定义视图函数与路由系统 #################################

def index(request):
    return HttpResponse('ok')


def callback(request, future):
    return HttpResponse(future.value)

request_list = []

def req(request):
    fu = Future(callback, url='www.baidu.com')
    request_list.append(fu)
    yield fu

def stop(request):
    obj = request_list[0]
    del request_list[0]
    obj.set_result('ok')
    return HttpResponse('ok')

routes = [
    (r'/index', index),
    (r'/req', req),
    (r'/stop', stop),
]


if __name__ == '__main__':
    car = CaroPig(routes)
    car.run()

````

