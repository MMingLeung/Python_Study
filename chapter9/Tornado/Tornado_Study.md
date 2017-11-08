# Tornado Study

## 一、与Django区别

tornado :

​                     socket : 有

​                     中间件： 无

​                     路由系统： 有

​                     视图函数： 有

​                     ORM : 无，使用SQLACHEMY

​                     模板引擎：有

​                     simple_tag : uimethod, uimodule

​                     cookie :  有

​                     session : 无

​                     csrf、xss ：有

​		

Django:

​                    socket: 无，wsgiref把请求交给框架

​                    中间件 ： 有

​                    路由系统 ： 有

​                     视图函数： 有 

​                     ORM框架 ： 有

​                     模板引擎： 有

​                     其它 ：缓存、信号、Form、ModelForm、Admin、simpletamplate、cookie、session 



# 二、基本使用

### 1、配置

```
settings = {

    # 实际模版文件路径
    'template_path':'part2/tpl',
    # 实际静态文件文件路径
    'static_path':'part2/static',
    # 静态文件前缀，用于html
    'static_url_prefix':'/static/',
	# 是否使用csrf
    'xsrf_cookies':True,
    # 加密cookie的盐
    'cookie_secret':'dqwd',
    # 使用authenticated装饰器，如果未成功获取cookie自动跳转到该地址
    'login_url':'/login',
    # 自定义方法
    'ui_methods':mt,
    'ui_modules':md,
}
```



### 2、路由系统

````python
application = tornado.web.Application([
    # 'n1'用于反向生成
    (r'/index', LoginHandler,{},'n1'),
], **settings)
````





###  3、视图函数

流程：

1. 定义get/post函数，接收对应请求
2. 获取请求的参数self.get_argument()、self.get_arguments()、slef.get_query_argument()
3. 渲染页面self.render('login.html', msg="") msg是回传的参数 self.redirect
4. 加密cookie设置self.set_secure_cookie('some_strs', user, expires=v) 
5. cookie获取self.get_cookie('some_strs')
   1. 使用自带的装饰器authenticated，需要定义get_current_user方法

````
from tornado.web import RequestHandler
from tornado.web import authenticated

class MattRequestHandler(object):
    def get_current_user(self):
        return self.get_cookie('lalal')


class LoginHandler(MattRequestHandler, RequestHandler):

    def get(self, *args, **kwargs):
        # 反向生成url
        url1 = self.application.reverse_url('n1')
        self.render('login.html', msg="")

    def post(self, *args, **kwargs):
        # get and  post请求的参数
        # self.get_argument()
        # self.get_arguments()

        # get 请求的参数
        # slef.get_query_argument()

        user = self.get_argument('user')
        pwd = self.get_argument('pwd')
        if user =='matt' and pwd == '123':
            import time
            v = time.time() + 300
            self.set_secure_cookie('lalal', user, expires=v)
            self.redirect('/index')
        else:
            self.render('login.html', msg='账号或密码错误')

class IndexHandler(MattRequestHandler, RequestHandler):


    @authenticated
    def get(self, *args, **kwargs):
        # if not self.get_cookie('lalal'):
        #     self.redirect('/login')
        #     return None
        # self.render('index.html')
        data_list = [
            {'title':'a1', 'a':1},
            {'title':'a2', 'a':2},
            {'title':'a3', 'a':3},
        ]
        self.render('index.html', data_list=data_list)

````



### 4、模板渲染

1. 继承模版，同django
2. For 循环
3. 取值
4. uimethod ，类似simpletag， 在页面显示函数的返回值
5. uimodule，在页面显示类里面所有函数的返回值，用于作CSS、JS、HTML相关设置

```

//layout.html
...
{% block content %}
{% end %}
...

//index.html
{% extends 'layout.html' %}

{% block content %}
<ul>
    {% for item in data_list%}
    <li>{{ item['title'] }} = {{ item['a'] }}</li>
    {% end %}
</ul>
<!--uimethod-->
<!--{{ tab() }}-->
{% raw tab() %}


<!--uimodule-->
{% module Custom(123) %}


{% end %}

```

