from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login as lg, logout as lo
from django.contrib.auth.decorators import login_required
import json
from audit import models
import random
import string
import datetime
from audit import task_handler
import os
from django.views.decorators.csrf import csrf_exempt
from AuditSystem import settings
import zipfile
from wsgiref.util import FileWrapper
# Create your views here.

@login_required
def index(request):
    '''
    主页
    :param request: 
    :return: 
    '''
    return render(request, 'index.html')

def login(request):
    '''
    登录页面
    1、使用django自带的账户认证authenticate方法认证（django.contrib.auth）
    2、调用django自带的login函数，把账户信息封装到request
    :param request: 
    :return: 
    '''
    msg = ''
    if request.method == 'POST':
        # 可以使用make_password check_password对密码进行加密和校验
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 认证
        user = authenticate(username=username, password=password)
        if user:
            # 登录，封装到request里面
            lg(request, user)
            # next原本是什么页面的登录后自动跳转
            return redirect(request.GET.get('next') or '/')
        else:
            msg = '账户或密码错误'
            return render(request, 'login.html', {'msg':msg})
    return render(request, 'login.html')

@login_required
def logout(request):
    '''
    登出
    :param request: 
    :return: 
    '''
    lo(request)
    return redirect('/login/')

@login_required
def host_list(request):
    '''
    主机列表页面
    :param request: 
    :return: 
    '''
    return render(request, 'host_list.html')

def test(request):
    '''
    测试html显示效果
    :param request: 
    :return: 
    '''
    return render(request, 'base.html')

def get_host_list(request):
    '''
    根据前端提交的host组id，在数据库中查询出结果
    :param request: gid
    :return: data
    '''
    gid = request.GET.get('gid')
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
    1、获取前端传入的某一台主机的id号
    2、通过用现在时间-超时时间（默认300s），需要写到配置文件中
    3、在Token表中根据账户id、主机id、时间范围查询是否有该token
    4、返回已有Token或者用过随机生成一个8位的token写如数据库
    5、返回给前端
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
    '''
    返回批量执行命令页面
    :param request: 
    :return: 
    '''
    return render(request, 'multi_task.html')

@login_required
def file_transfer(request):
    '''
    
    :param request: 
    :return: 
    '''
    random_str = ''.join(random.sample(string.ascii_lowercase + string.digits, 8))
    return render(request, 'multi_transfer.html', locals())


@login_required
def multi_task(request):
    '''
    前端发送ajax请求，实例化Task并传入request，调用is_valid判断输入是否合法，如果合法在数据库中的Task表生成
    :param request: 
    :return: 
    '''
    task_obj = task_handler.Task(request)
    if task_obj.is_valid():
        result = task_obj.run()
        print(result[1].pid)
        return HttpResponse(json.dumps({"task_id":result[0].id, "timeout":result[0].timeout, "pid":result[1].pid}))
    return HttpResponse(111)


@login_required
def multi_task_result(request):
    task_id = request.GET.get('task_id')
    task_obj = models.Task.objects.get(id=task_id)
    results = list(task_obj.tasklog_set.values('id', 'status', 'host_user_bind__host_name__hostname', 'host_user_bind__host_name__ip_addr', 'result'))
    return HttpResponse(json.dumps(results))

@login_required
def cancel_cmd(request):
    pid = request.POST.get('pid')
    os.killpg(int(pid))
    return HttpResponse('ok')

@login_required
@csrf_exempt
def task_file_upload(request):
    '''
    上传文件
    1、拼接上传路径 配置文件路径／用户ID／随机字符串
    2、获取上传的文件名
    3、打开文件写入
    :param request: 
    :return: 
    '''
    random_str = request.GET.get('random_str')
    upload_to = "%s/%s/%s" %(settings.FILE_UPLOADS, request.user.account.id, random_str)
    if not os.path.isdir(upload_to):
        os.makedirs(upload_to, exist_ok=True)

    file_obj = request.FILES.get('file')
    f = open("%s/%s" % (upload_to, file_obj.name), 'wb')
    for chunk in file_obj.chunks():
        f.write(chunk)
    f.close()
    return HttpResponse(json.dumps({'status':0}))

def send_zipfile(request,task_id,file_path):
    """
    Create a ZIP file on disk and transmit it in chunks of 8KB,
    without loading the whole file into memory. A similar approach can
    be used for large dynamic PDF files.
    """
    zip_file_name = 'task_id_%s_files' % task_id
    archive = zipfile.ZipFile(zip_file_name , 'w', zipfile.ZIP_DEFLATED)
    file_list = os.listdir(file_path)
    for filename in file_list:
        archive.write('%s/%s' %(file_path,filename),arcname=filename)
    archive.close()


    wrapper = FileWrapper(open(zip_file_name,'rb'))
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s.zip' % zip_file_name
    response['Content-Length'] = os.path.getsize(zip_file_name)
    #temp.seek(0)
    return response


@login_required
def task_file_download(request):
    task_id = request.GET.get('task_id')
    task_file_path = "%s/%s" % (settings.FILE_DOWNLOADS, task_id)
    return send_zipfile(request, task_id, task_file_path)