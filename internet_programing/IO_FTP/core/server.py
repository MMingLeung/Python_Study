import socket
import struct
import selectors
import os
import sys
import json
import subprocess
import hashlib
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from core import server_setout
from lib import md5_check, baotou_handler
import time


db_BASE_DIR = os.path.join(BASE_DIR, 'db' , 'accounts.json')
personal_upload_dir = os.path.join(BASE_DIR, 'db','personal_upload_dir')

class FTP_Server:
    '''
    服务端
    '''
    def __init__(self):
        '初始化'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("127.0.0.1", 9000))
        self.sock.listen(5)
        self.sock.setblocking(False)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, socket.SO_REUSEADDR)
        self.s = selectors.DefaultSelector()

    def accept(self, sock, mask):
        conn, addr = sock.accept()
        self.s.register(conn, selectors.EVENT_READ, self.read)

    def read(self, conn, mask):
        while True:
            try:
                head_struct = conn.recv(4)
                if not head_struct:break
                head_json_bytes_len = struct.unpack('i', head_struct)[0]
                head_json = conn.recv(head_json_bytes_len).decode("utf8")
                head_dict = json.loads(head_json)
                print(head_dict)
                cmd = head_dict['cmd']
                if hasattr(self, cmd):
                    func = getattr(self, cmd)
                    func(head_dict, conn)
            except Exception:
                break

    def put(self,head_dict, conn):
        '上传'
        FLAG = False

        #为put方法提供所需参数
        server_s = server_setout.ServerSetout()
        file_path,recv_md5 = server_s.put_setout(personal_upload_dir, head_dict, conn)

        file_size = head_dict["filesize"]
        recv_size = 0
        #判断是否存在该文件
        if os.path.exists(file_path):
            data = "file is existed rewrite or continue?(rewrite/continue)"
            conn.send(data.encode('utf8'))
            while not FLAG:
                try:
                    time.sleep(1)
                    dict_struct = conn.recv(4)
                    #time.sleep(1)
                    dict_json_bytes_len = struct.unpack('i', dict_struct)[0]
                    dict_json = conn.recv(dict_json_bytes_len).decode('utf8')
                    dict = json.loads(dict_json)
                    #断点续传
                    if dict['choice'] == 'continue':
                        with open(file_path, 'rb+') as f:
                            for i in f:
                                recv_size += len(i)
                            print('recv_size', recv_size, type(recv_size))
                            f.seek(recv_size)
                            recv_size_send = str(recv_size).encode('utf8')
                            print(recv_size_send)
                            time.sleep(1)
                            conn.send(recv_size_send)
                            print("begin to write: ", file_path)
                            time.sleep(1)
                            while recv_size < file_size:
                                time.sleep(1)
                                data = conn.recv(1024)
                                time.sleep(1)
                                f.write(data)
                                recv_size += len(data)
                                print("recvsize: %s, filesize: %s" % (recv_size, file_size))
                        my_md5 = md5_check.md5_check(file_path)
                        print(my_md5)
                        if my_md5 != recv_md5:
                            os.remove(file_path)
                            print("md5 doesn't match!")
                            #global FLAG
                            FLAG = True
                        else:
                            print("upload successed!")
                            #global FLAG
                            FLAG = True
                    elif dict['choice'] == 'rewrite':
                        #覆盖写入
                        print("begin to write: ", file_path)
                        with open(file_path, 'wb') as f:
                            while recv_size < file_size:
                                time.sleep(1)
                                data = conn.recv(1024)
                                time.sleep(1)
                                f.write(data)
                                recv_size += len(data)
                                print("recvsize: %s, filesize: %s" % (recv_size, file_size))
                        # with open(file_path, 'r') as f:
                        #     f = f.read()
                        #     for i in f:
                        #         md5.update(i.encode("utf8"))
                        my_md5 = md5_check.md5_check(file_path)
                        if my_md5 != recv_md5:
                            os.remove(file_path)
                            print("md5 doesn't match!")
                            #global FLAG
                            FLAG = True
                        else:
                            print("upload successed!")
                            #global FLAG
                            FLAG = True
                except Exception:
                    print('wating for client..')
        else:
            #如果文件不存在，正常写入
            while not FLAG:
                try:
                    data = "begin to write: "
                    conn.send(data.encode('utf8'))
                    print("begin to write: ", file_path)
                    with open(file_path, 'wb') as f:
                        while recv_size < file_size:
                            #time.sleep(1)
                            data = conn.recv(1024)
                            #time.sleep(1)
                            f.write(data)
                            recv_size += len(data)
                            print("recvsize: %s, filesize: %s" % (recv_size, file_size))
                    my_md5 = md5_check.md5_check(file_path)
                    print(my_md5)
                    if my_md5 != recv_md5:
                        os.remove(file_path)
                        print("md5 doesn't match!")
                        FLAG = True
                    else:
                        print("upload successed!")
                        FLAG = True
                except Exception:
                    print('wating for client..')



    def get(self, head_dict, conn):
        '客户端下载'
        server_s = server_setout.ServerSetout()
        file_path, head_struct, head_json_bytes = server_s.get_setout(personal_upload_dir, head_dict)

        conn.send(head_struct)
        conn.send(head_json_bytes)
        send_size = 0

        with open(file_path, 'rb') as f:
            for line in f:
                conn.send(line)
                send_size += len(line)
                print(send_size)
            else:
                print("User download success!")

    def ls(self, head_dict, conn):
        '查看服务器上用户的目录'
        # personal_dir = os.path.join(personal_upload_dir, head_dict["username"])
        # command = head_dict['cmd'] +' '+personal_dir
        #
        # res = subprocess.Popen(command,
        #                        shell=True,
        #                        stdout=subprocess.PIPE,
        #                        stderr=subprocess.PIPE)
        # data_err = res.stderr.read()
        # data_res = res.stdout.read()
        # data_size = len(data_err)+ len(data_res)
        # data_dict = {'filesize':data_size}
        # data_json_bytes = json.dumps(data_dict).encode("utf8")
        # data_json_bytes_len = len(data_json_bytes)
        # data_struct = struct.pack('i', data_json_bytes_len)
        server_l = server_setout.ServerSetout()
        head_struct, head_json_bytes, data_err, data_res = server_l.ls_setout(personal_upload_dir, head_dict)
        conn.send(head_struct)
        conn.send(head_json_bytes)
        conn.send(data_res)
        conn.send(data_err)

    def run(self):
        self.s.register(self.sock, selectors.EVENT_READ, self.accept)
        while True:
            #print("waiting for connect..")
            events = self.s.select()
            for key,mask in events:
                func = key.data
                obj = key.fileobj
                func(obj, mask)


server = FTP_Server()
server.run()

