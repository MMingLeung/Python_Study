from django.shortcuts import render, HttpResponse, redirect
from utils.random_check_code import rd_check_code
from web.forms.account import RegisterForm, LoginForm
from app01 import models
from project_1 import settings
from io import BytesIO
import os



def login(request):
    '''
    登录模块
    :param request: 
    :return: 
    '''
    if request.method == 'GET':
        result = LoginForm(request)
        return render(request, 'login.html', {'result':result})
    else:
        result = LoginForm(request, request.POST)
        if result.is_valid():
            username = request.POST.get('username')
            pwd = request.POST.get('password')
            user = models.UserInfo.objects.filter(username=username).first()
            if pwd == user.password:
                request.session[settings.LOGIN_USER_INFO_SESSION_KEY] = {
                    settings.USER_NAME_SESSION:username,
                    settings.USER_ID_SESSION:user.nid
                }
                return redirect('/index/')
            else:
                return render(request, 'login.html', {'msg': settings.ERROR_MSG, 'result':result})
        else:
            return render(request, 'login.html', {'result': result})

def check_code(request):
    '''
    :param request: 
    :return: 验证码
    '''

    stream = BytesIO()
    img, code = rd_check_code()
    img.save(stream, 'png')
    #code需要保存在 session
    request.session['code'] = code
    return HttpResponse(stream.getvalue())

def register(request):
    '''
    用户注册
    :param request: 
    :return: 
    '''

    if request.method == 'GET':
        obj = RegisterForm(request)
        return render(request, 'register.html', {'obj':obj})
    else:
        obj = RegisterForm(request, request.POST, request.FILES)
        print(request.FILES)
        if obj.is_valid():
            if not obj.cleaned_data['avatar']:
                obj.cleaned_data['avatar'] = '/static/img/default_img.jpg'
            obj.cleaned_data.pop('code')
            obj.cleaned_data.pop('password2')
            models.UserInfo.objects.create(**obj.cleaned_data)
            return redirect('/')
        return render(request, 'register.html', {'obj':obj})

def logout(request):
    '''
    登出
    '''

    request.session.clear()
    return redirect('/index/')

def upload(request):
    if request.method == "POST":
        file_obj = request.FILES.get("avatar")
        file_path = os.path.join('static/img', file_obj.name)
        with open(file_path, 'wb') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
        return HttpResponse(file_path)

