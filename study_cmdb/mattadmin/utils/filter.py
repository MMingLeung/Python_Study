# # 封装什么就处理什么
# class FilterList(object):
#     def __init__(self, option, data_list):
#         self.option = option
#         self.data_list = [1,2,3]
#
#     def show(self):
#         return self.option.nick()
#
#     def __iter__(self):
#         for i in self.data_list:
#             yield i
#
#
# class FilterOption(object):
#     def __init__(self, name):
#         self.name = name
#
#     def nick(self):
#         tpl = self.name + 'aaaa'
#         return tpl
#
# filterO_obj = FilterOption('matt')
# filterL_obj = FilterList(filterO_obj)
#
# # __iter__
# class Foo(object):
#     def __init__(self):
#         pass
#
#     def __iter__(self):
#         pass
#
#
# obj_list = [
#     FilterList(FilterOption('matt')),
#     FilterList(FilterOption('matt')),
#     FilterList(FilterOption('matt')),
# ]
#
# for obj in obj_list:
#     print(obj, end='')
#     for item in obj:
#         print(item, end='')
#     print()

from types import FunctionType
from django.utils.safestring import mark_safe
from copy import deepcopy


class FilterOption(object):
    def __init__(self, func_or_str, is_multi=False, text_func_name=None, val_func_name=None):
        self.func_or_str = func_or_str
        self.is_multi = is_multi
        self.text_func_name = text_func_name
        self.val_func_name = val_func_name


    @property
    def is_func(self):
        if isinstance(self.func_or_str, FunctionType):
            return True

    @property
    def name(self):
        if self.is_func:
            name = self.func_or_str.__name__
        else:
            name = self.func_or_str
        return name


class FilterList(object):
    def __init__(self, option, queryset, request):
        self.option = option
        self.queryset = queryset
        # request.GET同一个引用 需要deep.copy
        self.param_dict = deepcopy(request.GET)
        self.path_info = request.path_info

    def __iter__(self):
        # 11.5 URL
        # 剔除当前model.xx的全部参数
        yield mark_safe("<div class='all-area'>")
        print(self.option.name)
        if self.option.name in self.param_dict:
            pop_value = self.param_dict.pop(self.option.name)
            url = "{0}?{1}".format(self.path_info, self.param_dict.urlencode())
            self.param_dict.setlist(self.option.name, pop_value)
            yield mark_safe("<a href='{0}'>全部</a>".format(url))
        else:
            url = "{0}?{1}".format(self.path_info, self.param_dict.urlencode())
            yield mark_safe("<a href='{0}' class='active'>全部</a>".format(url))
        yield mark_safe("</div><div class='other-area'>")





        # 11.6 每个值的URL
        for row in self.queryset:


            # 11.8
            # 每次循环url都多了值
            # 需要深拷贝
            param_dict = deepcopy(self.param_dict)


            # 11.4 自定制显示以及value属性获取
            val = str(getattr(row, self.option.val_func_name)() if self.option.val_func_name else row.pk)

            row = getattr(row, self.option.text_func_name)() if self.option.text_func_name else str(row)
            active = False
            # 11.7 多选/单选
            if self.option.is_multi:
                val_list = param_dict.getlist(self.option.name)
                print(val_list, val)
                if val in val_list:
                    val_list.remove(val)
                    active = True
                    param_dict.setlist(self.option.name, val_list)
                else:
                    param_dict.appendlist(self.option.name, val)
            else:
                # 单选
                # 11.8 是否选中
                val_list = param_dict.getlist(self.option.name)
                print('valuelist',val_list, val, param_dict)
                if val in val_list:
                    active = True
                param_dict[self.option.name] = val

            url = "{0}?{1}".format(self.path_info, param_dict.urlencode())
            if active:
                yield mark_safe("<a href='{0}' class='active'>{1}</a>".format(url, row))
            else:
                yield mark_safe("<a href='{0}'>{1}</a>".format(url, row))
        yield mark_safe("</div>")
