#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
数据表格、批量操作按钮的渲染
'''


from types import FunctionType
from django.template import Library


register = Library()

def header(change_list):
    '''
    表格头的显示
    
    如果用户没有设置list_display，表格头显示model_name；
    否则如果是函数返回其结果；
    如果是字段名称，根据该字符串获取field对象的verbose_name属性。
    :param change_list: 
    :return: 
    '''
    if change_list.list_display == '__str__':
        yield change_list.basecaro_obj.model_class._meta.model_name
    else:
        for name in change_list.list_display:
            if isinstance(name, FunctionType):
                yield name(change_list.basecaro_obj, is_header=True)
            else:
                yield change_list.basecaro_obj.model_class._meta.get_field(name).verbose_name


def inner(change_list):
    '''
    表格内容的显示
    
    如果用户没有自定义__str__，返回row(model对象）的__str__的值；
    否则根据字段名称以反射形式获取值存放到列表里，如果是多对多则需要额外处理。
    :param change_list: 
    :return: 
    '''
    for row in change_list.result_list:
        if change_list.list_display == '__str__':
            yield [str(row), ]
        else:
            res = []
            # 多对多的一种对象暂未找到方法导入，暂时用此方法获取
            if hasattr(row, 'staff'):
                m2m_obj = getattr(row, 'staff')
            else:
                m2m_obj = None

            for name in change_list.list_display:
                if isinstance(name, FunctionType):
                    res.append(name(change_list.basecaro_obj, row))
                else:
                    obj = getattr(row, name)
                    choices = change_list.basecaro_obj.model_class._meta.get_field(name).choices
                    if choices:
                        res.append(choices[obj][1])
                    elif obj and isinstance(obj, type(m2m_obj)):
                        m2m_str = ''
                        for _ in obj.select_related():
                            m2m_str += str(_) + " "
                        res.append(m2m_str)
                    else:
                        res.append(obj)
            yield res


@register.inclusion_tag('md.html')
def show_list(change_list):
    return {'result_display': inner(change_list),
            'header_list': header(change_list)}

@register.inclusion_tag('changelist_action.html')
def show_action(change_list):
    return {'action_list': ((item.__name__, item.text) for item in change_list.action_list)}
