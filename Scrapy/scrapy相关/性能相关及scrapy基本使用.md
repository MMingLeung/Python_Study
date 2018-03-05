# 爬虫性能相关及基本使用

## 一、进程

一个程序在一个数据集上的一次动态执行的过程，也可以说是一个容器。



## 二、线程

可以说是轻量级的进程，是一个程序执行的最小单元。同一进程内的线程共享相同的资源，减少进程与进程之间的开销，提高并发性能。



## 三、并行和并发

并行：计算机系统内可以同时执行多个处理的一种计算方法。



并发：一个时间段中，有几个程序处于由启动到结束之间的过程，而且任何时刻只有一个程序运行在同一个CPU上。



串行：一个程序运行结束后，再执行另外一个程序。



## 四、同步与异步

同步：指一个进程在执行某个请求的时候，如果该请求需要一段时间才返回信息，那么该进程就一直等待，直到受到消息才执行下去。



异步：进程发送请求后不需要一直等待，可以继续执行下面的操作，当有消息返回时系统会通知进程进行处理。



## 五、IO模型

同步（synchronous） IO

异步（asynchronous） IO

阻塞（blocking） IO

非阻塞（non-blocking）IO

— 

对于网络IO，牵涉到两个系统对象，一个是调用IO的进程或线程，另一个是系统内核。

当发生read操作的时候经历：

1. 等待数据准备
2. 将数据从内核复制到进程中

—  

阻塞（blocking） IO：

用户进程发生系统调用时，内核态开始第一个阶段，准备数据。对于网络IO来说，需要等待数据到达，用户进程会进入阻塞，直到数据从内核态复制到内存，内核才返回结果，用户进程才解除阻塞。



非阻塞（non-blocking）IO：

用户进程发出系统调用，如果内核未准备好数据，将不会阻塞用户进程，而是返回error。用户进程继续发送系统调用，直到内核把数据准备好，复制到用户内存返回信息（此过程是阻塞）。

优点：可以在等待任务完成的时间可以处理其它任务。

缺点：轮询发送请求之间，任务可能完成，任务完成的响应延迟增大。



IO多路复用：

单个进程处理多个网络连接的IO。select/poll/epoll会不断轮询所有的socket，当某个socket有数据到达，就通知用户进程。

1. 用户调用select， 整个进程会阻塞，同时内核会轮询检测所有的socket
2. 当任何一个socket有数据到达，就会返回通知给用户进程。
3. 用户进程发起系统调用，把数据从内核复制到用户进程



## 六、实现

### 一、串行

````Python
url_list = [
    'www.baidu.com',
    'www.cnblogs.com',
]

# 1.串行
import requests
for url in url_list:
    response = requests.get(url)
    print(response.content)
````



### 二、多线程／进程

````Python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

url_list = [
    'www.baidu.com',
    'www.cnblogs.com',
]

def task(url):
    res = requests.get(url)
    print(res.content)

# 创建线程池
pool = ThreadPoolExecutor(10)
# 进程池
# pool = ProcessPoolExecutor(10)

for url in url_list:
    pool.submit(task, url) # 线程池中获取线程，执行task函数
pool.shutdown(wait=True) # 等待线程执行完毕才往下执行
````







### 三、异步非阻塞

#### 1、asyncio

````Python
import asyncio



@asyncio.coroutine
def fetch_async(host, url='/'):
    print(host, url)
    # 1.连接不等待
    reader, writer = yield from asyncio.open_connection(host, 80)
    
	# #### 相当于回调函数 ####
    request_header_content = """GET %s HTTP/1.0\r\nHost: %s\r\n\r\n""" % (url, host,)
    request_header_content = bytes(request_header_content, encoding='utf-8')
    writer.write(request_header_content)
    ########################
    
    # 2.发送请求不等待
    yield from writer.drain()
    # 3.获取返回消息不等待
    text = yield from reader.read()
    
    # #### 相当于回调函数 ####
    print(host, url, text)
    writer.close()
    ########################

tasks = [
    fetch_async('www.cnblogs.com', '/'),
    fetch_async('dig.chouti.com', '/')
]

