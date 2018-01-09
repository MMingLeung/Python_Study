#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
from lib.conf.config import settings

class Board(object):
    def __init__(self):
        pass

    @classmethod
    def initial(cls):
        return cls()

    def process(self, command_func, debug):
        if debug:
            output = open(os.path.join(settings.BASE_DIR, 'debug_files/board.out'), 'r', encoding='utf-8').read()
        else:
            output = command_func("sudo dmidecode -t1")
        return self.parse(output)

    '''
    SMBIOS 2.7 present.
    
    Handle 0x0001, DMI type 1, 27 bytes
    System Information
        Manufacturer: Parallels Software International Inc.
        Product Name: Parallels Virtual Platform
        Version: None
        Serial Number: Parallels-1A 1B CB 3B 64 66 4B 13 86 B0 86 FF 7E 2B 20 30
        UUID: 3BCB1B1A-6664-134B-86B0-86FF7E2B2030
        Wake-up Type: Power Switch
        SKU Number: Undefined
        Family: Parallels VM
    '''
    def parse(self, content):

        result = {}
        key_map = {
            'Manufacturer': 'manufacturer',
            'Product Name': 'model',
            'Serial Number': 'sn',
        }
        #循环遍历切分的信息
        for item in content.split('\n'):
            #根据"："切分
            row_data = item.strip().split(':')
            #如果列表长度是2
            if len(row_data) == 2:
                #所需信息的key与遍历的数据匹配
                if row_data[0] in key_map:
                    #赋值
                    result[key_map[row_data[0]]] = row_data[1].strip() if row_data[1] else row_data[1]
        return result
