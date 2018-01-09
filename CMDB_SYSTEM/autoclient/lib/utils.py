#!/usr/bin/env python
# -*- coding:utf-8 -*-
from Crypto.Cipher import AES
import time
import hashlib


def encrypt(message):
    key = b'zqwrfdsazxcsdwqe'
    cipher = AES.new(key, AES.MODE_CBC, key)

    by_data = bytearray(message, encoding='utf-8')
    by_data_len = len(by_data)
    if by_data_len == 16:
        add_bty = 16
    else:
        b = by_data_len % 16
        add_bty = 16 - b
    for _ in range(add_bty):
        by_data.append(add_bty)
    final_data = cipher.encrypt(by_data.decode('utf-8'))
    return final_data

def decrpyt(message):
    key = b'zqwrfdsazxcsdwqe'
    cipher = AES.new(key, AES.MODE_CBC, key)
    result = cipher.decrypt(message)
    return str(result[0:-result[-1]], encoding='utf-8')

def auth():
    ctime = time.time()
    key = 'aaa'
    new_key = '%s|%s' % (key, ctime)
    m = hashlib.md5()
    m.update(new_key.encode('utf-8')) # 转换成字节
    md5_key = m.hexdigest()
    md5_key_time = "%s|%s" % (md5_key, ctime)
    return md5_key_time