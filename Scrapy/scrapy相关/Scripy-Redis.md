# Scripy-Redis

## 一、配置

````python
# settings.py
# ############## scrapy-redis ##############
from scrapy_redis import connection
from scrapy_redis import defaults # 查看默认配置
REDIS_HOST = '192.168.0.150'                        # 主机名
REDIS_PORT = 6379                                   # 端口
# REDIS_URL = 'redis://user:pass@hostname:9001'     # 连接URL（优先于以上配置）
REDIS_PARAMS  = {}                                  # Redis连接参数             默认：REDIS_PARAMS = {'socket_timeout': 30,'socket_connect_timeout': 30,'retry_on_timeout': True,'encoding': REDIS_ENCODING,}）
REDIS_PARAMS['redis_cls'] = 'myproject.RedisClient' # 指定连接Redis的Python模块   默认：redis.StrictRedis
REDIS_ENCODING = "utf-8"                            # redis编码类型   默认：'utf-8'

# ############## 默认去重规则 ##############
from scrapy_redis.dupefilter import RFPDupeFilter
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 去重规则里面执行首先执行from_crawler，本质上是执行from_settings方法，而from_settings里面获取一个redis 连接通过get_redis_from_settings获得，其本质是使用redis.StrictRedis进行连接，可以使用Redis，兼容性更好
# request_fingerprint:根据url生成长度一致的唯一标示

# 调度器
from scrapy_redis.scheduler import Scheduler
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

from scrapy_redis.queue import PriorityQueue
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.PriorityQueue'  # 默认使用优先级队列（默认），其他：PriorityQueue（有序集合），FifoQueue（列表）、LifoQueue（列表）
SCHEDULER_QUEUE_KEY = '%(spider)s:requests'  # 调度器中请求存放在redis中的key
# github:requests --
SCHEDULER_SERIALIZER = "scrapy_redis.picklecompat"  # 对保存到redis中的数据进行序列化，默认使用pickle
# 存放在redis的数据是request对象，所以需要序列化
from scrapy_redis import picklecompat
SCHEDULER_PERSIST = True  # 是否在关闭时候保留原来的调度器和去重记录，True=保留，False=清空
SCHEDULER_FLUSH_ON_START = False  # 是否在开始之前清空 调度器和去重记录，True=清空，False=不清空
SCHEDULER_IDLE_BEFORE_CLOSE = 10  # 去调度器中获取数据时，如果为空，最多等待时间（最后没数据，未获取到）。
SCHEDULER_DUPEFILTER_KEY = '%(spider)s:dupefilter'  # 去重规则，在redis中保存时对应的key
SCHEDULER_DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'  # 去重规则对应处理的类


# 数据持久化
REDIS_ITEMS_KEY = '%(spider)s:items'
REDIS_ITEMS_SERIALIZER = 'json.dumps'


# 起始url (永远不会停下来)
REDIS_START_URLS_AS_SET = False  # 获取起始URL时，如果为True，则使用self.server.spop；如果为False，则使用self.server.lpop
REDIS_START_URLS_KEY = '%(name)s:start_urls'
````



## 二、初步理解

### 1、connection.py

````
get_redis_from_settings方法：
	1. 读取配置文件，放入字典中，调用get_redis并传入字典
	
get_redis方法：
	1. 默认使用redis.StrictRedis创建连接
	2. 返回一个redis连接对象
````



### 2、defaults.py

配置一览



### 3、dupefilter.py

去重规则

````
1.from_craler方法调用from_settings方法并传入scrapy.crawler.Crawler对象
2.from_settings方法内部获取redis连接对象，生成一个用于保存去重规则的key，实例化RFPDupeFilter。
3.request_fingerprint方法：根据url生成固定长度的字符串
4.request_seen方法：把request_fingerprint方法生成的字符串放入无序集合中。
````



### 4、picklecompat.py

pickle序列化



### 5、piplines.py

持久化，把序列化之后的对象放入redis中

````
1.from_crawler方法：调用from_settings
2.from_settings方法：读取配置文件获取key、序列化参数保存在字典中，实例化当前这个类
3.process_item方法：启动线程执行_process_item
4._process_item方法：key和序列化后的对象使用rpush放入redis列表中

````



### 6、queue.py

队列：有序集合、先进先出列表、后进献出列表

````
PriorityQueue类：
	push：有序集合，ZADD添加
	pop：zrange()		 
		 按照索引范围获取name对应的有序集合的元素
		 zremrangebyrank()
		 根据排行范围删除
		 反序列化
		 
LifoQueue类：
	后进先出
	push:lpush()
	pop:blpop()将多个列表排列，按照从左到右去pop对应列表的元素
	
FifoQueue类：
	先进先出
	push:lpush()
	pop:brpop()
````



### 7、scheduler.py

调度器

````
1. from_crawler方法：
	调用from_settings读取配置，实例化当前类并返回
2. enqueue_request方法：
	判断是否做去重且url是否未见过，放入队列
3. next_request方法：
	设置超时时间，取出request
````



### 8、spiders.py

````
1. RedisMixin类
	setup_redis：进行redis连接，绑定信号
	start_requests：调用next_requests
	next_requests：从redis队列中获取请求
	make_request_from_data：返回一个request的实例对象
	schedule_next_requests：引擎调度request，进行爬去的初始化
	spider_idle：等待调度request
	
2. RedisSpider类：
	调用父类的构造方法和setup_redis，返回一个RedisSpider的对象
	
3. RedisCrawlSpider类：
	调用父类的构造方法和setup_redis，返回一个RedisCrawlSpider类的对象
````





