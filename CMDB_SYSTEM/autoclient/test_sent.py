'''
发送测试
'''
import requests
import time
import hashlib
from test_cipher import decrpyt
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# 静态
API = 'http://127.0.0.1:8000/api/asset.html'
def auth():
    ctime = time.time()
    key = 'aaa'
    new_key = '%s|%s' % (key, ctime)
    m = hashlib.md5()
    m.update(new_key.encode('utf-8')) # 转换成字节
    md5_key = m.hexdigest()
    md5_key_time = "%s|%s" % (md5_key, ctime)
    return md5_key_time
#da88aa4a85e144f4e83bd6aef9f24a04|1514350986.108507


response = requests.get(API, headers={'OpenKey': auth()})
data = response.content
print(len(data))


origin_data = decrpyt(data)
print(origin_data)