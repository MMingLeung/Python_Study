from mattadmin import service
from backend import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.http.request import QueryDict
from mattadmin.utils.filter import FilterList
from mattadmin.utils.filter import FilterOption


class MyUserInfo(service.BaseMatt):

    # 4.1、中文表头
    def func(self, obj=None, is_header=False):
        '''
        self: base_obj
        obj:model.UserInfo
        :param obj: 
        :return: 
        '''
        if is_header:
            return '操作'
        else:
            param_dict = QueryDict(mutable=True)
            if self.request.GET:
                param_dict['_changelistfilter'] = self.request.GET.urlencode()

            base_edit_url = reverse('%s:%s_%s_change' % (self.site.name_space, self.app_label, self.model_name), args=(obj.pk,))
            edit_url = "{0}?{1}".format(base_edit_url, param_dict.urlencode())

            base_del_url = reverse('%s:%s_%s_delete' % (self.site.name_space, self.app_label, self.model_name),
                                    args=(obj.pk,))
            del_url = "{0}?{1}".format(base_del_url, param_dict.urlencode())

            return mark_safe("<a href='{0}'>编辑</a> | <a href='{1}'>删除</a>".format(edit_url, del_url))

    def checkbox(self, obj=None, is_header=False):
        if is_header:
            return '选项'
        else:
            tag = '<input type="checkbox" name="pk" value={0}>'.format(obj.pk)
            return mark_safe(tag)

    # 4.2 组合
    def comb(self, obj=None, is_header=False):
        if is_header:
            return '组合'
        else:
            return "%s-%s" % (obj.username, obj.email)

    def initial(self, request):
        '''
        
        :param request: 
        :return:True:返回带get参数的url
                False:回到首页
        '''
        pks = request.POST.getlist('pk')
        # 10.2可以做任何表的操作
        models.UserInfo.objects.filter(id__in=pks).update(username='hahahah')

        # 10.3 返回
        return True

    # 函数也是对象
    initial.text = '初始化'

    def mul_del(self, request):
        pass

    mul_del.text = '批量删除'

    action_list = [initial, mul_del]

    list_display = [checkbox, 'id', 'username', 'email', func, comb]

    # 11.2 组合搜索
    # 1、username UserInfo取
    # ug 是FK，去UserGrop表取
    # ur 是M2M，去角色表取
    # 2、单选/多选
    # 3、request.GET {'fk':[1,2,3,4], 'username':['wdw']}
    #  单选就是把列表覆盖，多选就是append

    def email(self, option, request):

        queryset = models.UserInfo.objects.filter(id__gt=2)

        return FilterList(option, queryset, request)


    filter_list = [
        FilterOption('username', False, text_func_name='text_username', val_func_name='value_username'),
        FilterOption('ug', True,),
        FilterOption('ur', False),
        FilterOption(email, False, text_func_name='text_email', val_func_name='value_email'),
    ]


service.site.register(models.UserInfo, MyUserInfo)
service.site.register(models.UserGroup)
service.site.register(models.Role)



