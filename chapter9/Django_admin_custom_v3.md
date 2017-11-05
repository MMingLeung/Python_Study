# Django 自定制admin

## 一、创建app 组件名为supermatt

	python manage.py startapp supermatt

## 二、注册到Django settings.py
注释掉django自带的admin和auth以及message，加入自定义app supermatt

	INSTALLED_APPS = [
	    # 'django.contrib.admin',
	    # 'django.contrib.auth',
	    'django.contrib.contenttypes',
	    'django.contrib.sessions',
	    # 'django.contrib.messages', # 操作提示
	    'django.contrib.staticfiles',
	    'app01.apps.App01Config',
	    'app02.apps.App02Config',
	    'supermatt.apps.SupermattConfig'
	]

把下面不需要的注释让程序更加干净

	TEMPLATES = [
	    {
	        'BACKEND': 'django.template.backends.django.DjangoTemplates',
	        'DIRS': [os.path.join(BASE_DIR, 'templates')]
	        ,
	        'APP_DIRS': True,
	        'OPTIONS': {
	            'context_processors': [
	                'django.template.context_processors.debug',
	                'django.template.context_processors.request',
	                # 'django.contrib.auth.context_processors.auth',
	                # 'django.contrib.messages.context_processors.messages',
	            ],
	        },
	    },
	]
	
	AUTH_PASSWORD_VALIDATORS = [
	    # {
	    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	    # },
	    # {
	    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	    # },
	    # {
	    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	    # },
	    # {
	    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	    # },
	]

## 三、让Django程序启动的时候调用自定义插件的py文件

	# /supermatt/apps.py
	class SupermattConfig(AppConfig):
	    name = 'supermatt'
	
	    def ready(self):
	        '''
	        程序刚运行时，执行该方法
	        :return: 
	        '''
		# 调用父类的ready方法
	        super(SupermattConfig, self).ready()
	
	        from django.utils.module_loading import autodiscover_modules
		# 程序启动的时候调用每个app内名为 smatt.py的脚本
	        autodiscover_modules('smatt')

## 四、在其它app上创建model类

	# app01
	from django.db import models
	
	class UserInfo(models.Model):
	    username = models.CharField(max_length=64)
	    email = models.EmailField()
	
	    def __str__(self):
	        return self.username
	
	class Role(models.Model):
	    title = models.CharField(max_length=64)
	
	    def __str__(self):
	        return self.title


## 五、在自定义插件supermatt中创建程序

该程序用于循环获取其它app注册的model，对其生成对应url已经html页面，已经对应增删改查的方法

	# /supermatt/service/test_vi.py
	class SuperMattSite(object):
	
	    def __init__(self):
	        '''
	        构造方法
	        '''
		# 存放model类名和BaseSupermatt对象的字典
	        self._registry = {}
		# 用于反向生成url
	        self.name_sapce = 'supermatt'
	        self.app_name = 'supermatt'


	    def register(self, model_class, m = BaseSupermatt):
		'''
		注册
		传入model类， 如果没有传入一个自定义的函数，就使用BaseSupermatt实例化对象
		'''
	        self._registry[model_class] = m(model_class, self)
	        '''
	        {
	        UserInfo类名: BaseSupermatt（UserInfo类名, SuperMattSite对象）#SuperMattUserInfo
	        Role 类名：BaseSupermatt（Role类名, SuperMattSite对象）
	        XX 类名： BaseSupermatt（Role类名, SuperMattSite对象）
	        }
	        '''
	
	    def login(self, request):
	        return HttpResponse('login')
	
	    def get_urls(self):
	        ret = [
	            url(r'^login/$', self.login, name='login'),
	        ]
	        for model_class, supermatt_obj in self._registry.items():
	            # print(model_class._meta.app_label, model_class._meta.model_name, supermatt_obj)
	            # 获取model_class的app名字和类名
	            # http://127.0.0.1:8000/su/app01/role
	            app_label = model_class._meta.app_label
	            model_name = model_class._meta.model_name
	            ret.append(url(r'^%s/%s/' % (app_label, model_name), include(supermatt_obj.urls)))
	        return ret
	
	    @property
	    def urls(self):
		'''
		返回的是一个元组
		url对应关系的列表， app名称， name_space
		'''
	        return self.get_urls(),self.app_name,self.name_space


	class BaseSupermatt(object):
	    '''
	    该类可以把所有数据都拿到
	    '''
	
	    list_display = '__all__'
	
	    def __init__(self, model_class, site):
	        #当前请求的model的类,把类当作参数
	        self.model_class = model_class
		# site 是SuperMattSite的对象包含其属性name_space （之后使用）
	        self.site = site
	        self.request = None
	
	    @property
	    def urls(self):
		'''
		获取当前app_label、model_name
		拼接url的别名
		'''
	        info = self.model_class._meta.app_label, self.model_class._meta.model_name
	        urlpatterns = [
	            url(r'^$', self.changelist_view, name='%s_%s_changelist' % info),
	            url(r'^add/$', self.add_view, name='%s_%s_add' % info),
	            url(r'^(.+)/delete/$', self.delete_view, name='%s_%s_delete' % info),
	            url(r'^(.+)/change/$', self.change_view, name='%s_%s_change' % info),
	        ]
	        return urlpatterns
	
	    def changelist_view(self, request):
	        '''
	        查看列表
	        :param request: 
	        :return: 
	        '''
	        self.request = request
	
	        # 数据有了需要页面
	        result_list = self.model_class.objects.all()
	        print(self.list_display)
	
	        context = {
	            'result_list':result_list,
	            'list_display':self.list_display,
	            'BaseSupermattObj':self
	        }
	        # info = self.model_class._meta.app_label, self.model_class._meta.model_name
	        # data = '%s_%s_changelist' % info
	        return render(request, 'change_list.html', context)
	
	    def add_view(self, request):
	        info = self.model_class._meta.app_label, self.model_class._meta.model_name
	        data = '%s_%s_add' % info
	        return HttpResponse(data)
	
	    def delete_view(self, request, pk):
	        self.model_class.objects.filter(id=pk).delete()
	        info = self.model_class._meta.app_label, self.model_class._meta.model_name
	        data = '%s_%s_delete_view' % info
	        return HttpResponse(data)
	
	    def change_view(self, request, pk):
	        info = self.model_class._meta.app_label, self.model_class._meta.model_name
	        data = '%s_%s_change_view' % info
	        return HttpResponse(data)


