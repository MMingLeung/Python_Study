#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from django.shortcuts import render, HttpResponse, redirect
from repository import models
from backend.page_config import asset as asset_config
from backend.page_config import server as server_config
from backend.utils import data_parser
from backend.utils.json_cls import JsonCustomEncoder
from rbac import models as rbacmodels
from rbac.service import initial_permission


def server(request):
    if request.method == 'GET':
        return render(request, 'server.html')
    elif request.method == 'POST':
        return HttpResponse(status=200)

def server_json(request):
    if request.method == 'GET':
        conditions = json.loads(request.GET.get('condition'))
        server_list = data_parser.get_data_list(request, server_config.table_config, conditions, models.Server)
        ret = {
            'server_list': list(server_list),
            'table_config': server_config.table_config,
            'global_dict': {},
            'search_config': server_config.search_config,
        }
        return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))
    elif request.method == 'PUT':
        all_list_json = request.body.decode('utf-8')
        all_list = json.loads(all_list_json)
        for row in all_list:
            if row:
                id = row.pop('id')
                models.Server.objects.filter(id=id).update(**row)
        return HttpResponse(status=201)

def asset(request):
    if request.method == 'GET':
        return render(request, 'asset.html')

def asset_json(request):
    if request.method == 'GET':
        conditions = json.loads(request.GET.get('condition'))
        server_list = data_parser.get_data_list(request, asset_config.table_config, conditions, models.Asset)
        device_status_choices = models.Asset.device_status_choices
        device_type_choices = models.Asset.device_type_choices
        ret = {
            'server_list': list(server_list),
            'table_config': asset_config.table_config,
            'global_dict':{
                'device_status_choices': device_status_choices,
                'device_type_choices': device_type_choices,
                'idc_choices':list(models.IDC.objects.values_list('id', 'name')),
                'business_unit_choices':list(models.BusinessUnit.objects.values_list('id', 'name'))
            },
            'search_config':asset_config.search_config,
        }
        return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))
    elif request.method == 'PUT':
        all_list_json = request.body.decode('utf-8')
        all_list = json.loads(all_list_json)
        for row in all_list:
            if row:
                id = row.pop('id')
                models.Asset.objects.filter(id=id).update(**row)
        return HttpResponse(status=201)
    elif request.method == 'DELETE':
        '''
        执行删除数据库信息相关操作
        '''
        print(request.body)
        return HttpResponse(status=204)

def chart(request):
    return render(request, 'chart.html')

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        obj = rbacmodels.User.objects.filter(username=username, password=password).first()
        if obj:
            initial_permission(request, obj.id)
            return redirect('/backend/asset.html')
        else:
            return HttpResponse('账号或密码错误')