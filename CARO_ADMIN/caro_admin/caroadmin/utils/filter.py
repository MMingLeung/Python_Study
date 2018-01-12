#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
用于组合搜索
'''

from types import FunctionType
from django.utils.safestring import mark_safe
from copy import deepcopy


class FilterOption:
    '''
    封装函数名/字段名称、是否多选、model class中返回用于html的文本和值的函数名称
    '''
    def __init__(self, func_or_field, is_multi=False, text_func=None, value_func=None):
        self.func_or_field = func_or_field
        self.is_multi = is_multi
        self.text_func = text_func
        self.value_func = value_func

    @property
    def is_func(self):
        if isinstance(self.func_or_field, FunctionType):
            return True
        else:
            return False

    @property
    def name(self):
        if self.is_func:
            return self.func_or_field.__name__
        else:
            return self.func_or_field


class FilterList:
    '''
    封装FilterOption对象、当前字段所获取的数据集合、request、当前的对象（BaseCaro或者其继承）
    
    通过__iter__方法，使前端遍历该类的对象时，生成对应的html标签
    '''
    def __init__(self, option, queryset, request, base_obj):
        self.option = option
        self.queryset = queryset
        self.param_dict = deepcopy(request.GET)
        self.base_obj = base_obj
        self.path_info = request.path_info

    def __iter__(self):
        # 生成"全部"标签及其href属性
        yield mark_safe('<div class="all-area">')
        if self.option.name in self.param_dict:
            pop_values = self.param_dict.pop(self.option.name)
            yield mark_safe("<a href='{}?{}'>全部</a>".format(self.path_info, self.param_dict.urlencode()))
            self.param_dict.setlist(self.option.name, pop_values)
        else:
            yield mark_safe("<a href='{}?{}' class='active'>全部</a>".format(self.path_info, self.param_dict.urlencode()))
        yield mark_safe('</div><div class="content-area">')

        # 遍历每一个model对象（每一行数据），
        for row in self.queryset:
            # 是否激活状态
            active = False

            # 多选的url需要深拷贝原GET请求参数
            param_dict = deepcopy(self.param_dict)

            # 如果option对象的model有定义获取value或text方法，通过反射获取。
            value = str(getattr(row, self.option.value_func)() if self.option.value_func else row.pk)
            text = getattr(row, self.option.value_func)() if self.option.text_func else str(row)

            if self.option.is_multi:
                # 多选
                value_list = param_dict.getlist(self.option.name)
                if value in value_list:
                    active = True
                    value_list.remove(value)
                    param_dict.setlist(self.option.name, value_list)
                else:
                    param_dict.appendlist(self.option.name, value)
            else:
                # 单选
                value_list = param_dict.getlist(self.option.name)
                print(value_list, 'value:', value, param_dict)
                if value in value_list:
                    active = True
                param_dict[self.option.name] = value

            # url
            base_url = "{}?{}".format(self.path_info, param_dict.urlencode())
            if active:
                tmp = mark_safe("<a href='{}' class='active'>{}</a>".format(base_url, text))
            else:
                tmp = mark_safe("<a href='{}'>{}</a>".format(base_url, text))
            yield tmp
        yield mark_safe('</div>')
