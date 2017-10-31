# Django Admin Study

## 一、简述

Django Admin 是内部的一个app。在admin.py中注册models，内部会自动根据models生成对应的URL以及后台管理页面及相应功能。



## 二、源码跟踪

1. settings.py 注册admin

```Python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app01.apps.App01Config',
]
```

2. 在admin.py注册自己创建的model

```python
admin.site.register(models.UserInfo,admin.ModelAdmin)
```

3. 进入查看register方法

部分代码

```python
# 如果没有传入admin_class 默认调用ModelAdmin
if not admin_class:
    admin_class = ModelAdmin
...
# 传入的可以是可迭代对象
if isinstance(model_or_iterable, ModelBase):
  model_or_iterable = [model_or_iterable]
  for model in model_or_iterable:
... 
# 字典_registry的key是model, value是ModelAdmin（默认）的实例
self._registry[model] = admin_class(model, self) #self 是AdminSite的对象

```

4. settings.py

```
ROOT_URLCONF = 'django_admin.urls'
```

5. 进入django\_admin.urls - \> admin.site.urls - \> urls

```Python
# 跳转到AdminSite
@property
def urls(self):
    return self.get_urls(), 'admin', self.name

# 进入get_urls方法
# 此处循环遍历_registry字典的k,v ，把url拼接成
# http://127.0.0.1:8000/admin/app01/userinfo/add/
# http://127.0.0.1:8000/admin/app01/userinfo/1/change/
# http://127.0.0.1:8000/admin/app01/userinfo/1/delete/
# 前面半段负责拼接app名/model名，后面include(model_admin.urls)负责拼接对应操作方法（默认调用ModelAdmin.urls）

for model, model_admin in self._registry.items():
    urlpatterns += [
        url(r'^%s/%s/' % (model._meta.app_label,                    model._meta.model_name),    include(model_admin.urls)),
        ]

```



## 三、自定义Admin 组件

1. models.py

```
from django.db import models

# Create your models here.
class UserInfo(models.Model):
    user = models.CharField(max_length=64)
    email = models.EmailField()
    group = models.ForeignKey("UserGroup", null=True, blank=True)
    m2m = models.ManyToManyField("Role", null=True, blank=True)

    def __str__(self):
        return self.user


class UserGroup(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return self.title

class Role(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name
```

2. admin.py

   1. 注册的两种写法

	  ```
	  # 1
	  admin.site.register(models.Role,admin.ModelAdmin)
	  # 2
	  @admin.register([models.UserInfo, ])
	  class UserAdmin(admin.ModelAdmin):
	      pass
	  ```

   2. 可修改的参数

	  ```
	 # 自定义UserInfoModelAdmin
	 admin.site.register([models.UserInfo,],UserInfoModelAdmin)

	# 
	class MyForm(ModelForm):
	    '''
	    UserInfo找到所有字段放到字典，找自定义form的字段，然后update
	    '''
		# 在后台显示增加一项other输入框
	    other = fields.CharField(widget=widgets.TextInput())
		#user 输入框增加中文错误信息提示
	    user = fields.CharField(widget=widgets.TextInput(),error_messages={"required":"用户名不能为空"})
	    class Meta:
	        models = models.UserInfo
		    # 显示所有字段
	        fields = '__all__'
	#  
	class UserInfoMolerAdmin(admin.ModelAdmin):

		#  通过自定义Form修改后台管理页面的字段的信息
	    form = MyForm

		# 在后台管理页面增加一列列名是test 内容是一个a标签
	    def test(obj):
	        '''
	        obj 是循环的当前对象所有行字段
	        函数的返回就是页面的显示
	        :return: 
	        '''
	        return mark_safe("<a href='http://www.baidu.com'>%s-%s</a>" %(obj.user, obj.email))

	    # 列标题显示
	    list_display = ('id','user', 'email', test)

	    # 列进入修改的连接位于哪个字段
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
	    
	    # 改变渲染的html页面
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
	    # fields = ('user') 显示
	    # exclude = ('user') 排除
	    # readonly_fields = ('user') 只读

	    # 详细页面划分上下部分
	    # fieldsets = ((
	    #     ('基本数据'),{
	    #         'fields':('user', 'email')
	    #     }),('其它', {
	    #     'classes':('collapse', 'wide', 'extrapretty'),
	    #     'fields':('user', 'email', 'group'),
	    # })
	    # )

	    # 多对多显示
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

	admin.site.register(models.UserGroup, UserGroupModelAdmin)
	# =====================inline end
	  ```


