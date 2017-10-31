from django.contrib import admin
from django.http import HttpResponse
from app01 import models
from django.utils.safestring import mark_safe
from types import FunctionType
# Register your models here.
from django.forms import widgets
from django.utils.html import format_html
from django.forms import ModelForm, fields
#判断是否是函数
# isinstance(xx, FunctionType)



# =====================model_form
class MyForm(ModelForm):
    '''
    先去UserInfo找到所有字段放到字典，找自定义form的字段，然后update
    '''
    other = fields.CharField(widget=widgets.TextInput())
    user = fields.CharField(widget=widgets.TextInput(),error_messages={"required":"用户名不能为空"})
    class Meta:
        models = models.UserInfo
        fields = '__all__'


# =====================formfield_overrides

class MyTextarea(widgets.Widget):
    def __init__(self, attrs=None):
        default_attrs = {
            'cols': '40',
            'rows': '10'
        }
        if attrs:
            default_attrs.update(attrs)
        super(MyTextarea, self).__init__(default_attrs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs)
        return format_html("<textarea {}>\r\n{}</textarea>", final_attrs, value)

# =====================formfield_overrides end



class UserInfoMolerAdmin(admin.ModelAdmin):

    form = MyForm

    def test(obj):
        '''
        obj 是循环的当前对象所有行字段
        函数的返回就是页面的显示
        :return: 
        '''
        return mark_safe("<a href='http://www.baidu.com'>%s-%s</a>" %(obj.user, obj.email))

    # 列显示
    list_display = ('id','user', 'email', test)

    # 列连接
    list_display_links = ('email',)

    # 右侧快速筛选  and 运算
    list_filter = ('user','email')

    # 连表，FK字段
    # list_select_related =

    # 分页
    # list_per_page = 10  #每页显示
    # list_max_show_all = 200 #显示全部数据
    # paginator = Paginator #插件

    # 列快速编辑
    list_editable = ('user', )

    # 模糊搜索
    search_fields = ('user', )

    # 操作后保留搜索条件
    preserve_filters = ('user', )

    # def changelist_view(self, request, extra_context=None):
    #     return HttpResponse('changelistview')

    # 详细页面save按钮
    save_as = False
    # 保存后继续编辑
    save_as_continue = True

    # save按钮在上面
    save_on_top = False

    # inlines 为外键连到的表设计的






    # action 列表页下拉框里面的功能
    def func(self, request, queryset):
        print(self, request, queryset)
        print(request.POST.getlist('_selected_action'))
    func.short_description = "中文显示自定义action"
    actions = [func, ]

    # for item in actions:
    #     # Func首字母大写 , item()
    #     if hasattr(item, 'short_description'):
    #         print(item.short_description)
    #     else:
    #         print(item.__name__.title())
    # end action

    # 定制模版
    # change_list_template = "my_change_list_template.html"

    # 默认FK是下拉框现在是搜索框
    # raw_id_fields = ('group', )

    # 详细编辑页面显示
    # fields = ('') 显示
    # exclude = ('user') 排除
    # readonly_fields = ('user') 只读

    # 详细页面划分
    # fieldsets = ((
    #     ('基本数据'),{
    #         'fields':('user', 'email')
    #     }),('其它', {
    #     'classes':('collapse', 'wide', 'extrapretty'),
    #     'fields':('user', 'email', 'group'),
    # })
    # )

    # M2M
    filter_vertical = ('m2m',)

    # 列表排序
    ordering = ('-id', )

    # 编辑时，是否在页面右上角显示view on set
    def view_on_site(self, obj):
        return 'http://www.baidu.com'

    # radio_fields 针对 FK
    radio_fields = {'group':admin.VERTICAL}

    # 列表显示搜索时，显示个数
    show_full_result_count = True


    # 设置详细页面的标签
    # formfield_overrides = {
    #     models.models.CharField:{'widget':MyTextarea},
    # }

    # 添加页面，填入值后，自动填充。email-同步User输入的值
    # prepopulated_fields = {'email':("user","user")}

    # 为空的时候显示
    # empty_value_display = ""

    # 修改错误提示



# =====================inline 在增加组的页面能增加用户

class UserInfoInline(admin.StackedInline): #StackedInline/TabularInline
    extra = 0
    model = models.UserInfo

class UserGroupModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    inlines = [UserInfoInline, ]
# =====================inline end

# admin.site.register(models.UserInfo,admin.ModelAdmin)
admin.site.register([models.UserInfo,],UserInfoMolerAdmin)
admin.site.register(models.UserGroup, UserGroupModelAdmin)
admin.site.register(models.Role,admin.ModelAdmin)


# 写法2
# @admin.register([models.UserInfo, ])
# class UserAdmin(admin.ModelAdmin):
#     pass

'''
内部就是创造一个这样的字典
_registry = {
models.UserInfo:admin.ModelAdmin(models.UserInfo, self=admin.site)
....
}
'''
