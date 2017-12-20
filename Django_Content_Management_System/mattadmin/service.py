# from django.conf.urls import url, include
# from django.shortcuts import HttpResponse, render
#
#
# class ChangeList:
#     def __init__(self, request, base_obk, list_display, result_list, model_cls, filter_list, action_list):
#         pass
#
#
# class BaseMatt:
#     def __init__(self, model_cls, site):
#         self.model_cls = model_cls
#         self.site = site
#         self.app_lable = self.model_cls._meta.app_label
#         self.model_name = self.model_cls._meta.model_name
#
#
#     @property
#     def urls(self):
#         return self.get_urls()
#
#     def get_urls(self):
#         info = self.app_lable, self.model_name
#         urlpatterns = [
#             url(r'%', self.changelist_view, name='_%s_%s_changelist' % info),
#         ]
#         return urlpatterns
#
#
#     list_display = '__all__'
#
#     def changelist_view(self, request):
#
#         self.request = request
#         result = self.model_cls.object.all()
#         context = {
#             'result':result,
#             'list_display':self.list_display,
#             'basematt_obj':self,
#         }
#         return render(request, 'change_list.html', context)
#
#     # 获取URL中的GET请求并在注册中的参数
#     def get_all_model_field_name_list(self):
#         return [item.name for item in self.model_cls._meta._get_fields()]
#
#     def get_change_list_condition(self, query_params):
#         field_list = self.get_all_model_field_name_list()
#         condition = {}
#         for i in query_params:
#             if i not in field_list:
#                 continue
#             condition[i+ '__in'] = query_params.getlist(i)
#         return condition
#
#
#
#
#
#
# class MattSite:
#     def __init__(self):
#         self.app_name = 'matt'
#         self.name_space = 'matt'
#         self._registry = {}
#
#     def register(self, model_cls, base_cls = BaseMatt):
#         self._registry[model_cls] = BaseMatt(model_cls, self)
#
#     @property
#     def urls(self):
#         return self.get_urls(), self.app_name, self.name_space
#
#     def get_urls(self):
#         urlpatterns = [
#             url(r'login/$', self.login, name='login'),
#         ]
#         for model_cls, base_obj in self._registry.items():
#             app_label = model_cls._meta.app_label
#             model_name = model_cls._meta.model_name
#             urlpatterns.append(url(r'%s/%s/' % (app_label, model_name), include(base_obj.urls)))
#         return urlpatterns
#
#     def login(self, request):
#         return HttpResponse('Login!')
#
# site = MattSite()

from django.conf.urls import url, include
from django.shortcuts import HttpResponse, render, redirect
import copy
from mattadmin.utils.pager import PageInfo
from mattadmin.utils.filter_code import FilterList, FilterOption
from django.http.request import QueryDict
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.template.response import TemplateResponse, SimpleTemplateResponse


class ChangeList(object):
    '''
    1、初始化
    2、生成增加按钮:
    	反向生成url，获取原来url，两者拼接，生成html标签字符串，最后返回
    3、生成组合搜索
    	1.循环遍历filter_list里面的Filteroption对象
    	2.判断是否是函数（自定义的函数最后必须返回FilterList对象）
    	3.不是，根据FilterOption对象名字获取该对象
    	4.判断是否是外间或者多对多，传入的查询出来数据有所不同
    	5.yield返回data_list
    '''
    def __init__(self, request, supermatt_model, list_display, result_list, model_cls, filter_list, action_list):
        '''
        初始化基本信息
        :param request: 
        :param supermatt_model: 基类obj
        :param list_display: 显示列表list
        :param result_list: 结果列表queryset
        :param model_cls: 当前数据类对象
        :param filter_list: 用户自定制搜索条件
        :param action_list: 自定制action
        '''
        self.request = request
        self.list_display = list_display
        self.filter_list = filter_list

        self.model_cls = model_cls
        self.supermatt_model = supermatt_model
        self.action_list = action_list


        query_params = copy.deepcopy(request.GET)
        query_params._mutable = True

        all_count = result_list.count()
        # 分页
        self.pager = PageInfo(self.request.GET.get('page'), per_page=5, all_count=all_count, base_url=self.supermatt_model.changelist_url(),
                              page_param_dict=query_params)
        self.result_list = result_list[self.pager.start:self.pager.stop]


    def add_btn(self):
        """
        列表页面定制新建数据按钮
        :return: 
        """
        add_url = reverse(
            '%s:%s_%s_add' % (self.supermatt_model.site.name_space, self.supermatt_model.app_label, self.supermatt_model.model_name))

        _change = QueryDict(mutable=True)
        _change['_change_filter'] = self.request.GET.urlencode()

        tpl = "<a class='btn btn-success' style='float:right' href='{0}?{1}'><span class='glyphicon glyphicon-share-alt' aria-hidden='true'></span> 新建数据</a>".format(
            add_url,
            _change.urlencode())
        return mark_safe(tpl)



    def gen_list_filter(self):
        '''
        生成组合搜索条件
        :return: 
        '''
        for option in self.filter_list:
            if option.is_func:
                data_list = option.field_or_func(self, option, self.request)
            else:
                _field = self.model_cls._meta.get_field(option.field_or_func)
                if isinstance(_field, ForeignKey):
                    data_list = FilterList(option, _field.rel.model.objects.all(), self.request)
                elif isinstance(_field, ManyToManyField):
                    data_list = FilterList(option, _field.rel.model.objects.all(), self.request)
                else:
                    data_list = FilterList(option, _field.model.objects.all(), self.request)
            yield data_list


