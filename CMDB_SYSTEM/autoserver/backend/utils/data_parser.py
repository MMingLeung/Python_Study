#!/usr/bin/env python
# -*- coding:utf-8 -*-


def get_data_list(request, table_config, conditions, model_cls):
    '''
    用于组合搜索数据库查询
    :param request: 
    :param table_config: 
    :param conditions: 
    :param model_cls: 
    :return: 
    '''
    from django.db.models import Q
    con = Q()
    for name, values in conditions.items():
        element = Q()
        element.connector = 'OR'
        for item in values:
            element.children.append((name, item))
        con.add(element, 'AND')
    filter_list = []
    for item in table_config:
        if not item['q']:
            continue
        filter_list.append(item['q'])
    server_list = model_cls.objects.filter(con).values(*filter_list)
    return server_list