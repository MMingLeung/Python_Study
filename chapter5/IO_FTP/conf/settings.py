#!-*- coding:utf-8 -*-
#!/usr/bin/pyhton

import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

db_BASE_DIR = os.path.join(BASE_DIR, 'db' , 'accounts.json')

personal_upload_dir = os.path.join(BASE_DIR, 'personal_uplaod_dir')

personal_download_dir = os.path.join(BASE_DIR, 'db')