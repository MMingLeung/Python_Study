# Scrapy 爬虫框架剖析

## 一、twisted 简单应用

程序调用过程：

1. 循环遍历url列表，调用getPage函数，下载页面，返回一个deferred对象（用于添加回调函数）
2. 添加回调函数，并且加入到deferred对象的列表
3. 调用DeferredList初始化deferred对象的列表
4. 加入回调函数
5. 启动
6. 当全部任务完成时，就用结束方法

````python
#!/usr/bin/env python
# -*- coding:utf-8 -*-

from twisted.web.client import defer, getPage, reactor

def one_done(content):
    print(content)

def all_done(arg):
    reactor.stop()


deferred_list = []

url_list = ['http://www.baidu.com', 'http://www.bing.com']

for url in url_list:
    deffered = getPage(bytes(url, encoding='utf8'))
    deffered.addCallback(one_done)
    deferred_list.append(deffered)

df_list = defer.DeferredList(deferred_list)
df_list.addCallback(all_done)
reactor.run()
````



## 二、twisted 标准用法

* 装饰器 + yield deferred 对象 + 回调函数

````python
#!/usr/bin/env python
# -*- coding:utf-8 -*-

from twisted.web.client import defer, getPage, reactor

def one_done(content):
    print(content)

def all_done(arg):
    reactor.stop()

@defer.inlineCallbacks
def task(url):
    deffered = getPage(bytes(url, encoding='utf8'))
    deffered.addCallback(one_done)
    yield deffered


deferred_list = []

url_list = ['http://www.baidu.com', 'http://www.bing.com']

for url in url_list:
    deferred = task(url)
    deferred_list.append(deferred)


df_list = defer.DeferredList(deferred_list)
df_list.addCallback(all_done)
reactor.run()
````



## 三、twisted 永恒循环

* yield 空的deffered对象，循环监测不会中断

````python
#!/usr/bin/env python
# -*- coding:utf-8 -*-

from twisted.web.client import defer, getPage, reactor

def one_done(content):
    print(content)

def all_done(arg):
    reactor.stop()

@defer.inlineCallbacks
def task():
    deffered1 = getPage(bytes('http://www.baidu.com', encoding='utf8'))
    deffered1.addCallback(one_done)
    yield deffered1

    deffered2 = defer.Deferred()
    yield deffered2

df = task()
df.addBoth(all_done)
reactor.run()
````



## 四、twisted 停止永恒循环的条件

* 每次获取完结果都在回调函数中移除url和监测列表是否还有未完成的请求的url，如果全部完成，空的deferred对象马上调用回调函数就能终止循环

````python
#!/usr/bin/env python
# -*- coding:utf-8 -*-

from twisted.web.client import defer, getPage, reactor

running_list = []
stop_deferred = None

def one_done(content, url):
    # print(content)
    running_list.remove(url)

def all_done(arg):
    reactor.stop()

def check_empty(res):
    if not running_list:
        stop_deferred.addCallback('1')

@defer.inlineCallbacks
def spider(url):
    deferred = getPage(bytes(url, encoding='utf8'))
    deferred.addCallback(one_done, url)
    deferred.addCallback(check_empty)
    yield deferred


def loop_deferred():
    global stop_deferred
    stop_deferred = defer.Deferred()
    return stop_deferred


@defer.inlineCallbacks
def task(url):
    yield spider(url)
    yield loop_deferred()

running_list.append('http://www.baidu.com')
df = task('http://www.baidu.com')
df.addBoth(all_done)
reactor.run()

````



## 五、twisted 进一步封装

````python
from twisted.web.client import getPage, reactor, defer

class ExcutionEngine(object):
    def __init__(self):
        self.running_list = []
        self.stop_deferred = None

    def one_done(self, response, url):
        print(response)
        if not self.running_list:
            self.stop_deferred.addCallback('1')

    def check_empty(self, response, url):
        self.running_list.remove(url)

    @defer.inlineCallbacks
    def open_spider(self, url):
        deferred = getPage(bytes(url, encoding='utf-8'))
        deferred.addCallback(self.one_done, url)
        deferred.addCallback(self.check_empty)
        yield deferred

    @defer.inlineCallbacks
    def stop(self):
        self.stop_deferred = defer.Deferred()
        yield self.stop_deferred

@defer.inlineCallbacks
def task(url):
    eng = ExcutionEngine()
    eng.running_list.append(url)

    yield eng.open_spider(url)
    yield eng.stop_deferred()

def all_done(arg):
    reactor.stop()

