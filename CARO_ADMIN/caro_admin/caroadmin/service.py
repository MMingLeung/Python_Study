#!/usr/bin/env python
# -*- coding:utf-8 -*-


from django.conf.urls import url, include
from django.shortcuts import HttpResponse, render, redirect
from django.http.request import QueryDict
from django.urls import reverse
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from django.template.response import TemplateResponse
from rbac.service import initial_permission
from rbac.models import User
from caroadmin.utils.page import PageInfo
from caroadmin.utils.filter import FilterList


class ChangeList:
    '''
    组合搜索、添加按钮、分页、数据的显示
    '''

    def __init__(self, request, basecaro_obj, result_list, filter_list, action_list, list_display):
        '''
        :param request: 请求所有信息 
        :param basecaro_obj: BaseCaro类的对象
        :param result_list: model对象获取的结果的对象集合(QuerySet)
        :param filter_list: 组合搜索列表（含有Option对象）
        :param action_list: 批量操作的列表（函数） 
        :param list_display: 显示列表（函数 or 字段名称的字符串）
        '''
        self.param_dict = request.GET
        self.param_dict._mutable = True
        self.basecaro_obj = basecaro_obj
        self.filter_list = filter_list
        self.action_list = action_list
        self.list_display = list_display
        self.request = request
        # 分页
        current_page = self.param_dict.get('page')
        all_count = result_list.count()
        self.page = PageInfo(all_count, current_page, self.param_dict, request.path_info)
        self.result_list = result_list[self.page.start:self.page.stop]
        if not self.result_list:
            self.param_dict['page'] = '1'
            current_page = self.param_dict.get('page')
            self.page = PageInfo(all_count, current_page, self.param_dict, request.path_info)
            self.result_list = result_list[self.page.start:self.page.stop]

    def add_btn(self):
        # 添加按钮的url
        base_add_url = reverse("{}:{}_{}_add".format(self.basecaro_obj.site_obj.name_space, self.basecaro_obj.app_label,
                                                     self.basecaro_obj.model_name))
        param_dict = QueryDict(mutable=True)
        if self.request.GET:
            param_dict['_changelistfilter'] = self.request.GET.urlencode()
        add_url = "{}?{}".format(base_add_url, self.request.GET.urlencode())
        tpl = '<a href="{url}" class="btn btn-success" style="float: right;">添加</a>'.format(url=add_url)
        return mark_safe(tpl)

    def gen_list_filter(self):
        from django.db.models.fields.related import ManyToManyField
        from django.db.models.fields.related import ForeignKey
        for option in self.filter_list:
            # 通过字符串获取model的field对象
            field = self.basecaro_obj.model_class._meta.get_field(option.name)
            if option.is_func:
                data_list = option.func_or_field(self, option)
            else:
                # 判断FK or M2M
                # 对应获取QuerySet不同的方法
                if isinstance(field, ForeignKey):
                    data_list = FilterList(option, field.rel.model.objects.all(), self.request, self)
                elif isinstance(field, ManyToManyField):
                    data_list = FilterList(option, field.rel.model.objects.all(), self.request, self)
                else:
                    data_list = FilterList(option, field.model.objects.all(), self.request, self)
            yield data_list


