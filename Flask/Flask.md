# Flask

## 一、基本应用

````Python
from flask import Flask

# 实例化传入一个名字，通常使用文件名
app = Flask(__name__)

# 路由系统
@app.route('/')
def hello_world():
    return "Hello World!"

if __name__ == '__main__':
    app.run()
    
````

<br>

Flask可以传入的参数：

````
static_path=None, # 停用
static_url_path=None, # 必需／开头的，设置前缀
static_folder='static',  # 静态目录路径
template_folder='templates', # 模板目录路径
instance_path=None, # 当前根目录 + \instance
instance_relative_config=False, # 去上面路径找配置文件
root_path=None # 根目录， 如果上面是False就去根目录找配置文件
````

<br>

## 二、配置文件

````python
default_config = ImmutableDict({
        'DEBUG':                                get_debug_flag(default=False),
        'TESTING':                              False,
        'PROPAGATE_EXCEPTIONS':                 None,
        'PRESERVE_CONTEXT_ON_EXCEPTION':        None,
        'SECRET_KEY':                           None,
        'PERMANENT_SESSION_LIFETIME':           timedelta(days=31),
        'USE_X_SENDFILE':                       False,
        'LOGGER_NAME':                          None,
        'LOGGER_HANDLER_POLICY':               'always',
        'SERVER_NAME':                          None,
        'APPLICATION_ROOT':                     None,
        'SESSION_COOKIE_NAME':                  'session',
        'SESSION_COOKIE_DOMAIN':                None,
        'SESSION_COOKIE_PATH':                  None,
        'SESSION_COOKIE_HTTPONLY':              True,
        'SESSION_COOKIE_SECURE':                False,
        'SESSION_REFRESH_EACH_REQUEST':         True,
        'MAX_CONTENT_LENGTH':                   None,
        'SEND_FILE_MAX_AGE_DEFAULT':            timedelta(hours=12),
        'TRAP_BAD_REQUEST_ERRORS':              False,
        'TRAP_HTTP_EXCEPTIONS':                 False,
        'EXPLAIN_TEMPLATE_LOADING':             False,
        'PREFERRED_URL_SCHEME':                 'http',
        'JSON_AS_ASCII':                        True,
        'JSON_SORT_KEYS':                       True,
        'JSONIFY_PRETTYPRINT_REGULAR':          True,
        'JSONIFY_MIMETYPE':                     'application/json',
        'TEMPLATES_AUTO_RELOAD':                None,
    })
````

<br>

### 1、设置配置文件的方法

````python
# 1、修改字典形式
app.config['DEBUG'] = True
app.config.update({})

# 2、通过py文件
app.config.from_pyfile('settings.py')

# ############ settings.py ############
DEBUG = True
# #####################################

# 3、环境变量
import os
os.environ['eeee'] = 'settings'
app.config.from_envvar("eeee") # 内部最后调用from_pyfile

# 4、json文件导入
app.config.from_json("JSON")

# 5、对象导入
app.config.from_object('settings.TestingConfig')
# setting.py
class Config:
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
# #####################################


````

<br>

## 三、路由系统

### 1、通过装饰器实现

````python
@app.route('/index/<username>')
@app.route('/post/<int:post_id>')
@app.route('/post/<float:post_id>')
@app.route('/post/<path:path>')
@app.route('/index', methods=['GET', 'POST'])

# 本质调用了add_url_rule函数
# 可以写成
@app.add_url_rule('/', view_func='函数名', endpoint='反向生成的url名字', methods=['GET', 'POST'])
````

<br>

### 2、路由系统中的url参数传递

````
# 默认只支持以下的形式
DEFAULT_CONVERTERS = {
    'default':          UnicodeConverter,
    'string':           UnicodeConverter,
    'any':              AnyConverter,
    'path':             PathConverter,
    'int':              IntegerConverter,
    'float':            FloatConverter,
    'uuid':             UUIDConverter,
}

````

<br>

### 2.1、扩展支持正则表达式

