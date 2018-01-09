#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import hashlib
import time
import importlib
from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from repository import models
from server.lib.data_cipher import encipher, decipher
from server import serializers

# django自带的序列化工具
# from django.core import serializers as ser

# from rest_framework import viewsets


api_key_record = {}

def asset(request):
    if request.method == 'GET':
        # META包含请求所有信息
        key = request.META.get('HTTP_OPENKEY')
        client_md5_key, client_ctime = key.split('|')
        server_time = time.time()

        if not key:
            return HttpResponse('非法用户')
        if server_time - float(client_ctime) > 10:
            return HttpResponse('超时')

        for key in list(api_key_record.keys()):
            if server_time > api_key_record[key]:
                del api_key_record[key]

        temp = "%s|%s" % (settings.AUTH_KEY, client_ctime)
        m = hashlib.md5()
        m.update(temp.encode('utf-8'))
        server_md5 = m.hexdigest()

        if client_md5_key != server_md5:
            return HttpResponse('非法KEY， 时间不对')
        else:
            if key in api_key_record:
                return HttpResponse('key已使用')
            else:
                api_key_record[key] = float(client_ctime) + 10
                return HttpResponse('关键信息')

    elif request.method == 'POST':
        print(len(request.body))
        data_encipher = decipher(request.body)
        data = json.loads(data_encipher)
        host_name = data['basic']['data']['hostname']

        # 旧数据
        server_obj = models.Server.objects.filter(hostname=host_name).first()

        for name, path in settings.API_PLUGINS.items():
            model_path, class_name = path.rsplit('.', 1)
            class_ = importlib.import_module(model_path)
            m = getattr(class_, class_name)
            if hasattr(m, 'initial'):
                plugin_obj = m.initial(data, server_obj)
            else:
                plugin_obj = m(data, server_obj)
            plugin_obj.execute()
        return HttpResponse('123')

# ################################# 自定义API #######################################
def servers(request):
    # 获取
    if request.method == 'GET':
        ret = {'data': None, 'code': None}
        server_list = list(models.Server.objects.values('id', 'hostname'))
        if server_list:
            ret['code'] = 200
        else:
            ret['code'] = 404
        ret['data'] = server_list
        # safe：可以允许字典以外的数据类型传输
        return JsonResponse(ret, safe=False)
    # 新增
    elif request.method == 'POST':
        return JsonResponse(status=201)

def servers_detail(request, id):
    if request.method == 'GET':
        obj = models.Server.objects.filter(id=id).first()
        return JsonResponse('get')
    elif request.method == 'DELTET':
        obj = models.Server.objects.filter(id=id).first().delete()
        return JsonResponse('del')
    elif request.method == 'PUT':
        # data = request.body.decode('utf-8')
        # obj = models.Server.objects.filter(id=id).update()
        return JsonResponse('put')
# ##################################################################################


# ################################# 扩展REST API ####################################
class ServerView(APIView):
    def get(self, request, *args, **kwargs):
        '''
        获取列表
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        '''

        data_list = models.Server.objects.all()

        # django自带序列化
        # data = serializers.serialize('json', data_list)

        # 可自定制序列化的类：序列化和form验证
        serializer = serializers.MySerializer(instance=data_list, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, *args, **kwargs):
        '''
        创建数据
        :param request: request经过封装
        :param args: 
        :param kwargs: 
        :return: 
        '''
        data = JSONParser().parse(request)
        serializer = serializers.MySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return HttpResponse(status=201)

class ServerDetail(APIView):
    def get(self, request, pk):
        '''
        获取单条数据详细信息
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        '''
        obj = models.Asset.objects.filter(id=pk).first()
        serializer = serializers.MySerializer(instance=obj)
        return JsonResponse(serializer.data, status=200)

    def post(self, request, pk):
        '''
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        '''
        pass

    def delete(self, request, pk):
        obj = models.Asset.objects.filter(id=pk).delete()
        pass

    def put(self, request, pk):
        '''
        修改单条数据
        :param request: 
        :param pk: 
        :return: 
        '''
        obj = models.Asset.objects.filter(id=pk).delete()
        data = JSONParser().parse(request)
        serializer = serializers.MySerializer(instance=obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(status=200)
# ##################################################################################


# ################################ 原生rest framwork ################################
# from rest_framework import serializers
# class ServerSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = models.Server
#         # 只能操作和显示该字段
#         fields = ('id', 'hostname')
#         depth = 1 # 0<= depth <= 10 查询表的层级

# class ServerViewSet(viewsets.ModelViewSet):
#     # queryset 名字不能修改 获取数据
#     queryset = models.Server.objects.all()
#     # 验证和数据库操作
#     serializer_class = ServerSerializer
####################################################################################