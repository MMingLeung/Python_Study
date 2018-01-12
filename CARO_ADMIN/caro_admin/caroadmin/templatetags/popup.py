#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
用于添加页面的数据处理，针对FK、M2M添加PopUp功能，以及相关页面渲染。
'''


from django.template import Library
from django.forms import ModelChoiceField
from django.urls import reverse
from caroadmin.service import site


register = Library()

@register.inclusion_tag('popup.html')
def add_list(form):
    form_list = []
    for item in form:
        pop_dict = {'item': None, 'is_pop': False, 'pop_url': None}
        if isinstance(item.field, ModelChoiceField) and item.field.queryset.model in site._registry :
            pop_dict['item'] = item
            pop_dict['is_pop'] = True
            target_app_label = item.field.queryset.model._meta.app_label
            target_model_name = item.field.queryset.model._meta.model_name
            base_url = reverse("{}:{}_{}_add".format(site.name_space, target_app_label, target_model_name))
            pop_dict['pop_url'] = base_url
        else:
            pop_dict['item'] = item
        form_list.append(pop_dict)

    return {'form':form_list}