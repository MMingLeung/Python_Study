# 后台管理程序


## 一、简介
使用Django框架，基于角色的访问控制实现后台管理系统。以配置文件的形式，利用ajax生成对应html标签，增加程序的可扩展性。

功能包括：</br>
1. 注册、登录</br>
2. 管理员对用户信息的增删改查</br>
3. 管理员对用户组信息的增删改查</br>



## 二、程序架构
程序包含两部分，第一部分是RBAC权限控制模块，第二部分是后台管理系统。

### 1.目录结构
#### 1.1程序目录
cms 后台管理程序</br>
├── app__cms  </br>
│   ├── data_config  页面显示的数据配置文件 </br>
│   ├── admin.py  </br>
│   ├── apps.py  </br>
│   ├── forms.py form组件 </br>
│   ├── __init__.py  </br>
│   ├── migrations  </br>
│   ├── models.py 数据库模型 </br>
│   ├── tests.py  </br>
│   └── views.py  视图函数</br>
├── cms  </br>
│   ├── __init__.py  </br>
│   ├── settings.py  配置文件</br>
│   ├── urls.py  路由系统</br>
│   └── wsgi.py </br>
├── db.sqlite3 </br>
├── manage.py </br>
├── rbac 权限管理程序</br>
│   ├── admin.py </br>
│   ├── apps.py </br>
│   ├── cbv  视图函数CBV模式例子</br>
│   ├── __init__.py </br>
│   ├── middleware 中间件</br>
│   ├── migrations </br>
│   ├── models.py 数据库模型</br> 
│   ├── readme 说明文件</br>
│   ├── service.py 自定义方法</br>
│   ├── templatetags 自定义模板标签</br>
│   ├── theme CSS主题</br>
│   └── urls.py </br>
├── static </br>
│   ├── carhartl-jquery-cookie-92b7715 </br>
│   ├── css </br>
│   ├── font </br>
│   ├── Highcharts-5.0.14 </br>
│   ├── img </br>
│   ├── jquery-3.2.1.js </br>
│   ├── kindeditor </br>
│   ├── nb_list.js 自执行函数</br>
│   └── plugins </br>
├── templates 模板</br>
└── utils </br>

#### 1.2 URL
/index.html  登录、注册页面  
/backend/index.html  后台管理首页  
/backend/basic\_info.html  员工资料查询及编辑页面  
/backend/basic\_ginfo.html  员工组查询编辑页面  
/backend/basic\_ginfo.html?md=detail&nid=X  员工组成员编辑页面



### 2.数据库结构

#### 2.1 RBAC

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/cms_backend/RBAC.png?raw=true)

#### 2.2 后台管理系统

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/cms_backend/backend_cms_sql.png?raw=true)


## 三、功能演示

管理员账号：jacob 密码：12345


### 1、注册、登录

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/cms_backend/cms_index.png?raw=true)


![](https://github.com/MMingLeung/Markdown-Picture/blob/master/cms_backend/cms_register.png?raw=true)

### 2、员工信息管理

搜索框支持组合搜索、模糊查询。

点击‘进入编辑模式’，勾选多选框进行编辑、保存、删除操作。

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/cms_backend/backend_index.png?raw=true)

### 3、员工组信息管理

搜索框支持组合搜索、模糊查询。

点击‘进入编辑模式’，勾选多选框进行编辑、保存、删除操作。

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/cms_backend/backend_group.png?raw=true)

#### 3.1、员工组人员的设置

选中用户名，点选中间操作按钮进行组内成员调整

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/cms_backend/backend_group_edit.png?raw=true)
