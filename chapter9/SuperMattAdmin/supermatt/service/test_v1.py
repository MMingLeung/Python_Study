from django.conf.urls import url, include
from django.shortcuts import HttpResponse, render, redirect
from django.contrib import admin
from django.urls import reverse

class BaseSupermatt(object):
    '''
    该类可以把所有数据都拿到
    '''

    list_display = '__all__'

    add_or_edit_model_form = None

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

        base_add_url = "{2}:{0}_{1}_add".format(self.app_label, self.model_name, self.site.name_sapce)
        add_url = reverse(base_add_url) + '?' + param_dict.urlencode()


        # 数据有了需要页面
        result_list = self.model_class.objects.all()
        print(self.list_display)



        context = {
            'result_list':result_list,
            'list_display':self.list_display,
            'BaseSupermattObj':self,
            'add_url':add_url
        }
        # info = self.model_class._meta.app_label, self.model_class._meta.model_name
        # data = '%s_%s_changelist' % info
        return render(request, 'change_list.html', context)

    def add_view(self, request):
        '''
        添加功能
        :param request: 
        :return: 
        '''
        print(request.GET.get('_changlistfilter')) #以后使用

        if request.method == 'GET':

            model_form_obj = self.get_add_or_edit_model_form()()
        else:
            model_form_obj = self.get_add_or_edit_model_form()(data=request.POST, files=request.FILES)
            if model_form_obj.is_valid():
                model_form_obj.save()
                # 添加成功跳转回列表显示页
                # su/app01/userinfo + request.GET.get

                base_list_url = reverse("{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.name_sapce))
                list_url = '{0}?{1}'.format(base_list_url, request.GET.get('_changlistfilter'))

                return redirect(list_url)
        context = {
            'form': model_form_obj,
            'model_class':self.model_class
        }
        for item in model_form_obj:
            # <class 'django.forms.boundfield.BoundField'>

            print (item, type(item), item.field,self.model_class._meta.get_field(item.name).verbose_name)
        from django.forms.boundfield import BoundField

        # info = self.model_class._meta.app_label, self.model_class._meta.model_name
        # data = '%s_%s_add' % info
        return render(request, 'add.html', context)

    def delete_view(self, request, pk):
        # 根据pk获取数据，然后删除
        # 获取url，跳转回上次列表页面
        if request.method == 'GET':
            self.model_class.objects.filter(pk=pk).first().delete()
            base_list_url = reverse("{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.name_sapce))
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
                base_list_url = reverse("{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.name_sapce))
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
        self.name_sapce = 'supermatt'
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
        return self.get_urls(),self.app_name,self.name_sapce

site = SuperMattSite()