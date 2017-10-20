# 第八章作业二

## 一、简介

使用Django框架，购物商城主页及后台商品管理。

功能包括：</br>
1. 官网首页动态轮播图</br>
2. 类似京东商品组合搜索</br>
3. 瀑布流图片</br>
4. 动态加载图片</br>
5. 基于Admin后台管理页面处理，前端显示</br>


## 二、程序架构

### 1、目录结构

├── app_shopping  主程序  
│   ├── admin.py  
│   ├── apps.py  
│   ├── __init__.py  
│   ├── migrations  
│   ├── models.py   数据库模型  
│   ├── urls.py     网站首页路由系统  
│   └── views.py   网站首页视图函数  
├── backend  后台程序  
│   ├── admin.py  
│   ├── apps.py  
│   ├── forms.py  表单类  
│   ├── __init__.py  
│   ├── migrations  
│   ├── urls.py    后台管理路由系统  
│   └── views.py   后台管理视图函数  
├── db.sqlite3  数据库  
├── manage.py  
├── README.md  
├── shopping_index  
│   ├── __init__.py  
│   ├── settings.py    配置文件  
│   ├── urls.py  
│   └── wsgi.py  
├── static   静态文件  
├── templates  html模板  
└── utils   



### 2、数据库结构

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/chapter8_h_2.png?raw=true)


## 三、功能演示

### 1、首页

实现组合搜索，轮播图功能

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/index/1.png?raw=true)

### 2、后台

后台管理前端数据

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/index/3.png?raw=true)
