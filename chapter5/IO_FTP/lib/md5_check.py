import hashlib

def md5_check(file_path):
    'md5校验'
    md5 = hashlib.md5()
    with open(file_path, 'r') as f:
        f = f.read()
        for i in f:
            md5.update(i.encode("utf8"))
    md5 = md5.hexdigest()
    return md5

# def md5_make(filename):
#     'md5生成'
#     md5 = hashlib.md5()
#     with open(filename, 'r') as file:
#         file = file.read()
#         for i in file:
#             md5.update(i.encode('utf8'))
#     md5 = md5.hexdigest()
#     return md5