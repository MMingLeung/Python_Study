from django.shortcuts import render, HttpResponse
from repository import models
from django.core import serializers
import json
from datetime import datetime, date
from backend.page_config import idc_page
from django.db.models import Q
from backend.page_config import asset as ASSET_CONFIG
from repository.forms import AssetForm

# Create your views here.
def get_data_list(model_cls, request, table_config):

    values_list = []
    for row in table_config:
        if not row['q']:
            continue
        values_list.append(row['q'])

    # ========获取搜索条件========
    condition = request.GET.get('condition')
    print(condition)
    condition_dict = json.loads(condition)

    # 最外面的Q
    con = Q()

    for name, values in condition_dict.items():
        ele = Q()  # select * from where xx=1 or xx=2
        ele.connector = 'OR'
        for item in values:
            ele.children.append((name, item))
        con.add(ele, 'AND')

    # ===============



    v = model_cls.objects.filter(con).values(*values_list)
    return v



def curd(request):
    # v = models.Server.objects.all()
    return render(request, "curd.html")


def curd_json(request):
    if request.method == 'DELETE':
        id_list = json.loads(str(request.body, encoding='utf8'))
        print(id_list)
        return HttpResponse('123')
    elif request.method == 'POST':
        pass
    elif request.method == 'GET':
    # 1
    # 无法序列化时间
    # json 扩展支持时间序列化
        class JsonCustomEncoder(json.JSONEncoder):

            def default(self, filed):
                if isinstance(filed, datetime):
                    return filed.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(filed, date):
                    return filed.strftime('%Y-%m-%d')
                else:
                    return json.JSONEncoder.default(self, filed)

        # v = models.Server.objects.values('id', 'hostname', 'create_at')

        # 2
        # v = models.Server.objects.all()

        # 序列化操作
        # 1
        # data = json.dumps(list(v), cls=JsonCustomEncoder)

        # 2
        # data = serializers.serialize('json', v)













        # ==========================

        table_config = [

            {'q': None,   #数据库查询字段
             'title': '', #标题
             'display': True, #是否显示
             'text': {     #内容
                 'tpl': '<input type="checkbox" value="{n1}">',
                 'kwargs': {'n1': '@id'}
             },
             'attrs': {'nid': '@id'},#td标签的属性

             },

            {'q': 'id',
             'title': 'ID',
             'display': True,
             'text': {
                 'tpl': '{n1}',
                 'kwargs': {'n1': '@id'}
             },
             'attrs': {'k1': 'v1', 'k2': '@id'},
             },

            {'q': 'hostname',
             'title': '主机名',
             'display': True,
             'text': {
                 'tpl': '{n1}',
                 'kwargs': {'n1': '@hostname'}
             },
             'attrs': {'edit-enable': 'true', 'k2': '@hostname'},

             },

            {'q': 'create_at',
             'title': '创建时间',
             'display': True,
             'text': {
                 'tpl': '{n1}',
                 'kwargs': {'n1': '@create_at'}
             },
             'attrs': {'k1': 'v1', 'k2': '@create_at'},
             },

            {'q': 'asset__cabinet_num',
             'title': '机柜号',
             'display': True,
             'text': {
                 'tpl': 'BJ-{n1}',
                 'kwargs': {'n1': '@asset__cabinet_num'}
             },
             'attrs': {'k1': 'v1', 'k2': '@asset__cabinet_num'},
             },

            {'q': 'asset__business_unit__name',
             'title': '业务线',
             'display': True,
             'text': {
                 'tpl': '{n1}',
                 'kwargs': {'n1': '@asset__business_unit__name'}
             },
             'attrs': {'k1': 'v1', 'k2': '@asset__business_unit__name'},
             },

            {'q': 'asset__business_unit__id',
             'title': '业务线ID',
             'display': False,
             'text': {
                 'tpl': '{n1}',
                 'kwargs': {'n1': '@asset__business_unit__id'}
             },
             'attrs': {'k1': 'v1', 'k2': '@asset__business_unit__id'},
             },

            # 页面显示：  标题：操作    删除、编辑（a标签）
            {'q': None,
             'title': '操作',
             'display': True,
             'text': {
                 'tpl': '<a href="/del?nid={n1}">删除</a>',
                 'kwargs': {'n1': '@id'}
             },
             },
        ]
        # @+id 数据库中取值

        search_config = [

            {'name': 'hostname__contains', 'text': '主机名', 'condition_type': 'input'},
            # 模糊匹配
            {'name': 'create_at', 'text': '创建时间', 'condition_type': 'input'},
            {'name': 'asset__cabinet_num', 'text': '机柜号', 'condition_type': 'input'},
        ]

        # ========获取搜索条件========
        condition = request.GET.get('condition')
        print(condition)
        condition_dict = json.loads(condition)

        # 最外面的Q
        con = Q()

        for name, values in condition_dict.items():
            ele = Q()  # select * from where xx=1 or xx=2
            ele.connector = 'OR'
            for item in values:
                ele.children.append((name, item))
            con.add(ele, 'AND')

            # ===============

        values_list = []
        #把‘q’添加到列表中，作为数据库查询的条件
        for row in table_config:
            if not row['q']:
                continue
            values_list.append(row['q'])

        v = models.Server.objects.filter(con).values(*values_list)

        ret = {
            'table_config': table_config,
            'server_list': list(v),
            'search_config':search_config,
        }

        return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))


