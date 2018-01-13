

# 项目管理系统

## 简介：

&emsp;&emsp;本系统基于 Django Web 框架，参考 admin 组件功能，开发的项目管理系统。含 RBAC 基于角色的权限访问功能。



* [快速使用](#1)

* [系统详解](#2)

  * [架构](#2_1)
  * [程序目录结构](#2_2)
  * [CURD 组件功能及原理](#2_3)
  * [项目管理系统](#2_4)
  * [RBAC权限管理](#2_5)

  ​

## <a id='1'>快速使用</a>：

### 1、环境



#### Python: 3.5



#### Packages: 

&emsp;&emsp;使用 pip install -r requirement.txt 所需的包。

````Python
# requirement.txt
Django==1.11.5
pytz==2017.3
````



### 2、使用

&emsp;&emsp;实例已经含有管理员账户和部分服务器数据，登录后可浏览效果。

&emsp;&emsp;账号：aaa

&emsp;&emsp;密码：aaa

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/caro_admin_index.png?raw=true)





## <a id='2'>系统详解</a>：

### 1、<a id='2_1'>架构</a>

<br>

* CURD 组件
* 项目管理系统
* RBAC 权限管理组件

<br>

### 2、<a id='2_2'>程序目录结构</a>

<br>

**CURD 组件**

````Python
caroadmin/
├── __init__.py
├── apps.py 设置启动执行的py文件名
├── models.py 
├── service.py 主逻辑
├── templates 模版
│   ├── add.html 添加页面
│   ├── change.html 修改页面
│   ├── changelist.html 列表显示页面
│   ├── changelist_action.html 批量操作模板
│   ├── layout.html 页面母版
│   ├── login.html 登录页面
│   ├── md.html 数据表格模板
│   ├── popup.html 弹窗增加页面
│   └── popup_response.html 弹窗附属页面
├── templatetags 处理显示数据的逻辑
│   ├── popup.py 
│   └── result_list.py 主要数据显示
├── utils 插件
│   ├── __init__.py
│   ├── filter.py 组合搜索插件
│   └── page.py 页码插件
└── views.py
````

<br>

**项目管理系统**

````Python
project_mamger_system/
├── __init__.py
├── __pycache__
├── apps.py
├── caro.py CURD 组件程序
└── models.py 数据库Model
````

<br>

**RBAC 权限管理组件**

```python
rbac/
├── __init__.py
├── apps.py
├── caro.py CURD 组件程序
├── middleware
│   └── rbac.py 权限验证中间件
├── models.py 数据库模型
├── readme
├── service.py
├── templatetags 
│   └── rbac.py 生成菜单树程序
├── theme 前端样式
│   ├── blue
│   ├── default
│   └── warm
└── urls.py
```

<br>

### 3、<a id='2_3'>CURD 组件功能及原理</a>

<br>

#### 功能说明

&emsp;&emsp;通过在其它 django app 中创建 caro.py ，调用 /caro_admin/caroadmin/service.py 下的 site 对象的register方法，传入 model 类名，便可自动生成对应的增、删、改、查页面和其相应的功能。

```python
# 例子：
# project_management_system/caro.py
service.site.reigster(Department)
```

<br>

#### 自定制功能

- 列表显示（list_display）
  - 自定制功能列
- 批量操作（action_list）
- 组合搜索（filter_list）

<br>

&emsp;&emsp;<u>在所在 app 中的 caro.py 文件下定义一个继承  service.BaseCaro 的类即可开始定制功能。</u>

<br>

**列表显示**

````Python
class YourModelNameBase(service.BaseCaro):
    '''
    list_display: Input the field's name of your model to make the table of  
                  display. 
                  besides, you can design functions and put its name into this
                  list.
    '''
    # functions of show checkbox in the website 
    def checkbox(self, obj=None, is_header=None):
        if is_header:
            return '选项'
        tpl = "<input type='checkbox' name='pk' value={}>".format(obj.pk)
            return mark_safe(tpl)
        
    list_display = [checkbox, 'id', 'name', 'description', 'floor']
````

<br>

**批量操作**

```Python
class YourModelNameBase(service.BaseCaro):
    '''
    Your could design multi-action function to deal with some process.
    * This function depand on "checkbox".
    
    action_list: [function's name, ]
    function.text: display on table's header
    '''
    def initial(self, request):
        pks = request.POST.getlist('pk')
        # do model's operate which you need.
        # ProjectRecord.objects.filter(id__in=pks).update(date='2013-3-2')
        
        # True: after finish, return to the current page.
        # False: after finish, return to the index page.
        return True

    initial.text = '初始化'

    action_list = [initial, ]
```

<br>

**组合搜索**

```python
class YourModelNameBase(service.BaseCaro):
    '''
	Create filter list functions on the web where you want to build.
	
	filter_list: A list which includes FilterOption's object.
	
	FilterOption: Encapsulates options and functionality for given field's name or 
				  a function.
				  args:
				  	is_multi: Can or can't multiple choice
				  	text_func: A fuction' name which Building in the field's model 
				  		       class, return a string for html tag's attribution
				 	val_func: A fuction' name which Building in the field's model 
				  		       class, return a string for html tag's attribution
    '''
    def your_function_name(self, option, request):
        from caro_admin.caroadmin.utils.filter import FilterList
        queryset = models.UserInfo.objects.filter(id__gt=2)
    return FilterList(option, queryset, request)

    filter_list = [
        FilterOption('model_field_name', is_multi=False, text_func='xx', val_func= 'xxx'),
        FilterOption('model_field_name', is_multi=True),
        FilterOption(your_function_name, is_multi=False),
    ]
```

<br>

#### 代码解释

1. 启动文件 caroadmin/apps.py

````python
from django.apps import AppConfig

class SupermattConfig(AppConfig):
    name = 'caroadmin'

    def ready(self):
        super(SupermattConfig, self).ready()

        from django.utils.module_loading import autodiscover_modules
        '设置启动时执行的 python 文件名'
        autodiscover_modules('caro')
````

<br>

2. 注册 Model 类

````python
service.site.reigster(Model_name)
````

<br>

3. caro_admin/urls.py 

````python
from django.conf.urls import url
from caroadmin import service


# url 对应关系
urlpatterns = [
    url(r'test/', service.site.urls),
]
````

<br>

4. caroadmin/service.py 

```python
'''
CaroSite: 封装一个 caroadmin app 实例对象，并绑定对应的路由系统中。通过 register 方法可以把 
	      model 类注册到当前对象中，通过 get_urls 方法为 model 提供一系列视图函数。
	      
BaseCaro: 为 caroadmin 对象封装属性和方法。包括增删改查路由系统、视图函数、模板、自定制功能。
'''    
```

<br>

5. 路由系统的补充

```python
'''
在 3 中注册到路由系统中，通过 urls 方法返回的是([url 对应关系], app_name, name_space).
如下：
	([
	url(r'^test/', ([url(r'^login/$', self.login, name='login'),
	url(r'^%s/%s/' % (app_label, model_name), include(basesupermatt_obj.urls))
	# app_label=app01, model_name=usergroup
	]
	, app_name, name_space)
	
其中 include 方法返回一下结果：
    	(
    		[
    		 url(r'^$', self.changelist_view, name='%s_%s_changelist' % info),
        	 url(r'^add/$', self.add_view, name='%s_%s_add' % info), 
        	 ....
        	],
        	 None, # app_name
        	 None # name_space
        )
        
总结: 一个 model 注册到 caroadmin 实例对象中，等于创建了增删改查4个路由系统对应关系。
	 http://127.0.0.1/test/app_name/model_name --> changelist_view,
	 http://127.0.0.1/test/app_name/model_name/add --> add_view,
	 ....
'''
```

<br>

6. 视图函数 changelist_view

```python
# caroadmin/service.py 
changelist_view(): 
	根据用户定制，显示列表页面，由 ChangeList 类的负责封装显示所需的属性与方法。
    
ChangeList: 
    封装了页码功能、数据列表、组合搜索条件、批量操作、显示列表功能。
    
FilterList 与 FilterOption: 
    FilterOption 封装组合搜索相关的属性和方法,用于生成组合搜索前端代码的逻辑判断。
    FilterList 根据 FilterOption 实例对象，通过 __iter__ 作为可迭代对象，生成具体前端代码。
    
```

<br>

### <a id='2_4'>4、项目管理系统</a>

<br>

&emsp;&emsp;本系统用于记录工程项目相关信息，配合 CURD 组件，信息化处理各项数据。

<br>

**数据库表**



|  表名  | WorkSpace |      |         |      |          |      |
| :--: | :-------: | :--: | :-----: | :--: | :------: | :--: |
|  id  |    主键     |      |         |      |          |      |
| 字段名称 |    序号     | 字段说明 |   类型    |  位数  |    属性    |  备注  |
|  id  |     1     |  -   |   int   |  -   | 非空、唯一、自增 |  -   |
| name |     2     | 办公区  | varchar |  64  |    非空    |  -   |



|  表名  | Department  |        |         |      |          |      |
| :--: | :---------: | :----: | :-----: | :--: | :------: | :--: |
|  主键  |     id      |        |         |      |          |      |
|  序号  |    字段名称     |  字段说明  |   类型    |  位数  |    属性    |  备注  |
|  1   |     id      |   -    |   int   |  -   | 非空、唯一、自增 |  -   |
|  2   |    name     |   部门   | varchar |  64  |    唯一    |  -   |
|  3   | description | 部门情况描述 |  text   |  -   |    -     |  -   |
|  4   |    floor    | 部门所在楼层 |   int   |  -   |    -     |  -   |



|  表名  | ProjectList |                       |              |      |          |      |
| :--: | :---------: | :-------------------: | :----------: | :--: | :------: | :--: |
|  主键  |     id      |                       |              |      |          |      |
|  序号  |    字段名称     |         字段说明          |      类型      |  位数  |    属性    |  备注  |
|  1   |     id      |           -           |     int      |  -   | 非空、唯一、自增 |  -   |
|  2   | work_space  |         办公区外键         |  foreignKey  |  -   |    -     |  -   |
|  3   | department  |         部门外键          |  foreignKey  |  -   |    -     |  -   |
|  4   | class_type  |        项目类型选择         | smallInteger |  -   |    -     |  -   |
|  5   | status_type |        项目状态选择         | smallInteger |  -   |    -     |  -   |
|  6   |  duration   |          工期           | IntegerField |  -   |    -     | 单位：天 |
|  7   |    price    |          费用           |    float     |  -   |    -     |  -   |
|  8   | start_data  |         开始日期          |     date     |  -   |    -     |  -   |
|  9   |  end_data   |         结束日期          |     date     |  -   |   可为空    |  -   |
|  10  |    staff    | project_list_staff 外键 |  foreignKey  |  -   |    -     | 多对多  |



|  表名  | UserProfile |           |            |      |          |       |
| :--: | :---------: | :-------: | :--------: | :--: | :------: | :---: |
|  主键  |     id      |           |            |      |          |       |
|  序号  |    字段名称     |   字段说明    |     类型     |  位数  |    属性    |  备注   |
|  1   |     id      |     -     |    int     |  -   | 非空、唯一、自增 |   -   |
|  2   |  name_obj   | RBAC用户表外键 | foreignKey |  -   |    唯一    | 一对一关联 |
|  3   |    name     |    用户名    |  varchar   |  32  |    -     |   -   |
|  4   |  workspace  |   办公区外键   | foreignKey |  -   |    -     |   -   |
|  5   |    memo     |    备注     |    text    |  -   |    -     |   -   |
|  6   | data_joined |   加入时间    |    date    |  -   |    -     |   -   |



|  表名  | ProjectRecord  |                |            |      |          |                |
| :--: | :------------: | :------------: | :--------: | :--: | :------: | :------------: |
|  主键  |       id       |                |            |      |          |                |
|  序号  |      字段名称      |      字段说明      |     类型     |  位数  |    属性    |       备注       |
|  1   |       id       |       -        |    int     |  -   | 非空、唯一、自增 |       -        |
|  2   |    project     | ProjectList 外键 | foreignKey |  -   |    唯一    | 与 day_num 联合唯一 |
|  3   |    day_num     |       天数       |    int     |  -   |    -     |    项目进行到第几天    |
|  4   |      date      |     办公区外键      |    date    |  -   |    -     |     工程开始日期     |
|  5   |    engineer    | UserProfile外键  | foreignKey |  -   |    -     |       -        |
|  6   | project_detail |      项目详细      |    text    |  -   |    -     |       -        |



|  表名  |  Reporter  |              |            |      |          |          |
| :--: | :--------: | :----------: | :--------: | :--: | :------: | :------: |
|  主键  |     id     |              |            |      |          |          |
|  序号  |    字段名称    |     字段说明     |     类型     |  位数  |    属性    |    备注    |
|  1   |     id     |      -       |    int     |  -   | 非空、唯一、自增 |    -     |
|  2   |   phone    |     电话号码     |  varchar   |  64  |    -     |    -     |
|  3   |    name    |      姓名      |  varchar   |  64  |    -     | 项目/报修发起人 |
|  4   |    sex     |      性别      |  varchar   |  32  |    -     |  工程开始日期  |
|  5   | department | Department外键 | foreignKey |  -   |    -     | 发起人所在部门  |
|  6   |   notes    |     联系记录     |    text    |  -   |    -     |    -     |



|  表名  | ReporterFollowerUp |               |            |      |                    |              |
| :--: | :----------------: | :-----------: | :--------: | :--: | :----------------: | :----------: |
|  主键  |         id         |               |            |      |                    |              |
|  序号  |        字段名称        |     字段说明      |     类型     |  位数  |         属性         |      备注      |
|  1   |         id         |       -       |    int     |  -   | 非空、          唯一、自增 |      -       |
|  2   |      reporter      |  Reporter外键   | foreignKey |  -   |         -          |      -       |
|  3   |        note        |      记录       |    text    |  -   |         -          |      -       |
|  4   |       status       |      状态       |    int     |  -   |         -          | 选项见models.py |
|  5   |     consultant     | UserProfile外键 | foreignKey |  -   |         -          |    跟进者外键     |
|  6   |        date        |     创建日期      |    date    |  -   |         -          |      -       |









### <a id='2_5'>5、RBAC权限管理</a>

&emsp;&emsp;基于角色的权限访问控制及菜单栏的自动生成。

<br>

**数据库表**

|  表名  |   User   |      |         |      |          |            |
| :--: | :------: | :--: | :-----: | :--: | :------: | :--------: |
|  主键  |    id    |      |         |      |          |            |
|  序号  |   字段名称   | 字段说明 |   类型    |  位数  |    属性    |     备注     |
|  1   |    id    |  -   |   int   |  -   | 非空、唯一、自增 |     -      |
|  2   | username | 用户名  | varchar |  32  |  非空、唯一   | 用户登录后台管理系统 |
|  3   | password |  密码  | varchar |  64  |    非空    | 用户登录后台管理系统 |
|  4   |  email   |  邮箱  | varchar | 256  |    非空    |     -      |



|  表名  |  Role   |      |         |      |          |      |
| :--: | :-----: | :--: | :-----: | :--: | :------: | :--: |
|  主键  |   id    |      |         |      |          |      |
|  序号  |  字段名称   | 字段说明 |   类型    |  位数  |    属性    |  备注  |
|  1   |   id    |  -   |   int   |  -   | 非空、唯一、自增 |  -   |
|  2   | caption | 角色名  | varchar |  32  |  非空、唯一   |  -   |



|  表名  | User2Role |         |            |      |          |      |
| :--: | :-------: | :-----: | :--------: | :--: | :------: | :--: |
|  主键  |    id     |         |            |      |          |      |
|  序号  |   字段名称    |  字段说明   |     类型     |  位数  |    属性    |  备注  |
|  1   |    id     |    -    |    int     |  -   | 非空、唯一、自增 |  -   |
|  2   |   user    | User表外键 | ForeignKey |  -   |    非空    |  -   |
|  3   |   role    | Role表外键 | ForeignKey |  -   |    非空    |  -   |



|  表名  |  Menu   |       |            |      |          |      |
| :--: | :-----: | :---: | :--------: | :--: | :------: | :--: |
|  主键  |   id    |       |            |      |          |      |
|  序号  |  字段名称   | 字段说明  |     类型     |  位数  |    属性    |  备注  |
|  1   |   id    |   -   |    int     |  -   | 非空、唯一、自增 |  -   |
|  2   | caption | 菜单名称  |  varchar   |  32  |    非空    |  -   |
|  3   | Parent  | 自关联外键 | ForeignKey |  -   |    非空    |  -   |



|  表名  | Permission |        |            |      |          |      |
| :--: | :--------: | :----: | :--------: | :--: | :------: | :--: |
|  主键  |     id     |        |            |      |          |      |
|  序号  |    字段名称    |  字段说明  |     类型     |  位数  |    属性    |  备注  |
|  1   |     Id     |   -    |    int     |  -   | 非空、唯一、自增 |  -   |
|  2   |  caption   |  权限名称  |  varchar   |  32  |    非空    |  -   |
|  3   |    url     | url正则  |  varchar   | 128  |    非空    |  -   |
|  4   |    menu    | Menu外键 | ForeignKey |  -   |    非空    |  -   |





|  表名  | Role2Permission |                           |            |      |          |      |
| :--: | :-------------: | :-----------------------: | :--------: | :--: | :------: | :--: |
|  主键  |       id        |                           |            |      |          |      |
|  序号  |      字段名称       |           字段说明            |     类型     |  位数  |    属性    |  备注  |
|  1   |       id        |             -             |    int     |  -   | 非空、唯一、自增 |  -   |
|  2   |      role       |          Role表外键          | ForeignKey |  -   |    非空    |  -   |
|  3   |   permission    | Permission            表外键 | ForeignKey |  -   |    非空    |  -   |



<br>

**配置说明**

````python
# ############################## RBAC权限相关配置开始 ##############################
# # 无需权限控制的URL
RBAC_NO_AUTH_URL = [
    '/backend/login.html',
    '/register.html',
    '/admin.*',
    '/rbac.*',
    '/backend/index.html',
    '/api*'
]

# session中保存权限信息的Key
RBAC_PERMISSION_SESSION_KEY = "rbac_permission_session_key"

# Http请求中传入的参数，根据其获取GET、POST、EDIT等检测用户是否具有相应权限
# 例如：
#       http://www.example.com?md=get   表示获取
#       http://www.example.com?md=post  表示添加
#       http://www.example.com?md=del   表示删除
RBAC_QUERY_KEY = "md"
RBAC_DEFAULT_QUERY_VALUE = "get"

# 无权访问时，页面提示信息
RBAC_PERMISSION_MSG = "无权限访问"

# Session中保存菜单和权限信息的Key
RBAC_MENU_PERMISSION_SESSION_KEY = "rbac_menu_permission_session_key"
RBAC_MENU_KEY = "rbac_menu_key"
RBAC_MENU_PERMISSION_KEY = "rbac_menu_permission_key"

# 菜单主题
RBAC_THEME = "default"
# ############################## RBAC权限相关配置结束 ##############################
````

<br>

**登录初始化**

&emsp;&emsp;登录验证后通过 /rbac/service.py initial_permission 方法把用户权限信息保存至Session中。

````python
Session 中保存：
RBAC_PERMISSION_SESSION_KEY: user_permission_dict
	permission_url_list: ['xxx/xxx/', 'xxx/xxx/add', 'xxx/xxx/change/']
	
RBAC_PERMISSION_MENU_DICT_SESSION_KEY: 
	{
      RBAC_MENU_LIST_SESSION_KEY: menu_list,
	  RBAC_PERMISSION_LIST_SESSION_KEY: menu_permission_list
	}
	
	menu_list: {
      'id':n, 
      'caption':'xxx', 
      'parent_id':'n'
    }
	
	menu_permission_list: {
      'premission_id':n, 
      'premission__url':'/xxx/xxx', 
      'premission__menu_id':m, 
      'premission__caption':'xx'
    }
````

<br>

**自定义中间件**

&emsp;&emsp;对所有请求做权限控制。

所需参数 RBAC_PERMISSION_SESSION_KEY

* 先判断是否无权限访问的 URL 
* 获取当前用户的 RBAC_PERMISSION_SESSION_KEY，如果没有则返回相应信息
* 构建用于正则匹配的 pattern
* 先判断当前 url 和字典中的 url 正则是否匹配
  * True: 匹配 md 参数
  * False: 最后返回错误信息

<br>

**菜单栏**

&emsp;&emsp;自动生成左侧菜单栏。

所需参数 RBAC_PERMISSION_MENU_DICT_SESSION_KEY:

 {RBAC_MENU_LIST_SESSION_KEY: menu_list, RBAC_PERMISSION_LIST_SESSION_KEY: menu_permission_list}

```
process_menu_tree_data
- menu_list 与 menu_permission_list 关联
- 关于打开层级菜单和标红样式作处理
- 菜单与菜单的层级结构

build_menu_tree_html
- 对菜单数据作字符串格式化，递归生成对应标签
```

<br>

自定义扩展：

&emsp;&emsp;可根据用户当前使用的html模板作对应的修改。

````
tpl1 = """
<div class='rbac-menu-item'>
<div class='rbac-menu-header'>{0}</div>
<div class='rbac-menu-body {2}'>{1}</div>
</div>
"""
tpl2 = """
<a href='{0}' class='{1}'>{2}</a>
"""
````

&emsp;&emsp;例子：

````html
    tpl1 = '''
    <li class="{2}">
        <a href="#">
            <i class="fa fa-bar-chart-o"></i> 
            <span class="nav-label">{0}</span>
            <span class="fa arrow"></span>
        </a>
        <ul class="{3}">
             {1}
        </ul>
    </li>'''
    tpl2 = '''
    <li class="{1}">
        <a href="{0}" >{2}</a>
    </li>
    '''
````



