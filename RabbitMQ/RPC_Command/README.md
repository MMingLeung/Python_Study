# 基于 RabbitMQ 远程发送命令

## 简介：

&emsp;&emsp;基于 Rabbitmq RPC 模式，实现对远方服务器发送命令及查询结果功能。



* [快速使用](#1)

* [程序详解](#2)

  * [架构](#2_1)
  * [目录](#2_2)
  * [服务端代码解释](#2_3)
  * [客户端代码解释](#2_4)

* [RPC模式详细](https://github.com/MMingLeung/Python_Study/tree/master/RabbitMQ)

  ​

## <a id='1'>快速使用</a>：

### 1、环境

#### Python: 3.5

#### RabbitMQ: 3.7.2

#### Packages: 

&emsp;&emsp;使用 pip install -r requirement.txt 所需的包。

````Python
# requirement.txt
pika==0.11.2
````



### 2、启动

> 1. 远方服务器启动 RabbitMQ Server 和 client.py 程序
> 2. 本地启动 /server/bin/run.py，进入菜单界面
> 3. 输入命令

<br>

**启动界面：**

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/rpc_command/index.png?raw=true)

<br>

**输入命令：**

第一条

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/rpc_command/input_command.png?raw=true)

<br>

第二条

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/rpc_command/input_command2.png?raw=true)

<br>

**查询结果：**

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/rpc_command/check_task.png?raw=true)

<br>

## <a id='2'>程序详解</a>：

### 1、<a id='2_1'>架构</a>

<br>

服务端：发送命令，接收命令的结果

客户端：接收命令，执行命令，返回结果

<br>

### 2、<a id='2_2'>程序目录结构</a>

<br>

**服务端**

````Python
./server/
├── __init__.py
├── bin
│   ├── __init__.py
│   └── run.py # 启动文件
├── config
│   ├── __init__.py
│   ├── __pycache__
│   ├── conf.py # 配置管理
│   └── settings.py # 用户配置
├── lib
└── src
    ├── __init__.py # 程序主逻辑
    └── my_rpc.py # RabbitMQ RPC 模式的类
````

<br>

**客户端**

````Python
client.py
````

<br>

### 3、<a id='2_3'>服务端代码解释</a>

<br>

````
/bin/run.py
# 设置配置文件路径至环境变量
# 程序启动入口
````

<br>

````
/config/settings.py
# 配置文件

/config/conf.py
# 从环境变量中获取配置文件路径，根据路径导入配置文件，把配置保存在对象的属性中
# 使用时，只需要导入 conf.py 中 settings （单例模式）获取配置
````

<br>

````
/src/__init__.py
# 程序主逻辑，根据用户输入，做相关操作（向队列发送消息、查询命令结果、打印历史命令、退出）

/src/my_rpc.py
# RabbitMQ RPC 模式
````

<br>

### 4、<a id='2_4'>客户端代码解释</a>

<br>

````
client.py
````

<br>



