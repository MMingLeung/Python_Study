#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
本py文件会在Django程序启动时自动执行一次，把model类注册到caro_admin组件中，
自动生成url对应关系。可自定类继承service.BaseCaro，扩展功能。
'''


from django.utils.safestring import mark_safe
from django.urls import reverse
from django.http.request import QueryDict
from project_management_system.models import Department, ProjectList, ProjectRecord, UserProfile, Reporter, ReporterFollowerUp, WorkSpace
from caroadmin.utils.filter import FilterOption
from caroadmin import service


class DepartmentBase(service.BaseCaro):
    list_display = ['id', 'name', 'description', 'floor']


service.site.reigster(Department, DepartmentBase)


class ProjectRecordBase(service.BaseCaro):
    def checkbox(self, obj=None, is_header=None):
        if is_header:
            return '选项'
        tpl = "<input type='checkbox' name='pk' value={}>".format(obj.pk)
        return mark_safe(tpl)

    def func(self, obj=None, is_header=None):
        if is_header:
            return '功能'
        else:
            param_dict = QueryDict(mutable=True)
            if self.request.GET:
                param_dict['_changelistfilter'] = self.request.GET.urlencode()

            change_base_url = reverse(
                "{}:{}_{}_change".format(self.site_obj.name_space, self.app_label, self.model_name), args=(obj.pk,))
            change_url = "{}?{}".format(change_base_url, param_dict.urlencode())
            del_base_url = reverse("{}:{}_{}_delete".format(self.site_obj.name_space, self.app_label, self.model_name),
                                   args=(obj.pk,))
            del_url = "{}?{}".format(del_base_url, param_dict.urlencode())
            tpl = "<a href='{}'>编辑</a> | <a href='{}'>删除</a>".format(change_url, del_url)
            return mark_safe(tpl)

    def initial(self, request):
        pks = request.POST.getlist('pk')
        ProjectRecord.objects.filter(id__in=pks).update(date='2013-3-2')
        return True

    initial.text = '初始化'

    action_list = [initial, ]

    list_display = [checkbox, 'id', 'project', 'day_num', 'date', 'engineer', 'project_detail', func]


service.site.reigster(ProjectRecord, ProjectRecordBase)


class ProjectListBase(service.BaseCaro):
    def checkbox(self, obj=None, is_header=None):
        if is_header:
            return '选项'
        tpl = "<input type='checkbox' name='pk' value={}>".format(obj.pk)
        return mark_safe(tpl)

    def func(self, obj=None, is_header=None):
        if is_header:
            return '功能'
        else:
            param_dict = QueryDict(mutable=True)
            if self.request.GET:
                param_dict['_changelistfilter'] = self.request.GET.urlencode()

            change_base_url = reverse(
                "{}:{}_{}_change".format(self.site_obj.name_space, self.app_label, self.model_name), args=(obj.pk,))
            change_url = "{}?{}".format(change_base_url, param_dict.urlencode())
            del_base_url = reverse("{}:{}_{}_delete".format(self.site_obj.name_space, self.app_label, self.model_name),
                                   args=(obj.pk,))
            del_url = "{}?{}".format(del_base_url, param_dict.urlencode())
            tpl = "<a href='{}'>编辑</a> | <a href='{}'>删除</a>".format(change_url, del_url)
            return mark_safe(tpl)

    list_display = [
        checkbox,
        'id',
        'work_space',
        'department',
        'class_type',
        'status_type',
        'duration',
        'price',
        'start_data',
        'end_data',
        'staff',
        func
    ]

    filter_list = [
        FilterOption('work_space', is_multi=False),
        FilterOption('staff', is_multi=False),
    ]

    def initial(self, request):
        pks = request.POST.getlist('pk')
        ProjectList.objects.filter(id__in=pks).update(start_date='2013-3-2')
        return True

    initial.text = '初始化'

    action_list = [initial, ]


service.site.reigster(ProjectList, ProjectListBase)


class UserProfileBase(service.BaseCaro):
    def checkbox(self, obj=None, is_header=None):
        if is_header:
            return '选项'
        tpl = "<input type='checkbox' name='pk' value={}>".format(obj.pk)
        return mark_safe(tpl)

    def func(self, obj=None, is_header=None):
        if is_header:
            return '功能'
        else:
            param_dict = QueryDict(mutable=True)
            if self.request.GET:
                param_dict['_changelistfilter'] = self.request.GET.urlencode()

            change_base_url = reverse(
                "{}:{}_{}_change".format(self.site_obj.name_space, self.app_label, self.model_name), args=(obj.pk,))
            change_url = "{}?{}".format(change_base_url, param_dict.urlencode())
            del_base_url = reverse("{}:{}_{}_delete".format(self.site_obj.name_space, self.app_label, self.model_name),
                                   args=(obj.pk,))
            del_url = "{}?{}".format(del_base_url, param_dict.urlencode())
            tpl = "<a href='{}'>编辑</a> | <a href='{}'>删除</a>".format(change_url, del_url)
            return mark_safe(tpl)

    list_display = [
        checkbox,
        'id',
        'user_obj',
        'name',
        'workspace',
        'memo',
        'data_joined',
        func
    ]


service.site.reigster(UserProfile, UserProfileBase)


class ReporterBase(service.BaseCaro):
    def checkbox(self, obj=None, is_header=None):
        if is_header:
            return '选项'
        tpl = "<input type='checkbox' name='pk' value={}>".format(obj.pk)
        return mark_safe(tpl)

    def func(self, obj=None, is_header=None):
        if is_header:
            return '功能'
        else:
            param_dict = QueryDict(mutable=True)
            if self.request.GET:
                param_dict['_changelistfilter'] = self.request.GET.urlencode()

            change_base_url = reverse(
                "{}:{}_{}_change".format(self.site_obj.name_space, self.app_label, self.model_name), args=(obj.pk,))
            change_url = "{}?{}".format(change_base_url, param_dict.urlencode())
            del_base_url = reverse("{}:{}_{}_delete".format(self.site_obj.name_space, self.app_label, self.model_name),
                                   args=(obj.pk,))
            del_url = "{}?{}".format(del_base_url, param_dict.urlencode())
            tpl = "<a href='{}'>编辑</a> | <a href='{}'>删除</a>".format(change_url, del_url)
            return mark_safe(tpl)

    list_display = [
        checkbox,
        'id',
        'phone',
        'name',
        'sex',
        'department',
        'notes',
        func
    ]


service.site.reigster(Reporter, ReporterBase)


class ReporterFollowerUpBase(service.BaseCaro):
    def checkbox(self, obj=None, is_header=None):
        if is_header:
            return '选项'
        tpl = "<input type='checkbox' name='pk' value={}>".format(obj.pk)
        return mark_safe(tpl)

    def func(self, obj=None, is_header=None):
        if is_header:
            return '功能'
        else:
            param_dict = QueryDict(mutable=True)
            if self.request.GET:
                param_dict['_changelistfilter'] = self.request.GET.urlencode()

            change_base_url = reverse(
                "{}:{}_{}_change".format(self.site_obj.name_space, self.app_label, self.model_name), args=(obj.pk,))
            change_url = "{}?{}".format(change_base_url, param_dict.urlencode())
            del_base_url = reverse("{}:{}_{}_delete".format(self.site_obj.name_space, self.app_label, self.model_name),
                                   args=(obj.pk,))
            del_url = "{}?{}".format(del_base_url, param_dict.urlencode())
            tpl = "<a href='{}'>编辑</a> | <a href='{}'>删除</a>".format(change_url, del_url)
            return mark_safe(tpl)

    list_display = [
        checkbox,
        'id',
        'reporter',
        'note',
        'status',
        'consultant',
        'date',
        func
    ]


service.site.reigster(ReporterFollowerUp, ReporterFollowerUpBase)


class WorkSpaceBase(service.BaseCaro):
    def checkbox(self, obj=None, is_header=None):
        if is_header:
            return '选项'
        tpl = "<input type='checkbox' name='pk' value={}>".format(obj.pk)
        return mark_safe(tpl)

    def func(self, obj=None, is_header=None):
        if is_header:
            return '功能'
        else:
            param_dict = QueryDict(mutable=True)
            if self.request.GET:
                param_dict['_changelistfilter'] = self.request.GET.urlencode()

            change_base_url = reverse(
                "{}:{}_{}_change".format(self.site_obj.name_space, self.app_label, self.model_name), args=(obj.pk,))
            change_url = "{}?{}".format(change_base_url, param_dict.urlencode())
            del_base_url = reverse("{}:{}_{}_delete".format(self.site_obj.name_space, self.app_label, self.model_name),
                                   args=(obj.pk,))
            del_url = "{}?{}".format(del_base_url, param_dict.urlencode())
            tpl = "<a href='{}'>编辑</a> | <a href='{}'>删除</a>".format(change_url, del_url)
            return mark_safe(tpl)

    list_display = [checkbox, 'id', 'name', func]


service.site.reigster(WorkSpace, WorkSpaceBase)