# 创建对象
loop = asyncio.get_event_loop()
# 传入任务
results = loop.run_until_complete(asyncio.gather(*tasks))
# 关闭
loop.close()
````



asyncio + aiohttp(进一步封装asynico)

````python
import aiohttp
import asyncio


@asyncio.coroutine
def fetch_async(url):
    print(url)
    response = yield from aiohttp.request('GET', url)
    # data = yield from response.read()
    # print(url, data)
    print(url, response)
    response.close()


tasks = [fetch_async('http://www.baidu.com/'), fetch_async('http://www.sina.com.cn/')]

event_loop = asyncio.get_event_loop()
results = event_loop.run_until_complete(asyncio.gather(*tasks))
event_loop.close()
````



asyncio + requests

````python
import asyncio
import requests


@asyncio.coroutine
def fetch_async(func, *args):
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, func, *args)
    response = yield from future
    print(response.url, response.content)


tasks = [
    fetch_async(requests.get, 'http://www.www.baidu.com/'),
    fetch_async(requests.get, 'http://www.sina.com.cn')
]

loop = asyncio.get_event_loop()
results = loop.run_until_complete(asyncio.gather(*tasks))
loop.close()
````



### 2、gevent（利用greenlet）

协程和异步非阻塞的关系：无任何关系，协程就是程序执行的切换，但是可以实现遇到IO阻塞时进行切换。这样就跟异步非阻塞类似的功能。

````python
import gevent
import requests
from gevent import monkey
from gevent.pool import Pool

monkey.patch_all()

def async_func(method, url, req_kwargs):
    response = requests.request(method=method, url=url, **req_kwargs)
    print(response.text)

# gevent.joinall([
#     gevent.spawn(async_func, method='GET', url='http://www.baidu.com', req_kwargs={}),
#     gevent.spawn(async_func, method='GET', url='http://www.google.com', req_kwargs={})
# ])

pool = Pool(5)
gevent.joinall([
    pool.spawn(async_func, method='GET', url='http://www.google.com', req_kwargs={}),
    pool.spawn(async_func, method='GET', url='http://www.baidu.com', req_kwargs={}),
])
````



### 3、Twisted

````python
from twisted.web.client import getPage, defer
from twisted.internet import reactor


def all_done(arg):
    reactor.stop()


def callback(contents):
    print(contents)


deferred_list = []

url_list = ['http://www.bing.com', 'http://www.baidu.com', ]
for url in url_list:
  	# 1.无等待且无发送数据，只创建对象和发送连接请求
    # deferred_list存放socket对象，只发送了连接请求，结果未知
    deferred = getPage(bytes(url, encoding='utf8')) # 相当于requests
    deferred.addCallback(callback) # 对请求的回调函数
    deferred_list.append(deferred)

# 2.
dlist = defer.DeferredList(deferred_list)
dlist.addBoth(all_done) # 所有请求执行完成才执行才回调函数

# 3.循环监测deferred_list，如果连接成功就发请求
# 4.发送请求后监测是否有返回数据，直到数据返回
reactor.run()
````



#### 4、Tornado







### 四、IO多路复用组件

预备知识：

````python
# socket客户端 阻塞 
import socket

client = socket.scoket()
client.connect((ip,port)) # 连接阻塞

client.send('GET / http/1.1\r\nhost:\r\ncontent-type:...\r\n\r\n')
client.recv(1024) # 接收阻塞
client.close()
````



````Python
# socket客户端 非阻塞
import scoket
import time 

client = socket.socket()
client.setblocking(False)
try:
	client.connect((ip,port)) # 非阻塞，但会报错
except Exception as e:
  	pass
  
# ###############################################
#        非阻塞                                  #
# while True:                                   #
# 可以处理其它事情，监测是否成功连接，如果成功就跳出循环 #
# ###############################################

data = "GET / http/1.1\r\nhost:\r\ncontent-type:...\r\n\r\n"
client.sendadd(data.encode('utf-8'))

# ###############################################
#        非阻塞                                  #
# while True:                                   #
# 可以处理其它事情，监测是否成功连接，如果成功就跳出循环 #
# ###############################################

