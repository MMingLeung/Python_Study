from Crypto.Cipher import AES
from autoserver import settings


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