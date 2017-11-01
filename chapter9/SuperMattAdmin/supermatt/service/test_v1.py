from django.conf.urls import url, include
from django.shortcuts import HttpResponse, render
from django.contrib import admin

class BaseSupermatt(object):
    '''
    该类可以把所有数据都拿到
    '''

    list_display = '__all__'

    def __init__(self, model_class, site):
        #当前请求的model的类,把类当作参数
        self.model_class = model_class
        self.site = site
        self.request = None

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

        self.request = request

        # 数据有了需要页面
        result_list = self.model_class.objects.all()
        print(self.list_display)


        context = {
            'result_list':result_list,
            'list_display':self.list_display,
            'BaseSupermattObj':self
        }
        # info = self.model_class._meta.app_label, self.model_class._meta.model_name
        # data = '%s_%s_changelist' % info
        return render(request, 'change_list.html', context)

    def add_view(self, request):
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        data = '%s_%s_add' % info
        return HttpResponse(data)

    def delete_view(self, request, pk):
        self.model_class.objects.filter(id=pk).delete()
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        data = '%s_%s_delete_view' % info
        return HttpResponse(data)

    def change_view(self, request, pk):
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        data = '%s_%s_change_view' % info
        return HttpResponse(data)




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