client.recv(1024)
client.close()
````



IO多路复用：

1. 监测多个socket对象的变化 r,w,e = select.select([],[],[],0.05)

2. r : 代表数据可读，w：代表连接成功

   ​

````Python
import socket
import select

class Request(object):
    def __init__(self, sock, info):
        self.sock = sock
        self.info = info

    def fileno(self):
        return self.sock.fileno()


class Unsurpassed(object):
    def __init__(self):
        self.sock_list = []
        self.conns = []

    def add_request(self, req_info):
        '''
        创建请求
         {'host':'www.baidu.com', 'port':80, 'path':'/'}
        :return: 
        '''
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        try:
            sock.connect((req_info['host'],req_info['port']))
        except BlockingIOError as e:
            pass
        obj = Request(sock, req_info)
        self.sock_list.append(obj)
        self.conns.append(obj)

    def run(self):
        '''
        开始事件循环
        监测连接是否成功，数据是否返回
        :return: 
        '''
        while True:
            # select.select([socket对象／任意有fileno方法的方法(自己创建的Request对象)])
            # 内部执行obj.fileno()
            r,w,e = select.select(self.sock_list, self.conns, [], 0.05)
            for obj in w:
                # 检查obj 是否连接
                # Request对象含有socket对象和字典所有信息
                data = "GET %s http/1.1\r\nhost:%s\r\n\r\n" % (obj.info['path'], obj.info['host'])
                obj.sock.send(data.encode('utf-8'))
                self.conns.remove(obj) # 防止重复send数据
            for obj in r:
                response = obj.sock.recv(8096)
                # 回调
                if obj.info.get('callback'):
                    obj.info['callback'](response)
                print(obj.info['host'],response)
                self.sock_list.remove(obj)
            # 所有请求已经返回
            if not self.sock_list:
                break


def done(response):
    '''
    :param response: 
    :return: 
    '''
    print('回调函数',response)



url_list = [
    {'host':'www.baidu.com', 'port':80, 'path':'/', 'callback':done},
    {'host':'www.bing.com', 'port':80, 'path':'/'},
    {'host':'www.zhihu.com', 'port':80, 'path':'/'},
]

uns = Unsurpassed()
for item in url_list:
    uns.add_request(item)
uns.run()
````

使用：

1. 创建url_list列表
2. 实例化Unsurpassed对象，调用add_request方法传入url_list
3. add_request 里面会循环url_list创建socket对象，并使用Request类（传入对象和info）封装一次，以便以后可以同时使用url字典里面的参数，以及select方法只要有fileno方法就能监测，所以也要创建相同的方法，返回值是原来的socket对象的fileno方法
4. run方法里面监测socket是否有变化，如果w连接发生变化，就遍历发送指定请求。如果r发生变化，获取信息，并调用回调函数。





### 五、Scrapy框架

#### 1、功能：

- 应用twisted下载页面
- html解析成对象（类似BS4）
- 代理
- 延迟下载
- 去重
- 深度、广度



