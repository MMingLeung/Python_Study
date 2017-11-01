from django.template import Library
from types import FunctionType
register = Library()

# @register.simple_tag
def table_head(list_display):
    # for item in list_display:
    #     # item 是自定义的list
    #     # BaseSupermattObj.model_class
    #     if isinstance(item, FunctionType):
    #         print(item.__name__.title())
    #     else:
    #         print(item)
    for row in list_display:
        yield [row.__name__.title() if isinstance(row, FunctionType) else row]

def table_body(result_display, list_display, basesupermatt_obj):
    '''
    生成器，每循环一遍才获取一次值
    :param result_display: 
    :param list_display: 
    :return: 
    '''

    # for row in result_display:
    #     sub = []
    #     for name in list_display:
    #         val = getattr(row, name)
    #         sub.append(val)
    #     yield sub
    print(result_display)
    for row in result_display:
        '''
        循环list_display，里面有字符串和函数
        '''
        yield [ name(basesupermatt_obj, row) if isinstance(name, FunctionType) else getattr(row, name) for name in list_display]



# 导入一个模板,可使用模板语言传值
@register.inclusion_tag("md.html")
def func(result_display, list_display, BaseSupermattObj):
    #返回值是生成器
    table_b = table_body(result_display, list_display, BaseSupermattObj)

    # v = [
    #     ['1','A','88'],
    #     ['2','B','99'],
    # ]

    table_h = table_head(list_display)
    return {'table_body':table_b, 'table_head':table_h}