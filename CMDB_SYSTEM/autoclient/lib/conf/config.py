#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
整合用户自定制及默认配置文件
'''
import os
import importlib
from . import global_settings


class Settings(object):
    def __init__(self):
        # 找到自定义配置
        # 找到默认配置
        # 封装到该对象中

        # ################ 默认配置 ################
        for name in dir(global_settings):
            if name.isupper():
                value = getattr(global_settings, name)
                setattr(self, name, value)

        # ################ 用户配置 ################
        # 环境变量存放公共的值os.eviron, 在start设置
        settings_module = os.environ['USER_SETTINGS']

        if not settings_module:
            return 

        # 根据字符串导入模块
        obj = importlib.import_module(settings_module)

        # 模块内所有的属性
        for name in dir(obj):
            # 配置默认大写
            if name.isupper():
                value = getattr(obj, name)

                # 设置到当前类的对象，以便使用
                setattr(self, name, value)


settings = Settings()