if __name__ == '__main__':
    task_one = task('http://www.baidu.com')
    task_one.addBoth(all_done)

    reactor.run()
````



## 六、仿Scrapy

- ```python
  # Request类
  封装url和回调函数
  ```


  # Scheduler类（调度器）
  1.构造方法
   - 队列
      - 引擎对象
        2.enqueue_request添加request对象到队列
        3.next_request next取值
        4.获取队列size


  # ExecutionEngine类
  1.构造方法
   - stop_deferred对象
      - 运行的deferred列表
        - 调度器对象
        - 正在运行的deferred集合

  2._handler_downloader_output 处理下载和输出
   - 调用request对象的回调函数并传入当前回调函数的返回值
      - 判断是否时生成器
        - 是，是否是Request对象，是，重新加入到调度器
        - 否，传给pipeline等...

  3._next_request
   - 如何start_requests有值，next获取每一个request
      - 最后放入调度器
        - 如果并发数<5 且调度器队列>0，获取页面数据，添加回调函数
        - 如果两者 = 0， 调用停止循环的函数

  4.open_spider
   - 把传入的start_requests 复制给类的属性
      - yield None
        - 调用reactor.callLater马上执行 _next_request 

5.crawl 方法

   -  生成engine 对象
      - 迭代器
      - 开始爬虫
      - 开始引擎

