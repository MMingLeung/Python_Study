#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
基于AES加密与解密
'''
from Crypto.Cipher import AES


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

