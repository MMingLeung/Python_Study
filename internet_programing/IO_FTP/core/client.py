import socket
import os
import json
import struct
import time
from conf import settings
from core import client_setout
from lib import auth, md5_check, baotou_handler, file_handler, roll_bar
import sys

@auth.auth
class FTP_Client:
    '''
    客户端程序
    '''
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    @property
    def client_conn(self):
        client_conn = self.client.connect(("127.0.0.1", 9000))
        return client_conn


    def run(self, username, quota):
        while True:
            send_cmd = input(">>: ")
            if not send_cmd:continue
            send_cmd = send_cmd.split()
            cmd = send_cmd[0]
            if hasattr(self, cmd):
                func = getattr(self, cmd)
                func(send_cmd, username, quota)

    def put(self, send_cmd, username, quota):
        '上传'
        flag = False

        #获得put方法所需的参数
        client = client_setout.ClientSetout()
        head_struct, head_json_bytes, filename, filesize = client.put_setout(send_cmd, username, quota)

        #发送报头长度
        self.client.send(head_struct)

        #发送报头
        self.client.send(head_json_bytes)

        #接收server发送过来的信息"memery is full"or"memery is not full"
        data = file_handler.loop_recv(self.client, flag)
        data = data.decode("utf-8")

        #检测用户配额空间是否已满
        file_handler.check_memery(data)

        data_rewrite_or_new = self.client.recv(1024)

        #上传的主逻辑
        #file_handler.write_file_put(data_rewrite_or_new, filename, filesize, self.client, flag)
        if data_rewrite_or_new.decode("utf8") == "file is existed rewrite or continue?(rewrite/continue)":
            data = data_rewrite_or_new.decode("utf8")
            print(data)
            choice = input(">>: ")
            # 重写
            if choice == 'rewrite':
                dict = {'choice': choice}
                dict_json = json.dumps(dict)
                dict_json_bytes = bytes(dict_json, encoding='utf8')
                dict_json_bytes_len = len(dict_json_bytes)
                dict_struct = struct.pack("i", dict_json_bytes_len)
                # choice = choice.encode("utf8")
                self.client.send(dict_struct)
                self.client.send(dict_json_bytes)
                send_size = 0
                while not flag:
                    try:
                        with open(filename, 'rb') as f:
                            for line in f:
                                time.sleep(1)
                                self.client.send(line)
                                time.sleep(1)
                                send_size += len(line)
                                roll_bar.roll_bar(send_size, filesize)
                            else:
                                print("Upload successful!")
                                flag = True
                    except Exception:
                        print("wating for server")
            # 续传
            if choice == 'continue':
                dict = {'choice': choice}
                dict_json = json.dumps(dict)
                dict_json_bytes = bytes(dict_json, encoding='utf8')
                dict_json_bytes_len = len(dict_json_bytes)
                dict_struct = struct.pack("i", dict_json_bytes_len)
                # choice = choice.encode("utf8")
                self.client.send(dict_struct)
                self.client.send(dict_json_bytes)
                while not flag:
                    try:
                        time.sleep(1)
                        data_re = self.client.recv(1024)
                        time.sleep(1)
                        # print('11111')
                        data = int(data_re)
                        if data:
                            send_size = data
                            with open(filename, 'rb') as f:
                                f.seek(send_size)
                                for line in f:
                                    self.client.send(line)
                                    send_size += len(line)
                                    roll_bar.roll_bar(send_size, filesize)
                                else:
                                    print("Upload successful!")
                                    # global FLAG
                                    flag = True
                    except Exception:
                        print("wating for server")
        else:
            # 如果服务器没有该文件则正常写入
            while not flag:
                try:
                    send_size = 0
                    with open(filename, 'rb') as f:
                        for line in f:
                            #time.sleep(1)
                            self.client.send(line)
                            #time.sleep(1)
                            send_size += len(line)
                            roll_bar.roll_bar(send_size, filesize)
                        else:
                            print("Upload successful!")
                            flag = True
                except Exception:
                    print("wating for server")

    def get(self, send_cmd, username, quota):
        '下载'
        flag = False
        #获取get所需参数
        client = client_setout.ClientSetout()
        head_struct, head_json_bytes, cmd, filename, file_path = client.get_setout(send_cmd, username)
        #发送报头及json数据长度
        self.client.send(head_struct)
        self.client.send(head_json_bytes)
        time.sleep(2)
        #下载的主逻辑
        while not flag:
            try:
                head_struct_recv = self.client.recv(4)
                head_len = struct.unpack('i', head_struct_recv)[0]
                #print("recv ok1")
                head_json_recv = self.client.recv(head_len).decode('utf8')
                #print("recv ok2")
                head_dict_recv = json.loads(head_json_recv)
                #print("recv ok3")
                filesize = head_dict_recv['filesize']
                filename = head_dict_recv['filename']
                # file_path = os.path.join(settings.personal_download_dir, username)
                # if not os.path.exists(file_path):
                #     print(1111)
                #     os.mkdir(file_path)
                file_path = os.path.join(file_path, filename)
                print("begin to downlaod: ", file_path)
                recv_size = 0
                with open(file_path, 'wb') as f:
                    print('write')
                    while recv_size < filesize:
                        data = self.client.recv(1024)
                        f.write(data)
                        recv_before = recv_size
                        recv_size += len(data)
                        roll_bar.roll_bar(recv_size - recv_before, filesize)
                        # print("recvsize: %s , filesize: %s" % (recv_size, filesize))
                md5 = md5_check.md5_check(file_path)
                if md5 != head_dict_recv["md5"]:
                    os.remove(file_path)
                    print("md5 doesn't match!")
                    flag = True
                else:
                    print('\nfile get successful!')
                    flag = True
            except Exception:
                pass

    def ls(self, send_cmd, username, quota):
        '查看服务器上用户的私人目录'
        #获取ls方法所需参数
        client = client_setout.ClientSetout()
        head_struct, head_json_bytes = client.ls_setout(send_cmd, username)
        # 发送报头及json数据长度
        self.client.send(head_struct)
        self.client.send(head_json_bytes)
        #解server送达报头
        baotou = baotou_handler.UnpackBaotou()
        data_size = baotou.unpack_baotou(self.client)

        recv_size = 0
        recv_data = b''
        #收取消息
        while recv_size < data_size:
            data = self.client.recv(1024)
            recv_size += len(data)
            recv_data += data
        print(recv_data.decode('utf8'))

# client = FTP_Client()
# client.run()