# 资产采集系统

## 简介：

​        本系统基于 Django Web 框架开发的服务器设备的资产采集系统，实现自动采集服务器硬件信息、入库、后台管理数据及提供 API 功能。



* <span href="#1">快速使用</span>



## <span id='1'>快速使用</span>：

### 1、环境

#### Python: 3.5

#### Packages: 

​        使用 pip install -r requirement.txt 所需的包。

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

​        实例已经含有管理员账户和部分服务器数据，登录后即可使用。

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/cmdb_index.png?raw=true)

​	*自定义配置在下面章节提及*



## 系统详解：

### 1、架构

* 资产采集
  * 服务器本地执行采集命令
  * 通过中控机利用paramiko模块执行采集命令
  * 通过SaltStack
* API
  * 提供主机列表
  * API验证
  * AES加密
* 后台管理系统
  * 可自定义的数据显示



### 2、程序目录结构

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



### 3、客户端功能及原理

#### 配置说明

​        本程序配置文件包括 /config/settings.py 和 /lib/conf/global_settings.py ，通过 /lib/conf/config.py 以反射的形式获取上述两个配置文件的内容，存放入类的变量中，用户导入该模块，使用 settings 对象可获取所有的配置信息。

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

​        本程序拥有三种获取资产信息的模式（本地/中控机/saltstack）

​        在 /src/plugins/ 中放置获取资产信息的插件，插件由 /src/plugins/\_\_init\_\_.py 负责根据不同的模式，选择对应发送命令的逻辑代码。

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





