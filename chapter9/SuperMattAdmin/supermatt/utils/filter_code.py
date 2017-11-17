from types import FunctionType
from django.utils.safestring import mark_safe
import copy

class FilterOption(object):
    def __init__(self, field_or_func, is_multi=False, text_func_name=None, val_func_name=None):
        '''
        
        :param field_or_func: 字段或者函数
        :param is_multi: 是否支持多选
        :param text_func_name: 在Model中定义函数，显示文本名称， 默认使用str(obj)
        :param val_func_name: 在Model中定义函数，显示文本名称，默认使用对象pk
        '''
        self.field_or_func = field_or_func
        self.is_multi = is_multi
        self.text_func_name = text_func_name
        self.val_func_name = val_func_name

    @property
    def is_func(self):
        if isinstance(self.field_or_func, FunctionType):
            return True

    @property
    def name(self):
        if self.is_func:
            # 返回函数的名字
            return self.field_or_func.__name__
        else:
            # 返回字段文本
            return self.field_or_func


class FilterList(object):
    def __init__(self, option, queryset, request):
        # FilterOption对象
        self.option = option
        # 根据field字段名获取的model对象的集合
        self.queryset = queryset
        # request.GET 请求的参数QueryDict类型
        self.param_dict = copy.deepcopy(request.GET)
        # 当前url
        self.path_info = request.path_info

    def __iter__(self):
        # ======先处理显示“全部”这个标签url======
        # 这个标签url能含有该field的任何一个参数
        # 比如username的“全部”按钮就是清空的username参数作用

        # 用于页面显示
        yield mark_safe("<div class='all-area'>")
        # 如果 option.name 在request.GET 里面，就pop出来，生成用于"全部"标签的url
        if self.option.name in self.param_dict:
            pop_val = self.param_dict.pop(self.option.name)
            # 该url是清空该field条件的url
            url = "{0}?{1}".format(self.path_info, self.param_dict.urlencode())
            # 不同的筛选需要保留原来的选中项，所以重新放入request.GET里面
            # 比如筛选 username、email ，当两者都有条件，点击username的“全部按钮”，只需要清空username 条件，email需要保留
            self.param_dict.setlist(self.option.name, pop_val)
        else:
            url = "{0}?{1}".format(self.path_info, self.param_dict.urlencode())
        if self.param_dict.getlist(self.option.name):
            yield mark_safe("<a href='{0}'>全部</a>".format(url))
        else:
            yield mark_safe("<a href='{0}' class='active'>全部</a>".format(url))
        yield mark_safe("</div><div class='others-area'>")
        # ======处理显示“全部”标签url结束======

        # ======处理field数据的显示======
        for row in self.queryset:
            # 循环当前field的每一个model对象
            # 在页面显示对应的a标签的text和url赋值
            # 单选的url：request.GET 参数后面需要增加，如果点击是同一个field的，需要覆盖。
            #

            from django.http.request import QueryDict
            # 所有条件self.param_dict
            # 如果是多选param_dict一直在添加值，之后的url里面的参数就不对了，所以需要循环刚进入进行深拷贝
            param_dict = copy.deepcopy(self.param_dict)
            # param_dict = self.param_dict

            # pk 是int 需要转换为str
            # 用于a标签的value值
            # 从对象中看看有没有它的一个方法（在Model文件中定义），有就调用返回一个名字，没有就用外键
            value = str(getattr(row, self.option.val_func_name)() if self.option.val_func_name else row.pk)
            # 用于a标签的文本
            text = getattr(row, self.option.text_func_name)() if self.option.text_func_name else str(row)

            # 用选中样式的判断
            active = False

            # 处理多选
            if self.option.is_multi:
                # 多选的话 param_dict 需要增加，最后体现在url GET请求的参数位置
                # {'page': ['2'], 'username': ['dqdw'], 'ewq': ['12'] 需要append进去
                # 获取当前的FilterOption对象的名字列表
                value_list = param_dict.getlist(self.option.name)
                # 如果当前对象的value值在列表里面，html页面需要显示选中样式
                # 再次点击需要移除
                if value in value_list:
                    value_list.remove(value)
                    from django.http.request import QueryDict
                    param_dict.setlist(self.option.name, value_list)
                    active = True
                else:
                    # 其它的a标签的url需要添加自身的name属性和value值
                    param_dict.appendlist(self.option.name, value)

            else:
                # 处理单选
                # 根据当前FilterOption对象获取request.GET QueryDict对象
                value_list = param_dict.getlist(self.option.name)
                if value in value_list:
                    active = True
                # 覆盖url GET请求对应的参数的值
                param_dict[self.option.name] = value

            # url拼接
            url = "{0}?{1}".format(self.path_info, param_dict.urlencode())
            if active:
                tpl = "<a href='{0}' class='active'>{1}</a>".format(url, text)
            else:
                tpl = "<a href='{0}'>{1}</a>".format(url, text)
            yield mark_safe(tpl)

        yield mark_safe("</div>")