- _stop_reactor

        - 停止爬虫

   -  parse

         - yield Request对象

      ​

  ```python

  #!/usr/bin/env python
  # -*- coding:utf-8 -*-
  from twisted.web.client import reactor, defer, getPage
  import queue
  import types


  class Scheduler(object):
      def __init__(self, engine):
          self.queue = queue.Queue()
          self.engine = engine

      def enqueue_request(self, request):
          self.queue.put(request)

      def next_request(self):
          try:
              req = self.queue.get(block=False)
          except Exception as e:
              self.queue = None
          return req

      def get_size(self):
          return self.queue.qsize()


  class Request(object):
      def __init__(self, url, callback):
          self.url = url
          self.callback = callback


  class ExcutionEngine(object):
      def __init__(self):
          self.scheduler = Scheduler(self)
          self._loop = None
          self.start_requests = None
          self.inprogress = set()

      @defer.inlineCallbacks
      def open_spider(self, start_requests):
          self.start_requests = start_requests
          yield None
          reactor.callLater(0, self._next_request)

      def _next_request(self):
          while self.start_requests:
              try:
                  request = next(self.start_requests)
              except StopIteration:
                  self.start_requests = None
              else:
                  self.scheduler.enqueue_request(request)

          print(len(self.inprogress), self.scheduler.get_size())
          while len(self.inprogress) < 5 and self.scheduler.get_size() > 0:
              request = self.scheduler.next_request()
              if not request:
                  break
              self.inprogress.add(request)
              print(request.url)
              d = getPage(bytes(request.url, encoding='utf-8'))
              d.addBoth(self._handle_downloader_output, request)
              d.addBoth(lambda x, req:self.inprogress.remove(req), request)
              d.addBoth(lambda x:self._next_request())

          if len(self.inprogress) == 0 and self.scheduler.get_size() == 0:
              from twisted.internet.defer import Deferred
              self._loop.callback(None)

      def _handle_downloader_output(self, response, request):
          gen = request.callback(response, request.callback)
          if isinstance(gen, types.GeneratorType):
              for req in gen:
                  self.scheduler.enqueue_request(req)

      @defer.inlineCallbacks
      def _wait(self):
          self._loop = defer.Deferred()
          yield self._loop


  @defer.inlineCallbacks
  def crawler(start_requests):
      engine = ExcutionEngine()
      start_requests = iter(start_requests)

      yield engine.open_spider(start_requests)
      yield engine._wait()

  def parse(response, callback):
      for i in range(10):
          yield Request('http://www.baidu.com/%s' % i, callback)

  def stop(arg):
      reactor.stop()

  if __name__ == '__main__':
      start_requests = [Request('http://www.baidu.com', parse), Request('http://www.github.com', parse),]
      obj = crawler(start_requests)
      obj.addBoth(stop)
      reactor.run()
  ````



         通过twisted内部的reactor启动事件循环，循环内部的deferred对象（含有一个空deferred对象，用于永恒循环），如果deferred对象有返回消息则回调对应的函数。待所有deferred对象完成任务后，向空deferred对象调用callback，停止永恒循环，最后回调总体回调函数，停止reactor。

​````python
from twisted.web.client import reactor, getPage, defer
import types
import queue


class Response(object):
    def __init__(self, body, request):
        self.body = body
        self.request = request
        self.url = request.url  #

    @property
    def text(self):
        return self.body.decode('utf-8')


class Request(object):
    def __init__(self, url, callback=None):
        self.url = url
        self.callback = callback


class Spider(object):
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url)


class GithubSpider(Spider):
    name = 'github'
    start_urls = ['http://www.github.com']

    def parse(self, response):
        print(response.text)


class Crawler(object):
    def __init__(self, spidercls):
        self.spidercls = spidercls
        self.engine = None
        self.spider = None

    @defer.inlineCallbacks
    def crawl(self):
        self.spider = self.spidercls()
        self.engine = ExcutionEngine()
        start_request = iter(self.spider.start_requests())

        yield self.engine.open_spider(self.spider, start_request)
        yield self.engine.start()


class CrawlerProcess(object):
    def __init__(self):
        self._active = set()
        self.crawlers = set()

    def crawl(self, spidercls, *args, **kwargs):
        crawler = Crawler(spidercls)
        self.crawlers.add(crawler)
        d = crawler.crawl(*args, **kwargs)
        self._active.add(d)
        return d

    def start(self):
        dl = defer.DeferredList(self._active)
        dl.addBoth(self._stop_reactor)
        reactor.run()

    def _stop_reactor(self, _=None):
        reactor.stop()


class Scheduler(object):
    def __init__(self, engine):
        self.q = queue.Queue()
        self.engine = engine

    def enqueue_request(self, request):
        self.q.put(request)

    def next_request(self):
        try:
            req = self.q.get(block=False)
        except Exception as e:
            req = None
        return req

    def get_size(self):
        return self.q.qsize()


class ExcutionEngine(object):
    def __init__(self):
        self.schedule = Scheduler(self)
        self._close_loop = None
        self.inprogress = set()
        self.deferred_list = None

    @defer.inlineCallbacks
    def open_spider(self, spider, start_requests):
        self.spider = spider
        self.start_requests = start_requests
        yield None
        reactor.callLater(0, self._next_request)

    def _next_request(self):
        while self.start_requests:
            try:
                request = next(self.start_requests)
            except StopIteration:
                self.start_requests = None
            else:
                self.schedule.enqueue_request(request)

        print(len(self.inprogress), self.schedule.get_size())
        while len(self.inprogress) < 5 and self.schedule.get_size() > 0:
            request = self.schedule.next_request()
            if not request:
                break
            self.inprogress.add(request)
            # reactor.run()之后, 并发发送请求
            d = getPage(bytes(request.url, encoding='utf-8'))
            d.addBoth(self._handle_downloader_output, request)
            d.addBoth(lambda x, req: self.inprogress.remove(req), request)
            d.addBoth(lambda x: self._next_request())  #

        if len(self.inprogress) == 0 and self.schedule.get_size() == 0:
            self._close_loop.callback(None)

    def _handle_downloader_output(self, body, request):
        response = Response(body, request)
        func = request.callback or self.spider.parse
        gen = func(response)
        if isinstance(gen, types.GeneratorType):
            for req in gen:
                self.schedule.enqueue_request(req)

    @defer.inlineCallbacks
    def start(self):
        self._close_loop = defer.Deferred()
        yield self._close_loop


if __name__ == '__main__':
    spider_cls_list = [GithubSpider, ]

    crawler_process = CrawlerProcess()
    for spider_cls in spider_cls_list:
        # 初始化爬虫
        crawler_process.crawl(spider_cls)
    # 执行爬虫
    crawler_process.start()

# 1、CrawlProcess初始化，循环遍历spider类列表时调用CrawlProcess的crawl方法并传入spider类
# 2、CrawlProcess的crawl方法内部实例化一个Crawler类并执行crawl方法
# 3、Crawler类crawl方法本质上是实例化spider类和一个引擎并调用引擎的方法返回两个deferred对象
# 4、其中一个是空的Deferred对象用于当reactor启动时形成永恒循环，另外一个deferred对象什么都没有做
# 5、当reactor启动，什么都没有做的deferred对象中的reactor.callLater执行，本质是执行_next_reqeust函数
# 6、_next_reqeust函数中把已经转换成迭代器的request放入队列中，然后一个个取，调用getPage发送请求获取数据，等数据返回自动执行回调函数
# 7、其回调函数一是处理返回值，调用爬虫的回调函数并判断返回值是否是生成器，如果是继续放入调度器中；如果是item对象做持久化处理。
# 8、直到所有请求处理完毕，向空deferred对象调用callback，停止永恒循环
# 9、最后停止reactor

  ```