class BaseSupermatt(object):
    def __init__(self, model_class, site):
        # 当前请求的model的类,把类当作参数
        from django.db.models.base import ModelBase
        print(type(model_class))
        self.model_class = model_class
        self.site = site
        self.request = None
        self.app_label = self.model_class._meta.app_label
        self.model_name = self.model_class._meta.model_name

    def get_urls(self):
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        urlpatterns = [
            url(r'^$', self.changelist_view, name='%s_%s_changelist' % info),
            # url(r'^add/$', self.add_view, name='%s_%s_add' % info),
            # url(r'^(.+)/detail/$', self.detail_view, name='%s_%s_detail' % info),
            # url(r'^(.+)/delete/$', self.delete_view, name='%s_%s_delete' % info),
            # url(r'^(.+)/change/$', self.change_view, name='%s_%s_change' % info),
        ]
        # urlpatterns += self.another_urls()
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls()

    filter_list = []
    action_list = []
    change_list_template = []
    def changelist_view(self, request):
        '''
        显示数据
        各项子功能：
        1、数据列表
        2、筛选
        3、分页
        4、是否编辑
        5、组合搜索
        6、定制行为
        :param request: 
        :return: 
        '''
        self.request = request
        result_list = self.model_class.objects.filter(**self.get_change_list_condition(request.GET))
        if request.method == 'POST':
            # 执行action行为
            action = request.POST.get('action')
            if not action:
                return redirect(self.changelist_param_url(request.GET))
            if getattr(self, action)(request, result_list):
                return redirect(self.changelist_param_url(request.GET))
            else:
                return redirect(self.changelist_url())

        # 组合搜索
        change_list = ChangeList(request, self,
                                 self.list_display,
                                 result_list,
                                 self.model_class,
                                 self.filter_list,
                                 action_list=self.action_list)
        print('change_list',change_list.model_cls)
        context = {
            'cl': change_list,
        }
        return TemplateResponse(request, self.change_list_template or [
            '%s/%s/change_list.html' % (self.app_label, self.model_name),
            '%s/change_list.html' % self.app_label,
            'change_list.html'
        ], context)

    # 获取URL中的GET请求且在注册了的model中参数
    def get_all_model_field_name_list(self):
        # item是model每个field的对象
        return [item.name for item in self.model_class._meta._get_fields()]

    def get_change_list_condition(self, query_params):
        fields = self.get_all_model_field_name_list()
        condition = {}
        for k in query_params:
            if k not in fields:
                continue
            condition[k + '__in'] = query_params.getlist(k)
        return condition




class SuperMattSite(object):
    def __init__(self, app_name='supermatt', name_space='supermatt'):
        self._registry = {}
        self.name_space = name_space
        self.app_name = app_name

    def register(self, model_class, supermatt_model_class=BaseSupermatt):
        self._registry[model_class] = supermatt_model_class(model_class, self)

    def get_urls(self):
        urlpattens = [
            url(r'^login/$', self.login, name='login'),
        ]
        for model_class, supermatt_obj in self._registry.items():
            # print(model_class._meta.app_label, model_class._meta.model_name, supermatt_obj)
            # 获取model_class的app名字和类名
            # http://127.0.0.1:8000/su/app01/role
            app_label = model_class._meta.app_label
            model_name = model_class._meta.model_name
            urlpattens.append(url(r'^%s/%s/' % (app_label, model_name), include(supermatt_obj.urls)))
        return urlpattens

    def login(self, request):
        return HttpResponse('login')

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.name_space

site = SuperMattSite()