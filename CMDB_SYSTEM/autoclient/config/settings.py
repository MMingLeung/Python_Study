#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
用户自定义配置文件
'''
import os


# 插件
# 增加插件只需在此增加对应类名和路径
PLUGINS_DICT = {
    'basic':'src.plugins.basic.Basic',
    'board':'src.plugins.board.Board',
    'cpu':'src.plugins.cpu.Cpu',
    'disk':'src.plugins.disk.Disk',
    'memory':'src.plugins.memory.Memory',
    'nic':'src.plugins.nic.Nic',
}

# 模式
MODE = 'agent' # saltstack/agent/ssh

# ssh
SSH_USER= 'root'
SSH_PASSWORD = 'password'
SSH_PORT = 22

# 私钥
SSH_KEY = '/xxx/xx/xx'

# 调试模式
DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# API
API = 'http://127.0.0.1:8000/api/asset.html'

# 唯一标识
CERT_PATH = os.path.join(BASE_DIR, 'config', 'cert')

# auth_key
AUTH_KEY = 'aaa'

# cipher_key
CIPHER_KEY = 'zqwrfdsazxcsdwqe'