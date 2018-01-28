# Django 中间件

## 一、简介

<br>

**定义：对所有请求作批量操作**

<br>

应用： SESSION、缓存、黑名单



## 二、自定义中间件

<br>

**流程图：**

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/django_middleware_process.png?raw=true)

<br>

**代码：**

````python
from django.utils.deprecation import MiddlewareMixin


'''
* 类必须继承 MiddlewareMixin
----------------------------------------------------
含有以下方法：
1.process_request (常用)
2.process_view
3.process_exception
4.process_response (常用)
5.process_template_response (少用)
----------------------------------------------------
执行顺序：
1. process_request_1 ... process_request_2 -> 2/

2. process_view_1 ... process_view_n -> 3/  
# process_view 如有返回视图函数的调用结果跳至 6

3. 视图函数 view  -> / 
# 如有报错跳至 4
# 如返回的是一个对象，对象含有 render 方法，跳至 5

4. process_exception_n ... process_exception_1 -> 6/

5. process_template_response_n .. process_template_response_1 -> 6/
# 如有报错跳至 4

6. process_response_n ... process_response_1 -> 7/

7. 客户端
'''
class MyMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        print("process_request")

    def process_view(self, request, callback, callback_args, callback_kargs):
        print(callback, callback_args, callback_kargs)
        print("process_view1")
        # return callback(request, *callback_args, **callback_kargs)

    def process_exception(self, request, exception):
        print(exception)
        print("process_exception1")
        return HttpResponse('error')

    def process_response(self, request, response):
        print("process_response")
        return response


    def process_template_response(self, request, response):
        print('process_template_response1')
        return response
````