![](https://github.com/MMingLeung/Markdown-Picture/blob/master/scrapy.png?raw=true)

1. 爬虫交给引擎
2. 引擎交给调度器
3. 下载器访问网站
4. 数据返回给爬虫并调用回调函数
5. 消息持久化



#### 2、安装

Window: pip3 install wheel

​		download twisted.wheel到本地 , pip3 安装

​		pip3 install scrapy

Mac/Linux : pip/pip3 install scrapy



#### 3、使用

1. 创建项目：控制台输入 scrapy startapp sp1

2. 自动创建的文件目录如下：

3. ````
   sp1/    
       scrapy.cfg # 初始配置文件
       sp1/
            |— spiders/
            |— middlewares.py # 中间键
            |— items.py # 格式化
            |— settings.py # 
            |— pipelines.py # 持久化

   ````

4.  创建爬虫 scraps genspider baidu baidu.com

5. 修改爬虫协议setting.py ROBOTSTXT_OBEY = False

6. 运行爬虫 scrapy crawl baidu (—nolog)



####  4、选择器

````
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import HtmlXPathSelector, Selector

hxs = Selector(response=response)
# 找所有div(标签名)
result = hxs.xpath('//div')
# 找第二个div(标签名)
result = hxs.xpath('//div[2]')
# 找有id属性的div(标签名)
result = hxs.xpath('//div[@id]')
# 找有id = a1 的div(标签名)
result = hxs.xpath('//div[@id='a1']')
# 找有id = a1 且 value = '123' 的div(标签名)
result = hxs.xpath('//div[@id='a1'][@value='123']')
#  找href包含'link'的a（标签名）
result = hxs.xpath('//a[contains(@href, "link")]')
# href以"link"开头
result = hxs.xpath('//a[starts-with(@href, "link")]')
# id = i + 数字
result = hxs.xpath('//a[re:test(@id, "a\d+")]')
# id = i + 数字的a标签的文本并且获取标签字符串列表（原来是对象）
result = hxs.xpath('//a[re:test(@id, "i\d+")]/text()').extract()
# id = i + 数字的a标签的href属性并且获取标签字符串列表（原来是对象）
result = hxs.xpath('//a[re:test(@id, "i\d+")]/@href').extract()
# 单一个’／‘代表当前的标签开始，找到a标签的href属性并获取字符串列表
result = hxs.xpath('/html/body/ul/li/a/@href').extract()
# 双‘//’代表从整个html文件开始
result = hxs.xpath('//body/ul/li/a/@href').extract_first()

# 获取对象后可以继续循环遍历
# 再使用‘/’继续获取指定标签
````



#### 5、简单自动登录点赞

````Python
import scarpy
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.http.cookies import CookieJar
import json

class ChoutiSpider(scarpy.Spider):
  	name = 'chouti'
    allowed_domains = ['chouti.com']
    start_urls = ['http://chouti.com/']
    
   	def start_request(self):
	'''
	根据start_urls，从此处开始启动爬虫
	'''    
    for url in start_urls:
      	yield Request(url, dont_filter=True ,callback=self.parse1)
        
    def parse1(self, response):
      	'''
      	自动登录需要：
      	1.cookies
      	2.请求题包含账号密码
      	'''
        # 获取cookies
        self.cookie = CookieJar()
        self.cookie = self.cookie.extract_cookies(response, response.request)
        data = "phone=86xxxxxx&password=xxxxxx&oneMonth=1"
        # 或者以字典形式使用urllib.parse.encode转换
        url = 'http://dig.chouti.com/login'
        yield Request(url=url,
                     cookies=self.cookie,
                     body=data,
                     method='POST',
                     callback=self.parse2,
                     headers={'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'})
        
     def parse2(self, response):
      	 '''
      	 查看是否正常获取新闻列表页面
      	 '''
         print(json.loads(response.text))
         url = 'http://dig.chouti.com'
         yield Request(url, cookies=self.cookie, callback=self.parse3)
     
        
     def parse3(self, response):
      	'''
      	登录完成之后进行点赞操作
      	1、找到对应标签
      	2、发送GET请求
      	3、递归点赞
      	'''
        hxs = Selector(response)
        link_id_list = hxs.xpath('//div[@class="part2"]/@share-linkid').extract()
        base_like_url = 'http://dig.chouti.com/link/vote?linksId={0}'
        for link in link_id_list:
          	url = base_like_url.format(link)
            yield Request(url=url, method='POST', callback=self.parse4, cookies=self.cookie)
        
       	pages_hxs = Selector(response)
        page_url_list = pages_hxs.xpath('//div[@class="dig_lcpage"]/a/@href')
		base_url = "http://dig.chouti.com{0}"
        for url in page_url_list:
          url = base_url.format(url)
          yield Request(url=url, method='GET', callback=self.parse3, cookies=self.cookie)
    
    def parse4(self, response):
      	print(response.text)
    

````



#### 6、消息持久化

1. items.py 根据所需要处理的数据创建对应的Field()对象
2. spider 中yield item的对象
3. settings.py 注册ITEM_PIPELINES
4. 爬虫运行的时候就会运行piplines.py 对应的类的函数



````python
# items.py
import scrapy


class Sp2Item(scrapy.Item):
    url = scrapy.Field()
    text = scrapy.Field()
   
````



````Python
# spider
# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from sp2.items import Sp2Item

class JiandanSpider(scrapy.Spider):
    name = 'jiandan'
    allowed_domains = ['jandan.net']
    start_urls = ['http://jandan.net/']

    def start_requests(self):
        '''
        该方法从指定起始url开始启动爬虫
        :return: 
        '''
        for url in self.start_urls:
            yield Request(url, dont_filter=True, callback=self.parse1,headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko)"})


    def parse1(self, response):
        hxs = Selector(response)
        a_list = hxs.xpath('//div[@class="indexs"]/h2/a')
        for tag in a_list:
            url = tag.xpath('./@href').extract_first()
            text = tag.xpath('./text()').extract_first()
            yield Sp2Item(url=url, text=text) # 
````



````Python
# settings.py
ITEM_PIPELINES = {
   'sp2.pipelines.Sp2Pipeline': 300, # 优先级越小越优先
   'sp2.pipelines.Sp3Pipeline': 100, 
}
````



````python
# piplines.py 
# 流程：
# 1.先找是否有from_crawler()，有就执行，在里面实例化Sp2Pipeline对象并且可以获取settings.py的配置（数据库配置）
# 2.open_spider 打开爬虫时，执行一些操作，如：连接数据库
# 3.process_item 爬虫执行到yield item_obj切换到该函数，item可以其存放的属性，如有raise DropItem()则不执行下一个pipline的process_item方法，return item 则执行。
# 4.close_spider 关闭爬虫时，执行一些操作，如：关闭数据库
from scrapy.exceptions import DropItem


class Sp2Pipeline(object):
    def __init__(self, v):
        self.v = v
        self.f = None

    def process_item(self, item, spider):
        '''
        :param item: 爬虫中yield回来的对象
        :param spider: 爬虫对象obj = JiandanSpider()
        :return: 
        '''
        if spider.name == 'jiandan':
            print(type(item))
            self.f.write(item.url)
            self.f.write(item.name)
            # raise DropItem() # 不执行下一个pipline的process_item方法
            return item # 传递给下一个pipline的process_item方法

    @classmethod
    def from_crawler(cls, crawler):
        '''
        初始化，用于创建pipline对象
        :param crawler: 
        :return: 
        '''
        print('实例化对象from_crawler2')
        val = crawler.settings.get('TEST')
        return cls(val)

    def open_spider(self, spider):
        print('打开爬虫2')
        self.f = open('test.txt', 'a+')

    def close_spider(self, spider):
        print('关闭爬虫2')
        self.f.close()
````



#### 7、去重及自定义

````python
# settings.py
# 默认去重规则
from scrapy.dupefilter import RFPDupeFilter
# DUPEFILTER_CLASS = 'scrapy.dupefileter.RFPDupeFilter' # 修改成自己定义的类即可
# DUPEFILTER_DEBUG = False
# JOBDIR = '日志路径'

class RepeatUrl:
  	def __init__(self):
      	self.visited_url = set()
    
    @classmethod
    def from_settings(cls, settings):
       	return cls()
      
    def request_seen(self, request):
      	if request.url in self.visited_url:
          	return True
        return False
    
    def open(self):
      	'''
      	爬虫启动时调用
      	'''
      	pass
      
    def close(self, reason):
      	'''
      	爬虫结束时调用
      	'''
        pass
      
    def log(self, request, spider):
      	pass	
````



#### 8、自定义扩展

````python
# settings.py
EXTENSIONS = {
   # 'scrapy.extensions.telnet.TelnetConsole': None,
   'sp2.extends.MyExtension':300,
}

````



````python
from scrapy import signals

class MyExtension(object):
    def __init__(self, value):
        self.value = value

    @classmethod
    def from_crawler(cls, crawler):
        val = crawler.settings.get('TEST')
        ext = cls(val)

        # 注册信号
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)

        return ext

    def spider_opened(self, spider):
        print('signal_opened')

    def spider_closed(self, spider):
        print('signal_closed')
        
