from supermatt.service import test_v1
from app01 import models
from django.urls import reverse
from django.utils.safestring import mark_safe

class SuperMattUserInfo(test_v1.BaseSupermatt):

    def func(self, obj):
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

        name = '{0}:{1}_{2}_change'.format(self.site.name_sapce, self.model_class._meta.app_label, self.model_class._meta.model_name)
        # change需要传一个id号
        url = reverse(name, args=(obj.pk,))
        print(url)

        return mark_safe('<a href="{0}">编辑</a>'.format(url))

    def checkbox(self, obj):
        tag = "<input type='checkbox' value='{0}'>".format(obj.pk)
        return mark_safe(tag)

    # list_display = "__all__"
    list_display = [checkbox, 'id', 'username', 'email', func]


class SuperMattRole(test_v1.BaseSupermatt):
    # list_display = "__all__"
    list_display = ['id', 'title']

test_v1.site.register(models.UserInfo,SuperMattUserInfo)
test_v1.site.register(models.Role, SuperMattRole)