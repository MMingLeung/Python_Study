#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
基于AES的加密解密功能
'''
from Crypto.Cipher import AES
from django.conf import settings


def encipher(message):
    cipher = AES.new(settings.CIPHER_KEY, AES.MODE_CBC, settings.CIPHER_KEY)
    # 处理数据，变成长度是16个字节的倍数
    bytesarr_message = bytearray(message, encoding='utf-8')
    len_bytesarr_message = len(bytesarr_message)
    if len_bytesarr_message == 16:
        add_bytes = 16
    else:
        tmp = len_bytesarr_message % 16
        add_bytes = 16 - tmp
    for _ in range(add_bytes):
        bytesarr_message.append(add_bytes)
    data = cipher.encrypt(bytesarr_message.decode('utf-8'))
    return data

def decipher(message):
    cipher = AES.new(settings.CIPHER_KEY, AES.MODE_CBC, settings.CIPHER_KEY)
    result = cipher.decrypt(message)
    return str(result[0:-result[-1]], encoding='utf-8')