````Python
from werkzeug.routing import BaseConverter
class TestConverter(BaseConverter):
    '''
    自定义url匹配规则
    '''
    def __init__(self, map, regex):
        super(TestConverter, self).__init__(map)
        self.regex = regex

    def to_python(self, value):
        '''
        返回给视图函数的值
        '''
        return int(value)

    def to_url(self, value):
        '''
        使用url_for反向生成url,使用该函数处理，返回值用于生成url的参数
        :param value: 
        :return: 
        '''
        val = super(TestConverter, self).to_url(value)
        return val
        
app.url_map.converters['test'] = TestConverter


# 使用例子
@app.route('/test/<test("\d+"):nid>')
def hello_world(nid):
    print(url_for('test',nid='111')) # 反向生成/index/111+传递的参数nid
    return 'Hello World!'
````

<br>

### 3、反向生成URL

根据endpoint生成，默认是函数名称。

````
from flask import url_for
@app.add_url_rule('/', view_func=hello_world, endpoint='xxx', methods=['GET', 'POST'])
 def hello_world():
     url = url_for('xxx')
     return 'Hello World!'
````

<br>

## 四、视图函数

### 1、CBV

#### 1、方法1 继承views.View

````python
def auth(func):
    def inner(*args, **kwargs):
        print('begin')
        result = func(*args, **kwargs)
        print('end')
        return result
    return inner

class IndexView(views.View):
    methods = ["GET",]
    decorators = [auth,] # 装饰器

    def dispatch_request(self):
        print('index')
        return 'IndexView dispatch'
app.add_url_rule('/indexview', view_func=IndexView.as_view(name='indexview'))
````

<br>

#### 2、方法2 继承view.MethodView

````Python
class IndexView(views.MethodView):
    methods = ["GET",]
    decorators = [auth,]

    def get(self):
        return "GET"

    def post(self):
        return "POST"
app.add_url_rule('/indexview', view_func=IndexView.as_view(name='indexview'))
````

<br>

## 五、模板

使用jinja2模板，使用方法与django基本一致

#### 1、自定义模板

`````[
# 定义一个函数
def test_func():
    return '<h1>test_func</h1>'

# 在视图函数中使用 render_template('login.html', func =test_func)传递

# 前端 {{ func()|safe }}
`````

<br>

## 六、Session

在请求中储存用户信息

<br>

### 1、使用自带Session

<br>

````
from flask import Flask, views, render_template, session

@app.route('/test2')
def hello_world(id):
    print(session['username'])
    return "Hello World!"
    
@app.route('/test1')
def hello_world(id):
    session['username'] = 'lalala'
    return "Hello World!"
app.secret_key = 'session'
````

<br>

### 2、自定义Session

<br>

Session 处理流程：

1. 请求过来，通过路由系统找到匹配的视图函数
2. 在视图函数中对 session 进行操作
3. 执行 SessionInterface 中的 open_session 方法，执行以下操作
   1. 获取 sid(也称 session_id  cookie)
   2. 根据 sid 在 session 中获取响应的值
   3. 封装 sid 和获取的值到 Session 对象中
   4. 如果上述其中不能获取或无法经过签名验证则返回只含 sid 的 Session 对象
4. 返回用户之前，执行 SessionInterface 中的 save_session 方法
   1. 获取响应所需的参数
   2. 获取 Session 对象中键值对部分，并序列化放入内存 or Redis 中
   3. 回写 cookie 到响应对象中

<br>

````Python
class MySession(dict, SessionMixin):
  	'''
  	initial：用于需要保存信息，字典格式
  	sid：加密的随机字符串
  	'''
    def __init__(self, initial=None, sid=None):
        self.sid = sid
        self.initial = initial
        super(MySession, self).__init__(initial or ())