'''信号
engine_started = object() 
engine_stopped = object()
spider_opened = object()
spider_idle = object()
spider_closed = object()
spider_error = object()
request_scheduled = object()
request_dropped = object()
response_received = object()
response_downloaded = object()
item_scraped = object()
item_dropped = object()
'''
````



#### 8、中间件

##### 1、配置文件注册

`````
SPIDER_MIDDLEWARES = {
   'sp2.middlewares.Sp2SpiderMiddleware': 543,
}

DOWNLOADER_MIDDLEWARES = {
   'sp2.middlewares.MyCustomDownloaderMiddleware': 543,
}
`````





##### 1、爬虫中间件

````Python
class SpiderMiddleware(object):

    def process_spider_input(self,response, spider):
        """
        下载完成，执行，然后交给parse处理
        :param response: 下载完成的数据
        :param spider: 
        :return: 
        """
        print('md_process_spider_input')

    def process_spider_output(self,response, result, spider):
        """
        spider处理完成，返回时调用
        :param response:下载完成的数据
        :param result:准备给调度器的对象
        :param spider:
        :return: 必须返回包含 Request 或 Item 对象的可迭代对象(iterable)
        """
        print("md_process_spider_output")
        return result

    def process_spider_exception(self,response, exception, spider):
        """
        异常调用
        :param response:
        :param exception:
        :param spider:
        :return: None,继续交给后续中间件处理异常；含 Response 或 Item 的可迭代对象(iterable)，交给调度器或pipeline
        """
        return None


    def process_start_requests(self,start_requests, spider):
        """
        爬虫启动时调用
        :param start_requests:
        :param spider:
        :return: 包含 Request 对象的可迭代对象
        """
        print('md_process_start_requests')
        return start_requests
