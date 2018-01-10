# 资产采集系统

## 简介：

&emsp;&emsp;本系统基于 Django Web 框架开发的服务器设备的资产采集系统，实现自动采集服务器硬件信息、入库、后台管理数据及提供 API 功能。



* [快速使用](#1)

* [系统详解](#2)

  * [架构](#2_1)
  * [程序目录结构](#2_2)
  * [客户端功能及原理](#2_3)
  * [服务端功能及原理](#2_4)

  ​

## <a id='1'>快速使用</a>：

### 1、环境

#### Python: 3.5

#### Packages: 

&emsp;&emsp;使用 pip install -r requirement.txt 所需的包。

````Python
# requirement.txt
certifi==2017.11.5
chardet==3.0.4
Django==1.11.5
djangorestframework==3.7.7
idna==2.6
Naked==0.1.31
pycrypto==2.6.1
pytz==2017.3
PyYAML==3.12
requests==2.18.4
shellescape==3.4.1
urllib3==1.22
````



### 2、设置

&emsp;&emsp;实例已经含有管理员账户和部分服务器数据，登录后即可使用。

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/cmdb_index.png?raw=true)

*自定义配置在下面章节提及*



## <a id='2'>系统详解</a>：

### 1、<a id='2_1'>架构</a>

* 资产采集
  * 服务器本地执行采集命令
  * 通过中控机利用paramiko模块执行采集命令
  * 通过SaltStack
* API
  * 数据入库
  * API验证
  * AES加密
* 后台管理系统
  * 自定义的数据显示
  * RBAC 权限管理



### 2、<a id='2_2'>程序目录结构</a>

**服务器**

````Python
├── autoserver
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── backend 后台管理系统APP
│   ├── __init__.py
│   ├── apps.py
│   ├── migrations
│   ├── page_config 页面配置
│   ├── urls.py
│   ├── utils   相关插件
│   └── views.py
├── db.sqlite3
├── manage.py
├── rbac RBAC权限管理APP
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── cbv
│   ├── middleware 自定义中间件
│   ├── models.py 数据库模型
│   ├── readme 使用说明
│   ├── service.py 处理逻辑
│   ├── templatetags 菜单树相关
│   └── theme CSS/JS
├── repository
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   └── models.py  保存服务器信息的数据库模型
├── server 自定义API
│   ├── __init__.py
│   ├── apps.py
│   ├── lib 插件
│   ├── plugins 入库组件
│   ├── serializers.py rest_framework自定义序列化工具
│   ├── urls.py
│   └── views.py
├── static
└── templates

````



**中控机/客户端（被采集信息的服务器）**

````Python
├── bin
│   └── start.py 启动文件
├── config
│   ├── cert 唯一标识
│   └── settings.py
├── debug_files 调试用服务器配置
│   ├── board.out
│   ├── cpuinfo.out
│   ├── disk.out
│   ├── memory.out
│   └── nic.out
├── lib  插件库
│   ├── conf
│   	├── config.py
│   	├── global_settings.py
│   ├── convert.py 单位转换
│   └── utils.py 加密解密插件
├── src
│   ├── client.py 处理发送功能的逻辑
│   ├── plugins 采集插件
│   └── script.py 处理不同模式下的处理逻辑
├── test_cipher.py 测试加密
└── test_sent.py 测试发送
````



### 3、<a id='2_3'>客户端功能及原理</a>

#### 配置说明

&emsp;&emsp;本程序配置文件包括 /config/settings.py 和 /lib/conf/global_settings.py ，通过 /lib/conf/config.py 以反射的形式获取上述两个配置文件的内容，存放入类的变量中，用户导入该模块，使用 settings 对象可获取所有的配置信息。

```python
'''
采集资产配置相关：
        参考 Django 中间件的形式，利用反射获取模块并执行当中的获取数据操作。
	扩展：
		按照以下格式输入“文件名：路径”
'''
PLUGINS_DICT = {
    'basic':'src.plugins.basic.Basic',
    'board':'src.plugins.board.Board',
    'cpu':'src.plugins.cpu.Cpu',
    'disk':'src.plugins.disk.Disk',
    'memory':'src.plugins.memory.Memory',
    'nic':'src.plugins.nic.Nic',
}

# 模式
MODE = 'agent' # saltstack/agent/ssh

# ssh
SSH_USER= 'root'
SSH_PASSWORD = 'password'
SSH_PORT = 22

# 私钥
SSH_KEY = '/xxx/xx/xx'

# 调试模式
DEBUG = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# API
API = 'http://127.0.0.1:8000/api/asset.html'

# 唯一标识
CERT_PATH = os.path.join(BASE_DIR, 'config', 'cert')

# auth_key
AUTH_KEY = 'aaa'

# cipher_key 必须16位
CIPHER_KEY = 'zqwrfdsazxcsdwqe'
```



#### 采集资产

&emsp;&emsp;本程序拥有三种获取资产信息的模式（本地/中控机/saltstack）

&emsp;&emsp;在 /src/plugins/ 中放置获取资产信息的插件，插件由 /src/plugins/\_\_init\_\_.py 负责根据不同的模式，选择对应发送命令的逻辑代码。

````python
# /src/plugins/__init__.py 部分代码
...

# 通过切分配置中的字典获取路径和类名
path, class_name = value.rsplit('.',1)
# 以字符串形式导入模块
module = importlib.import_module(path)
# 反射获取类
class_ = getattr(module, class_name)
# initial 为钩子函数
if hasattr(class_, 'initial'):
    obj = class_.initial()
  else:
      obj = class_()
# 传入 command 方法作为参数，其作用是根据模式选择对应的发送命令的逻辑
result = obj.process(self.command, self.debug)

...
````



````python
# 三种模式对应的发送命令的逻辑
def __agent(self, cmd):
  	# 模式一、本地获取
    import subprocess
    output = subprocess.getoutput(cmd)
    return output

def __salt(self, cmd):
    # 模式二、saltstack
    import salt.client
    # py2
    # local = salt.client.LocalClient()
    # result = local.cmd(self.host_name, 'cmd.run', [cmd])
    # return result[self.host_name]

    # py3
    import subprocess
    cmd = "salt %s cmd.run '%s'" % (self.host_name, cmd)
    output = subprocess.getoutput(cmd)
    return output

def __ssh(self, cmd):
  	# 模式三、paramiko
    import paramiko
    # key
    # private_key = paramiko.RSAKey.from_private_key_file(self.ssh_key)
    # ssh = paramiko.SSHClient()
    # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # ssh.connect(hostname=self.host_name, port=self.ssh_port, username=self.ssh_user, pkey=private_key)
    # stdin, stdout, stderr = ssh.exec_command(cmd)
    # result = stdout.read()
    # ssh.close()

    # password
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=self.host_name, port=self.ssh_port, username=self.ssh_user, password=self.ssh_password)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    result = stdout.read()
    ssh.close()
    return result
````



<u>关于本地采集的唯一标识问题</u>：使用本地模式采集机器时，在有虚拟机情况下使用本地文件记录第一次采集的主机名作为唯一标识。



### 4、<a id='2_4'>服务端功能及原理</a>

#### 配置说明

&emsp;&emsp;详见 settings.py 中注释



#### API

&emsp;&emsp;包含数据入库、 API 验证、 AES 加密三个功能



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



**API验证**

&emsp;&emsp;为了防止数据被篡改，API接受数据先对请求进行一个验证。

&emsp;&emsp;参考 tornado cookie 加密，客户端（被采集资产机器）使用 key 与时间戳拼接后进行 md5 加密，该密文与其中的时间戳拼接，放入请求头中发送。

&emsp;&emsp;API服务端，获取之后进行三个步验证。

&emsp;&emsp;（1）从请求头获取字符串，切分获得密文与时间戳，使用该时间戳与服务器当前时间判断是否超出超时时间（限制key的使用时间）。

&emsp;&emsp;（2）使用服务器与客户端共同的key与客户端时间戳进行md5加密，判断是否与客户端的相同（判断客户端的时间是否被修改以及key正确与否）。

&emsp;&emsp;（3）服务器利用 Redis 维护一个已使用的key与其超时时间的字典，判断当前key是否再其中（限制key只能使用一次）。



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



#### 后台管理

&emsp;&emsp;可定制的页面显示，通过对配置字典的修改，即可获得对应效果。



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



#### RBAC权限管理

&emsp;&emsp;基于角色的权限访问控制及菜单栏的自动生成。



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



**自定义中间件**

&emsp;&emsp;对所有请求做权限控制。

所需参数 RBAC_PERMISSION_SESSION_KEY

* 先判断是否无权限访问的 URL 
* 获取当前用户的 RBAC_PERMISSION_SESSION_KEY，如果没有则返回相应信息
* 循环上述字典，把 code_list 转换为大写形式 [code.upper()  for code in code_list]
* 先判断当前 url 和字典中的 url 正则是否匹配
  * True: 匹配 md 参数
  * False: 最后返回错误信息



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

