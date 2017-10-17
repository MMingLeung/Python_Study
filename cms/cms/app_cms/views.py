from django.shortcuts import render,HttpResponse, redirect
from .forms import LoginForm, RegisterForm, AddUserForm,AddGroupForm
from io import BytesIO
from utils.random_check_code import rd_check_code
from cms import settings
from django.db import transaction
from app_cms import models as c_models
from rbac import models as r_models
from django.contrib.auth.hashers import make_password, check_password
from rbac.service import initial_permission
import json


from django.http import QueryDict
from app_cms.data_config.basic_info_json_data import \
    table_config as BIJS_table_config, \
    motai_config as BIJS_motai_config, \
    search_config as BIJS_search_config
from app_cms.data_config.basic_ginfo_json_data import \
    table_config as BGIJS_table_config, \
    motai_config as BGIJS_motai_config, \
    search_config as BGIJS_search_config
from utils.data_list import get_data_list



# Create your views here.

def index(request):

    if request.method == 'GET':
        login_form = LoginForm(request)
        register_form = RegisterForm(request)
        return render(request, 'index.html', {'login_form':login_form, 'register_form':register_form})


def check_code(request):
    '''
    :param request: 
    :return: 验证码
    '''
    stream = BytesIO()
    img, code = rd_check_code()
    img.save(stream, 'png')
    #code需要保存在 session
    request.session[settings.CHECK_CODE_SESSION_KEY] = code
    return HttpResponse(stream.getvalue())


def register(request):

    form = RegisterForm(request=request, data=request.POST)
    print(request.POST)
    login_form = LoginForm(request)
    if form.is_valid():
        with transaction.atomic():
            form.cleaned_data.pop('code')
            form.cleaned_data.pop('password2')
            nickname = form.cleaned_data.pop('nickname')
            form.cleaned_data['password'] = make_password(form.cleaned_data['password'], settings.MakePasswordSalt, 'pbkdf2_sha256')
            new_user_obj = r_models.User.objects.create(**form.cleaned_data)
            c_models.UserInfo.objects.create(nickname=nickname,user_id=new_user_obj.id)
        return HttpResponse('注册成功')
    else:
        return render(request, 'index.html', {'register_form': form, 'login_form':login_form})


def login(request):

    login_form = LoginForm(request=request, data=request.POST)
    register_form = RegisterForm(request)
    if login_form.is_valid():
        username = login_form.cleaned_data['username']
        password = login_form.cleaned_data['password']
        try:
            database_obj = r_models.User.objects.filter(username=username).first()
        except Exception as e:
            return render(request, 'index.html',
                          {'login_form': login_form, 'register_form': register_form, 'errors': '账号或密码错误'})
        if check_password(password, database_obj.password):
            request.session[settings.SESSION_USER_INFO] = {'username':database_obj.username, 'id':database_obj.id}
            initial_permission(request, database_obj.id)
            return redirect('/backend/index.html')
        else:
            return render(request, 'index.html', {'login_form':login_form, 'register_form':register_form, 'errors':'账号或密码错误'})
    else:
        return render(request, 'index.html', {'login_form': login_form, 'register_form':register_form})


def backend_index(request):

    if not request.session.get(settings.SESSION_USER_INFO):
        return redirect('/index.html')
    else:
        return render(request, 'backend_index.html')


def basic_info_json(request):

    if request.permission_code == 'GET':
        if request.method == 'GET':


            data = get_data_list(request, BIJS_table_config, r_models.User)

            ret = {
                'table_config': BIJS_table_config,
                'server_list': list(data),
                'search_config': BIJS_search_config,
                'motai_config':BIJS_motai_config,
            }
            return HttpResponse(json.dumps(ret))

    elif request.permission_code == 'EDIT':
        if request.method == 'PUT':
            response = {'status':True, 'error':None}
            try:
                all_list = json.loads(str(request.body, encoding='utf8'))
                print(all_list)
                for row in all_list:
                    print(row)
                    if row:
                        id = row.pop('id')
                        #此处bug
                        #无法通过User表反向关联到Userinfo，已有OneToOne关系
                        nickname = row.pop('userinfo__nickname')
                        a = r_models.User.objects.filter(id=id).update(**row)
                        c_models.UserInfo.objects.filter(id=id).update(nickname=nickname)
                return HttpResponse(json.dumps(response))
            except Exception as e:
                print(e)
                response['error'] = "出错"
                response['status'] = False
                return HttpResponse(json.dumps(response))

    elif request.permission_code == 'ADD':
        if request.method == 'POST':
            flag = False
            response = {'status':True, 'data':None}
            new_user_info_dict = request.POST.get('new_user_info_dict')
            new_user_info_dict = json.loads(new_user_info_dict)
            #<QueryDict: {'username': ['Ken010102'], 'email': ['Ken010102@gmail.com'], 'code': ['f']
            st = ''
            item = '{n1}={n2}&'
            for k,v in new_user_info_dict.items():
                tmp = item.format(n1=k, n2=v)
                st += tmp
            q = QueryDict(st[:-1])
            add_form = AddUserForm(data=q)
            if add_form.is_valid():
                with transaction.atomic():
                    nickname = add_form.cleaned_data.pop('nickname')
                    add_form.cleaned_data['password'] = make_password(add_form.cleaned_data['password'], settings.MakePasswordSalt,
                                                                  'pbkdf2_sha256')
                    new_user_obj = r_models.User.objects.create(**add_form.cleaned_data)
                    c_models.UserInfo.objects.create(nickname=nickname, user_id=new_user_obj.id)
                    flag = True
            if not flag :
                response['status'] = False
                response['data'] = "输入信息有误"
            print(response)
            return HttpResponse(json.dumps(response))

    elif request.permission_code == 'DELETE':
        if request.method == 'DELETE':
            response = {'status':True, 'data':None}
            id_list = json.loads(str(request.body, encoding='utf8'))
            user_id = request.session.get(settings.SESSION_USER_INFO)['id']
            try:
                for i in id_list:
                    if user_id == i:
                        continue
                    c_models.UserInfo.objects.filter(id=i).first().delete()
                    r_models.User.objects.filter(id=i).first().delete()
            except Exception as e:
                response['status'] = False
                response['data'] = '删除失败'
            print("DELETE",response)
            return HttpResponse(json.dumps(response))


