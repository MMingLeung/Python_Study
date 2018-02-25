import os
import subprocess
from lib import file_handler,md5_check, baotou_handler


class ServerSetout:

    def put_setout(self, personal_upload_dir, head_dict, conn):
        file_path_now = os.path.normpath(os.path.join(personal_upload_dir, head_dict['username']))
        print(file_path_now)
        # '/Users/mingleung/PycharmProjects/PythonStudyLesson/day8/IO_FTP/db/personal_upload_dir/Jack'
        #判断文件夹是否存在
        file_handler.path_exist(file_path_now)

        # 判断文件夹大小是否超出配额
        file_handler.quota(file_path_now, head_dict, conn)

        #md5
        recv_md5 = head_dict["md5"]

        #上传路径拼接
        file_path = os.path.join(file_path_now, head_dict["filename"])
        print("filepath is ", file_path)
        return file_path, recv_md5

    def get_setout(self, personal_upload_dir, head_dict):
        filename = head_dict["filename"]
        file_path = os.path.join(personal_upload_dir, head_dict['username'], head_dict['filename'])
        if not os.path.isfile(file_path):
            print("file doesn't exist! ")
            return
        else:
            file_size = os.path.getsize(file_path)
            md5 = md5_check.md5_check(file_path)
            head_dict_send = {'filename':filename, 'filesize':file_size, 'md5':md5}
            baotou = baotou_handler.PackBaotou()
            head_struct, head_json_bytes = baotou.pack_baotou(head_dict_send)
            return file_path,head_struct, head_json_bytes


    def ls_setout(self, personal_upload_dir, head_dict):

        personal_dir = os.path.join(personal_upload_dir, head_dict["username"])
        command = head_dict['cmd'] +' '+personal_dir

        res = subprocess.Popen(command,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        data_err = res.stderr.read()
        data_res = res.stdout.read()
        data_size = len(data_err)+ len(data_res)

        data_dict = {'filesize':data_size}
        baotou = baotou_handler.PackBaotou()
        head_struct, head_json_bytes = baotou.pack_baotou(data_dict)
        return head_struct,head_json_bytes,data_err,data_res
        # data_json_bytes = json.dumps(data_dict).encode("utf8")
        # data_json_bytes_len = len(data_json_bytes)
        # data_struct = struct.pack('i', data_json_bytes_len)
