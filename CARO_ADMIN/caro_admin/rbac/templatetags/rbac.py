#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
RBAC 菜单树生成函数
'''
import re
import os
from django.conf import settings
from django.template import Library
from django.utils.safestring import mark_safe


def process_menu_tree(request):
    '''
    
    :param request: 
    :return: 
    '''

    # 获取menu_list、permission_menu_list
    permission_menu_dict = request.session[settings.RBAC_PERMISSION_MENU_DICT_SESSION_KEY]
    menu_list = permission_menu_dict[settings.RBAC_MENU_LIST_SESSION_KEY]
    permission_menu_list = permission_menu_dict[settings.RBAC_PERMISSION_LIST_SESSION_KEY]

    # permission_url挂靠到menu_list里的字典中
    all_menu_dict = {}
    for menu in menu_list:
        menu['opened'] = False
        menu['status'] = False
        menu['child'] = []
        all_menu_dict[menu['id']] = menu

    for per_item in permission_menu_list:
        item = {
            'id': per_item['permission__id'],
            'caption': per_item['permission__caption'],
            'url': per_item['permission__url'],
            'parent_id': per_item['permission__menu_id'],
            'opened': False,
            'status': True,
        }
        menu_id = item['parent_id']
        all_menu_dict[menu_id]['child'].append(item)

        if re.match(item['url'], request.path_info):
            item['opened'] = True

        if item['opened']:
            pid = item['parent_id']
            while not all_menu_dict[pid]['opened']:
                all_menu_dict[pid]['opened'] = True
                pid = all_menu_dict[pid]['parent_id']
                if not pid:
                    break

        if item['status']:
            pid = item['parent_id']
            while not all_menu_dict[pid]['status']:
                all_menu_dict[pid]['status'] = True
                pid = all_menu_dict[pid]['parent_id']
                if not pid:
                    break

    # 菜单的层级关系
    result = []
    for menu in menu_list:
        if menu['parent_id']:
            all_menu_dict[menu['id']]['child'].append(menu)
        else:
            result.append(menu)
    return result


def build_menu_tree(menu_list):
    tpl1 = '''
    <li class="{2}">
        <a href="#">
            <i class="fa fa-bar-chart-o"></i> 
            <span class="nav-label">{0}</span>
            <span class="fa arrow"></span>
        </a>
        <ul class="{3}">
             {1}
        </ul>
    </li>'''
    tpl2 = '''
    <li class="{1}">
        <a href="{0}" >{2}</a>
    </li>
    '''
    result = ''
    for menu in menu_list:
        if not menu['status']:
            continue
        if menu.get('url'):
            result += tpl2.format(menu['url'], "active" if menu['opened'] else "", menu['caption'])
        else:
            if menu.get('child'):
                child = build_menu_tree(menu.get('child'))
            else:
                child = ""
            result += tpl1.format(menu['caption'], child, "active" if menu['opened'] else "", "nav nav-second-level collapse in" if menu['opened'] else "nav nav-second-level collapse")
    return result


register = Library()

@register.simple_tag
def rbac_menu(request):
    menu_list = process_menu_tree(request)
    tree = build_menu_tree(menu_list)
    return mark_safe(tree)

@register.simple_tag
def rbac_css():
    file_path = os.path.join('rbac', 'theme', settings.RBAC_CSS, 'rbac.css')
    if os.path.exists(file_path):
        return mark_safe(open(file_path, 'r', encoding='utf-8').read())
    else:
        raise Exception('模版不存在')

@register.simple_tag
def rbac_js():
    file_path = os.path.join('rbac', 'theme', settings.RBAC_JS, 'rbac.js')
    if os.path.exists(file_path):
        return mark_safe(open(file_path, 'r', encoding='utf-8').read())
    else:
        raise Exception('模版不存在')