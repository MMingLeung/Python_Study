from django.shortcuts import HttpResponse
from django.conf import settings
import hashlib
import time


api_key_record = {}
                                            #超时时间
# {'eqwqweqwewqeqwew|213123123.123':'321321321.32131'}

#验证规则装饰器
def auth(func):
    def wrapper(request, *args, **kwargs):
        # 方法1改进：
        client_md5_key_time = request.META.get('HTTP_OPENKEY')
        print(client_md5_key_time)
        client_md5_key, client_ctime = client_md5_key_time.split('|')
        server_time = time.time()

        # 时间检测
        if server_time - float(client_ctime) > 10:
            return HttpResponse('时间检测 非法')

        # 列表检测
        if client_md5_key in api_key_record:
            return HttpResponse('列表检测 非法')
        else:
            api_key_record[client_md5_key_time] = float(client_ctime) + 10


        # key——time检测
        temp = "%s|%s" % (settings.AUTH_KEY, client_ctime)
        m = hashlib.md5()
        m.update(bytes(temp, encoding="utf8"))
        server_md5_key = m.hexdigest()
        if server_md5_key != client_md5_key:
            return HttpResponse('无法访问')
        elif server_md5_key == client_md5_key:
            res = func(request)
            return HttpResponse(res)

        # 超时的md5需要删除
        for k in list(api_key_record.keys()):
            v = api_key_record[k]
            if server_time > v:
                del api_key_record[k]
    return wrapper