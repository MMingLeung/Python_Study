"""ModelForm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from app01 import views
from supermatt.service import test_v1
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # include 如果参数是模块路径，导入模块找urlpatterns变量，获取列表
    # url(r'^test/$', include('app01.urls')),
    # 可以这样写
    # url(r'^test/$', ([
    #             url(r'^test/', views.test),
    #             url(r'^test/', views.test),
    #             url(r'^test/', views.test),
    #                  ],'app_name','name_space')),

    url(r'^su/', test_v1.site.urls),
    url(r'^test/', views.test),
    url(r'^test2/', views.test2),
]