class MySessionInterface(SessionInterface):
    session_class = MySession
    # 用于把session信息保存在内存中（现使用redis）
    container = {}

    def __init__(self):
        import redis
        self.redis = redis.Redis()

    def _generate_sid(self):
        return str(uuid.uuid4())

    def _get_signer(self, app):
        if not app.secret_key:
            return None
        return Signer(app.secret_key, salt='flask-session',
                      key_derivation='hmac')

    def open_session(self, app, request):
        """
        app:flask对象
        request:请求所有信息
        """
        # 获取随机字符串
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
          	# 没有就生成
            sid = self._generate_sid()
            # 返回一个字典
            return self.session_class(sid=sid)
		
        # 如果sid有值，解密
        signer = self._get_signer(app)
        try:
            sid_as_bytes = signer.unsign(sid)
            sid = sid_as_bytes.decode()
        except BadSignature:
          	# 解密失败，重新创建，返回
            sid = self._generate_sid()
            return self.session_class(sid=sid)

        # session保存在redis中
        # val = self.redis.get(sid)
        # session保存在内存中
        val = self.container.get(sid)

        if val is not None:
            try:
                data = json.loads(val)
                return self.session_class(data, sid=sid)
            except:
                return self.session_class(sid=sid)
        return self.session_class(sid=sid)

    def save_session(self, app, session, response):
        """
        session:MySession对象包含随机字符串sid和一个字典
        """
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        expires = self.get_expiration_time(app, session)

        val = json.dumps(dict(session))

        # session保存在redis中
        # self.redis.setex(name=session.sid, value=val, time=app.permanent_session_lifetime)
        # session保存在内存中
        self.container.setdefault(session.sid, val)
		# 签名
        session_id = self._get_signer(app).sign(want_bytes(session.sid))

        response.set_cookie(app.session_cookie_name, session_id,
                            expires=expires, httponly=httponly,
                            domain=domain, path=path, secure=secure)        
````



## 七、蓝图

让程序结构更加清晰

<br>

````python
'''
手动创建类似蓝图的功能

目录结构：
/—run.py
/— project/
		|— views/
		|— account.py
	|— __init__.py
'''

# ##################### run.py #####################
from project1 import app # 1.导入__init__.py所有代码

if __name__ == '__main__':
    app.run() 
    
# ##################### __init__.py #####################
from flask import Flask

app = Flask(__name__)
# 执行到这里，还没有执行account.py
# 还需要导入account
from .views import account    
    
    
# ##################### account.py #####################
from flask import render_template
from .. import app

@app.route("/")
def login():
    return render_template('login.html')


````



<br>

````Python
'''
蓝图
/— run.py
/— project/
	|— views/
		|— account.py
	|— __init__.py
'''
# ##################### run.py #####################
from project import app


if __name__ == '__main__':
  app.run()

# ##################### __init__.py #####################
from flask import Flask


app = Flask(__name__)
# 注册蓝图
from .views.account import account
app.register_blueprint(account)

# ##################### account.py #####################
from flask import render_template, Blueprint


# 创建蓝图
# url_prefix 前缀,template_folder 模版文件夹, static_folder 静态文件夹
account = Blueprint('account', __name__, url_prefix='/abc', template_folder='', static_folder='')

@account.route("/")
def login():
    return "login"
````



## 八、Message

保存数据的集合，使用一次就删除。

````Python
from flask import Flask, flash, request, get_flashed_messages

app = Flask(__name__)
app.secret_key = 'some_secret'


@app.route('/')
def get_flash():
    messages = get_flashed_messages()
    print(messages)
    return "get"


@app.route('/set')
def set_flash():
    v = request.args.get('p')
    flash(v)
    return 'set'


if __name__ == "__main__":
    app.run()
````



## 九、中间件

````Python
class MiddleWare:
    def __init__(self,wsgi_app):
        self.wsgi_app = wsgi_app
 
    def __call__(self, *args, **kwargs):
    	# 先执行
      	# ...
        # 后执行原来的wsgi_app的__call__方法
        return self.wsgi_app(*args, **kwargs)
		

if __name__ == "__main__":
  	# 请求过来执行app对象的__call__方法，改为中间件的__call__方法
    app.wsgi_app = MiddleWare(app.wsgi_app)
````

