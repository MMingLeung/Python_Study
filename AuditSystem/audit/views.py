from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login as lg, logout as lo
from django.contrib.auth.decorators import login_required
import json
from audit import models
import random
import string
import datetime
from audit import task_handler
# Create your views here.

@login_required
def index(request):
    return render(request, 'index.html')

def login(request):
    msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 认证
        user = authenticate(username=username, password=password)
        if user:
            # 登录，封装到request里面
            lg(request, user)
            return redirect(request.GET.get('next') or '/')
        else:
            msg = '账户或密码错误'
            return render(request, 'login.html', {'msg':msg})
    return render(request, 'login.html')

@login_required
def logout(request):
    lo(request)
    return redirect('/login/')

@login_required
def host_list(request):

    return render(request, 'host_list.html')

def test(request):
    return render(request, 'base.html')

def get_host_list(request):
    gid = request.GET.get('gid')
    # a = request.user.account.host_groups.host_user_binds.
    if gid:
        # 未分组机器
        if gid == '-1':
            host_list = request.user.account.host_user_binds.all()
        else:
            group_obj = request.user.account.host_groups.get(id=gid)
            host_list = group_obj.host_user_binds.all()
        # print(host_list.values('id', 'host_name__hostname'))
        data = list(host_list.values('id', 'host_name__hostname', 'host_name__ip_addr', 'host_name__port','host_name__idc__name', 'host_user__username'))
        return  HttpResponse(json.dumps(data))


@login_required()
def get_login_token(request):
    '''
    生成token并返回
    :param request: 
    :return: 
    '''
    bind_host_id = request.POST.get('bind_host_id')
    time_obj = datetime.datetime.now() - datetime.timedelta(seconds=300)
    exist_token_objs = models.Token.objects.filter(account_id=request.user.account.id, host_user_bind_id=bind_host_id, date__gt=time_obj)
    if exist_token_objs:
    # has token already
        token_data = {'token':exist_token_objs[0].val}
    else:
        token_val = ''.join(random.sample(string.ascii_lowercase+string.digits, 8))
        token_obj = models.Token.objects.create(host_user_bind_id=bind_host_id, account=request.user.account, val=token_val)
        token_data = {'token':token_val}
    return HttpResponse(json.dumps(token_data))



@login_required
def multi_task_cmd(request):
    return render(request, 'multi_task.html')


@login_required
def multi_task(request):

    task_obj = task_handler.Task(request)
    if task_obj.is_valid():
        result = task_obj.run()
        

