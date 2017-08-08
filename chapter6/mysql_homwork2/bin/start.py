#! -*- coding:utf8 -*-
#! /usr/bin/Python

'start program'

import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from core import main

if __name__ == '__main__':
    main.run()