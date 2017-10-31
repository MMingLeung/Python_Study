from src.plugins import PluginManager
import requests
from config import settings
import json


class Base():
    def post_asset(self, server_info):

        requests.post(settings.API, json=server_info)
        #body:json.dumps(server_info) POST里面没有值
        #headers = {'content-type':'application/json'}
        #取值request.body
        #json.loads(request.body)

class Agent(Base):
    def execute(self):
        server_info = PluginManager().exec_plugin()
        self.post_asset(server_info)

class SSHSALT(Base):
    #获取未采集主机信息
    def get_host(self):
        response = requests.get(settings.API)
        result = json.loads(response.text)
        if not result['status']:
            return
        '''
        {
        'status':'True',
        'data':['c1.com', 'c2.com']
        }
        需要反序列化
        '''
        return result['data']


    def execute(self):
        host_list = self.get_host()
        for host in host_list:
            server_info = PluginManager(host).exec_plugin()
            self.post_asset(server_info)

