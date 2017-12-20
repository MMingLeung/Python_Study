# #!/usr/bin/env python
# # -*- coding:utf-8 -*-
'''
RBAC 登录后初始化用户信息至session中
1、保存用户权限中的url
2、保存有挂靠到菜单的权限信息
3、保存菜单信息
'''
from django.conf import settings
from rbac import models

def initial_permission(request, user):

    permission_queryset = user.roles.values('permission__id', 'permission__caption', 'permission__url', 'permission__menu_id').distinct()

    permission_url_list = []
    permission_menu_list = []

    for per in permission_queryset:
        permission_url_list.append(per['permission__url'])
        if per['permission__menu_id']:
            permission_menu_list.append(per)
    request.session[settings.RBAC_PERMISSION_URL_LIST_SESSION_KEY] = permission_url_list


    menu_list = list(models.Menu.objects.values('id', 'caption', 'parent_id'))

    request.session[settings.RBAC_PERMISSION_MENU_DICT_SESSION_KEY] = {
        settings.RBAC_PERMISSION_LIST_SESSION_KEY:permission_menu_list,
        settings.RBAC_MENU_LIST_SESSION_KEY:menu_list
    }