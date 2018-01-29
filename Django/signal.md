# Django 信号

## 一、简介

&emsp;&emsp;Django 提供信号调度，在框架执行到某处时，让解偶的应用程序得到通知。从而可以做自定义的操作。



## 二、信号种类

````Python
# ############################ Model signals ###########################
    pre_init                    # django的model执行其构造方法前，自动触发
    post_init                   # django的model执行其构造方法后，自动触发
    pre_save                    # django的model对象保存前，自动触发
    post_save                   # django的model对象保存后，自动触发
    pre_delete                  # django的model对象删除前，自动触发
    post_delete                 # django的model对象删除后，自动触发
    m2m_changed                 # django的model中使用m2m字段操作第三张表（add,remove,clear）前后，自动触发
    class_prepared              # 程序启动时，检测已注册的app中model类，对于每一个类，自动触发
    
# ########################## Management signals #########################
    pre_migrate                 # 执行migrate命令前，自动触发
    post_migrate                # 执行migrate命令后，自动触发
    
# ####################### Request/response signals ######################
    request_started             # 请求到来前，自动触发
    request_finished            # 请求结束后，自动触发
    got_request_exception       # 请求异常后，自动触发

# ############################# Test signals ############################
    setting_changed             # 使用test测试修改配置文件时，自动触发
    template_rendered           # 使用test测试渲染模板时，自动触发
    
# ########################## Database Wrappers #########################    
    connection_created          # 创建数据库连接时，自动触发
````



## 三、使用

**方式一：**

````python
from django.core.signals import request_started


def callback(sender, **kwargs):
  	'''
  	请求到来前执行
  	'''
    print('request_started signal callback')

# 信号连接
request_started.connect(callback)
````

<br>

**方式二：**

装饰器形式使用信号

````python
from django.core.signals import request_started
from django.dispatch import receiver


@receiver(request_started)
def callback(sender, **kwargs):
    print('request_started signal callback')

````

<br>

**自定义：**

```python
# 装饰器
import django.dispatch

# 自定义信号
my_signal = django.dispatch.Signal(providing_args=["name", "email"])

# 回调函数
def callback(sender, **kwargs):
    print(sender, kwargs)
    print("callback")
    
# 连接
my_signal.connect(callback)

# ############################## views.py ##############################

def test(request):
    ...
    
    my_signal.send(sender='test', name='a', email='b')
    
    ...
    
    return Httpresponse('test')
```

