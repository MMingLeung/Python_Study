#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
启动文件
'''
import os
import sys


# 把自定义的配置文件路径设置到环境变量中
os.environ['USER_SETTINGS'] = "config.settings"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


if __name__ == '__main__':
    from src import script
    script.run()