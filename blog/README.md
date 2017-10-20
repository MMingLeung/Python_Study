# 第八章作业三

## 一、简介

用Django + Mysql 搭建开发个人博客及后台管理系统，功能包括：登录、注册、首页博文展示、文章详细页面、个人博客页面、个人博客后台管理等。

## 二、程序架构

### 1、目录结构

project/  
|---- app01/ 后台管理程序  
|&emsp;&emsp;&emsp;&emsp;|-----migrations/  
|&emsp;&emsp;&emsp;&emsp;|-----__init__.py  
|&emsp;&emsp;&emsp;&emsp;|-----admin.py  
|&emsp;&emsp;&emsp;&emsp;|-----apps.py  
|&emsp;&emsp;&emsp;&emsp;|-----forms.py django form表单类  
|&emsp;&emsp;&emsp;&emsp;|-----models.py django orm 模型  
|&emsp;&emsp;&emsp;&emsp;|-----tests.py 测试  
|&emsp;&emsp;&emsp;&emsp;|-----urls.py 后台管理系统路由系统  
|&emsp;&emsp;&emsp;&emsp;|-----views.py 后台管理系统视图函数  
|  
|-----project_1/  
|&emsp;&emsp;&emsp;&emsp;|-----__init__.py  
|&emsp;&emsp;&emsp;&emsp;|-----settings.py 配置文件  
|&emsp;&emsp;&emsp;&emsp;|-----urls.py  主路由系统  
|&emsp;&emsp;&emsp;&emsp;|----- wsgi.py  
|  
|-----static/ 静态文件  
|&emsp;&emsp;&emsp;&emsp;|-----carhartl-jquery-cookie jquery/      cookie插件  
|&emsp;&emsp;&emsp;&emsp;|-----css/  css文件  
|&emsp;&emsp;&emsp;&emsp;|-----font/  字体库  
|&emsp;&emsp;&emsp;&emsp;|-----img/ 上传图片文件夹  
|&emsp;&emsp;&emsp;&emsp;|-----kindeditor/ 编辑框插件  
|&emsp;&emsp;&emsp;&emsp;|-----plugins/ 插件    
|                         
|-----templates/ html模板  
|   
|-----utils/ 自定义插件    
|&emsp;&emsp;&emsp;&emsp;|-----comment.py 评论功能插件  
|&emsp;&emsp;&emsp;&emsp;|-----page.py 导航页码插件  
|&emsp;&emsp;&emsp;&emsp;|-----random_check_code 校验码插件  
|&emsp;&emsp;&emsp;&emsp;|-----xss.py  防xss攻击插件  
|             
|-----web/  博客程序  
|&emsp;&emsp;&emsp;&emsp;|-----forms/  
|&emsp;&emsp;&emsp;&emsp;|&emsp;&emsp;&emsp;&emsp;|------ account.py 跟用户相关的form表单类  
|&emsp;&emsp;&emsp;&emsp;|&emsp;&emsp;&emsp;&emsp;  
|&emsp;&emsp;&emsp;&emsp;|-----views/ 博客程序视图函数  
|&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;|------ account.py 用户行为相关的视图函数  
|&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;|------ home.py  博客主页视图函数      
|           
|&emsp;&emsp;&emsp;&emsp;|----- urls.py 路由系统  

### 2、数据库结构

见附件excel

## 三、功能演示

### 1、注册

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/blog/1.png?raw=true)

### 2、登录

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/blog/2.png?raw=true)

### 3、首页

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/blog/3.png?raw=true)

### 4、个人首页

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/blog/5.png?raw=true)

### 5、文章最终页

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/blog/6.png?raw=true)

### 6、后台管理

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/blog/7.png?raw=true)

### 7、后台新建文章

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/blog/8.png?raw=true)