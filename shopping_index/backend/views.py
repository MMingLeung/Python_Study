from django.shortcuts import render, HttpResponse, redirect
from app_shopping import models
from utils.pager import PageInfo
from backend.forms import Commodity
import os

# Create your views here.
def index(request):
    return render(request, 'backend_index.html')

def manage_commodity(request, *args, **kwargs):
    condition = {}
    for k,v in kwargs.items():
        kwargs[k] = int(v)
        if v != "0":
            condition[k] = v
    print("1",condition)



    # 查询商品列表
    # commodity_list = models.Commodity.objects.filter(**condition)

    # 搜索框选项
    choice_list = [{'name':'名称', 'key':'name__contains'},]
    # 搜索框的值
    search_kv = request.GET.get('name__contains')
    for item in choice_list:
        if request.GET.get(item['key']):
            condition[item['key']]= request.GET.get(item['key'])
    print("2",condition)




    # 组合搜索
    type_list = models.Type.objects.all().values('id', 'name')
    price_list = models.PriceLevel.objects.all().values('id', 'title')
    print(type_list)

    # 分页
    page_path = '/backend/manage_commodity/choice-'+str(kwargs['type_id'])+'-'+ str(kwargs['p_level_id'])
    current_page = request.GET.get("page")
    article_list_count = models.Commodity.objects.filter(**condition).count()
    page_info = PageInfo(current_page, 5, article_list_count, page_path)
    commodity_list = models.Commodity.objects.filter(**condition)[page_info.start():page_info.stop()]



    return render(request, 'backend_manage_com.html', {'commodity_list':commodity_list,
                                                       'type_list':type_list,
                                                       'price_list':price_list,
                                                       'kwargs':kwargs,
                                                       'page_info':page_info,
                                                       'choice_list':choice_list})



def edit(request, id):
    if request.method == 'GET':
        obj = models.Commodity.objects.filter(id=id).first()
        init_dict = {
            'id':id,
            'name':obj.name,
            'about':obj.about,
            'price':obj.price,
            'img':obj.img,
            'p_level_id':obj.p_level_id,
            'type_id':obj.type_id
        }
        form = Commodity(request=request, data=init_dict)
        obj = models.Commodity.objects.filter(id=id).first()
        request.session['id'] = id
        return render(request, 'edit_com.html', {'form':form, 'id':id, 'obj':obj})
    elif request.method == 'POST':
        form = Commodity(request, request.POST, request.FILES)
        if form.is_valid():
            if request.FILES:
                upload(request)
            else:
                img_obj = models.Commodity.objects.filter(id=id).first()
                img_path = str(img_obj.img).rsplit('/',1)
                form.cleaned_data['img'] = img_path[1]
            img_path = '/static/images/{}'
            form.cleaned_data['img'] =  img_path.format(form.cleaned_data['img'])
            models.Commodity.objects.filter(id=id).update(**form.cleaned_data)
            return redirect('/backend/manage_commodity/choice-0-0')
        return render(request, 'backend_manage_com.html', {'form':form, 'id':id, 'obj':obj})


def upload(request):
    if request.method == "POST":
        file_obj = request.FILES.get("img")
        print("file_obj",file_obj)
        file_path = os.path.join('static/images', file_obj.name)
        with open(file_path, 'wb') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
        return HttpResponse(file_path)

def delete(request, id):
    if request.method == 'GET':
        try:
            models.Commodity.objects.filter(id=id).delete()
            return HttpResponse('删除成功')
        except Exception as e:
            return HttpResponse('删除失败')


