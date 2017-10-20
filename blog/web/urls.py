from django.conf.urls import url
from web.views import account
from web.views import home

urlpatterns = [
    url(r'^index/', home.index),
    url(r'^login/', account.login),
    url(r'^logout/', account.logout),
    url(r'^register/', account.register),
    url(r'^upload/', account.upload),
    url(r'^up.html/$', home.up),
    url(r'^comments-(\d+).html/$', home.ajax_comment),
    # KindEditor上传图片
    url(r'^upload_img', home.upload_img),
    # 生成验证码
    url(r'^check_code/', account.check_code),
    #根据标题筛选文章
    url(r'^all/(?P<type_id>\d+)/', home.index),
    #根据各标签进行匹配
    url(r'^(?P<site_name>(\w+))/(?P<key>((tag)|(category)|(date)))/(?P<val>(\w+-*\w*))/', home.filter),
    url(r'^(\w+)/p/(\d+).html$', home.final_article),
    #个人博客
    url(r'^(\w+)/', home.user_blog),
    #如果无法匹配返回首页
    url(r'^', home.index),
]
