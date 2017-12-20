from django.urls import reverse
from django.template import Library
from types import FunctionType
from django.urls import reverse
from django.forms import ModelChoiceField, MultipleChoiceField
from mattadmin import service


register = Library()

# 8、simpletag
@register.inclusion_tag('add_edit_form.html')
def show_add_edit_form(model_form):
    # 6、不使用as_p显示
    form_list = []
    for item in model_form:
        row = {'is_pop': False, 'item': None, 'popup_url': None}
        # item是html标签,label中文名字，通过model获取
        from django.forms.boundfield import BoundField
        from django.forms.models import ModelMultipleChoiceField
        if isinstance(item.field, ModelChoiceField) and item.field.queryset.model in service.site._regstry:
            # 7、获取app_label app_name,用于反向生成url
            from django.db.models.query import QuerySet
            # queryset是查询数据的集合
            print("item",item.field.label)
            #print(item.field.queryset, item.field.queryset.model._meta.app_label)  # fk
            target_app_label = item.field.queryset.model._meta.app_label
            target_model_name = item.field.queryset.model._meta.model_name
            row['is_pop'] = True
            row['item'] = item
            url_name = reverse('{}:{}_{}_add'.format(service.site.name_space, target_app_label, target_model_name))
            target_url = "{}?popup={}".format(url_name, item.auto_id)
            row['popup_url'] = target_url
        else:
            row['item'] = item
        form_list.append(row)
    return {'form':form_list}
