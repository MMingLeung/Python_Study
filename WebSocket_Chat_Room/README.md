# 基于 WebSocket 的聊天室

## 简介：

&emsp;&emsp;基于 Tornado 框架 WebSocket 实现聊天室功能。

&emsp;&emsp;具体功能包括：

- 一对一聊天
  - 搜索好友
  - 添加好友
- 群聊
  - 添加群友
  - 管理员功能（添加群友、删除群友、禁言）

<br>

- [快速使用](#1)
- [功能详解](#2)
  - [程序目录](#2_1)
  - [一对一聊天](#2_2)
  - [群聊](#2_3)



## <a id='1'>快速使用</a>：

### 1、环境

#### Python: 3.5

<br>

#### Packages:

&emsp;&emsp;使用 pip install -r requirement.txt 所需的包。

```python
# requirement.txt
PyMySQL==0.8.0
tornado==4.5.3
```

<br>

#### Mysql:

&emsp;&emsp;导入数据库

````mysql
mysql -uroot -p db_name < /db/chat_room_db
````

<br>

### 2、功能演示

#### URL 一览：

````
/index 首页
/login 登录
/chat_one2one 一对一聊天
/search_friend 搜索好友
/add_friend 添加好友
/chat_group 群聊
/group_block 群禁言
/group_del_mem 删除群友
/group_add_mem 添加群友
````

<br>

#### 用户账户：

````
账号    密码
user_A 123
user_B 123
user_C 123
user_E 123
````

<br>

#### 登录：

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/chat_room/login.png?raw=true)

<br>

#### 一对一聊天：

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/chat_room/one2one.png?raw=true)

<br>

#### 群聊：

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/chat_room/group.png?raw=true)

<br>

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/chat_room/group2.png?raw=true)



<br>

## <a id='2'>功能详解</a>：

### 1、<a id='2_1'>程序目录</a>

````
chat_room_v001/
├── app.py
├── db # 数据库
│   └── chat_room_db
├── handlers 
│   ├── chat.py # web_socket handler
│   ├── friends.py # 处理与好友、群聊相关的 handler
│   ├── index.py # 首页 handler
│   └── login.py # 登录 handler
├── lib
│   ├── CUSTOMIZED_SESSION # 自定义 session
│   ├── __init__.py
│   └── db_controller.py # 操作数据库的插件
├── requirements.txt
├── static
│   ├── __pycache__
│   ├── jquery-1.12.4.js
│   ├── settings.py # 配置
│   └── uimethod_index.py # UI_Method 
└── templates # 模板
    ├── index.html
    ├── login.html
    └── message.html
````

<br>

### 2、<a id='2_2'>一对一聊天</a>

<br>

### 3、<a id='2_3'>群聊</a>