````



##### 2、下载器中间件

````python
# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class SpiderMiddleware(object):

    def process_spider_input(self,response, spider):
        """
        下载完成，执行，然后交给parse处理
        :param response: 下载完成的数据
        :param spider: 
        :return: 
        """
        print('md_process_spider_input')

    def process_spider_output(self,response, result, spider):
        """
        spider处理完成，返回时调用
        :param response:下载完成的数据
        :param result:准备给调度器的对象
        :param spider:
        :return: 必须返回包含 Request 或 Item 对象的可迭代对象(iterable)
        """
        print("md_process_spider_output")
        return result

    def process_spider_exception(self,response, exception, spider):
        """
        异常调用
        :param response:
        :param exception:
        :param spider:
        :return: None,继续交给后续中间件处理异常；含 Response 或 Item 的可迭代对象(iterable)，交给调度器或pipeline
        """
        return None


    def process_start_requests(self,start_requests, spider):
        """
        爬虫启动时调用
        :param start_requests:
        :param spider:
        :return: 包含 Request 对象的可迭代对象
        """
        print('md_process_start_requests')
        return start_requests



class DownMiddleware(object):
    def process_request(self, request, spider):
        """
        请求需要下载时执行
        :param request: 
        :param spider: 
        :return:  
            None,继续后续中间件去下载；
            Response对象，停止process_request的执行，开始执行process_response
            Request对象，停止中间件的执行，将Request重新调度器
            raise IgnoreRequest异常，停止process_request的执行，开始执行process_exception
        """
        print('DMD_process_request')
        from scrapy.http import Request
        # 在下载前自定义请求头等信息
        # request.method = 'POST'
        # request.headers['xxx']='xxxx'

        # 自定义下载
        # import requests
        # res = requests.get(url='xxx')
        # return data

        return None



    def process_response(self, request, response, spider):
        """
        spider处理完成，返回时调用
        :param response:
        :param result:
        :param spider:
        :return: 
            Response 对象：转交给其他中间件process_response
            Request 对象：停止中间件，request会被重新调度下载
            raise IgnoreRequest 异常：调用Request.errback
        """
        print('DMD_process_response')
        print(spider)

        # 返回值做特殊操作，如编码处理、响应头解析
        # response.encoding = 'utf-8'

        # 自定义类，封装response，用于扩展

        return response

    def process_exception(self, request, exception, spider):
        """
        当下载处理器(download handler)或 process_request() (下载中间件)抛出异常
        :param response:
        :param exception:
        :param spider:
        :return: 
            None：继续交给后续中间件处理异常；
            Response对象：停止后续process_exception方法
            Request对象：停止中间件，request将会被重新调用下载
        """
        return None
