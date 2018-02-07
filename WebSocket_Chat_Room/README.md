# 基于 WebSocket 聊天室增强版

## 简介：

&emsp;&emsp;基于 Tornado 框架 WebSocket 实现聊天室功能。

&emsp;&emsp;具体功能包括：

1. 一对一聊天
   1. 搜索好友
   2. 添加好友
2. 群聊
   1. 添加群友
   2. 管理员功能（添加群友、删除群友、禁言）



- [快速使用](#1)
- [2](#2)
  - [2-1](#2_1)
  - [2-2](#2_2)
  - [2-3](#2_3)
  - [2-4](#2_4)



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



