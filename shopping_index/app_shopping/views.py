from django.shortcuts import render, HttpResponse
from app_shopping import models
from django.db import connection, connections


# Create your views here.
def index(request, *type__name, **kwargs):

    #处理kwargs
    condition = {}
    for k,v in kwargs.items():
        if not v :
            kwargs[k] = 0
        else:
            kwargs[k] = int(v)
            condition[k] = int(v)

    condition_key_list = []
    for k,v in condition.items():
        if v == 0:
            condition_key_list.append(k)
    for key in condition_key_list:
        condition.pop(key)
    print("condition",condition)

    obj = models.Commodity.objects.filter(**condition)

    # 价格
    price_list = models.PriceLevel.objects.all().values('id', 'title')
    # 类型
    type_list = models.Type.objects.all().values('id', 'name')
    print(kwargs)


    return render(request, 'index.html', {'obj':obj, 'kwargs':kwargs, 'price_list':price_list, 'type_list':type_list})