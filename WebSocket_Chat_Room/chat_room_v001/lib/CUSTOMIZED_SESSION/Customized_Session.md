# 自定义 Session 组件

## 一、简介

&emsp;&emsp;为 Tornado 框架设计 Session 组件。包括缓存 Session 和 Redis Session，通过工厂模式选择 Session 组件，在 Tornado 视图函数的钩子函数 initialize 中实例化 Session，Session 的构造函数则通过 Tornado handler 对象对 cookie 进行操作，通过 \_\_getitem\_\_ , \_\_setitem\_\_ , \_\_delitem\_\_ 操作缓存 / Redis 中的值。



## 二、架构

- Session 工厂
- Tornado 视图函数 initialize 方法



## 三、代码

#### Session 组件

````python
# 配置文件
# 
SESSION_ENGINE = 'my_session.CachedSession' # CachedSession or RedisSession
# 超时时间
EXPIRE_TIME = 300
# 浏览器的 cookie id
SESSION_ID = '__session_id__'
````



````python
# 工厂类
'''
根据配置文件选择 Session 组件
'''
import importlib
from session_code import settings
    
    
class SessionFactory:
    @staticmethod
    def get_session():

        path, class_name = settings.SESSION_ENGINE.rsplit('.', 1)
        module_ = importlib.import_module(path)
        class_ = getattr(module_, class_name)
        return class_
````



````python
import hashlib
import time
import json
from study_round2.simple_1.session_code import settings


def gen_random_key():
    md5 = hashlib.md5()
    md5.update(str(time.time()).encode('utf-8'))
    return md5.hexdigest()

class CachedSession:
	'''
	缓存 Session
	'''
    # 缓存 Session
    container = {}

    def __init__(self, handler):
      	'''
      	实例化时执行以下操作：
      		1、获取原来 cookie 值且在本地缓存字典中，无则创建。
      		2、通过 tornado handler 对象写入 cookie 中。
      	通过 __getitem__、__setitem__、__delitem__ 对保存在缓存中的字典执行相应操作。
      	'''
        
        self.handler = handler
        self.session_id = settings.SESSION_ID
        self.expire = settings.EXPIRE_TIME

        self.initial()

    def initial(self):
        # 取原来cookie
        client_random_str = self.handler.get_cookie(self.session_id)
        if client_random_str and client_random_str in self.container:
            self.client_random_str = client_random_str
        else:
            # 客户端没有cookie或是伪造的，给客户端设置 cookie
            self.client_random_str = gen_random_key()
            self.container[self.client_random_str] = {}

        self.handler.set_cookie(self.session_id, self.client_random_str, expires=time.time()+settings.EXPIRE_TIME)


    def __setitem__(self, key, value):
        self.container[self.client_random_str][key] = value

    def __getitem__(self, item):
        return self.container[self.client_random_str][item]

    def __delitem__(self, key):
        if key in self.container:
            del self.container[self.client_random_str][key]


class RedisSession:
    def __init__(self, handler):
        self.handler = handler
        self.session_id = settings.SESSION_ID
        self.expire = settings.EXPIRE_TIME

        self.initial()

    @property
    def conn(self):
        import redis
        r = redis.Redis(host='192.168.0.150', port=6379)
        return r

    def initial(self):
        client_random_str = self.handler.get_cookie(self.session_id)
        if client_random_str and self.conn.exists(client_random_str):
            self.client_random_str = client_random_str
        else:
            self.client_random_str = gen_random_key()

        expire_time = time.time()+settings.EXPIRE_TIME
        self.handler.set_cookie(self.session_id, self.client_random_str, expires=expire_time)
        self.conn.expire(self.client_random_str, expire_time)

    def __setitem__(self, key, value):
        self.conn.hset(self.client_random_str, key, json.dumps(value))

    def __getitem__(self, item):
        data = self.conn.hget(self.client_random_str, item)
        if not data:
            return None
        return json.loads(data)


    def __delitem__(self, key):
        self.conn.hdel(self.client_random_str, key)
````



#### Tornado 登录功能实现 Session

````Python
class LoginSessionHandler(tornado.web.RequestHandler):
    def initialize(self):
        # 钩子函数 首先执行
        class_ = SessionFactory.get_session()
        # 实例化 session 类的对象
        self.session = class_(self)

    def get(self, *args, **kwargs):
        self.render('login_session.html')

    def post(self, *args, **kwargs):
        username = self.get_argument('username')
        password = self.get_argument('password')
        if username == 'a' and password == 'a':
            self.session['user'] = username

            a = self.session.container[self.session.client_random_str]['user']
            print(a)

            self.write('ok')
        else:
            self.redirect('/login')
````





