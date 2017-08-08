from lib import file_handler, md5_check, baotou_handler
import os


class ClientSetout:

    def put_setout(self, send_cmd, username, quota):
        cmd = send_cmd[0]
        filename = send_cmd[1]

        # 检测文件是否存在
        filesize = file_handler.is_exist(filename)

        # 生成md5
        md5 = md5_check.md5_check(filename)
        print(md5)

        # 生成报头
        head_dict = {"username":username,"cmd":cmd, "filename":os.path.basename(filename),
                     'filesize':filesize, 'quota':quota, 'md5':md5}
        baotou = baotou_handler.PackBaotou()
        head_struct, head_json_bytes = baotou.pack_baotou(head_dict)
        return head_struct, head_json_bytes , filename, filesize

    def get_setout(self, send_cmd, username):
        cmd = send_cmd[0]
        filename = send_cmd[1]
        file_path = send_cmd[2]
        head_dict = {'cmd':cmd, 'filename':filename, "filepath":file_path, 'username':username}
        baotou = baotou_handler.PackBaotou()
        head_struct, head_json_bytes = baotou.pack_baotou(head_dict)
        return head_struct, head_json_bytes, cmd, filename, file_path

    def ls_setout(self, send_cmd, username):

        head_dict = {'cmd':send_cmd[0], 'username':username}
        baotou = baotou_handler.PackBaotou()
        head_struct, head_json_bytes = baotou.pack_baotou(head_dict)
        return head_struct, head_json_bytes