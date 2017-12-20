#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
RBAC 权限中间件
1、过滤免登录URL
2、获取当前用户session中的url，判断与当前url是否匹配
'''
import re
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import HttpResponse


class RbacMiddleware(MiddlewareMixin):
    def process_request(self, request, *args, **kwargs):
        for pattern in settings.NO_AUTH_URL:
            if re.match(pattern, request.path_info):
                return None

        permission_url_list = request.session.get(settings.RBAC_PERMISSION_URL_LIST_SESSION_KEY)

        if not permission_url_list:
            return HttpResponse(settings.RBAC_NO_SESSION_MSG)

        flag = False
        for url in permission_url_list:
            pattern = settings.RBAC_URL_PATTERN.format(url)
            if re.match(pattern, request.path_info):
                flag = True
                break
        if not flag:
            if settings.RBAC_DEBUG:
                msg = '拥有以下权限：' + '<br/>' + '<br/>'.join(str(per) for per in permission_url_list if not None)
                return HttpResponse(msg)
            else:
                return HttpResponse(settings.RBAC_ERROR_MSG)
