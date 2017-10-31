# import time
# from concurrent.futures import ThreadPoolExecutor
# #进程
# from concurrent.futures import ProcessPoolExecutor
#
# def task(i):
#     time.sleep(1)
#     print(i)
#
# #线程池
# p = ThreadPoolExecutor(10)
#
# for row in range(100):
#     p.submit(task, row)

#方式1：静态令牌
import requests
#根据主板、时间生成随机字符串

# response = requests.get('http://127.0.0.1:8000/api/asset.html', headers={'OpenKey':'key'})
# print(response.text)

#方式1改良：动态令牌
import time
import hashlib
#
# key = 'key'
# ctime = time.time()
# new_key = "%s|%s" % (key, ctime)
#
# m = hashlib.md5()
# m.update(bytes(new_key,encoding='utf8'))
# md5_key = m.hexdigest()
# md5_key_time = "%s|%s" % (md5_key, ctime)
#
# response = requests.get('http://127.0.0.1:8000/api/asset.html', headers={'OpenKey':md5_key_time})
# print(response.text)

#方法1：完善
#服务器把10s以内的md5_key_time保存
#对比时间



###########RSA##############
# import rsa
# import base64
#
# # ######### 1. 生成公钥私钥 #########
# pub_key_obj, priv_key_obj = rsa.newkeys(256)
#
# pub_key_str = pub_key_obj.save_pkcs1()
# pub_key_code = base64.standard_b64encode(pub_key_str)
#
# priv_key_str = priv_key_obj.save_pkcs1()
# priv_key_code = base64.standard_b64encode(priv_key_str)
#
# print(pub_key_code)
# print(priv_key_code)
#
#
# # ######### 2. 加密 #########
# def encrypt(value):
#     key_str = base64.standard_b64decode(pub_key_code)
#     pk = rsa.PublicKey.load_pkcs1(key_str)
#     val = rsa.encrypt(value.encode('utf-8'), pk)
#     return val
#
#
# # ######### 3. 解密 #########
# def decrypt(value):
#     key_str = base64.standard_b64decode(priv_key_code)
#     pk = rsa.PrivateKey.load_pkcs1(key_str)
#     val = rsa.decrypt(value, pk)
#     return val
#
#
# # ######### 基本使用 #########
# if __name__ == '__main__':
#     v = 'wupeiqi'
#     v1 = encrypt(v)
#     print(v1)
#     v2 = decrypt(v1)
#     print(v2)



####################
'''
from Crypto.Cipher import AES


def encrypt(message):
    key = b'dfdsdfsasdfdsdfs' #长度有限制16个字节
    cipher = AES.new(key, AES.MODE_CBC, key)
    bmessage = bytearray(message, encoding='utf-8')
    v1 = len(bytes(message, encoding='utf-8'))
    v2 = v1 % 16
    v3 = 16 - v2
    for i in range(v3):
        bmessage.append(32)
    data = bmessage.decode('utf-8')
    msg = cipher.encrypt(data)
    return msg


def decrypt(message):
    key = b'dfdsdfsasdfdsdfs'
    cipher = AES.new(key, AES.MODE_CBC, key)
    result = cipher.decrypt(message)
    return result.decode('utf-8').strip()

v = '我是你爸'
print(len(v))
data = encrypt(v)
print(data)
result = decrypt(data)
print(len(result),result)

'''
from Crypto.Cipher import AES

#==========加密==========
def encrypt(message):
    key = b'dfdsdfsasdfdsdfs' #长度有限制16个字节
    cipher = AES.new(key, AES.MODE_CBC, key)
    # bytearray 字节数组
    ba_data = bytearray(message, encoding='utf-8')
    len1 = len(ba_data) #总长度
    len2 = len1 % 16 #还需要加
    if len2 == 0:
        need_add = 16
    else:
        need_add = 16 - len2
    for i in range(need_add):
        ba_data.append(need_add) #bytesarray只能加数字ASCII
    final_data = ba_data.decode('utf-8')
    msg = cipher.encrypt(final_data) #要加密的字符串必需是16个字节的倍数

    return msg

#==========解密==========

def decrypt(message):

    key = b'dfdsdfsasdfdsdfs'
    cipher = AES.new(key, AES.MODE_CBC, key)
    result = cipher.decrypt(message)
    #这种加空格的方式会去掉原有空格
    #解决方法
    #result[-1] 代表添加的个数也是添加的内容
    data = result[0:-result[-1]]
    data = str(data, encoding='utf-8')

    return data


# data = encrypt(v)
# print(data)
# result = decrypt(data)
# print(len(result),result)

a = encrypt("dsds")
b = decrypt(a)
print(len(b), b)


#  pip3 install wheel pip3 install pycrypto-2.6.1-cp35-none-win32.whl #根据py版本

def auth():
    key = 'key'
    ctime = time.time()
    new_key = "%s|%s" % (key, ctime)

    m = hashlib.md5()
    m.update(bytes(new_key, encoding='utf8'))
    md5_key = m.hexdigest()
    md5_key_time = "%s|%s" % (md5_key, ctime)

    return md5_key_time

# response = requests.post(url='http://127.0.0.1:8000/api/asset.html', headers={'OpenKey':auth()}, json={'k1':'v1'})


import json

#变成字节，省去request把字符串变成字节
# v1 = bytes(json.dumps({'k1':'v1'}), encoding='utf8')
#加密后的字节，服务器经过解密，json.loads，获取服务器数据，再入库
v1 = encrypt(json.dumps({'k1':'v1'}))




# response = requests.post(
#     url='http://127.0.0.1:8000/api/asset.html',
#     headers={'OpenKey':auth(), 'Content-Type':'application/json'},
#     data=v1)
# print(response.text)
from config import settings

response = requests.get(settings.API, headers={'OpenKey':auth(), 'Content-Type':'application/json'})
print(response.text)