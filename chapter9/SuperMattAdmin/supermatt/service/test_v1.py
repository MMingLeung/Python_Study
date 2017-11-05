import copy

from django.conf.urls import url, include
from django.shortcuts import HttpResponse, render, redirect
from django.urls import reverse

from supermatt.utils.pager import PageInfo
from supermatt.utils.filter_code import FilterList

class BaseSupermatt(object):
    '''
    该类可以把所有数据都拿到
    '''


    list_display = '__all__'

    action_list = []

    add_or_edit_model_form = None

    filter_list = []

    def __init__(self, model_class, site):
        #当前请求的model的类,把类当作参数
        self.model_class = model_class
        self.site = site
        self.request = None
        self.app_label = self.model_class._meta.app_label
        self.model_name = self.model_class._meta.model_name


    def get_add_or_edit_model_form(self):
        if self.add_or_edit_model_form:
            return self.add_or_edit_model_form
        else:
            from django.forms import ModelForm
            # 对象由类创建，类由type创建
            # 通过对象找到提供的字段
            # class MyModelForm(ModelForm):
            #     class Meta:
            #         model = self.model_class
            #         fields = '__all__'

            _Meta = type('Meta', (object,), {'model':self.model_class, 'fields':'__all__'})
            MyModelForm = type('MyModelForm', (ModelForm, ), {"Meta":_Meta})
            return MyModelForm



    @property
    def urls(self):
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        urlpatterns = [
            url(r'^$', self.changelist_view, name='%s_%s_changelist' % info),
            url(r'^add/$', self.add_view, name='%s_%s_add' % info),
            url(r'^(.+)/delete/$', self.delete_view, name='%s_%s_delete' % info),
            url(r'^(.+)/change/$', self.change_view, name='%s_%s_change' % info),
        ]
        return urlpatterns

    def changelist_view(self, request):
        '''
        查看列表
        :param request: 
        :return: 
        '''
        # 以后使用
        self.request = request

        # 生成页面上的添加按钮的url,拼接点击之前的request.GET请求参数，用于操作完返回刚刚页面
        # QueryDict
        from django.http.request import QueryDict
        # u = request.GET.urlencode()
        param_dict = QueryDict(mutable=True) # 默认元素可以修改
        if request.GET:
            param_dict['_changlistfilter'] = request.GET.urlencode()
        print(request.GET.urlencode())

        base_add_url = "{2}:{0}_{1}_add".format(self.app_label, self.model_name, self.site.name_space)
        add_url = reverse(base_add_url) + '?' + param_dict.urlencode()
        test_url = reverse(base_add_url) + '?' + request.GET.urlencode()

        # 数据有了需要页面

        # 分页开始

        condition = {}
        base_page_url = reverse("{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.name_space))
        print('page', base_page_url)
        # querydict 类型
        page_param_dict = copy.deepcopy(request.GET)
        page_param_dict._mutable = True


        all_count = self.model_class.objects.filter(**condition).count()
        page_obj = PageInfo(request.GET.get('page'),  3, all_count, base_page_url, page_param_dict)
        result_list = self.model_class.objects.filter(**condition)[page_obj.start:page_obj.stop]

        # 分页结束

        # ########### Action操作 ###########
        # GET： 显示下拉框
        # POST：
        action_list = []

        for i in self.action_list:
            tpl = {'name':i.__name__, 'text':i.text}
            action_list.append(tpl)
        if request.method == "POST":
            # 1. 获取select 标签 name = action
            func_name_str = request.POST.get('action')
            ret = getattr(self, func_name_str)(request)
            action_page_url = reverse("{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.name_space))
            if ret:
                action_page_url = "{0}?{1}".format(action_page_url, request.GET.urlencode())
            return redirect(action_page_url)
        print('actionlist', action_list)
        # ########### 组合搜索 ###########
        # filter_list = self.filter_list
        # 当用户访问列表页面时，进行一下的操作
        # 定义一个空列表，用于存放传给前端渲染数据FilterList的实例对象
        filter_list = []
        # 循环对象自身的filter_list(用户自定义的)
        # 里面是FilterOption对象
        for option in self.filter_list:
            # 如果是函数
            if option.is_func:
                # 调用自身，最后返回的必须是FilterList对象
                data_list = option.field_or_func(self, option, request)
            else:
                # 如果是field 字段名：'username', 'ug', 'role'
                from django.db.models.fields.related import ForeignKey, ManyToManyField
                # 根据model字段名字获取其对象
                field = self.model_class._meta.get_field(option.field_or_func)
                # 判断是否是FK／M2M
                # 如果是，FilterList传入的queryset则是关联的表的数据
                # 否则是自己的数据
                if isinstance(field, ForeignKey):
                    data_list = FilterList(option, field.rel.model.objects.all(), request)
                elif isinstance(field, ManyToManyField):
                    print('2', field.rel.model)  # role
                    data_list = FilterList(option, field.rel.model.objects.all(), request)
                else:
                    data_list = FilterList(option, field.model.objects.all(), request)
            filter_list.append(data_list)





        context = {
            'result_list':result_list,
            'list_display':self.list_display,
            'BaseSupermattObj':self,
            'add_url':add_url,
            'page_str':page_obj.pager(),
            'action_list':action_list,
            'filter_list':filter_list,

        }
        return render(request, 'change_list.html', context)

    def add_view(self, request):
        '''
        添加功能
        :param request: 
        :return: 
        '''
        # print(request.GET.get('_changlistfilter')) #以后使用
        # print('addddd',request.GET) #以后使用

        if request.method == 'GET':

            model_form_obj = self.get_add_or_edit_model_form()()

        else:
            model_form_obj = self.get_add_or_edit_model_form()(data=request.POST, files=request.FILES)
            if model_form_obj.is_valid():
                # 这个obj就是提交的数据
                obj = model_form_obj.save()
                # 如果是popup返回给调用框
                popid = request.GET.get('popup')
                if popid:
                    # 获取新增数据
                    return render(request, 'popup_response.html',
                                  {'data_dict':{
                                                'text':str(obj),
                                                'pk':obj.pk,
                                                'popid':popid}
                                  })
                else:
                    # 添加成功跳转回列表显示页
                    # su/app01/userinfo + request.GET.get
                    base_list_url = reverse("{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.name_space))
                    list_url = '{0}?{1}'.format(base_list_url, request.GET.get('_changlistfilter'))



                    return redirect(list_url)

        context = {
            'form': model_form_obj,
        }

        return render(request, 'add.html', context)

    def delete_view(self, request, pk):
        # 根据pk获取数据，然后删除
        # 获取url，跳转回上次列表页面
        if request.method == 'GET':
            self.model_class.objects.filter(pk=pk).first().delete()
            base_list_url = reverse("{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.name_space))
            list_url = '{0}?{1}'.format(base_list_url, request.GET.get('_changlistfilter'))
            return redirect(list_url)

    def change_view(self, request, pk):

        # 1.获取_changlistfilter传递的参数
        # request.GET.get("_changlistfilter")

        # 2.获取数据默认显示并选中ModelForm
        # get_add_or_edit_model_form
        obj = self.model_class.objects.filter(pk=pk).first()
        if request.method == 'GET':

            if not obj:
                return HttpResponse('id不存在')
            # instance=obj自动选中默认值
            model_form_obj = self.get_add_or_edit_model_form()(instance=obj)


            # 3.返回页面

        else:
            # 更新必须传instance
            model_form_obj = self.get_add_or_edit_model_form()(data=request.POST, files=request.FILES, instance=obj)
            if model_form_obj.is_valid():
                model_form_obj.save()
                base_list_url = reverse("{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.name_space))
                list_url = '{0}?{1}'.format(base_list_url, request.GET.get('_changlistfilter'))
                return redirect(list_url)

        context = {
                'form':model_form_obj
            }
        return render(request, 'edit.html', context)


class SuperMattSite(object):

    def __init__(self):
        '''
        构造方法
        '''
        self._registry = {}
        self.name_space = 'supermatt'
        self.app_name = 'supermatt'


    def register(self, model_class, m = BaseSupermatt):
        self._registry[model_class] = m(model_class, self)
        '''
        {
        UserInfo类名: BaseSupermatt（UserInfo类名, SuperMattSite对象）#SuperMattUserInfo
        Role 类名：BaseSupermatt（Role类名, SuperMattSite对象）
        XX 类名： BaseSupermatt（Role类名, SuperMattSite对象）
        }
        '''

    def login(self, request):
        return HttpResponse('login')

    def get_urls(self):
        ret = [
            url(r'^login/$', self.login, name='login'),
        ]
        for model_class, supermatt_obj in self._registry.items():
            # print(model_class._meta.app_label, model_class._meta.model_name, supermatt_obj)
            # 获取model_class的app名字和类名
            # http://127.0.0.1:8000/su/app01/role
            app_label = model_class._meta.app_label
            model_name = model_class._meta.model_name
            ret.append(url(r'^%s/%s/' % (app_label, model_name), include(supermatt_obj.urls)))
        return ret

    @property
    def urls(self):
        return self.get_urls(),self.app_name,self.name_space

site = SuperMattSite()