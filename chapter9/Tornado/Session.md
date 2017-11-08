# 自定义Session 

# 一、简述

Tornado中没有Session，需要为其自定制

# 二、Session组件本质

根据配置文件，使用字符串形式导入模块，以反射形式获取类，实例化之后调用类里面的\_\_getitem\_\_、\_\_setitem\_\_、\_\_delitem\_\_对属性的设置



### 1、配置

````
# 选择使用哪一种形式保存Session
SESSION_ENGINE = 'session_code.CacheSession'

SESSION_ID = "__session_id__"

SESSION_EXPIRE_TIME = 300
````



### 2、具体逻辑

````
# 保存在内存中的session
class CacheSession(object):
    # 静态字段
    container = {}
	
    def __init__(self, handler):
    	# 在视图函数的的钩子中传入当前handler对象
        self.handler = handler
        # 过期时间
        self.session_exp = settings.SESSION_EXPIRE_TIME
        # 自定义session id名字
        self.session_id = settings.SESSION_ID
        # 初始化函数
        self.initial()

    def initial(self):
        # 先获取客户端的cookie (作为container的key)
        # 如果有，继续使用
        # 如果没有，就生成随机字符串，放入container
        # 最后不管有没有重新生成，cookie时间都加上
        
        # 获取
        client_random_str = self.handler.get_cookie(self.session_id)
        if client_random_str and client_random_str in self.container:
            self.random_str = client_random_str
        else:
            self.random_str = gen_random_str()
            self.container[self.random_str] = {}
        self.handler.set_cookie(self.session_id, self.random_str, expires=time.time() + self.session_exp)


    def __getitem__(self, item):
    	# 用于视图函数根据key获取session的value
        return self.container[self.random_str].get(item)

    def __setitem__(self, key, value):
    	# 用于视图函数根据key设置session的value
        self.container[self.random_str][key] = value

    def __delitem__(self, key):
    	# 用于视图函数根据key删除session的value
    	# 防止报错先判断key是否在字典中
        if key in self.container[self.random_str]:
            del self.container[self.random_str][key]
````



````
# 保存在redis中的session
class RedisSession(object):

    def __init__(self, handler):
        self.handler = handler
        self.session_exp = settings.SESSION_EXPIRE_TIME
        self.session_id = settings.SESSION_ID
        self.initial()

	# 连接redis
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
		# 判断是否存在
        if client_random_str and self.conn.exists(client_random_str):
            self.random_str = client_random_str
        else:
            self.random_str = gen_random_str()
		# 自身Tornado对象设置过气时间
        self.handler.set_cookie(self.session_id, self.random_str, expires=time.time() + self.session_exp)
        #设置过期时间
        self.conn.expire(self.random_str, self.session_exp)


    def __getitem__(self, item):
    	# 获取的数据是bytes格式，需要解码
        data_str =  self.conn.hget(self.random_str, item).decode('utf-8')
		# 如果能获取数据，反序列化获取内容
        if data_str:
            return json.loads(data_str)
        else:
            return None

    def __setitem__(self, key, value):
		# 设置
        self.conn.hset(self.random_str, key, json.dumps(value))

    def __delitem__(self, key):
    	# 删除
        self.conn.hdel(self.random_str, key)
````



````
# 入口
class SessionFactory(object):

    @staticmethod
    def get_session():
        import settings
        md, cls_name = settings.SESSION_ENGINE.rsplit('.', maxsplit=1)
        import importlib
        md = importlib.import_module(md)
        cls = getattr(md, cls_name)
        return cls
        
#调用
class IndexHandler(RequestHandler):
    def initialize(self):
        # 钩子
        print('initial')
        # ######### 获取类 #########
        cls = SessionFactory.get_session()
        # ######### 实例化 #########
        self.session = cls(self) # 把IndexHandler对象传入，可以使用其方法，如set_cookie等


    def get(self):
    	# ######### 获取session里面的user值，判断是否合法 #########
        user = self.session['user']
        if user:
            self.write("欢迎登录")
 
#######################################
class LoginHandler(RequestHandler):
    def initialize(self):
        # 钩子
        print('initial')
        # ######### 获取类 #########
        cls = SessionFactory.get_session()
        # ######### 实例化 #########
        self.session = cls(self) # 把IndexHandler对象传入，可以使用其方法，如set_cookie等


    def get(self):
        self.render('login.html')

    def post(self):
        user = self.get_argument('user')
        pwd = self.get_argument('pwd')
        if user == 'matt' and pwd == '123':
        	# ######### 账号密码匹配，自定义的信息写入session #########
            self.session['user'] = user
            self.redirect('/index')
        else:
            self.redirect('/login')
````



