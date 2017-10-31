"""autoserver URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from api import views
from rest_framework import routers


#2、创建对象
routers = routers.DefaultRouter()
#路由映射
routers.register(r'servers', views.ServerViewSet)

urlpatterns = [

    url(r'^asset.html$', views.asset),
    #url(r'^servers.html$', views.servers),
    #url(r'^servers/(d+).html$', views.servers_detail),


    # url(r'^', include(routers.urls)),
    url(r'^servers/(\d+)/', views.ServerDetail.as_view()),
    url(r'^servers/', views.ServerView.as_view()),

]
