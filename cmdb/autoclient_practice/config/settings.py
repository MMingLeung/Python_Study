#自定义配置
import os

USER_NAME = 'matt'

PWD = 'qwert'

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODE = 'AGENT'

DEBUG = True

PLUGINS_DICT = {
    'basic':'src.plugins.basic.Basic',
    'board':'src.plugins.board.Board',
    'cpu':'src.plugins.cpu.Cpu',
    'disk':'src.plugins.disk.Disk',
    'memory':'src.plugins.memory.Memory',
    'nic':'src.plugins.nic.Nic',
}

API = 'http://127.0.0.1:8000/api/asset.html'

CERT_PATH =os.path.join(BASEDIR, 'config', 'cert')

AUTH_KEY = 'key'

OPEN_KEY = b'dfdsdfsasdfdsdfs'