def basic_info(request):

    return render(request, 'backend_basic_info.html')


def basic_ginfo(request):

    if request.permission_code == 'GET':
        return render(request, 'backend_basic_ginfo.html')
    elif request.permission_code == 'DETAIL':
        if request.method == 'GET':
            # 先查询该组的成员id,姓名
            id = request.GET.get('nid')
            group_name = c_models.UserToGroup.objects.filter(group_id=id).values('group__title').distinct()
            print('group_name', group_name)
            in_group = c_models.UserToGroup.objects.filter(group_id=id).values('user_id', 'user__user__username')

            # 查询不在该组的成员id,姓名
            not_ingroup1 = c_models.UserToGroup.objects.exclude(group_id=id).values('user_id', 'user__user__username')


            # 不在UserToGroup的人
            not_ingroup2 = c_models.UserInfo.objects.extra(
                where=['app_cms_userinfo.id not in (select user_id from app_cms_usertogroup)']
            ).values('user_id', 'user__username')
            print('not_ingroup2', not_ingroup2)
            return render(request, 'backend_basic_ginfo_detail.html', {'in_group':in_group,
                                                                       'not_ingroup1':not_ingroup1,
                                                                       'not_ingroup2':not_ingroup2,
                                                                       'id':id,
                                                                       'group_name':group_name})

    elif request.permission_code == 'EDIT':
        #选择的人id和组id
        sel = request.POST.getlist('sel')
        group_id = request.GET.get('nid')
        sel2 = request.POST.getlist('sel2')

        print('sel',sel)
        print('group_id',group_id)
        print('sel2',sel2)

        #情况1：在无分组选择一个人往添加到左边分组


        u2g_id_list = c_models.UserToGroup.objects.all()
        old_u2g = []


        for item in u2g_id_list:
            old_u2g.append(item.user_id)
        print('UserToGroup所有人', old_u2g)

        if sel:
            #交集，在UserToGroup表中的需要改到这一组
            update_list = set(sel).intersection(old_u2g)
            #差集，不在UserToGroup表中的需要创建
            create_list = set(sel).difference(old_u2g)
        else:
            update_list=[]
            create_list=[]


        # #差集 老的存在新的没有
        # 移动到右边的需要删除
        if sel2:
            delete_list = set(sel2).difference(sel)
        else:
            delete_list = []
        if update_list:
            c_models.UserToGroup.objects.filter(user__user_id__in=update_list).update(group_id=group_id)
        elif create_list:
            for i in create_list:
                c_models.UserToGroup.objects.create(user_id=i, group_id=group_id)
        elif delete_list:
            c_models.UserToGroup.objects.filter(user__user_id__in=delete_list).delete()
        return redirect('/backend/basic_ginfo.html?md=detail&nid='+group_id)


def basic_ginfo_json(request):

    if request.permission_code == 'GET':
        if request.method == 'GET':

            data = get_data_list(request, BGIJS_table_config, c_models.UserGroup)

            ret = {
                'table_config': BGIJS_table_config,
                'server_list': list(data),
                'search_config': BGIJS_search_config,
                'motai_config':BGIJS_motai_config,
            }
            return HttpResponse(json.dumps(ret))

    elif request.permission_code == 'ADD':
        if request.method == 'POST':
            flag = False
            response = {'status':True, 'data':None}
            new_user_info_dict = request.POST.get('new_user_info_dict')
            new_user_info_dict = json.loads(new_user_info_dict)
            #<QueryDict: {'username': ['Ken010102'], 'email': ['Ken010102@gmail.com'], 'code': ['f']
            st = ''
            item = '{n1}={n2}&'
            for k,v in new_user_info_dict.items():
                tmp = item.format(n1=k, n2=v)
                st += tmp
            q = QueryDict(st[:-1])
            add_form = AddGroupForm(data=q)
            if add_form.is_valid():
                with transaction.atomic():
                    c_models.UserGroup.objects.create(**add_form.cleaned_data)
                    flag = True
            if not flag :
                response['status'] = False
                response['data'] = "输入信息有误"
            print(response)
            return HttpResponse(json.dumps(response))

    elif request.permission_code == 'EDIT':
        if request.method == 'PUT':
            response = {'status': True, 'error': None}
            try:
                all_list = json.loads(str(request.body, encoding='utf8'))
                for row in all_list:
                    if row:
                        id = row.pop('id')
                        c_models.UserGroup.objects.filter(id=id).update(**row)
                return HttpResponse(json.dumps(response))
            except Exception as e:
                response['error'] = e
                response['status'] = False
                return HttpResponse(json.dumps(response))

    elif request.permission_code == 'DELETE':
        print('delete')
        if request.method == 'DELETE':
            response = {'status': True, 'data': None}
            try:
                id_list = json.loads(str(request.body, encoding='utf8'))
                for group_id in id_list:
                    obj = c_models.UserToGroup.objects.filter(group_id=group_id)
                    if obj:
                        response['data'] = '请删除该组成员之后再删除组'
                        raise Exception('删除出错')
                    else:
                        c_models.UserGroup.objects.filter(id=group_id).delete()
            except Exception as e:
                response['status'] = False
            return HttpResponse(json.dumps(response))

