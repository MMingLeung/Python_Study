#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys


# set the settings file's path to environment
os.environ['SETTINGS_PATH'] = 'server.config.settings'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

if __name__ == '__main__':
    from server import src
    src.start()


