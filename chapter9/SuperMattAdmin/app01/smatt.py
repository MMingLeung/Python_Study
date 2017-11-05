from django.http.request import QueryDict
from django.urls import reverse
from django.utils.safestring import mark_safe

from app01 import models
from supermatt.service import test_v1


class SuperMattUserInfo(test_v1.BaseSupermatt):

    def func(self, obj=None, is_header=False):
        'obj是当前的model对象'

        # ===========反向生成url
        # 反向生成需要获取app_label，app_model_name，namespace
        # name = namespace:label_model_name

        # 方法1
        # print(self.model_class._meta.app_label, self.model_class._meta.model_name)
        # print(self.site.name_space)

        # 方法2
        # from supermatt.service import test_v1
        # print(test_v1.site.name_space)
        # print(type(obj)._meta.app_label)
        # pk = primary_key

        # ===================
        if is_header:
            return '操作'
        else:
            # name = '{0}:{1}_{2}_change'.format(self.site.name_space, self.model_class._meta.app_label, self.model_class._meta.model_name)
            # # change需要传一个id号
            # url = reverse(name, args=(obj.pk,))
            # print(url)

            # 生成url
            param_dict = QueryDict(mutable=True)  # 默认元素可以修改
            if self.request.GET:
                param_dict['_changlistfilter'] = self.request.GET.urlencode()
            base_edit_url = reverse("{2}:{0}_{1}_change".format(self.app_label, self.model_name, self.site.name_space), args=(obj.pk,))
            edit_url = base_edit_url + '?' + param_dict.urlencode()
            base_del_url = reverse("{2}:{0}_{1}_delete".format(self.app_label, self.model_name, self.site.name_space),
                                    args=(obj.pk,))
            del_url = base_del_url + '?' + param_dict.urlencode()

        return mark_safe('<a href="{0}">编辑</a> | <a href="{1}">删除</a> '.format(edit_url,del_url))

    def checkbox(self, obj=None, is_header=False):
        if is_header:
            # 可以扩展全选功能
            return '选项'
        else:
            tag = "<input type='checkbox' value='{0}' name='pk'>".format(obj.pk)
            return mark_safe(tag)

    # list_display = "__all__"
    list_display = [checkbox, 'id', 'username', 'email', func]

    def initial(self, request):
        '''
        返回True，回到原来页面
        返回False，回到首页
        :param request: 
        :return: 
        '''
        pk_list = request.POST.getlist('pk')
        print(pk_list)
        models.UserInfo.objects.filter(pk__in=pk_list).update(username='初始化')
        return True
    # 赋值text的属性
    initial.text = "初始化"

    def multi_del(self, request):
        pass

    multi_del.text = '批量删除'
    # 必需是函数或者对象
    action_list = [initial,multi_del]

    # 1、取数据，放在页面上
    # username --> UserInfo
    # ug --> UserGroup
    # role --> Role
    # 2、有些单选或者多选，自定义
    # request.GET {'xx':[1,2],}
    # 保留当前url条件+新选择的条件
    # 单选：替换
    # 多选：增加
    # reverse + request.GET.urlencode()

    from supermatt.utils.filter_code import FilterOption



    def email(self, option, request):
        from supermatt.utils.filter_code import FilterList
        queryset = models.UserInfo.objects.filter(id__gt=2)
        return FilterList(option, queryset, request)


    filter_list = [
                    FilterOption('username', is_multi=False, text_func_name='text_username', val_func_name='value_username'),
                    # FilterOption('email', is_multi=False, text_func_name='text_email', val_func_name='value_email'),
                    FilterOption(email, is_multi=False, text_func_name='text_email', val_func_name='value_email'),
                    FilterOption('ug', is_multi=True),
                    FilterOption('role', is_multi=False),

                   ]

test_v1.site.register(models.UserInfo,SuperMattUserInfo)


class SuperMattRole(test_v1.BaseSupermatt):
    # list_display = "__all__"
    list_display = ['id', 'title']


test_v1.site.register(models.Role, SuperMattRole)
test_v1.site.register(models.UserGroup)