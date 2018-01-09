#!/usr/bin/env python
# -*- coding:utf-8 -*-


table_config = [
        {'q': None,
         'title': '选项',
         'disable': True,
         'text':
             {
                 'tpl': '<input type="checkbox" value={n1}>',
                 'kwargs': {'n1': '@id'}
             },
         'attrs':{
             'k1':'v1'
         }

         },
        {'q': 'id',
         'title': 'ID',
         'disable': False,
         'text':
             {
                 'tpl':'{n1}',
                 'kwargs':{'n1':'@id'}
             },
         'attrs': {
             'k1': '@id'
         }
         },
        {'q': 'hostname',
         'title': '主机名',
         'disable': True,
         'text':
             {
                 'tpl':'{n1}',
                 'kwargs':{'n1':'@hostname'}
             },
         'attrs': {
             'k1': '@hostname',
             'edit-enable':'true',
             'origin': '@hostname',
             'name': 'hostname'
         }
         },
        {'q': 'asset__business_unit__name',
         'title': '业务线',
         'disable': True,
         'text':
             {
                 'tpl':'{n1}',
                 'kwargs':{'n1':'@asset__business_unit__name'}
             },
         'attrs': {
             'k1': '@asset__business_unit__name'
         }
         },
        {'q': None,
         'title': '操作',
         'disable': True,
         'text':
             {
                 'tpl':'<a href={n1}>删除</a>',
                 'kwargs':{'n1':'@id'}
             },
         'attrs': {
             'k1': 'v1'
         }
         },
    ]

search_config = [
    {'name': 'hostname', 'text': '主机名', 'search_type': 'input', },
    {'name': 'asset__business_unit__name', 'text': '业务线', 'search_type': 'input'},
]