class BaseCaro:
    # 存放需要显示的字段名称或自定义函数
    list_display = '__str__'

    # model_form对象
    add_or_edit_form = None

    # 批量操作
    action_list = []

    # 组合搜索
    filter_list = []

    # 自定义的模板
    changelist_template = []

    # 钩子url列表
    another_urls = []

    def __init__(self, model_class, site_obj):
        self.model_class = model_class
        self.site_obj = site_obj
        self.app_label = model_class._meta.app_label
        self.model_name = model_class._meta.model_name

    # ################## URL相关开始 ##################
    @property
    def urls(self):
        return self.get_urls()

    def get_urls(self):
        info = self.app_label, self.model_name
        urlpatterns = [
            url(r'^$', self.changelist_view, name='%s_%s_changelist' % info),
            url(r'^add/$', self.add_view, name='%s_%s_add' % info),
            url(r'^(\d+)/change/$', self.change_view, name='%s_%s_change' % info),
            url(r'^(\d+)/delete/$', self.delete_view, name='%s_%s_delete' % info),
        ]
        urlpatterns += self.another_urls
        return urlpatterns

    def changelist_url_param(self):
        base_changelist_url = reverse(
            "{}:{}_{}_changelist".format(self.site_obj.name_space, self.app_label, self.model_name))
        param_dict = QueryDict(mutable=True)
        if self.request.GET:
            param_dict['_changelistfilter'] = self.request.GET.urlencode()
        changelist_url = "{}?{}".format(base_changelist_url, self.request.GET.urlencode())
        return changelist_url

    def changelist_url_base(self):
        return reverse(
            "{}:{}_{}_changelist".format(self.site_obj.name_space, self.app_label, self.model_name))

    # ################## URL相关结束 ##################

    def get_add_or_edit_model_form(self):
        if self.add_or_edit_form:
            return self.add_or_edit_form
        else:
            _meta = type('Meta', (object,), {'model': self.model_class, 'fields': '__all__'})
            my_model_form = type('MyMoldeForm', (ModelForm,), {'Meta': _meta})
            return my_model_form

    def get_all_fields(self):
        return [item.name for item in self.model_class._meta._get_fields()]

    def get_list_condition(self, query_params):
        fields = self.get_all_fields()
        condition = {}
        for k in query_params:
            if k not in fields:
                continue
            condition[k + '__in'] = query_params.getlist(k)
        return condition

    def changelist_view(self, request):
        self.request = request

        if request.method == "POST":
            action = request.POST.get('action')
            func = getattr(self, action)
            res = func(request)
            if res:
                return redirect(self.changelist_url_param())
            else:
                return redirect(self.changelist_url_base())

        result_list = self.model_class.objects.filter(**self.get_list_condition(request.GET))
        changelist = ChangeList(request, self, result_list, self.filter_list, self.action_list, self.list_display)
        context = {
            'cl': changelist,
        }
        return TemplateResponse(request, self.changelist_template or [
            'test/%s/%s/changelist.html' % (self.app_label, self.model_name),
            'test/%s/changelist.html' % self.app_label,
            'changelist.html',
        ], context)

    def add_view(self, request):
        self.request = request
        model_form = self.get_add_or_edit_model_form()()
        # from django.forms.boundfield import BoundField
        # from django.forms.fields import CharField
        if request.method == 'POST':
            model_form = self.get_add_or_edit_model_form()(data=request.POST, files=request.FILES)
            if model_form.is_valid():
                obj = model_form.save()
                change_list = self.changelist_url_param()
                popup_id = request.GET.get('popup')
                if popup_id:
                    context = {
                        'popup_dict': {
                            'popup_id': popup_id,
                            'text': str(obj),
                            'pk': obj.pk
                        }
                    }
                    return render(request, 'popup_response.html', context)
                return redirect(change_list)
        return render(request, 'add.html', {'form': model_form})

    def change_view(self, request, pk):
        model_obj = self.model_class.objects.filter(id=pk).first()
        model_form = self.get_add_or_edit_model_form()(instance=model_obj)

        if request.method == 'POST':
            model_form = self.get_add_or_edit_model_form()(data=request.POST, files=request.POST, instance=model_obj)
            if model_form.is_valid():
                model_form.save()
                change_list = self.changelist_url_param()
                return redirect(change_list)
        context = {
            'form': model_form
        }
        return render(request, 'change.html', context)

    def delete_view(self, request, pk):
        obj = self.model_class.objects.filter(id=pk).delete()
        param_dict = QueryDict(mutable=True)
        base_add_url = reverse("{}:{}_{}_changelist".format(self.site_obj.name_space, self.app_label, self.model_name))
        if not obj:
            return redirect(base_add_url)
        else:
            if request.GET:
                param_dict['_changelistfilter'] = request.GET.urlencode()
            change_list = "{}?{}".format(base_add_url, param_dict.urlencode())
            return redirect(change_list)


class CaroSite:
    def __init__(self):
        self._registry = {}
        self.name_space = 'caro'
        self.app_name = 'caro'

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.name_space

    def get_urls(self):

        urlpatterns = [
            url(r'^login$', self.login, name='login'),
            url(r'^logout', self.logout, name='login'),
        ]
        for model_class, base_obj in self._registry.items():
            self.base_obj = base_obj
            self.model_name = model_class._meta.model_name
            self.app_label = model_class._meta.app_label
            urlpatterns.append(url(r'%s/%s/' % (self.app_label, self.model_name), include(base_obj.urls)))
        return urlpatterns

    def logout(self, request):
        '''

        :param request: 
        :return: 
        '''
        request.session.delete()
        return redirect('/test/login')

    def login(self, request):
        if request.method == "GET":
            return render(request, 'login.html')
        elif request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            obj = User.objects.filter(username=username, password=password).first()
            if obj:
                initial_permission(request, obj)
                changelist_url = reverse("{}:{}_{}_changelist".format(self.name_space, self.app_label, self.model_name))
                return redirect(changelist_url)
            return HttpResponse('error')

    def reigster(self, model_class, base_cls=BaseCaro):
        self._registry[model_class] = base_cls(model_class, self)


site = CaroSite()
