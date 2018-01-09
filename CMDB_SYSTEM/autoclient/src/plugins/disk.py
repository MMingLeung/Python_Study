#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import os
from lib.conf.config import settings


class Disk(object):
    def __init__(self):
        pass

    @classmethod
    def initial(cls):
        return cls()

    def process(self, command_func, debug):
        if debug:
            output = open(os.path.join(settings.BASE_DIR, 'debug_files/disk.out'), 'r', encoding='utf-8').read()
        else:
            output = command_func("sudo MegaCli  -PDList -aALL")
        return self.parse(output)

    def parse(self, content):
        """
        解析shell命令返回结果
        :param content: shell 命令结果
        :return:解析后的结果
        """
        response = {}
        result = []
        #根据四个回车切分
        for row_line in content.split("\n\n\n\n"):
            result.append(row_line)
        for item in result:
            temp_dict = {}
            #每一段根据回车切分
            for row in item.split('\n'):
                if not row.strip():
                    continue
                if len(row.split(':')) != 2:
                    continue
                #根据"："切分
                key, value = row.split(':')
                name = self.mega_patter_match(key)
                if name:
                    if key == 'Raw Size':
                        raw_size = re.search('(\d+\.\d+)', value.strip())
                        if raw_size:
                            #获取正则的分组的信息并赋值
                            temp_dict[name] = raw_size.group()
                        else:
                            raw_size = '0'
                    else:
                        temp_dict[name] = value.strip()
            if temp_dict:
                #根据slot插槽编号构建reponse字典
                response[temp_dict['slot']] = temp_dict
        return response

    @staticmethod
    def mega_patter_match(needle):
        #根据输入的硬盘信息，输出指定信息
        #slot插槽编号、 Raw size容量、Inquiry型号、PDtype 接口类型（sate/ide）
        grep_pattern = {'Slot': 'slot', 'Raw Size': 'capacity', 'Inquiry': 'model', 'PD Type': 'pd_type'}
        for key, value in grep_pattern.items():
            #以key开头的就返回自定义字典的value
            if needle.startswith(key):
                return value
        return False
