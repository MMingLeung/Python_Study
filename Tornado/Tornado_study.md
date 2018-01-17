# Tornado 学习

## 一、框架对比

| 框架名称/功能 | Socket  | 中间件  | 路由  系统 | 视图  函数 | ORM  | 模版引擎 | 缓存   | 信号   | Form | Admin | Csrf | Xss  |
| ------- | ------- | ---- | :----- | ------ | ---- | ---- | ---- | ---- | ---- | ----- | ---- | ---- |
| Django  | Wsgiref | 有    | 有      | 有      | 有    | 有    | 有    | 有    | 有    | 有     | 有    | 有    |
| Tornado | 自带异步非阻塞 | 无    | 有      | 有      | 无    | 有    | 无    | 无    | 无    | 无     | 有    | 无    |



## 二、简单使用

````python
#/usr/bin/env python
# -*- coding:utf-8 -*-
import tornado.web


# ######################## 视图函数开始 ########################
class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write('S1')


class HomeHandler(tornado.web.RequestHandler):
    def get(self, nid, *args, **kwargs):
        url = self.application.reverse_url('n2', 5123)
        print(nid, url)
# ######################## 视图函数结束 ########################

# ######################## 路由系统开始 ########################
application = tornado.web.Application([
    (r'/index', IndexHandler),
    (r'/home/(\d+)', HomeHandler),
])

# 路由补充
# 检查域名，匹配到则优先运行
application.add_handlers('www.s4.com',
    [(r'/index', IndexHandler, {}, 'n1'),
    (r'/home/(\d+)', HomeHandler, {}, 'n2'),]
)
# ######################## 路由系统结束 ########################

if __name__ == '__main__':
	# 绑定端口
    application.listen(8880)
    # 启动
    tornado.ioloop.IOLoop.instance().start()
````



## 三、配置文件

````python
settings = {
  	# 模版路径
    'template_path': 'templates',
  	# 静态文件地址
    'static_path': 'static',
  	# 静态文件前缀
    'static_prefix': '/sss/',
  	# CSRF Token
    'xsrf_token': True,
  	# 加密 cookie
    'cookie_secret': 'aaa',
  	# 使用官方验证 cookie 装饰器，如验证失败自动跳转的地址
    'login_url': '/login',
}

....


application = tornado.web.Application([
    ...
    ...
], **settings)
````



## 四、获取请求中的参数

````python
# 从 GET 取值
self.get_query_argument('xx')
self.get_query_arguments('xx')

# 从 POST 取值
self.get_body_argument('xx')
self.get_body_arguments('xx')

# 从 GET 和 POST 中取值
self.get_argument('xx')
self.get_arguments('xx')
````



## 五、XSRF(CSRF)

```html
// html
{% raw xsrf_form_html() %}
```



## 六、Cookie

```python
# 设置
self.set_secure_cookie('cookie_name', value, expires=ctime)

# 获取
self.get_secure_cookie('cookie_name')

#####################################################################
# 官方 cookie 验证装饰器
from tornado.web import authenticated


# 必须重写 get_current_user 方法(建议使用多继承实现)
def get_current_user(self):
    return self.get_secure_cookie('cookie_name')
 
```



## 七、模版引擎

````Html
// 引用静态文件 
<link rel="stylesheet" href="{{ static_url('a.css')}}">

// 使用模版
{% extends 'layout.html'%}

// 循环
{% for item in data_list %}
{% end %}
````

