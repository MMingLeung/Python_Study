#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from datetime import datetime, date


class JsonCustomEncoder(json.JSONEncoder):
    '''
    JSON序列化时间
    '''
    def default(self, filed):
        if isinstance(filed, datetime):
            return filed.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(filed, date):
            return filed.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, filed)