from . import global_settings
import importlib
import os

class Setting():
    def __init__(self):
        #设置默认配置全局变量
        for key in dir(global_settings):
            if key.isupper():
                value = getattr(global_settings, key)
                setattr(self, key, value)

        #设置自定义全局变量
        m = importlib.import_module(os.environ['USER_SETTINGS'])
        for key in dir(m):
            if key.isupper():
                value = getattr(m, key)
                setattr(self, key, value)

settings = Setting()