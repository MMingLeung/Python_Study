import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['USER_SETTINGS'] = 'config.settings'

from lib.conf.config import settings
from src.plugins import PluginsManage
from src import script

if __name__ == '__main__':
    # server_info = PluginsManage().execute_plugin()
    # for i,v in server_info.items():
    #     print(i,v)
    script.run()