## 五、在app01创建smatt.py（相当于自带的admin.py）

注册到自定义的插件中

	class SuperMattRole(test_v1.BaseSupermatt):
	    list_display = ['id', 'title']
	
	test_v1.site.register(models.UserInfo,SuperMattUserInfo)
	test_v1.site.register(models.Role, SuperMattRole)

## 六、程序调用过程

1. model注册 — \> \_registry字典添加数据  — \>在主程序urls写入路由关系 —\> 生成根据SuperMattSite 默认定义的url（如login）和app注册的models生成的路由对应关系 
2. 访问url —\> 根据result \_display(数据库查询到结果query\_set), list\_display(默认或者用户自定制的数据库需要显示字段名称) 根据 list\_display 是字符串或者函数， 函数直接调用把结果放到生成器里面 —\> 前面页面获取数据显示


~~~

1、test_v1.site.register(models.Role, SuperMattRole)
调用test_v1的SuperMattSite（site是其实例对象）里面的regiter方法，传入类models.Role, SuperMattRole这个自定义的类

2、regiter方法， 根据类名和传入的类分别作为key和value 放入类的变量self._registry中。

3、在django 程序的urls.py写入url关系

url(r'^su/', test_v1.site.urls)

在页面访问su/这个url就会调用test_v1.site的urls的方法

urls 返回的是一个url列表，app_name，name_space的元组
urls列表：[
            url(r'^login/$', self.login, name='login'),
        ]

4、除了上述的login url 之外还执行了一个循环
for model_class, supermatt_obj in self._registry.items():
# 获取model_class的app名字和类名
# 生成http://127.0.0.1:8000/su/app01/role这一类url
   	app_label = model_class._meta.app_label
    model_name = model_class._meta.model_name
	ret.append(url(r'^%s/%s/' % (app_label, model_name), include(supermatt_obj.urls)))

5、现在 urls 里面是这样：
# urls(r'^su/$', ([
#             url(r'^login/$', self.login, name='login'),
#             url(r'^%s/%s/' % (app_label, model_name), include(supermatt_obj.urls))
#                  ]，self.app_name,self.name_sapce),
	
6、来看看include生成什么：
		include(supermatt_obj.urls)  , include 传入supermatt_obj.urls， 这个就是生成_registry的时候，如果自己传入继承BaseSuperMatt就使用自己的，默认使用BaseSuperMatt，然后调用urls方法：
	@property
     def urls(self):
 	'''
 	获取当前app_label、model_name
 	拼接url的别名
	'''
         info = self.model_class._meta.app_label, self.model_class._meta.model_name
        urlpatterns = [
             url(r'^$', self.changelist_view, name='%s_%s_changelist' % info),
             url(r'^add/$', self.add_view, name='%s_%s_add' % info),
             url(r'^(.+)/delete/$', self.delete_view, name='%s_%s_delete' % info),
             url(r'^(.+)/change/$', self.change_view, name='%s_%s_change' % info),
         ]
         return urlpatterns
