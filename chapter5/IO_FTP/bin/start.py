#!-*- coding:utf-8 -*-
#!/usr/bin/pyhton

import os, sys
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
#print(sys.path)

from core import db_handle, main



if __name__ == "__main__":
    main.run()
