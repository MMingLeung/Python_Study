import os
import json
import struct
import time
from lib import roll_bar,md5_check

def is_exist(filename):
    '判断文件是否存在'
    if not os.path.isfile(filename):
        return
    else:
        filesize = os.path.getsize(filename)
        return filesize

def check_memery(data):
    '判断用户配额是否已满'
    if data == "memery is full":
        print(data)
        return
    else:
        print(data)

def loop_recv(client, flag):
    '接收信息'
    while not flag:
        try:
            data = client.recv(1024)
        except Exception :
            print('no data')
        if data:
            #flag = True
            return data

def path_exist(file_path):
    '判断文件夹是否存在'
    if not os.path.exists(file_path):
        os.mkdir(file_path)


def quota(file_path, head_dict, conn):
    # 判断文件夹大小是否超出配额
    file_dir_size = os.path.getsize(file_path)
    file_dir_can_use_size = int(head_dict["quota"]) - file_dir_size
    #print(int(head_dict["filesize"]))
    if file_dir_can_use_size < int(head_dict["filesize"]):
        conn.send("memery is full".encode("utf8"))
        return
    else:
        conn.send("memery is not full".encode("utf8"))