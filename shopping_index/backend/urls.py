"""shopping_index URL Configuration

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
    url(r'^index/', views.index),
    url(r'^edit/(?P<id>\d+)', views.edit),
    url(r'^manage_commodity/choice-(?P<type_id>\d+)-(?P<p_level_id>\d+)', views.manage_commodity),
    url(r'^upload/', views.upload),
    url(r'^delete/(?P<id>\d+)', views.delete),

]
