from django.template import Library
from types import FunctionType
from django.urls import reverse

register = Library()


def header(base_obj, list_display):
    # 4.3 默认表头
    if list_display == '__all__':
        yield '对象列表'
    else:
        for item in list_display:
            if isinstance(item, FunctionType):
                yield item(base_obj, is_header=True)
            else:
                obj = base_obj.model_cls._meta.get_field(item)
                yield obj.verbose_name


def inner(result_list, list_display, base_obj):
    # for row in result_list:
    #     sub = []
    #     for name in list_display:
    #         val = getattr(row, name)
    #         sub.append(val)
    #     yield sub
    print(result_list)
    if list_display == '__all__':
        # 4.3默认内容
        for row in result_list:
            yield [str(row),]
    else:
        for row in result_list:
            # name 是函数
            # app_label
            # model_name
            # url = namespace:app_label,model_name
            print(111,type(row))
            yield [name(base_obj, row) if isinstance(name, FunctionType) else getattr(row, name) for name in list_display]


# 3.4、渲染
@register.inclusion_tag('md.html')
def result_display(result_list, list_display, base_obj):
    v = inner(result_list, list_display, base_obj)

    # 4、中文表头
    h = header(base_obj,list_display )

    return {'result_list':v, 'head':h}