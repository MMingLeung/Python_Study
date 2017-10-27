from django.shortcuts import render, HttpResponse
import json
from repository import models
from django.conf import settings
import hashlib
import time
from django.http import JsonResponse
from api.service import PluginsManage
from utils.decrypt import decrypt
from utils.auth import auth
# Create your views here.




@auth
def asset(request):

    # client_md5_key_time = request.META.get('HTTP_OPENKEY')
    # client_md5_key, client_ctime = client_md5_key_time.split('|')
    # server_time = time.time()
    #
    # # 时间检测
    # if server_time - float(client_ctime) > 10:
    #     return HttpResponse('时间检测 非法')
    #
    # # 列表检测
    # if client_md5_key in api_key_record:
    #     return HttpResponse('列表检测 非法')
    # else:
    #     api_key_record[client_md5_key_time] = float(client_ctime) + 10
    #
    # # key——time检测
    # temp = "%s|%s" % (settings.AUTH_KEY, client_ctime)
    # m = hashlib.md5()
    # m.update(bytes(temp, encoding="utf8"))
    # server_md5_key = m.hexdigest()
    # if server_md5_key != client_md5_key:
    #     return HttpResponse('无法访问')
    # # elif server_md5_key == client_md5_key:
    # #     return HttpResponse('允许访问')
    #
    # # 超时的md5需要删除
    # for k in list(api_key_record.keys()):
    #     v = api_key_record[k]
    #     if server_time > v:
    #         del api_key_record[k]



    if request.method == 'GET':
        #方式1：令牌（静态存在隐患）
        # open_key = request.META.get('HTTP_OPENKEY')
        # if open_key != settings.AUTH_KEY:
        #     return HttpResponse('无法访问')
        # return HttpResponse('允许访问')
        print(13123123123123)
        #方法1改进：
        return 'get'





    elif request.method == 'POST':

        ################
        #加密解密json.loads
        server_info = decrypt(request.body)
        server_info = json.loads(server_info)
        # print(server_info)

        ###############


        # server_info = json.loads(request.body.decode('utf8'))
        host_name = server_info['basic']['data']['hostname']
        server_obj = models.Server.objects.filter(hostname=host_name).first()
        if not server_obj:
            return HttpResponse('无该资产')

        #server_obj可以获取基本信息（单条）
        #旧资产信息
        # asset_obj = server_obj.asset
        # disk_list = server_obj.disk.all()
        # mem_list = server_obj.memory.all()
        #处理新旧信息
        '''
        1、比较新旧资产：根据槽位、名称。例如：新：['5', '1'],老：['4', '5', '6']
        2、建立集合取交集，差集。
            新增：1， 删除：4，6 ，更新：5
        3、增加：根据上述值去server_info表中找到相应详细信息，入库
        4、删除：
        5、更新：比较新老数据，不一致的更新
        #硬盘、内存
        #基本信息
        '''
        # ============处理基本信息===========
        server_info['basic']['data'].pop('hostname')
        models.Server.objects.filter(hostname=host_name).update(**server_info['basic']['data'])



        # ============处理硬盘===========
        # new_disk_slot_set = set()
        # old_disk_slot_set = set()
        # #1.1、disk新资产槽位slot
        # for k,v in server_info.items():
        #     if k == 'disk':
        #         # new_disk_slot_set.add(v['data']['slot'])
        #         for k,j in v['data'].items():
        #             new_disk_slot_set.add(j['slot'])
        # # print("new_disk_slot_set:",new_disk_slot_set)
        # #1.2、disk旧资产槽位slot
        # for i in disk_list:
        #     old_disk_slot_set.add(i.slot)
        #
        # #2.1、新增：取差集
        # new_create = new_disk_slot_set - old_disk_slot_set
        # need_update = new_disk_slot_set & old_disk_slot_set
        # need_delete = old_disk_slot_set - new_create - need_update
        # # print('need_update',need_update)
        # # print('new_create',new_create)
        # # print('need_delete',need_delete)
        # for k,v in server_info['disk']['data'].items():
        #     # print(v)
        #     if v['slot'] in new_create:
        #         v['server_obj_id'] = server_obj.id
        #         models.Disk.objects.filter(server_obj=server_obj).create(**v)
        # #2.2、更新：并集
        #     if v['slot'] in need_update:
        #         models.Disk.objects.filter(server_obj=server_obj, slot=v['slot']).update(**v)
        # #2.3、删除
        # models.Disk.objects.filter(server_obj=server_obj, slot__in=need_delete).delete()

        # add_to_db(server_info, server_obj, disk_list, 'disk')
        # ============处理硬盘完毕===========


        # ============处理内存===========
        # add_to_db(server_info, server_obj, mem_list, 'memory')
        # ============处理内存完毕===========

        # ============处理硬盘（上课内容）===========
        # if not server_info['disk']['status']:
        #     models.ErrorLog.objects.create(content=server_info['disk']['data'], asset_obj=server_info.asset, title='【%s】采集错误信息' % host_name)
        # new_disk_dict = server_info['disk']['data']
        # old_disk = models.Disk.objects.filter(server_obj=server_obj)
        #
        # new_slot_list = list(new_disk_dict.keys())
        # old_slot_list = []
        # for item in old_disk:
        #     old_slot_list.append(item.slot)
        # #交集：
        # update_list = set(new_slot_list).intersection(old_slot_list)
        #
        # #差集
        # create_list = set(new_slot_list).difference(old_slot_list)
        #
        # #差集 老的存在新的没有
        # delete_list = set(old_slot_list).difference(new_slot_list)
        #
        # #delete
        # if delete_list:
        #     models.Disk.objects.filter(server_obj=server_obj, slot__in=delete_list).delete()
        #     #log
        #     models.AssetRecord.objects.create(server_obj=server_obj.asset, content="移除硬盘：%s" % (','.join(delete_list)), )
        #
        # #create
        # record_list = []
        # for slot in create_list:
        #     disk_dict = new_disk_dict[slot] #字典
        #     disk_dict['server_obj'] = server_obj
        #     models.Disk.objects.create(**disk_dict)
        #     temp = '新增硬盘：位置{slot},容量{capacity},型号{model,类型{pd_type}'.format(**disk_dict)
        #     record_list.append(temp)
        # if record_list:
        #     content = ";".join(record_list)
        #     models.AssetRecord.objects.create(server_obj=server_obj.asset,
        #                                       content=content)
        #
        # #update
        # record_list = []
        # row_map = {'capacity':'容量', 'pd_type':'类型', 'model':'型号'}
        # for slot in update_list:
        #     new_disk_row = new_disk_dict[slot]
        #     old_disk_row = models.Disk.objects.filter(slot=slot, server_obj=server_obj).first()
        #     for k,v in new_disk_dict.items():
        #         #k:capacity,slot.....
        #         #v:5xx,1...
        #         #反射
        #         value = getattr(old_disk_row, k)
        #         if v != value:
        #             record_list.append("槽位%s，%s由%s变成为%s" % (slot, row_map[k], value, v))
        #             setattr(old_disk_row, k, v)
        #     old_disk_row.save()
        # if record_list:
        #     content = ";".join(record_list)
        #     models.AssetRecord.objects.create(server_obj=server_obj.asset,
        #                                       content=content)
        #

        #处理硬盘数据作业
        res = PluginsManage(server_info , host_name, server_obj).execute_plugin()
        print(res)

        return HttpResponse('api_asset')


