#!/usr/bin/env python
# -*- coding:utf-8 -*-
import hashlib
import time
import json
from lib.CUSTOMIZED_SESSION import settings


def gen_random_key():
    md5 = hashlib.md5()
    md5.update(str(time.time()).encode('utf-8'))
    return md5.hexdigest()

class CachedSession:

    container = {}

    def __init__(self, handler):
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
        # self.handler.get_cookie_secret()
        if self.container[self.client_random_str].get(item):
            return self.container[self.client_random_str][item]
        return None

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
        # 取原来cookie
        client_random_str = self.handler.get_cookie(self.session_id)
        if client_random_str and self.conn.exists(client_random_str):
            self.client_random_str = client_random_str
        else:
            # 客户端没有cookie或是伪造的，给客户端设置 cookie
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

class SessionFactory:

    @staticmethod
    def get_session():
        import importlib
        from lib.CUSTOMIZED_SESSION import settings
        path, class_name = settings.SESSION_ENGINE.rsplit('.', 1)
        module_ = importlib.import_module(path)
        class_ = getattr(module_, class_name)
        return class_