def asset(request):
    return render(request, 'asset.html')


def asset_json(request):
    if request.method == 'DELETE':
        id_list = json.loads(str(request.body, encoding='utf8'))
        print(id_list)
        return HttpResponse('123')
    elif request.method == 'POST':
        response = {'status':True, 'data':None}
        try:
            create_dict = request.POST.get("create_dict")
            create_dict = json.loads(create_dict)
            print(create_dict)
            tags = create_dict.pop('tag')
            print(tags)
            add_obj = models.Asset.objects.create(**create_dict)
            print(add_obj.id)
            for i in tags:
                add_obj.tag.add(add_obj.id, i)
        except Exception as e:
            response['status'] = False
            response['data'] = e
            return HttpResponse(json.dumps(response))
        return HttpResponse(json.dumps(response))
    elif request.method == 'PUT':
        all_list = json.loads(str(request.body, encoding='utf8'))
        print(all_list)
        for row in all_list:
            nid = row.pop('id')
            models.Asset.objects.filter(id=nid).update(**row)
        return HttpResponse('123')
    elif request.method == 'GET':

        # 1
        # 无法序列化时间
        # json 扩展支持时间序列化
        class JsonCustomEncoder(json.JSONEncoder):

            def default(self, filed):
                if isinstance(filed, datetime):
                    return filed.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(filed, date):
                    return filed.strftime('%Y-%m-%d')
                else:
                    return json.JSONEncoder.default(self, filed)

        # v = models.Server.objects.values('id', 'hostname', 'create_at')

        # 2
        # v = models.Server.objects.all()

        # 序列化操作
        # 1
        # data = json.dumps(list(v), cls=JsonCustomEncoder)

        # 2
        # data = serializers.serialize('json', v)

        # ==========================


        # @+id 数据库中取值

        #=================


        #=================




        # [{},{},{}]
        # obj.get_xx_display直接取内容
        v = get_data_list(models.Asset, request, ASSET_CONFIG.table_config)
        print(v)

        #===============================模态对话框
        motai_config = [
            {'q': 'cabinet_num',  # 数据库查询字段
             'title': '机柜号',  # 标题
             'display': True,  # 是否显示
             'text': {  # 内容
                 'tpl': '<input type="text" value="" class="form-control">',

             },
             'attrs': {'type': 'input', 'class':'form-control', 'name':'cabinet_num', },  # td标签的属性
             },

            {'q': 'cabinet_order',  # 数据库查询字段
             'title': '机柜内序号',  # 标题
             'display': True,  # 是否显示
             'text': {  # 内容
                 'tpl': '<input type="text" value="" class="form-control">',
             },
             'attrs': {'type': 'input', 'class': 'form-control', 'name': 'cabinet_order'},  # td标签的属性
             },

            {'q': 'idc',  # 数据库查询字段
             'title': 'idc',  # 标题
             'display': True,  # 是否显示
             'text': {  # 内容
                 'tpl': '<input type="text" value="" class="form-control">',
             },
             'attrs': {'type': 'select', 'class': 'form-control', 'id': 'idc','globalKey':'idc_choices'},  # td标签的属性
             },

            {'q': 'device_type_id',  # 数据库查询字段
             'title': '设备类型',  # 标题
             'display': True,  # 是否显示
             'text': {  # 内容
                 'tpl': '<input type="text" value="" class="form-control">',
             },
             'attrs': {'id': 'device_type_id', 'type': 'select', 'class': 'form-control', 'name': 'device_type_id', 'globalKey': 'device_type_choices'},  # td标签的属性
             },

            {'q': 'device_status_id',  # 数据库查询字段
             'title': '设备状态',  # 标题
             'display': True,  # 是否显示
             'text': {  # 内容
                 'tpl': '<input type="text" value="" class="form-control">',
             },
             'attrs': {'id': 'device_status_id', 'type': 'select', 'class': 'form-control', 'name': 'device_status_id',
                       'globalKey': 'device_status_choices'},  # td标签的属性
             },

            {'q': 'business_unit',  # 数据库查询字段
             'title': '业务线',  # 标题
             'display': True,  # 是否显示
             'text': {  # 内容
                 'tpl': '<input type="text" value="" class="form-control">',
             },
             'attrs': {'id': 'business_unit','type': 'select', 'class': 'form-control', 'name': 'business_unit',
                       'globalKey': 'business_unit_choices'},  # td标签的属性
             },

            {'q': 'tag',  # 数据库查询字段
             'title': '标签',  # 标题
             'display': True,  # 是否显示
             'text': {  # 内容
                 'tpl': '<input type="text" value="" class="form-control">',
             },
             'attrs': {'id': 'tag','type': 'checkbox', 'class': 'form-control', 'name': 'tag',
                       'globalKey': 'tag_choices', 'multiple1':'multiple'},  # td标签的属性
             },

        ]



        ret = {
            'table_config': ASSET_CONFIG.table_config,
            'server_list': list(v),
            'global_dict': {
            'device_status_choices': models.Asset.device_status_choices,
            'device_type_choices': models.Asset.device_type_choices,
            'idc_choices':list(models.IDC.objects.values_list('id', 'name')),
            'business_unit_choices':list(models.BusinessUnit.objects.values_list('id', 'name')),
            'tag_choices':list(models.Tag.objects.values_list('id', 'name'))
            },
            'search_config': ASSET_CONFIG.search_config,
            'motai_config':motai_config
        }
        return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))


def idc(request):
    return render(request, 'idc.html')


def idc_json(request):
    if request.method == 'DELETE':
        id_list = str(request.body, encoding='utf8')
        print(id_list)
        return HttpResponse('123')
    elif request.method == 'PUT':
        all_list = str(request.body, encoding='utf8')
        print(all_list)
        return HttpResponse('123')
    elif request.method == 'GET':

        class JsonCustomEncoder(json.JSONEncoder):

            def default(self, filed):
                if isinstance(filed, datetime):
                    return filed.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(filed, date):
                    return filed.strftime('%Y-%m-%d')
                else:
                    return json.JSONEncoder.default(self, filed)




        values_list = []
        for row in idc_page.table_config:
            if not row['q']:
                continue
            values_list.append(row['q'])

        v = models.IDC.objects.values(*values_list)
        # [{},{},{}]
        # obj.get_xx_display直接取内容



        ret = {
            'table_config': idc_page.table_config,
            'server_list': list(v),
            'global_dict':{},

        }
        return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))


def chart(request):
    return render(request, 'chart.html')