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
from rest_framework import routers
from django.conf.urls import url, include
from server import views
# ################################ 原生rest framwork ################################
# 作用：快速搭建api
# routers = routers.DefaultRouter()
# routers.register(r'users', views.ServerViewSet)
# ##################################################################################

urlpatterns = [
    url(r'^asset.html$', views.asset),

    # ############################## 原生rest framwork ###############################
    # url(r'^', include(routers.urls)),

    # ############################## 扩展rest framwork api ###########################
    url(r'^servers/', views.ServerView.as_view()),
    url(r'^servers/(\d+)/$', views.ServerDetail.as_view()),
    # ###############################################################################

    # ################################ 自定义 api ####################################
    # url(r'^servers/(\d+).html$', views.servers_detail),
    # url(r'^servers.html$', views.servers),
    # ###############################################################################


]
