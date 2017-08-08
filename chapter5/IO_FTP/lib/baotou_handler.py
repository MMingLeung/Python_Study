import json
import struct
import os
#生成报头字典

# def make_dict(username, cmd, filename, filesize, quota, md5):
#     head_dict = {"username":username,"cmd":cmd, "filename":filename,
#              'filesize':filesize, 'quota':quota, 'md5':md5}
#     return head_dict
#
# def make_dict_server_get(filename,file_size,md5):
#     head_dict_send = {'filename': filename, 'filesize': file_size, 'md5': md5}
#     return head_dict_send

class PackBaotou:
    def translate_json(self,head_dict):
        return json.dumps(head_dict)

    def encoding_bytes(self,head_dict_json):
        head_json_bytes = bytes(head_dict_json, encoding='utf8')
        return head_json_bytes

    def len_json_bytes(self,head_json_bytes):
        head_json_bytes_len = len(head_json_bytes)
        return head_json_bytes_len

    def head_struct_j(self,head_json_bytes_len):
        head_struct = struct.pack("i", head_json_bytes_len)
        return head_struct

    def pack_baotou(self, head_dict):
        head_json = self.translate_json(head_dict)
        head_json_bytes = self.encoding_bytes(head_json)
        head_json_bytes_len = self.len_json_bytes(head_json_bytes)
        head_struct = self.head_struct_j(head_json_bytes_len)
        return head_struct, head_json_bytes


class UnpackBaotou:
    def unpack_baotou(self,client):

        head_struct_recv = client.recv(4)
        head_len = struct.unpack('i', head_struct_recv)[0]
        head_json = client.recv(head_len).decode('utf8')
        head_dict_recv = json.loads(head_json)
        data_size = head_dict_recv['filesize']
        return data_size