#API
#http://127.0.0.1:8000/api/servers/1.html GET 获取单条信息
#http://127.0.0.1:8000/api/servers.html  获取多条信息
#http://127.0.0.1:8000/api/servers.html POST 增加信息
#http://127.0.0.1:8000/api/servers/1.html DELETE 删除单条信息
#http://127.0.0.1:8000/api/servers/1.html PUT 更新信息

def servers(request):
    '''
    get:获取
    post：增加
    :param request: 
    :return: 
    '''
    if request.method =='GET':
        v = models.Server.objects.values_list('id', 'hostname' )
        server_list = list(v)
        return JsonResponse(server_list, safe=False)
    elif request.method == 'POST':
        # models.Server.objects.create()
        return JsonResponse(status=200)

def servers_detail(request, id):
    if request.method == 'GET':
        v = models.Server.objects.filter(id=id).first()
        return JsonResponse(dict(v))
    elif request.method == 'POST':
        pass
    elif request.method == 'PUT':
        #修改
        detail = request.body
        return HttpResponse('11')




#=================================================
#3、继承类
from rest_framework import viewsets,serializers

class ServerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Server
        fields = ('id', 'hostname', 'sn', 'asset_id') #只能操作和显示该字段
        # exclude = ('xx',) #除外
        depth = 1 #0：只查询自己，1：查询下一层


#本质继承是django的view的CBV
class ServerViewSet(viewsets.ModelViewSet):
    #名字不能改，用于显示
    queryset = models.Server.objects.all().order_by('-id')
    #验证和数据库操作，显示哪里列
    serializer_class = ServerSerializer
#========================================




from rest_framework.views import APIView
from rest_framework .parsers import JSONParser
from . import serializers

#自定制rest_framework
class ServerView(APIView):



    def get(self, request, *args, **kwargs):
        '''
        获取列表
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        '''
        # 自己序列化
        # from django.core import serializers
        data_list = models.UserProfile.objects.all()
        # data = serializers.serialize('json', data_list)
        # return HttpResponse(data)

        #rest_framework序列化+form验证
        #many=True 多条数据， instance=data_list 对象
        serializer = serializers.MySerializer(instance=data_list, many=True)
        print(serializer.data)

        return JsonResponse(serializer.data, safe=False)


    def post(self, request, *args, **kwargs):
        '''
        新增数据
        :param request: 
         :param args: 
        :param kwargs: 
        :return: 
        '''
        #封装后的request ,
        print(request, type(request))
        #获取数据
        print(request._request.body)
        # print(request.data)
        # models.UserProfile.objects.create(**request.data)


        data = JSONParser().parse(request)
        serializer = serializers.MySerializer(data=data)
        if serializer.is_valid():
            print(serializer.data)
            print(serializer.errors)
            print(serializer.validated_data)
            serializer.save() #执行self.create(validate_data)
        return HttpResponse('123')


class ServerDetail(APIView):

    def get(self, request, nid):
        '''
        获取单条数据
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        '''
        obj = models.UserProfile.objects.filter(id=nid).first()
        #序列化
        serializer = serializers.MySerializer(instance=obj)
        return JsonResponse(serializer.data)


    def delete(self, request, nid):
        '''
        删除单条数据
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        '''
        obj = models.UserProfile.objects.filter(id=nid).first().delete()
        return HttpResponse(status=204)



    def put(self, request, nid):
        '''
        修改单条数据
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        '''
        obj = models.UserProfile.objects.filter(id=nid).first().delete()
        #原数据
        data = JSONParser().parse(request)
        serializer = serializers.MySerializer(instance=obj, data=data)
        if serializer.is_valid():
            print(serializer.data)
            print(serializer.errors)
            print(serializer.validated_data)
            serializer.save()  # 执行self.create(validate_data)
            return HttpResponse(status=200)


