from supermatt.service import test_v1
from app01 import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.http.request import QueryDict

class SuperMattUserInfo(test_v1.BaseSupermatt):

    def func(self, obj=None, is_header=False):
        'obj是当前的model对象'

        # ===========反向生成url
        # 反向生成需要获取app_label，app_model_name，namespace
        # name = namespace:label_model_name

        # 方法1
        # print(self.model_class._meta.app_label, self.model_class._meta.model_name)
        # print(self.site.name_sapce)

        # 方法2
        # from supermatt.service import test_v1
        # print(test_v1.site.name_sapce)
        # print(type(obj)._meta.app_label)
        # pk = primary_key

        # ===================
        if is_header:
            return '操作'
        else:
            # name = '{0}:{1}_{2}_change'.format(self.site.name_sapce, self.model_class._meta.app_label, self.model_class._meta.model_name)
            # # change需要传一个id号
            # url = reverse(name, args=(obj.pk,))
            # print(url)

            # 生成url
            param_dict = QueryDict(mutable=True)  # 默认元素可以修改
            if self.request.GET:
                param_dict['_changlistfilter'] = self.request.GET.urlencode()
            base_edit_url = reverse("{2}:{0}_{1}_change".format(self.app_label, self.model_name, self.site.name_sapce), args=(obj.pk,))
            edit_url = base_edit_url + '?' + param_dict.urlencode()
            base_del_url = reverse("{2}:{0}_{1}_delete".format(self.app_label, self.model_name, self.site.name_sapce),
                                    args=(obj.pk,))
            del_url = base_del_url + '?' + param_dict.urlencode()

        return mark_safe('<a href="{0}">编辑</a> | <a href="{1}">删除</a> '.format(edit_url,del_url))

    def checkbox(self, obj=None, is_header=False):
        if is_header:
            # 可以扩展全选功能
            return '选项'
        else:
            tag = "<input type='checkbox' value='{0}'>".format(obj.pk)
            return mark_safe(tag)

    # list_display = "__all__"
    list_display = [checkbox, 'id', 'username', 'email', func]


test_v1.site.register(models.UserInfo,SuperMattUserInfo)


class SuperMattRole(test_v1.BaseSupermatt):
    # list_display = "__all__"
    list_display = ['id', 'title']


test_v1.site.register(models.Role, SuperMattRole)