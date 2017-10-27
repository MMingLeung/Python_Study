import os

print(os.environ) #环境变量

#加入环境变量，公共的值。当前运行程序，不影响其它程序
os.environ['USER_SETTINGS'] = 'config.settings'
print(os.environ) #环境变量
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.plugins import PluginManager
from lib.config.config import settings

# print(settings.USER)
# print(settings.PWD)
# print(settings.EMAIL)


from src import script

if __name__ == '__main__':
    server_info = PluginManager().exec_plugin()
    print(server_info)
    # script.run()

