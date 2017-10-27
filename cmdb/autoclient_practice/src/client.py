import requests
from lib.conf.config import settings
from src.plugins import PluginsManage
from concurrent.futures import ThreadPoolExecutor
import time
import hashlib
from lib.utils import encrypt, auth

class Base():

    def post_asset(self, server_info):

        data = encrypt(server_info)
        response = requests.post(
            settings.API,
            data=data,
            headers={'OpenKey':auth(),'Content-Type':'application/json'}
        )
        print(response.text)


class Agent(Base):

    def execute(self):
        server_info = PluginsManage().execute_plugin()
        hostname = server_info['basic']['data']['hostname']
        file = open(settings.CERT_PATH, 'r', encoding='utf8')
        cert = file.read()
        file.close()
        #第一次获取的服务器信息中的名字写入本地文件，用于以后如果服务器有人修改了依然根据旧名字进行统计，避免程序误以为新增计算机
        if not cert:
            with open(settings.CERT_PATH, 'w', encoding='utf8') as f:
                f.write(hostname)
        else:
            #以本地文件为准
            server_info['basic']['data']['hostname'] = cert
        self.post_asset(server_info)


class SSHSALT(Base):
    def get_host(self):
        response = requests.get(settings.API, headers={'OpenKey':auth(), 'Content-Type':'application/json'})
        result = response.text
        print('result',result)
        if not result:
            return
        return result['data']


    def run(self, host):
        server_info = PluginsManage(host).execute_plugin()
        self.post_asset(server_info)


    def execute(self):
        host_list = self.get_host()
        #线程池
        p = ThreadPoolExecutor(20)
        for host in host_list:
            p.submit(self.run, host)
