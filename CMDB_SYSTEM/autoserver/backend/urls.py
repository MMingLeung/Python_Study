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
from django.conf.urls import url
from backend import views


urlpatterns = [
    url(r'^server.html$', views.server),
    url(r'^server_json.html$', views.server_json),
    url(r'^asset.html$', views.asset),
    url(r'^asset_json.html$', views.asset_json),
    url(r'^chart.html$', views.chart),
    url(r'^login.html$', views.login),
]
