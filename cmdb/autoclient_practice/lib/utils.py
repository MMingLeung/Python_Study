import time
import hashlib
from Crypto.Cipher import AES
import json
from config import settings


#=========api验证========
def auth():

    key = settings.AUTH_KEY
    ctime = time.time()
    new_key = "%s|%s" % (key, ctime)
    m = hashlib.md5()
    m.update(bytes(new_key, encoding='utf8'))
    md5_key = m.hexdigest()
    md5_key_time = "%s|%s" % (md5_key, ctime)

    return md5_key_time



#==========加密==========
def encrypt(message):
    key = settings.OPEN_KEY #长度有限制16个字节
    cipher = AES.new(key, AES.MODE_CBC, key)
    # bytearray 字节数组
    message = json.dumps(message)
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

    key = settings.OPEN_KEY
    cipher = AES.new(key, AES.MODE_CBC, key)
    result = cipher.decrypt(message)
    #这种加空格的方式会去掉原有空格
    #解决方法
    #result[-1] 代表添加的个数也是添加的内容
    data = result[0:-result[-1]]
    data = str(data, encoding='utf-8')

    return data