#! -*-code:utf8-*-
import os
USER = 'root'

PWD = 'qwert'

MODE = 'AGENT' #SALT, SSH

SSH_USER = 'root'

SSH_PWD = 'qwert'

SSH_KEY = '/xxx/xxxx/xx' #私钥路径

SSH_PORT = 22

DEBUG = True

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PLUGINS_DICT = {
    'basic':'src.plugins.basic.Basic',
    'board':'src.plugins.board.Board',
    'cpu':'src.plugins.cpu.Cpu',
    'disk':'src.plugins.disk.Disk',
    'memory':'src.plugins.memory.Memory',
    'nic':'src.plugins.nic.Nic',
}

API = "http://127.0.0.1:8000"