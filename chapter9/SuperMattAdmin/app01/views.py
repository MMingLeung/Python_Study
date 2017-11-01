from django.shortcuts import render, HttpResponse
from django.urls import reverse

# Create your views here.
def test(request):
    '''
    反向生成
    include 导入其它文件路径include('app01.urls', namespace='aaa')
    app01.urls
    xxxx name = xxx
    :param request: 
    :return: 
    '''
    #根据namespace分发对应地址
    # url = reverse('supermatt:login')
    # print(url)

    # namesapce:定义的名称name
    url = reverse('supermatt:app01_userinfo_add')
    print(url)
    return HttpResponse('213')

def test2(request):
    return HttpResponse('22222')