根据生成一个urlpatterns列表，里面是url以及别名

然后include最后返回的是(urlconf_module, app_name, namespace)

7、最终urls 是这样：
      urls(r'^su/$', ([
	                 url(r'^login/$', self.login, name='login'),
	                 url(r'^%s/%s/' % (app_label, model_name), (
	url(r'^$', self.changelist_view, name='%s_%s_changelist' % info),
      url(r'^add/$', self.add_view, name='%s_%s_add' % info),
      url(r'^(.+)/delete/$', self.delete_view, name='%s_%s_delete' % info),
       url(r'^(.+)/change/$', self.change_view, name='%s_%s_change' % info),app_name, namespace)
]，self.app_name,self.name_sapce ),

8、 程序执行下来生成了一堆url，我们就可以访问这些url了

比如http://127.0.0.1:8000/su/login/ 就等于说调用self.login函数

9、现在我有一个model名字是role, app名字是app01，我可以访问

http://127.0.0.1:8000/su/app01/role/

此时程序在路由系统中找到
url(r'^$', self.changelist_view, name='%s_%s_changelist' % info),

找到了BaseSupermatt类里面的self.changelist_view的函数，我们需要渲染一个页面并且显示数据
	def changelist_view(self, request):
        '''
        查看列表
        :param request: 
        :return: 
        ''‘
        self.request = request
        # 根据当前对象查询数据
        result_list = self.model_class.objects.all()
        context = {
            'result_list':result_list,   # 数据结果一个个queryset对象
            'list_display':self.list_display, # 自定义或默认显示的字段名或者是函数
            'BaseSupermattObj':self # BaseSupermatt这个对象
        }
        return render(request, 'change_list.html', context)

10、 渲染页面change_list.html
页面中我们使用tamplatetags 渲染，调用一个叫func的函数

# ==========html==========

{% load sumatt_list %}
{% func result_list list_display BaseSupermattObj %}

# ==========summatt_list.py func函数==========
# 1、func函数调用table_body,table_head生成两个对象返回给页面
# 2、table_body：如果用户自定义了list_display，像这样
# list_display 里面可以是字段名称，或者是函数
# 3、 table_head 循环遍历list_display 判断如果是函数就把函数名称首字母改为大写，放入生成器中， 如果不是就直接放入
# 4、table_body 传入result_display, list_display, basesupermatt_obj
#        1、循环result_display （里面是query_set 对象）
#        2、如果不是函数调用getattr(query_set_obj ,  list_display_字典名或者函数)
#    3、list_display的值是函数的话，调用该函数func(basesupermatt_obj,  遍历到此处的query_set数据)
#            例如：执行下面的func流程
#                         通过basesupermatt_obj可以获取反向生成url的参数，以及# query_set对象的fk，构建一个编辑的链接。
# 5、 最后返回一个字典{'table_body':table_b, 'table_head':table_h}
# 6、 该tamplatetags使用@register.inclusion_tag("md.html") ，调用了md.html模板
# 7、md.html模板循环遍历上述的字典显示数据
# ==========/app01/sumatt.py========== 
# 自定义SuperMattUserInfo类继承BaseSupermatt
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
# ==========/app01/sumatt.py========== end 
#

from django.template import Library
from types import FunctionType
register = Library()

def table_head(list_display):
    for item in list_display:
        # item 是自定义的list
        # BaseSupermattObj.model_class
        if isinstance(item, FunctionType):
            print(item.__name__.title())
        else:
            print(item)
    for row in list_display:
        yield [row.__name__.title() if isinstance(row, FunctionType) else row]

def table_body(result_display, list_display, basesupermatt_obj):
    '''
    生成器，每循环一遍才获取一次值
    :param result_display: 
    :param list_display: 
    :return: 
    '''

    for row in result_display:
        '''
        循环list_display，里面有字符串和函数
        '''
        yield [ name(basesupermatt_obj, row) if isinstance(name, FunctionType) else getattr(row, name) for name in list_display]
~~~



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
	
	# ========== md.html ========== 
	<table border="1">
	    <thead>
	    <tr>
	    {% for item in table_head %}
	        <th>
	        {% for row in item %}
	            {{ row }}
	        {% endfor %}
	        </th>
	    {% endfor %}
	     </tr>
	    </thead>
	    <tbody>
	    {% for item in table_body %}
	        <tr>
	        {% for val in item %}
	            <td>{{ val }}</td>
	            {% endfor %}
	        </tr>
	    {% endfor %}
	    </tbody>
	</table>

## 七、数据列表页面渲染及增删改查

### 1、显示中文表头

我们访问[http://127.0.0.1:8000/su/app01/userinfo/](http://127.0.0.1:8000/su/app01/userinfo/)，程序根据url找到self.changelist\_view这个方法。

#### 需求：现在需要生成中文的表头，以及添加增加按钮，并且该按钮增加完成后返回刚刚查看的页面。

实现：

1. 返回刚刚查看的页面
  1. 需要获取当前用户url；
    2. 通过request.GET.urlencode获取请求中的参数；
    3. 放入一个QueryDict中；
    4. 反向生成url，reverse(‘name\_space: app\_label\_model\_name ’)
    5. Redirect 反向生成的url + ？ + request.GET.urlencode

  2. 中文表头
    1. 现在生成的表头是依靠templatetags的table\_head生成的
    2. 中文表头的位置，models 里面的verbose\_name属性，以及自定制的is\_header里面
    3. 通过model\_class.\_meta.get\_field(字段名称)获取其对象，就可以获取verbose\_name属性
    4. 自定义的函数通过is\_header  =True 返回表头字符串

    def changelist_view(self, request):
          '''
          查看列表
          :param request: 
          :return: 
          '''
          # 以后使用
          self.request = request
        
          # 生成页面上的添加按钮的url,拼接点击之前的request.GET请求参数，用于操作完返回刚刚页面
          # QueryDict
          from django.http.request import QueryDict
          param_dict = QueryDict(mutable=True) # 默认元素可以修改
          if request.GET:
              param_dict['_changlistfilter'] = request.GET.urlencode()
          base_add_url = "{2}:{0}_{1}_add".format(self.app_label, self.model_name, self.site.name_sapce)
          add_url = reverse(base_add_url) + '?' + param_dict.urlencode()


          # 数据有了需要页面
          result_list = self.model_class.objects.all()
          print(self.list_display)
      
          context = {
              'result_list':result_list,
              'list_display':self.list_display,
              'BaseSupermattObj':self,
              'add_url':add_url
          }
          return render(request, 'change_list.html', context)


### 2、编辑、删除按钮操作完成需要返回

#### 编辑按钮通过table\_body函数，遍历 list\_display ，如果是函数就调用，返回html标签的，所以需要生成html标签时加入反向生成的URL

	# 部分代码
	param_dict = QueryDict(mutable=True)  # 默认元素可以修改
	 if self.request.GET:
		   #  获取用户当前url 
	            param_dict['_changlistfilter'] = self.request.GET.urlencode()
	            # edit url
	            base_edit_url = reverse("{2}:{0}_{1}_change".format(self.app_label, self.model_name, self.site.name_sapce), args=(obj.pk,))
	            edit_url = base_edit_url + '?' + param_dict.urlencode()
	            # del url
	            base_del_url = reverse("{2}:{0}_{1}_delete".format(self.app_label, self.model_name, self.site.name_sapce),args=(obj.pk,))
	            del_url = base_del_url + '?' + param_dict.urlencode()
	
	        return mark_safe('<a href="{0}">编辑</a> | <a href="{1}">删除</a> '.format(edit_url,del_url))


#### 1、编辑功能的实现

1. 点击编辑按钮跳转到[http://127.0.0.1:8000/su/app01/userinfo/5/change/?\_changlistfilter=page%3D1%26id%3D666%26name%3Dawd](http://127.0.0.1:8000/su/app01/userinfo/5/change/?_changlistfilter=page%3D1%26id%3D666%26name%3Dawd)（后面GET请求参数是测试的）
2. 找到BaseSupermatt.change\_view
3. 根据pk和model\_class 得到对象
4. 判断是否存在该对象
5. 使用Model\_Form ，用调一个函数返回model\_form的类
6. 实例化并传入instance，使显示的时候默认选中
7. 提交修改时判断字段是否合法，然后save， redirect 反响生成的url

   def get_add_or_edit_model_form(self):
           if self.add_or_edit_model_form:
               return self.add_or_edit_model_form
           else:
               from django.forms import ModelForm
               # 对象由类创建，类由type创建
               # 通过对象找到提供的字段
               # class MyModelForm(ModelForm):
               #     class Meta:
               #         model = self.model_class
               #         fields = '__all__'
       
               _Meta = type('Meta', (object,), {'model':self.model_class, 'fields':'__all__'})
               MyModelForm = type('MyModelForm', (ModelForm, ), {"Meta":_Meta})
               return MyModelForm
       
       def change_view(self, request, pk):
       
           # 1.获取_changlistfilter传递的参数
           # request.GET.get("_changlistfilter")
       
           # 2.获取数据默认显示并选中ModelForm
           # get_add_or_edit_model_form
           obj = self.model_class.objects.filter(pk=pk).first()
           if request.method == 'GET':
       
               if not obj:
                   return HttpResponse('id不存在')
               # instance=obj自动选中默认值
               model_form_obj = self.get_add_or_edit_model_form()(instance=obj)
           # 3.返回页面
               else:
               # 更新必须传instance
               model_form_obj = self.get_add_or_edit_model_form()(data=request.POST, files=request.FILES, instance=obj)
               if model_form_obj.is_valid():
                   model_form_obj.save()
                   base_list_url = reverse("{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.name_sapce))
                   list_url = '{0}?{1}'.format(base_list_url, request.GET.get('_changlistfilter'))
                   return redirect(list_url)
       
           context = {
                   'form':model_form_obj
               }
           return render(request, 'edit.html', context)


#### 2、删除功能

根据pk，查询出model对象调用delete方法，重定向url

### 2、对添加功能的页面改进

#### 原来使用.as\_p快速渲染html，现在需要改进为添加html标签的class属性以便使用bootstrap模板以及显示中文列名和错误信息

1. 找到add\_view 函数

2. 创建一个add\_list.py 使用templatetags的register.inclusion\_tag
  渲染（add\_list.py  生成数据 —\> html模板渲染）add\_view 函数传入model\_form\_obj 和self.model\_class。

  model_form_obj:<class 'django.forms.widgets.MyModelForm'> 

  1、循环model_form_obj得到<class 'django.forms.boundfield.BoundField'> 

  2、导入from django.forms.boundfield import BoundField

  3、里面有变量form 对应的html标签, name : 字段名称, field : model的Field

  ​

  self.model_class: <class 'app01.models.UserInfo'>

  1、model对象有_meta方法获取其有关的属性

  2、_meta.get_field(字段名) 获取model的一个的对象，相当于username = 

  models.CharField(max_length=64, verbose_name='用户名') 这个username对象，

  就可以获取verbose_name属性，在页面显示

  ​

  ~~~
  # templatetags的py文件 sumatt_add_list.py
     from django.template import Library
     register = Library()
     def head(model_form_obj, model_class):
         for item in model_form_obj:
             yield model_class._meta.get_field(item.name).verbose_name,\
                   item.as_widget(attrs={'class': 'form-control'}),item.errors
     
     @register.inclusion_tag('add_md.html')
     def add_list(model_form_obj, model_class)：
         '''
         返回数据给add_md.html模板
         '''
         h = head(model_form_obj, model_class)
         return {'head': h}

  ~~~


3. 创建inclusion\_tag所需要的html模版

      {% for item in head %}
             <p>{% for i in item %}
                 {{ i }}
                 {% endfor %}
                 </p>
          {% endfor %}
          <input type="submit" value="submit">

### 2.1、对form.as_p的渲染改进

````
# 直接使用model_form_obj里面的BoundField对象.field.label就可以获取中文标题，也就是verbose_name，
item.errors.0获取错误信息
````



### 3、PopUp 实现增加用户信息时可以动态增加用户组信息

1. 首先要判断是popup增加还是正常访问的增加，此处需要在a标签上加入popup参数,生成标签是在templatetags的函数中实现
2. 然后在add_view中判断

````python
# /tamplatetags/sumatt_add_list.py
from django.template import Library
from django.forms import ModelChoiceField
from django.urls import reverse
register = Library()
from supermatt.service import test_v1

def head(model_form_obj):
	'''
	处理html需要显示的内容
	'''
    form_list = []
    for item in model_form_obj:
		# 增加一下信息
		# is_popup：代表是否是popup的方法
		# item: model_form_obj 里面的对象
		# popurl：popup函数需要传入的地址
        row = {'is_popup': False, 'item': None, 'popurl': None}
		
		# 判断是否是FK 或者 m2m 对应增加popup增加，且注册在该组件中
        if isinstance(item.field, ModelChoiceField) and item.field.queryset.model in test_v1.site._registry:
            # ModelMultipleChoiceField继承ModelChoiceField
            # QuerySet 有个model对象，代表对应的model的类名
            # 可以item.field.queryset.model._meta.app_label 等属性用于反向生成URL
            row['is_popup'] = True
            row['item'] = item
            # 反向生成URL
            target_url = reverse("{0}:{1}_{2}_add".format(test_v1.site.name_space,
                         item.field.queryset.model._meta.app_label,                                               					       item.field.queryset.model._meta.model_name))
            # 拼接，item.auto_id：该标签的id值，用于添加完成后增加到里面
            target_url = "{0}?popup={1}".format(target_url, item.auto_id)
            row['popurl'] = target_url
        else:
            row['item'] = item
        yield row

````

3. 页面显示

   1. 判断is_popup，为真添加一个a标签，onclick方法调用自己定义的PopUpOpen函数，传入popurl

   2. PopUpOpen 弹出窗户，提交，后台处理

   3. ```
      # add_view后台部分代码
      # 如果是以popup提交，获取popid:标签的id，text:增加的对象的文本内容，pk:主键
      # 渲染到popup_response.html
      popid = request.GET.get('popup')
        if popid:
        return render(request, 'popup_response.html',
        {'data_dict':{
        'text':str(obj),
        'pk':obj.pk,
        'popid':popid}
        })
      ```

   4. ````js
      // popup_response.html
      <script>
        	// 调用opener 也就是弹出popup窗户的主体的popCallBack方法
          var data_dict = {{ data_dict|safe }}
          opener.popCallBack(data_dict);
          window.close()
      </script>
      ````

      ​

```js
<form method="POST" novalidate style="width: 700px; margin: 0 auto;margin-top: 20px;">
 {% csrf_token %}
    {% for col in form %}
        {% if col.is_popup %}
                <p>{{ col.item.field.label }}{{ col.item }}<a href="#" onclick='PopUpOpen("{{ col.popurl }}")'>添加</a>{{ col.item.errors.0 }}</p>
            {% else %}
             <p>{{ col.item.field.label }}{{ col.item }}{{ col.item.errors.0 }}</p>
        {% endif %}
    {% endfor %}
    <input type="submit" value="submit">
</form>

<script>
    function popCallBack(data_dict) {
      	// 获取返回的字典信息
      	// popid:标签的id
      	// text:增加的对象的文本内容 
        // pk:主键
        console.log(data_dict);
        var tar = document.createElement('option');
        tar.innerHTML = data_dict.text;
        tar.setAttribute('value', data_dict.pk);
        tar.setAttribute('selected', 'selected');
        document.getElementById(data_dict.popid).appendChild(tar)
    }
    function PopUpOpen(url) {
        window.open(url, url, 'status=1, height:500, width:600, toolbar=0, resizeable=0')
    }
</script>
```



### 4、分页

#### 考虑：

​	分页是通过url带上?page=xx 实现的，当用户点击分页的时候可能会有原来url的一些信息，所以分页必须带上



#### 实现：

1. 通过reverse反向生成url获取原来的url（/su/app01/userinfo/）
2. 需要拼接原来GET请求的信息，request.GET可以获取一个queryset的字典，通过._mutable = True可以修改里面的值，queryset可能在别的地方调用必须使用深复制一份新的修改。
3. PageInfo需要传入当前页页数，每页显示页数，数据总条数，原来url，原来GET请求的信息
4. PageInfo内部拼接

````
nex = " <li><a href='%s?%s'>下一页</a></li>" % (self.base_url, self.page_param_dict.urlencode())
// 最后拼接成/su/app01/userinfo/?page=xxx&之前的一些参数&....
````



````python
# PageInfo完整代码
class PageInfo:
    '''
    current_page:当前点击的页码
    per_page：每页显示的数据数量    
    all_count：数据总共的数量
    base_url：网页根地址
    show_page：页码总共显示的个数
    page_param_dict: url原参数
    '''
    def __init__(self, current_page, per_page, all_count, base_url, page_param_dict,show_page=11):
        print('allcount', all_count)
        try:
            #当前页转换为int
            self.current_page =int(current_page)
        except Exception as e :
            self.current_page = 1
        self.per_page = per_page
        self.all_count = all_count
        self.base_url = base_url
        self.page_param_dict = page_param_dict
        #计算总共的页码数
        #a 是商，b是余数，余数大于1需要增加一页放置
        a, b = divmod(self.all_count, per_page)
        if b:
            a += 1
            #总页数
        self.all_page = a
        self.show_page = show_page

    @property
    def start(self):
        #数据开始的序号，比如我点击第一页，数据开始位置是0
        return (self.current_page-1) * self.per_page

    @property
    def stop(self):
        # 数据结束的序号，比如我点击第一页，数据结束位置是10 ， 0-10显示10条
        return self.current_page * self.per_page


    def pager(self):
        #建立列表存放计算得出的数据序号
        page_list = []
        #显示页码的一半 -1 2 3 4 5-6-7 8 9 10 11- 显示11条，左右各5条
        half = int((self.show_page - 1) / 2)
        # 11 - 1 / 2 = 5

        print(self.all_count)

        # 如果数据总页数 < 11 , 只显示现有数据的总页数，就是all_page
        # 开始页数永远等于1 ， 结束页码就是最大页数
        if self.all_page < self.show_page:
            start = 1
            end = self.all_page + 1
        else:
            #总页数大于11

            #如果我点击12345永远显示前11页，当前页为1， 结束页等于show_page
            if self.current_page <= 5:
                start = 1
                end = self.show_page + 1
            else :
                #如何点击的页码+  后5页 > 总共页数，对极限值做判断， 后面的页码不需要增加
                if self.current_page + half > self.all_page:
                    #最后一页往前面数，减去show_page + 1
                    start = self.all_page - self.show_page + 1
                    end = self.all_page + 1
                else:
                    #当前页往前5页，和往后5页（开始的问题，会出现负数，所以要加判断）
                    start = self.current_page - half
                    end = self.current_page + half +1


        if self.current_page <= 1:
            prev = " <li><a href='%s?page=#'>上一页</a></li>" % (self.base_url)
        else:
            self.page_param_dict['page'] = self.current_page - 1
            prev = " <li><a href='%s?%s'>上一页</a></li>" % (self.base_url, self.page_param_dict.urlencode(), )

        page_list.append(prev)


        for i in range(start, end):
            self.page_param_dict['page'] = i
            if i == self.current_page:
                temp = " <li class='active'><a href='%s?page=%s'>%s</a></li>" % (self.base_url,i,i,)
            else:
               temp = " <li><a href='%s?%s'>%s</a></li>" % (self.base_url, self.page_param_dict.urlencode(),i,)
            page_list.append(temp)


        if self.current_page >= self.all_page:
            nex = " <li><a href='%s?page=%s'>下一页</a></li>" % (self.base_url, self.current_page)
        else:
            nex = " <li><a href='%s?%s'>下一页</a></li>" % (
            self.base_url, self.page_param_dict.urlencode())

        page_list.append(nex)

        page_list = ''.join(page_list)
        return page_list

````



### 5、Action下拉框的实现

在app01/smatt.py中定义action_list , 存放的是action执行的功能和其显示文本

````
    def initial(self, request):
        '''
        返回True，回到原来页面
        返回False，回到首页
        :param request: 
        :return: 
        '''
        pk_list = request.POST.getlist('pk')
        print(pk_list)
        models.UserInfo.objects.filter(pk__in=pk_list).update(username='初始化')
        return True
    # 赋值text的属性
    initial.text = "初始化"

    def multi_del(self, request):
        pass

    multi_del.text = '批量删除'
    # 必需是函数或者对象
    action_list = [initial,multi_del]
````



````python
# Supermatt/service/test_v1.py  
# changelist_view

....

# ########### Action操作 ###########
        # GET： 显示下拉框
        # POST：
        action_list = []
      	# 循环app01传过来的action_list,把类名作为和文本信息传入
        for i in self.action_list:
            # 把函数名字和文本信息放入action_list
            tpl = {'name':i.__name__, 'text':i.text}
            action_list.append(tpl)
        if request.method == "POST":
            # 1. 获取select 标签 name = action
            # 2. 通过反射获取函数并且调用传入request
            func_name_str = request.POST.get('action')
            ret = getattr(self, func_name_str)(request)
            action_page_url = reverse("{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.name_space))
            if ret:
            	# 回到当前页
                action_page_url = "{0}?{1}".format(action_page_url, request.GET.urlencode())
            return redirect(action_page_url)
````



````html
<!-- 页面显示-->
	{% if action_list %}
    <select class="form-control" style="width: 200px;display: inline-block" name="action">
        {% for item in action_list %}
            <option value="{{ item.name }}">{{ item.text }}</option>
        {%  endfor %}
    </select>
    <input type="submit" class="btn btn-primary" value="执行" style="display: inline-block">
    {% endif %}
````



### 6、组合搜索

思考：

1.  需要取出数据，在页面上显示
2. 让用户自定义的，可以传入是函数或者字符串，用于标识显示哪个数据表
3. 单选多选的设置
4. 选中后url的变化
5. 面向对象的思维，类与类的嵌套使用



功能实现：

1. 定义一个类，用于判断传入的是数据库字段名称还是函数、是否是多选、html显示的文本名字的函数名、html中val显示的名字的函数名。

````python
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
      	'''
      	判断是否是函数
      	'''
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
````

2. 定义一个函数用于循环遍历model的field字段，生成html标签，放入生成器中给前端渲染

````Python
class FilterList(object):
    def __init__(self, option, queryset, request):
        self.option = option
        self.queryset = queryset
        self.param_dict = copy.deepcopy(request.GET)
        # 当前url
        self.path_info = request.path_info

    def __iter__(self):
        # self.paramdict = <QueryDict: {'page': ['2'], 'ewq': ['12']}>
        # print('__iter__',self.option.name)
        # print('begin',self.param_dict)
        yield mark_safe("<div class='all-area'>")
        # 如果 option.name 在request.GET 里面，就pop出来，生成用于"全部"标签的url
        #
        if self.option.name in self.param_dict:
            pop_val = self.param_dict.pop(self.option.name)
            url = "{0}?{1}".format(self.path_info, self.param_dict.urlencode())
            # 不同的筛选需要保留原来的选中项，所以重新放入request.GET里面
            self.param_dict.setlist(self.option.name, pop_val)
        else:
            url = "{0}?{1}".format(self.path_info, self.param_dict.urlencode())
        # print('end', self.param_dict)
        yield mark_safe("<a href='{0}'>全部</a>".format(url))
        yield mark_safe("</div><div class='others-area'>")


        for row in self.queryset:
            from django.http.request import QueryDict
            # 所有条件self.param_dict
            # 如果是多选param_dict一直在添加值，之后的url里面的参数就不对了，所以需要循环刚进入进行深拷贝
            param_dict = copy.deepcopy(self.param_dict)
            # param_dict = self.param_dict

            # pk 是int 需要转换为str
            value = str(getattr(row, self.option.val_func_name)() if self.option.val_func_name else row.pk)
            text = getattr(row, self.option.text_func_name)() if self.option.text_func_name else str(row)

            active = False
            if self.option.is_multi:
                # 多选的param_dict需要增加
                # {'page': ['2'], 'username': ['dqdw'], 'ewq': ['12'] 需要append进去
                value_list = param_dict.getlist(self.option.name)
                if value in value_list:
                    value_list.remove(value)
                    active = True
                    print(value_list == param_dict)
                else:
                    param_dict.appendlist(self.option.name, value)

            else:
                # 单选就是覆盖 param_dict 的值
                value_list = param_dict.getlist(self.option.name)
                print('value_list',value_list, 'value', value)

                if value in value_list:
                    active = True
                param_dict[self.option.name] = value
                # 是否被选中设置


            # print('param_dict11111',param_dict)
            url = "{0}?{1}".format(self.path_info, param_dict.urlencode())
            if active:
                tpl = "<a href='{0}' class='active'>{1}</a>".format(url, text)
            else:
                tpl = "<a href='{0}'>{1}</a>".format(url, text)
            yield mark_safe(tpl)

        yield mark_safe("</div>")
````



3. 程序调用过程

   1. ````python
      # 在自己app01/smatt.py注册Model的时候，实例化FilterOption，把需要做组合搜索的字段传入
         filter_list = [
                          FilterOption('username', is_multi=False, text_func_name='text_username', val_func_name='value_username'),
                          FilterOption('email', is_multi=False, text_func_name='text_email', val_func_name='value_email'),
                          FilterOption('ug', is_multi=True),
                          FilterOption('role', is_multi=False),

                         ]
      ````

   2. ````python
      # 当用户访问列表页面时，进行一下的操作
      # test_v1.BaseSupermatt.changelist 部分代码

      		# 定义一个空列表，用于存放传给前端渲染数据FilterList的实例对象
              filter_list = []
              # 循环对象自身的filter_list(用户自定义的)
              # 里面是FilterOption对象
              for option in self.filter_list:
              	# 如果是函数
                  if option.is_func:
                      # 调用自身，最后返回的必须是FilterList对象
                      data_list = option.field_or_func(self, option, request)
                  else:
                      # 如果是field 字段名：'username', 'ug', 'role'
                      from django.db.models.fields.related import ForeignKey, ManyToManyField
                      # 根据model字段名字获取其对象
                      field = self.model_class._meta.get_field(option.field_or_func)
                      # 判断是否是FK／M2M
                      # 如果是，FilterList传入的queryset则是关联的表的数据
                      # 否则是自己的数据
                      if isinstance(field, ForeignKey):
                          data_list = FilterList(option, field.rel.model.objects.all(), request)
                      elif isinstance(field, ManyToManyField):
                          data_list = FilterList(option, field.rel.model.objects.all(), request)
                      else:
                          data_list = FilterList(option, field.model.objects.all(), request)
                  filter_list.append(data_list)
      ````

   3. ````python
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
              yield mark_safe("<a href='{0}'>全部</a>".format(url))
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
                          # value_list.remove(value) # 此方法无法移除
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
      ````

   4. ````Html
      <!-- 循环获取FilterList,FilterList 定义了__iter__函数， 可以迭代 -->
       	{% if filter_list %}
              <div class="row" style="margin-left: 30px" id="comb-search">
              <h3>组合搜索</h3>
              {% for fl in filter_list %}
      {#             fl = FieldList(queryset=[UserInfo,])#}
                  <div class="row">
                   {% for row in fl %}
      {#                 __iter__ 方法 yield queryset的每一个对象#}
                       {{ row }}
                       {% endfor %}
                  </div>
              {% endfor %}
              </div>
          {% endif %}
      ````

      ​

      ​



