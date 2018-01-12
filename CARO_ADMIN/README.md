# 项目管理系统

## 简介：

&emsp;&emsp;本系统基于 Django Web 框架，参考 admin 组件功能，开发的项目管理系统。含 RBAC 基于角色的权限访问功能。



* [快速使用](#1)

* [系统详解](#2)

  * [架构](#2_1)
  * [程序目录结构](#2_2)
  * [CURD 组件功能及原理](#2_3)
  * [服务端功能及原理](#2_4)

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
    list_display: input the field's name of your model to make the table of  
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
    * this function depand on "checkbox".
    
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
	
    '''
    def your_function_name(self, option, request):
        from caro_admin.caroadmin.utils.filter import FilterList
        queryset = models.UserInfo.objects.filter(id__gt=2)
    return FilterList(option, queryset, request)

    filter_list = [
        FilterOption('model_field_name', is_multi=False),
        FilterOption('model_field_name', is_multi=True),
        FilterOption(your_function_name, is_multi=False),
    ]
```













### 4、<a id='2_4'>服务端功能及原理</a>

<br>

#### 配置说明

&emsp;&emsp;详见 settings.py 中注释



<br>

#### API

&emsp;&emsp;包含数据入库、 API 验证、 AES 加密三个功能



<br>

**数据入库**

&emsp;&emsp;与采集资产的模式相同，从配置文件中读取插件的路径，以反射的形式调用入库的方法。

````python
# settings.py
API_PLUGINS = {
    'Disk':'server.plugins.disk.Disk',
    'Memory':'server.plugins.memory.Memory',
    'Nic':'server.plugins.nic.Nic',
    'Server':'server.plugins.server.Server',
    'Cpu':'server.plugins.cpu.Cpu',
}
````





&emsp;&emsp;硬盘入库逻辑：

````Python
# /autoserver/server/plugins/disk.py
'''
1、通过新数据和旧数据，获取其 slot(槽位) 号
2、交集：更新
3、新与旧的差集：新增
4、旧与新的差集：删除
'''
# 更新
# 循环 slot 列表，根据 slot 号获取一条新数据，根据server_obj(从视图函数中传入)获取旧数据(对象)，循环新数据（字典），通过反射形式从旧数据对象中获取对应的值并与新值对比，通过setattr设置，最后model_obj.save()
````



<br>

**API验证**

&emsp;&emsp;为了防止数据被篡改，API接受数据先对请求进行一个验证。

&emsp;&emsp;参考 tornado cookie 加密，客户端（被采集资产机器）使用 key 与时间戳拼接后进行 md5 加密，该密文与其中的时间戳拼接，放入请求头中发送。

&emsp;&emsp;API服务端，获取之后进行三个步验证。

&emsp;&emsp;（1）从请求头获取字符串，切分获得密文与时间戳，使用该时间戳与服务器当前时间判断是否超出超时时间（限制key的使用时间）。

&emsp;&emsp;（2）使用服务器与客户端共同的key与客户端时间戳进行md5加密，判断是否与客户端的相同（判断客户端的时间是否被修改以及key正确与否）。

&emsp;&emsp;（3）服务器利用 Redis 维护一个已使用的key与其超时时间的字典，判断当前key是否再其中（限制key只能使用一次）。

<br>

**AES加密**（autoserver/server/lib/data_cipher.py）

&emsp;&emsp; API 验证中仍有漏洞，如果数据被抓包后以更快速度传输就有篡改隐患，为此给数据加密。

&emsp;&emsp;使用 AES 加密，被加密数据长度必须是 16 的倍数。加密程序通过 bytesarray 类型，对原有数据增加16 或者 16与余数的差的<u>数量</u>，内容为<u>16 或者 16与余数的差</u>

````python
# 例子
tmp = len(bytearray('aaaaaaaaaaaaaa', encoding='utf-8'))
if tmp == 16:
    add_bytes = 16
else:
    tmp = tmp % 16
    add_bytes = 16 - tmp
for _ in range(add_bytes):
    bytesarr_message.append(add_bytes)
# 结果：result = b'aaaaaaaaaaaaa333'
# 解密后取值：result[0:-[result[-1]]]
````

<br>

#### 后台管理

&emsp;&emsp;可定制的页面显示，通过对配置字典的修改，即可获得对应效果。

<br>

**前端显示配置详解**(autoserver/backend/page_config/)

````python
1、表格
	table_config:
    {'q': '数据库查询字段名',
     'title': '表头中文',
     'disable': '是否显示',
     'text':
         {
             'tpl': '格式化的key',
             'kwargs': {'key': '格式化的内容'} # @+字段：取值 @@+字段：取固定元组里的值
         },
     'attrs': {
         'edit-enable': '能否编辑',
         'edit-type': '编辑框input/select',
         'global_key': '对应@@功能',
         'origin': '原始值',
         'name': '数据库查询字段名'
     }
     
2、 搜索框
     search_config： 
    {'name': '数据库查询字段名', 'text': '中文名', 'search_type': '搜索框input/select', },
    {'name': '数据库查询字段名', 'text': '中文名', 'search_type': '搜索框input/select', 'global_key': '取model中choices值/外键的key'},
'''
````

<br>

#### RBAC权限管理

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
|  2   |  caption   |  菜单名称  |  varchar   |  32  |    非空    |  -   |
|  3   |    url     | url正则  |  varchar   | 128  |    非空    |  -   |
|  4   |    menu    | Menu外键 | ForeignKey |  -   |    非空    |  -   |





|  表名  | Action  |      |         |      |          |      |
| :--: | :-----: | :--: | :-----: | :--: | :------: | :--: |
|  主键  |   id    |      |         |      |          |      |
|  序号  |  字段名称   | 字段说明 |   类型    |  位数  |    属性    |  备注  |
|  1   |   id    |  -   |   int   |  -   | 非空、唯一、自增 |  -   |
|  2   | caption | 菜单名称 | varchar |  32  |    非空    |  -   |
|  3   |  code   | 请求方式 | varchar |  32  |    非空    |  -   |



|  表名  | Permission2Action2Role |               |            |      |          |      |
| :--: | :--------------------: | :-----------: | :--------: | :--: | :------: | :--: |
|  主键  |           id           |               |            |      |          |      |
|  序号  |          字段名称          |     字段说明      |     类型     |  位数  |    属性    |  备注  |
|  1   |           id           |       -       |    int     |  -   | 非空、唯一、自增 |  -   |
|  2   |       permission       | Permission表外键 | ForeignKey |  -   |    非空    |  -   |
|  3   |         action         |   Action表外键   | ForeignKey |  -   |    非空    |  -   |
|  4   |          role          |    Role表外键    | ForeignKey |  -   |    非空    |  -   |

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
	user_permission_dict: {'permission__url':['GET', 'POST', ...]}
	
RBAC_MENU_PERMISSION_SESSION_KEY: 
	{
      RBAC_MENU_KEY: menu_list,
	  RBAC_MENU_PERMISSION_KEY: menu_permission_list
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
* 循环上述字典，把 code_list 转换为大写形式 [code.upper()  for code in code_list]
* 先判断当前 url 和字典中的 url 正则是否匹配
  * True: 匹配 md 参数
  * False: 最后返回错误信息

<br>

**菜单栏**

&emsp;&emsp;自动生成左侧菜单栏。

所需参数 RBAC_MENU_PERMISSION_SESSION_KEY:

 {RBAC_MENU_KEY: menu_list, RBAC_MENU_PERMISSION_KEY: menu_permission_list}

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

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/rbac_menu_extend.png?raw=true)

