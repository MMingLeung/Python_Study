# 爬虫性能相关

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
#!/usr/bin/env python
# -*-coding:utf-8 -*-

import socket
import select

class Request(sock):
	def __init__(self, info):
      	self.sock = sock
        self.info = info
   
  	def fileno(self):
      	return self.sock.fileno()
  	
class Unsurpassed(object):
  	def __init__(self):
    	self.req_list = []
        self.conns = []
  	
    def add_request(self, req_info):
      	for url in url_list:
          	sock = socket.scoket()
            try:
            	sock.connect((url['host'], url['port']))
            except BlockingIOError as e:
                pass
            obj = Request(sock, req_info)
            self.req_list.append(obj)
            self.conns.append(obj)
      
    def run(self):
      	r,w,e = select.select(self.req_list, self.conns, [], 0.05)
        while True:
          	for obj in w:
              	data = "GET %s \r\nhost:%s\r\n\r\n" % (obj.info.path, obj.info.host)
                obj.sock.sendadd(data.encode('utf-8'))
            	self.req_list.move(obj)
            for obj in r:
              	data = obj.sock.recv(1024)
                print(data)
                obj.info['callback']()
                self.conns.remove(obj)
           	if not self.req_list:
              	break
                

def done():
  	print('callback')
	return 
  
  
    
url_list = [{'host':'www.google.com', 'port':80, 'path':'/', 'callback':done},
           	{'host': 'www.github.com', 'port':80, 'path':'/'}]


obj = Unsurpassed()
obj.add_request(url_list)
obj.run

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

