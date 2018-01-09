#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
配置文件说明：
1、table_config:
    {'q': '数据库查询字段名',
     'title': '表头中文',
     'disable': 是否显示,
     'text':
         {
             'tpl': '格式化的key',
             'kwargs': {'key': '格式化的内容'} # @+字段：取值 @@+字段：取固定元组里的值
         },
     'attrs': {
         'edit-enable': '能否编辑',
         'edit-type': '编辑框input/select',
         'global_key': '对应@@功能',
         'origin': '原始值',
         'name': '数据库查询字段名'
     }
     
2、 search_config： 
    {'name': '数据库查询字段名', 'text': '中文名', 'search_type': '搜索框input/select', },
    {'name': '数据库查询字段名', 'text': '中文名', 'search_type': '搜索框input/select', 'global_key': '取model中choices值/外键的key'},
'''


table_config = [
    {'q': None,
     'title': '选项',
     'disable': True,
     'text':
         {
             'tpl': '<input type="checkbox" value={n1}>',
             'kwargs': {'n1': '@id'}
         },
     'attrs': {
         'k1': 'v1'
     },
     },
    {'q': 'id',
     'title': 'ID',
     'disable': False,
     'text':
         {
             'tpl': '{n1}',
             'kwargs': {'n1': '@id'}
         },
     'attrs': {
         'k1': '@id'
     }
     },
    {'q': 'device_type_id',
     'title': '设备类型',
     'disable': True,
     'text':
         {
             'tpl': '{n1}',
             'kwargs': {'n1': '@@device_type_choices'}
         },
     'attrs': {
         'k1': '@@device_type_choices',
         'edit-enable': 'true',
         'edit-type': 'select',
         'global_key': 'device_type_choices',
         'origin': '@device_type_id',
         'name': 'device_type_id'
     }
     },
    {'q': 'device_status_id',
     'title': '设备状态',
     'disable': True,
     'text':
         {
             'tpl': '{n1}',
             'kwargs': {'n1': '@@device_status_choices'}
         },
     'attrs': {
         'k1': '@@device_status_choices',
         'edit-enable': 'true',
         'edit-type': 'select',
         'global_key': 'device_status_choices',
         'origin': '@device_status_id',
         'name': 'device_status_id'
     }
     },
    {'q': 'cabinet_num',
     'title': '机柜号',
     'disable': True,
     'text':
         {
             'tpl': '{n1}',
             'kwargs': {'n1': '@cabinet_num'}
         },
     'attrs': {
         'k1': '@cabinet_num',
         'edit-enable': 'true',
         'origin': '@cabinet_num',
         'name': 'cabinet_num',
     }
     },
    {'q': 'cabinet_order',
     'title': '机柜内编号',
     'disable': True,
     'text':
         {
             'tpl': '{n1}',
             'kwargs': {'n1': '@cabinet_order'}
         },
     'attrs': {
         'k1': '@cabinet_order',
         'edit-enable': 'true',
         'origin': '@cabinet_order',
         'name': 'cabinet_order',
     }
     },
    {'q': 'idc__name',
     'title': '机房',
     'disable': True,
     'text':
         {
             'tpl': '{n1}',
             'kwargs': {'n1': '@idc__name'}
         },
     'attrs': {
         'k1': '@idc__name',
         'edit-enable': 'true',
         'edit-type': 'select',
         'global_key': 'idc_choices',
         'origin': '@idc_id',
         'name': 'idc_id',
     }
     },
    {'q': 'idc_id',
     'title': '机房',
     'disable': False,
     'text':
         {},
     'attrs': {
         'k1': '@idc_id',
         'origin': '@idc_id',
         'name': 'idc_id',
     },
     },
    {'q': 'business_unit_id',
     'title': '机房',
     'disable': False,
     'text':
         {},
     'attrs': {
         'origin': '@business_unit_id',
         'name': 'business_unit_id',
     },
     },
    {'q': 'business_unit__name',
     'title': '业务线',
     'disable': True,
     'text':
         {
             'tpl': '{n1}',
             'kwargs': {'n1': '@business_unit__name'}
         },
     'attrs': {
         'edit-enable': 'true',
         'edit-type': 'select',
         'global_key': 'business_unit_choices',
         'name': 'business_unit_id',
         'origin': '@business_unit_id',
     }
     },
    {'q': None,
     'title': '操作',
     'disable': True,
     'text':
         {
             'tpl': '<a href={n1}>删除</a>',
             'kwargs': {'n1': '@id'}
         },
     'attrs': {
         'k1': 'v1'
     }
     },
]

search_config = [
    {'name': 'cabinet_num__contains', 'text': '机柜号', 'search_type': 'input', },
    {'name': 'device_type_id', 'text': '设备类型', 'search_type': 'select', 'global_key': 'device_type_choices'},
]