````



#### 9、自定义命令



````Python
# 1.settings.py 加入存放自定义命令py文件的文件夹名字
COMMANDS_MODULE = 'spider_test.commands'
````



````Python
# 2.自定义
from scrapy.commands import ScrapyCommand


class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def run(self, args, opts):
        # from scrapy.crawler import CrawlerProcess
        # from scrapy.crawler import ExecutionEngine
        # CrawlerProcess.start() # 内部reactor.run()运行死循环
        # 获取爬虫列表
        spider_list = self.crawler_process.spiders.list()
        for name in spider_list:
            # 初始化爬虫
            # 1.调用父类的crawl()
            # 2.内部把sipder生成器变成迭代对象
            # 3.放到队列
            # 4.取对象
            # 5.执行下载
            self.crawler_process.crawl(name, **opts.__dict__)
        # 开始执行爬虫
        self.crawler_process.start()
````



3. 执行：scrapy + py文件名字



#### 10、中间件实现代理



默认代理设置：

````python
# 自定义命令py文件
from scrapy.commands import ScrapyCommand


class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def run(self, args, opts):
        import os
        # from scrapy.contrib.downloadermiddleware.httpproxy import HttpProxyMiddleware
        # scrapy 定义的规则找"_proxy"的环境变量作为代理
        os.environ['http_proxy'] = 'http://root:xxxx@xxx.xxx.xx.xx:xxxx/'
        os.environ['https_proxy'] = 'http://xxx.xxx.xx.xx:xxxx/'
        
        # .... 省略下面代码

````







自定义：

````Python
# middlewares.py
# 需要在settings.py中加入该中间件
def to_bytes(text, encoding=None, errors='strict'):
    if isinstance(text, bytes):
        return text
    if not isinstance(text, six.string_types):
        raise TypeError('to_bytes must receive a unicode, str or bytes '
                        'object, got %s' % type(text).__name__)
    if encoding is None:
        encoding = 'utf-8'
    return text.encode(encoding, errors)


class MyProxyMiddleware(object):
    def process_request(self, request, spider):
        PROXIES = [
            {'ip_port': 'xxx.xxx.xxx.xxx:80', 'user_pass': ''},
        ]
        proxy = random.choice(PROXIES)
        if proxy['user_pass'] is not None:
            request.meta['proxy'] = to_bytes("http://%s" % proxy['ip_port'])
            encoded_user_pass = base64.encodebytes(proxy['user_pass'])
            request.headers['Proxy-Authorization'] = to_bytes('Basic ' + encoded_user_pass)
            print("**************ProxyMiddleware have pass************" + proxy['ip_port'])

        else:
            print("**************ProxyMiddleware no pass************" + proxy['ip_port'])
			request.meta['proxy'] = to_bytes("http://%s" % proxy['ip_port'])


````



#### 11、配置文件

````python
# ######## 1.爬虫名称 ########
BOT_NAME = 'sp3'

# ######## 2.爬虫路径 ########
SPIDER_MODULES = ['sp3.spiders']
NEWSPIDER_MODULE = 'sp3.spiders'

# ######## 3.请求头 ########
# USER_AGENT = 'sp3 (+http://www.yourdomain.com)'

# ######## 4.爬虫协议 ########
ROBOTSTXT_OBEY = True

# ######## 5.请求的并发数 ########
#CONCURRENT_REQUESTS = 32

# ######## 6.延迟下载秒数 ########
#DOWNLOAD_DELAY = 3

# ######## 7.单域名访问并发数 ########
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
# 单IP请求的并发数，有值忽略CONCURRENT_REQUESTS_PER_DOMAIN
#CONCURRENT_REQUESTS_PER_IP = 16

