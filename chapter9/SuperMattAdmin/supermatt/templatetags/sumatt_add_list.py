from django.template import Library

register = Library()

def head(model_form_obj, model_class):
    for item in model_form_obj:
        # model_class根据model_form_obj的对象的name属性

        yield model_class._meta.get_field(item.name).verbose_name,\
              item.as_widget(attrs={'class': 'form-control'}),item.errors



@register.inclusion_tag('add_md.html')
def add_list(model_form_obj, model_class):
    # model_form包含form model所有内容
    # 显示中文
    # 使用boostrap
    # self.model_class._meta.get_field(item.name).verbose_name


    # for item in model_form_obj:
        # model_form_obj 里面包含 BoundField 类
        # name 字段名称, field 属性（model的field), form (根据model字段生成的html标签)
        # <class 'django.forms.boundfield.BoundField'>

        # print('11111',item.as_widget(attrs={'class':'form-control'}))
        # from django.db.models import options
              # item, type(item), item.field, model_class._meta.get_field(item.name).verbose_name)
    from django.forms.boundfield import BoundField
    h = head(model_form_obj, model_class)
    return {'head': h}