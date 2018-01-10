import requests
import json
from abc import ABCMeta, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from src.plugins import PluginManager
from lib.conf.config import settings
from lib.utils import encrypt, decrpyt, auth


class Base(metaclass=ABCMeta):
    @abstractmethod
    def execute(self):
        raise NotImplementedError

    def post_asset(self, server_info):
        res = requests.get(settings.API, headers={'OpenKey':auth()})
        csrf = res.text
        token = res.cookies.items()[0][1]
        cookies = res.cookies.get_dict()
        data = encrypt(json.dumps(server_info))
        requests.post(settings.API, data=data, headers={'OpenKey':auth(), 'X-CSRFToken':token}, cookies=cookies)
        # 发送
        # body: json.dumps
        # headers = {'content-type':'application/JSON'}
        # request.body 取值
        # json.loads() --> 字节类型 --> 字符串


class Agent(Base):
    def execute(self):
        server_info = PluginManager().exec_plugin()
        # 唯一标识
        host_name = server_info['basic']['data']['hostname']
        cert_name = open(settings.CERT_PATH, 'r', encoding='utf-8').read()
        if not cert_name.strip():
            with open(settings.CERT_PATH, 'w') as file:
                file.write(host_name)
        elif cert_name != host_name:
            server_info['basic']['data']['hostname'] = cert_name
        self.post_asset(server_info)


class SSHSALT(Base):
    def get_host(self):
        response = requests.get(settings.API, headers={'OpenKey':settings.AUTH_KEY})
        result = json.loads(decrpyt(response.content))
        if not result['status']:
            return
        return result['data']

    def send(self, host):
        server_info = PluginManager(host).exec_plugin()
        self.post_asset(server_info)

    def execute(self):
        host_list = self.get_host()
        pool = ThreadPoolExecutor(20)
        for host in host_list:
            pool.submit(self.send, host)
