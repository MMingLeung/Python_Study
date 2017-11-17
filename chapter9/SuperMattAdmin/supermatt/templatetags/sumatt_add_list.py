from django.template import Library
from django.forms import ModelChoiceField
from django.urls import reverse
register = Library()
from supermatt.service import test_v1



def head(model_form_obj):



    for item in model_form_obj:

        row = {'is_popup': False, 'item': None, 'popurl': None}

        # model_class根据model_form_obj的对象的name属性
        print(item.field)
        if isinstance(item.field, ModelChoiceField) and item.field.queryset.model in test_v1.site._registry:
            # ModelMultipleChoiceField继承ModelChoiceField
            from django.db.models.query import QuerySet
            # QuerySet 有个model对象，代表对应的表的类名
            # 可以item.field.queryset.model._meta.app_label 等属性用于反向生成URL
            row['is_popup'] = True
            row['item'] = item
            target_url = reverse("{0}:{1}_{2}_add".format(test_v1.site.name_space,
                                                          item.field.queryset.model._meta.app_label,
                                                          item.field.queryset.model._meta.model_name))
            target_url = "{0}?popup={1}".format(target_url, item.auto_id)
            row['popurl'] = target_url
        else:
            row['item'] = item

        yield row


@register.inclusion_tag('add_md.html')
def add_list(model_form_obj):
    # model_form包含form model所有内容
    # 显示中文
    # 使用boostrap
    # self.model_class._meta.get_field(item.name).verbose_name

    form = head(model_form_obj)

    return {'form': form}