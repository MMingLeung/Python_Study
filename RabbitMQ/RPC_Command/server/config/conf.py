#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Using singleton to saving configurations which in settings file.

When you using it just: 

from server.config.conf import settings
settings.CONF_NAME
'''
import os
import importlib


class Settings(object):
    def __init__(self):
        setting_module = os.environ['SETTINGS_PATH']
        _module = importlib.import_module(setting_module)
        for name in dir(_module):
            if name.isupper():
                value = getattr(_module, name)
                setattr(self, name, value)

settings = Settings()