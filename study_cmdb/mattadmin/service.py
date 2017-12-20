from django.conf.urls import url, include
from django.shortcuts import HttpResponse, render, redirect
from django.contrib import admin
from django.urls import reverse # 2、反向生成URL
from django.http.request import QueryDict
# 不用重写init方法，可以实现自动增加显示，需要跟__str__搭配
from django.forms.models import ModelForm, ModelMultipleChoiceField
from mattadmin.utils.pager import PageInfo
import copy
from mattadmin.utils.page_test import PageInfo
'''
1.数据列表页面定制显示列
    不定制只显示model类对象列表
    定制继承BaseMatt及list_display可指定显示列
'''

class BaseMatt:


    # 3、控制页面显示
    list_display = '__all__'

    # 10.1、action
    action_list = []

    # 11、组合筛选
    filter_list = []

    # 5.2、添加使用的form
    add_or_edit_model_form = None

    def get_add_or_edit_model_form(self):
        if self.add_or_edit_model_form:
            return self.add_or_edit_model_form
        else:
            from django.forms import ModelForm
            from backend.models import UserInfo
            # class MyModelForm(ModelForm):
            #     class Meta:
            #         model = self.model_cls
            #         fields = '__all__'
            _meta = type("Meta", (object, ), {'model':self.model_cls, 'fields':'__all__'})
            myform = type('MyModelForm', (ModelForm, ), {'Meta':_meta})

            return myform



    def __init__(self, model_cls, site):
        self.model_cls = model_cls
        self.site = site
        self.app_label = self.model_cls._meta.app_label
        self.model_name = self.model_cls._meta.model_name


    @property
    def urls(self):
        return self.get_urls()

    def get_urls(self):
        '''
        1、CURD路由分发
        :return: 
        '''
        # print('路由分发')
        info = self.app_label, self.model_name
        # print(info)
        urlpatterns = [
            url(r'^$', self.changelist_view, name="%s_%s_changelist" % info),
            url(r'^add/$', self.add_view, name="%s_%s_add" % info),
            url(r'^(.+)/change/$', self.change_view, name="%s_%s_change" % info),
            url(r'^(.+)/delete/$', self.delete_view, name="%s_%s_delete" % info),
        ]
        return urlpatterns

    def changelist_view(self, request):
        # 2、反向生成URL
        # url = reverse('matt:backend_userinfo_changelist')
        # url = reverse('%s:%s_%s_changelist' % (self.site.name_space, self.app_label, self.model_name))
        # print(url)

        # 3.1、获取数据，从model_cls获取（QuerySet类型）
        # 3.2、控制显示
        self.request = request
        # print(self.list_display)


        # 3.3、模版不能这样输出，只能自定义使用templatetag
        # for item in result_list:
        #     for name in self.list_display:
        #         val = getattr(item, name)
        #         print(name, val, end=' ')


        # 5、生成页面添加按钮
        # 需要反向生成URL
        base_url = reverse('%s:%s_%s_add' % (self.site.name_space, self.app_label, self.model_name))
        # 获取原来GET参数
        param_dict = QueryDict(mutable=True)
        if self.request.GET:
            param_dict['_changelistfilter'] = request.GET.urlencode()
        url = "{0}?{1}".format(base_url, param_dict.urlencode())

        # 9、分页
        condition = {}

        '''
        current_page:当前点击的页码
        per_page：每页显示的数据数量    
        all_count：数据总共的数量
        base_url：网页根地址
        show_page：页码总共显示的个数
        page_param_dict: url原参数
        '''
        current_page = request.GET.get('page')
        all_count = self.model_cls.objects.filter(**condition).count()
        page_url = reverse('%s:%s_%s_changelist' % (self.site.name_space, self.app_label, self.model_name))
        page_paramdict = copy.deepcopy(request.GET)
        page_paramdict._mutable = True
        # page = PageInfo(current_page, 3, all_count, page_url, page_paramdict)
        page = PageInfo(current_page, all_count, page_url, page_paramdict)

        result_list = self.model_cls.objects.filter(**condition)[page.start:page.stop]


        # 10、action
        # get 显示下拉框
        # post 执行逻辑
        action_list = []
        for item in self.action_list:
            tmp = {'name':item.__name__, 'text':item.text}
            action_list.append(tmp)

        if request.method == 'POST':
            # 1、获取选项
            # 2、
            # print('执行action')
            action_func_name_str = request.POST.get('action')
            res = getattr(self, action_func_name_str)(request)
            base_url = reverse('%s:%s_%s_changelist' % (self.site.name_space, self.app_label, self.model_name))
            if res:
                # 获取原来GET参数
                url = "{0}?{1}".format(base_url, param_dict.urlencode())
                return redirect(url)
            else:
                return redirect(base_url)


        # 11.1、组合搜索

        from mattadmin.utils.filter import FilterList
        filter_list = []
        for option in self.filter_list:
            if option.is_func:
                data_list = option.func_or_str(self, option, request)
            else:
                # 'username' 'ug' 'ur'
                #  判断FK OR M2M
                # 获取该字段对应的的对象
                from django.db.models.fields.related import ForeignKey
                from django.db.models.fields.related import ManyToManyField
                field = self.model_cls._meta.get_field(option.func_or_str)
                # 获取数据
                if isinstance(field, ForeignKey):
                    '''
                     kwargs['rel'] = self.rel_class(
            self, to, to_field,
                    ...
                       self.model = to
                    '''
                    # 把queryset进行封装，只要有__iter__方法
                    data_list = FilterList(option, field.rel.model.objects.all(), self.request)
                elif isinstance(field, ManyToManyField):
                    data_list =  FilterList(option, field.rel.model.objects.all(), self.request)
                else:
                    # 可以知道字段写在哪个类里面，从而获取类
                    data_list =  FilterList(option, field.model.objects.all(), self.request)
            filter_list.append(data_list)

        context = {
            'result_list':result_list,
            'list_display':self.list_display,
            'base_obj':self,
            'url':url,
            'page':page.pager(),
            'action_list':action_list,
            'filter_list':filter_list,

        }

        return render(request, 'changelist.html', context)

    def add_view(self, request):
        # 5.1、添加页面

        # input框，根据数据库字段个数不同有所不同

        # 5.3 接收到后台数据
        if request.method == 'GET':
            model_form = self.get_add_or_edit_model_form()()

        else:

            # 正常用户点击
            model_form = self.get_add_or_edit_model_form()(data=request.POST, files=request.FILES)
            if model_form.is_valid():
                # 返回值是新增数据
                obj = model_form.save()

                # 9、popUp请求
                popid = request.GET.get('popup')
                if popid:
                    # 1、数据库保存
                    # 2、关闭并且增加的数据加入原来的页面对应地方
                    text = str(obj) # 文本
                    pk = obj.pk # 值
                    context = {
                        'data_dict':{
                            'text': text,
                            'pk': pk,
                            'popid': popid,
                        }

                    }
                    return render(request, 'popup_response.html', context)


                else:
                    # 5.4 添加成功进行跳转

                    param_dict = request.GET
                    param_url = param_dict['_changelistfilter']
                    base_url = reverse('%s:%s_%s_changelist' % (self.site.name_space, self.app_label, self.model_name))
                    url = "{0}?{1}".format(base_url, param_url)

                    return redirect(url)



        context = {
            'form':model_form
        }
        return render(request, 'add.html', context)

    def change_view(self, request, pk):
        # 5.4、
        # 获取传递的参数
        # 根据pk显示默认值

        model_obj = self.model_cls.objects.filter(pk=pk).first()
        if not model_obj:
            return HttpResponse('.....')
        if request.method == 'GET':
            model_form = self.get_add_or_edit_model_form()(instance=model_obj)
        else:
            model_form = self.get_add_or_edit_model_form()(data=request.POST, files=request.FILES, instance=model_obj)
            if model_form.is_valid():
                model_form.save()
                param_dict = QueryDict(mutable=True)
                param_dict['_changelistfilter'] = request.GET.urlencode()
                base_url = reverse('%s:%s_%s_changelist' % (self.site.name_space, self.app_label, self.model_name))
                url = "{0}?{1}".format(base_url, param_dict.urlencode())
                return redirect(url)

        context = {
            'form':model_form,
        }
        return render(request, 'edit.html', context)

    def delete_view(self, request, pk):
        # 5.5、根据pk删除
        self.model_cls.objects.filter(pk=pk).delete()
        param_dict = QueryDict(mutable=True)
        param_dict['_changelistfilter'] = request.GET.urlencode()
        base_url = reverse('%s:%s_%s_changelist' % (self.site.name_space, self.app_label, self.model_name))
        url = "{0}?{1}".format(base_url, param_dict.urlencode())
        return redirect(url)


class MattSite:
    def __init__(self):
        self._regstry = {}
        self.app_name = "matt"
        self.name_space = "matt"


    def register(self, model_cls, base_cls = BaseMatt):
        self._regstry[model_cls] = base_cls(model_cls, self)

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.name_space

    def get_urls(self):
        urlpatterns = [
            url(r'^login/$', self.login, name='login'),
        ]
        # print(self._regstry.items())
        for model_cls, base_obj in self._regstry.items():
            # print(base_obj.urls)
            app_label = model_cls._meta.app_label
            model_name = model_cls._meta.model_name
            urlpatterns.append(
                url(r'%s/%s/' % (app_label, model_name), include(base_obj.urls))
            )
        return urlpatterns

    def login(self, request):
        return HttpResponse('123')

site = MattSite()