# import importlib
#
#
# path = 'scrapy.middlerware.C1'
#
# md,cls_name = path.rsplit('.', maxsplit=1)
# print(cls_name)
#
# importlib.import_module(md)


class Foo(object):
    def __getitem__(self, item):
        return "123"

    def __setitem__(self, key, value):
        pass

    def __delitem__(self):
        pass

obj = Foo()
# b = obj['k1']
# print(b)

# obj['k1'] = 666
#
# del obj['k1']

import redis
import time
import hashlib
import settings
import json

def gen_random_str():

    md5 = hashlib.md5()
    md5.update(str(time.time()).encode('utf-8'))
    return md5.hexdigest()


class CacheSession(object):

    # 静态字段
    container = {}

    def __init__(self, handler):
        self.handler = handler
        self.session_exp = settings.SESSION_EXPIRE_TIME
        self.session_id = settings.SESSION_ID
        self.initial()

    def initial(self):
        # 先获取客户端的cookie (作为container的key)
        # 如果用继续使用
        # 如果没有就生成随机字符串，放入container
        # 最后不管有没有重新生成，cookie都过时时间都加上
        client_random_str = self.handler.get_cookie(self.session_id)
        if client_random_str and client_random_str in self.container:
            self.random_str = client_random_str
        else:
            self.random_str = gen_random_str()
            self.container[self.random_str] = {}
        self.handler.set_cookie(self.session_id, self.random_str, expires=time.time() + self.session_exp)


    def __getitem__(self, item):
        return self.container[self.random_str].get(item)

    def __setitem__(self, key, value):
        self.container[self.random_str][key] = value

    def __delitem__(self, key):
        if key in self.container[self.random_str]:
            del self.container[self.random_str][key]

class RedisSession(object):



    def __init__(self, handler):
        self.handler = handler
        self.session_exp = settings.SESSION_EXPIRE_TIME
        self.session_id = settings.SESSION_ID
        self.initial()

    @property
    def conn(self):
        conn = redis.Redis(host='192.168.0.10', port=6379)
        return conn

    def initial(self):
        # 先获取客户端的cookie (作为container的key)
        # 如果用继续使用
        # 如果没有就生成随机字符串，放入container
        # 最后不管有没有重新生成，cookie都过时时间都加上
        client_random_str = self.handler.get_cookie(self.session_id)

        if client_random_str and self.conn.exists(client_random_str):
            self.random_str = client_random_str
        else:
            self.random_str = gen_random_str()

        self.handler.set_cookie(self.session_id, self.random_str, expires=time.time() + self.session_exp)
        self.conn.expire(self.random_str, self.session_exp)


    def __getitem__(self, item):
        data_str =  self.conn.hget(self.random_str, item).decode('utf-8')

        if data_str:
            return json.loads(data_str)
        else:
            return None

    def __setitem__(self, key, value):

        self.conn.hset(self.random_str, key, json.dumps(value))

    def __delitem__(self, key):
        self.conn.hdel(self.random_str, key)

class SessionFactory(object):

    @staticmethod
    def get_session():
        import settings
        md, cls_name = settings.SESSION_ENGINE.rsplit('.', maxsplit=1)
        import importlib
        md = importlib.import_module(md)
        cls = getattr(md, cls_name)
        return cls