# ######## 9.是否支持cookie,cookie_jar ########
# COOKIES_ENABLED = False
# COOKIES_DEBUG = True

# ######## 10.监控爬虫信息 ########
# CMD --> telnet ip port
#TELNETCONSOLE_ENABLED = False
#TELNETCONSOLE_HOST = ''
#TELNETCONSOLE_PORT = [6023,]

# ######## 11.默认请求头 ########
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# ######## 12.爬虫中间件 ########
#SPIDER_MIDDLEWARES = {
#    'sp3.middlewares.Sp3SpiderMiddleware': 543,
#}

# ######## 13.下载中间件 ########
#DOWNLOADER_MIDDLEWARES = {
#    'sp3.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# ######## 14.基于信号自定义扩展 ########
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}


# ######## 15.pipline配置 ########
#ITEM_PIPELINES = {
#    'sp3.pipelines.Sp3Pipeline': 300,
#}

# ######## 16.自动限速 ########
# AUTOTHROTTLE_ENABLED = True
# 初始下载延迟
# AUTOTHROTTLE_START_DELAY = 5
# 最大延迟
# AUTOTHROTTLE_MAX_DELAY = 60
# 平均并发数
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# 显示状态
# AUTOTHROTTLE_DEBUG = False

# ######## 17.最大深度 ########
# DEPTH_LIMIT = 3

# ######## 18.调度器 ########
# 默认0
# 后进先出，深度优先
# DEPTH_PRIORITY = 0
# SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleLifoDiskQueue'
# SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.LifoMemoryQueue'

# 先进先出，广度优先
# DEPTH_PRIORITY = 1
# SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
# SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'

# 调度器
# 默认队列存在于内存，可以自定义方法修改存放位置
from scrapy.core.scheduler import Scheduler
# SCHEDULER = 'scrapy.core.scheduler.Scheduler'
# from scrapy.core.scheduler import Scheduler

# ######## 19.去重规则 ########
# DUPEFILTER_CLASS = 'step8_king.duplication.RepeatUrl'

# ######## 20.缓存 ########
# 生成文件，下次直接访问缓存文件
# 是否启用缓存策略
# HTTPCACHE_ENABLED = True

# 缓存策略：所有请求均缓存，下次在请求直接访问原来的缓存即可
# HTTPCACHE_POLICY = "scrapy.extensions.httpcache.DummyPolicy"
# 缓存策略：根据Http响应头：Cache-Control、Last-Modified 等进行缓存的策略
# HTTPCACHE_POLICY = "scrapy.extensions.httpcache.RFC2616Policy"

# 缓存超时时间
# HTTPCACHE_EXPIRATION_SECS = 0

# 缓存保存路径
# HTTPCACHE_DIR = 'httpcache'

# 缓存忽略的Http状态码
# HTTPCACHE_IGNORE_HTTP_CODES = []

# 缓存存储的插件
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# ################

# ######## 21.自定义命令 ########
COMMANDS_MODULE = 'sp3.commands'

# ######## 22.HTTPS证书 ########
DOWNLOADER_HTTPCLIENTFACTORY ="scrapy.core.downloader.webclient.ScrapyHTTPClientFactory"
DOWNLOADER_CLIENTCONTEXTFACTORY = "step8_king.https.MySSLFactory"

# https.py
# from scrapy.core.downloader.contextfactory import ScrapyClientContextFactory
# from twisted.internet.ssl import (optionsForClientTLS, CertificateOptions, PrivateCertificate)
# 
# 
# class MySSLFactory(ScrapyClientContextFactory):
#     def getCertificateOptions(self):
#         from OpenSSL import crypto
#         v1 = crypto.load_privatekey(crypto.FILETYPE_PEM, open('/Users/matt/client.key.unsecure', mode='r').read())
#         v2 = crypto.load_certificate(crypto.FILETYPE_PEM, open('/Users/matt/client.pem', mode='r').read())
#         return CertificateOptions(
#             privateKey=v1,  # pKey对象
#             certificate=v2,  # X509对象
#             verify=False,
#             method=getattr(self, 'method', getattr(self, '_ssl_method', None))
#         )
````



