from django.conf.urls import url
from app01 import views


urlpatterns = [
    url(r'^(\d+)/delete_article$', views.delete_article),
    url(r'^(\d+)/edit_article.html$', views.edit_article),
    url(r'^(\d+)/manager/new_article/', views.manager_new_article),
    url(r'^(\w+)/manager.html$', views.manager),
    url(r'^(\d+)/manager/article_management/choice-(?P<article_type_id>\d+)-(?P<category_id>\d+)-(?P<tags__nid>\d+)/$', views.article_management),
    url(r'^(?P<nid>(\d+))/manager/(?P<key>((category)|(tag)|(user))).html$', views.manager_filter),
]
