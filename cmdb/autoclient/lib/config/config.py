#! -*-code:utf8-*-

from . import global_settings
import os
import importlib

class Settings(object):
    def __init__(self):

        # ====== 找到默认配置 ======
        #循环便利global_settings里面的变量名，其中大写的是全局变量
        for name in dir(global_settings):
            #如果是大写
            if name.isupper():
                #获取变量的值
                #getattr获取属性的值，在这里是获取全局变量的值
                value = getattr(global_settings, name)
                #把全局变量设置到类的变量中，供程序调用
                setattr(self, name, value)

        #====== 找到自定义配置 ======
        #获取环境变量名为USER_SETTINGS的值，就是config.settings
        settings_module = os.environ.get('USER_SETTINGS')
        if not settings_module:
            return
        #根据字符串导入模块，导入config/settings.py
        m = importlib.import_module(settings_module)
        #循环遍历变量名
        for name in dir(m):
            #如果是大写
            if name.isupper():
                #获取变量的值
                value = getattr(m, name)
                #把变量和值设置到类的变量
                setattr(self, name, value)




#实例化供程序调用
settings = Settings()

