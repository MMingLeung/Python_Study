from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Count, F
from django.db import transaction
from utils.pager import PageInfo
from app01 import models
from project_1 import settings
import datetime
import json
import os


def index(request, *args, **kwargs):
    '''
    :param request: 
    :param args: 
    :param kwargs: type_id
    :return: request, type_choice_list, article_list, type_id, page_info
    '''

    #获取用户选择的标签
    condition = {}
    #如果kwargs有值就赋给type_id
    type_id = int(kwargs.get('type_id')) if kwargs.get('type_id') else None
    if type_id:
        #article_type_id对应数据库Article表的字段，用于查询
        condition['article_type_id'] = type_id
    #获取数据库中的type_choice
    type_choice_list = models.Article.type_choices

    #分页
    current_page = request.GET.get("page")
    article_list_count = models.Article.objects.all().count()
    page_info = PageInfo(current_page, 5, article_list_count, '/')
    article_list = models.Article.objects.filter(**condition)[page_info.start():page_info.stop()]
    return render(request, 'index.html',
                  {'type_choice_list':type_choice_list,
                   'article_list':article_list,
                   'type_id':type_id,
                   'page_info':page_info}
                  )

def user_blog(request, site_name):
    '''
    个人博客首页
    :param request: 
    :param site_name: 
    :return: 
    '''

    blog_obj = models.Blog.objects.filter(site=site_name).first()
    #没有此blog返回首页
    if not blog_obj:
        return redirect('/')

    #分页以及个人文章列表
    current_page = request.GET.get("page")
    article_list_count =  blog_obj.article_set.all().count()
    site = '/{}/'.format(site_name)
    page_info = PageInfo(current_page, 3, article_list_count, site)
    article_list = blog_obj.article_set.all()[page_info.start():page_info.stop()]

    #粉丝数量
    fans_count = models.UserFans.objects.filter(user=blog_obj.user).values("user_id").annotate(c=Count("id"))

    #关注数量
    follow_count = models.UserFans.objects.filter(follower=blog_obj.user).values("follower_id").annotate(c=Count("id"))

    #类型分类
    category_list = models.Article.objects.filter(blog=blog_obj).values("category_id", "category__title").annotate(c=Count("nid"))

    #标签分类
    tag_list = models.Article.objects.filter(blog=blog_obj).values("tags__nid", "tags__title").annotate(c=Count("nid"))

    #时间分类
    time_sort = models.Article.objects.filter(blog=blog_obj).extra(select={'c':"DATE_FORMAT(create_time,'%%Y-%%m')"}).values('c').annotate(ct=Count('nid'))

    return render(request, 'user_blog.html', {'article_list':article_list,
                                              'page_info':page_info,
                                              'user_obj':blog_obj.user,
                                              'category_list':category_list,
                                              'tag_list':tag_list,
                                              'time_sort':time_sort,
                                              'blog':blog_obj,
                                              'fans_count':fans_count,
                                              'follow_count':follow_count})

def final_article(request, site_name, art_id):
    if request.method == 'GET':
        # 标签查询
        tag_list = models.Article.objects.filter(blog__site=site_name).values("tags__nid", "tags__title").annotate(
        c=Count("nid"))
        # 分类
        category_list = models.Article.objects.filter(blog__site=site_name).values("category__title").annotate(
        c=Count("nid"))
        # 时间分类
        time_sort = models.Article.objects.filter(blog__site=site_name).extra(
        select={"c": "DATE_FORMAT(create_time,'%%Y-%%m')"}).values("c").annotate(ct=Count('nid'))
        user_obj = models.UserInfo.objects.filter(blog__site=site_name).first()

        #获取文章的所有信息
        article_info = models.Article.objects.filter(nid=art_id).first()
        print(article_info)
        article_detail = models.ArticleDetail.objects.filter(article__nid=art_id).first()



        #################评论
        msg_list = [
            {'id': 1, 'content': '很好', 'parent_id': None, 'user':'A', 'time':'2017'},
            {'id': 2, 'content': '对', 'parent_id': None, 'user':'A', 'time':'2017'},
            {'id': 3, 'content': '啦啦啦', 'parent_id': None, 'user':'A', 'time':'2017'},
            {'id': 4, 'content': '不好', 'parent_id': 1, 'user':'A', 'time':'2017'},
            {'id': 5, 'content': '补不好', 'parent_id': 4, 'user':'A', 'time':'2017'},
            {'id': 6, 'content': '不对', 'parent_id': 2, 'user':'A', 'time':'2017'},
            {'id': 7, 'content': '好好', 'parent_id': 5, 'user':'A', 'time':'2017'},
            {'id': 8, 'content': '哇哇哇', 'parent_id': 3, 'user':'A', 'time':'2017'},
        ]

        msg_list = models.Comment.objects.filter(article__nid=art_id).values("nid", "content", "reply")
        msg2list = []
        for i in msg_list:
            msg2list.append(i)
        # print(msg2list)

        msg_list_dict = {}
        # 创建一个key
        for item in msg_list:
            item['child'] = []
            msg_list_dict[item['nid']] = item
        result = []
        # 有两个数据结构 msg_list，msg_list_dict
        for item in msg_list:
            pid = item['reply']
            if pid:
                msg_list_dict[pid]['child'].append(item)
            else:
                result.append(item)
        # print(result)
        ############## 打印 ##################
        '''
        1 
          2
        3
          4
            5
        '''
        comment_str = """"""
        """
        <div class='comment'>
            <div class='content'>asd</div>
            <div class='content'>asd</div>
                <div class='comment'>
                <div class='content'>asd</div>
                <div class='content'>asd</div>
                </div>
            <div class='content'>asd</div>
        </div>
        """

        ############################
        # comment_str += "<div class='comment'>"
        # for row in result:
        #     tpl = "<div class='content'>%s</div>" %(row['content'])
        #     comment_str += tpl
        #     if row['child']:
        #         comment_str += "<div class='comment'>"
        #         for j in row['child']:
        #             tpl = "<div class='content'>%s</div>" % (j['content'])
        #             comment_str += tpl
        #         comment_str += "</div>"
        # comment_str += "</div>"
        #
        from utils.comment import comment_tree
        comment_str = comment_tree(result)
        return render(request, "final_article.html", {'tag_list':tag_list, 'category_list':category_list, 'time_sort':time_sort, "user_obj":user_obj, 'article_info':article_info, 'article_detail':article_detail, 'comment_str':comment_str, 'result':result, 'site_name':site_name, 'art_id':art_id})
    else:
        reply_content = request.POST.get('reply_content')
        user_id = request.session.get(settings.LOGIN_USER_INFO_SESSION_KEY)[settings.USER_ID_SESSION]
        reply_id = request.POST.get('reply_id')
        if reply_id:
            reply_content = reply_content.split()[2]
            models.Comment.objects.create(content=reply_content, article_id=art_id, user_id=user_id, reply_id=reply_id)
        else:
            models.Comment.objects.create(content=reply_content, article_id=art_id, user_id=user_id)
        return redirect('/' + site_name + '/p/' + art_id + '.html')

def filter(request, site_name, key, val):
    '''
    根据分类筛选
    :param request: 
    :param site_name: 
    :param key: 
    :param val: 
    :return: 
    '''

    blog_obj = models.Blog.objects.filter(site=site_name).first()

    if key == 'tag':
        if val == 'None':
            article_list = models.Article.objects.filter(blog=blog_obj).extra(
                where=['app01_article.nid not in (select article_id from app01_article2tag)'],
            )
            print(article_list.query)
        else:
            article_list = models.Article.objects.filter(blog=blog_obj, tags__nid=val).all()
            print(article_list)
    elif key == 'category':
        article_list = models.Article.objects.filter(blog=blog_obj, category_id=val).all()
        print(article_list)
    else:
        article_list = models.Article.objects.extra(
            where=["DATE_FORMAT(create_time,'%%Y-%%m')=%s"],
            params=[val,],
        ).all()
        print(article_list)

    #粉丝数量
    fans_count = models.UserFans.objects.filter(user=blog_obj.user).values("user_id").annotate(c=Count("id"))

    #关注数量
    follow_count = models.UserFans.objects.filter(follower=blog_obj.user).values("follower_id").annotate(c=Count("id"))


    #分页以及个人文章列表
    current_page = request.GET.get("page")
    article_list_count = article_list.count()
    site = '/{}/{}/{}/'.format(site_name, key, val)
    page_info = PageInfo(current_page, 3, article_list_count, site)
    article_list = article_list.all()[page_info.start():page_info.stop()]

    # 标签查询
    tag_list = models.Article.objects.filter(blog__site=site_name).values("tags__nid", "tags__title").annotate(
    c=Count("nid"))
    # 分类
    category_list = models.Article.objects.filter(blog__site=site_name).values("category__title", "category_id").annotate(
    c=Count("nid"))
    # 时间分类
    time_sort = models.Article.objects.filter(blog__site=site_name).extra(
    select={"c": "DATE_FORMAT(create_time,'%%Y-%%m')"}).values("c").annotate(ct=Count('nid'))
    user_obj = models.UserInfo.objects.filter(blog__site=site_name).first()

    return render(request, "user_blog.html",
                  {'article_list':article_list,
                   'tag_list':tag_list,
                   'category_list':category_list,
                   'time_sort':time_sort,
                   'user_obj':user_obj,
                   'page_info':page_info,
                   'fans_count':fans_count,
                   'follow_count':follow_count,
                   'blog':blog_obj
                   })

def up(request):
    '''
    赞踩功能
    1、根据前端ajax传入的文章id ,赞踩的参数（自定义的1或者0）以及session中的用户id判断是否赞踩过
    2、使用事务管理数据库的操作
    '''
    response = {'code': 1, 'msg': None}
    try:
        user_id = request.session.get(settings.LOGIN_USER_INFO_SESSION_KEY)[settings.USER_ID_SESSION]
    except Exception:
        response['msg'] = "请登录"
        return HttpResponse(json.dumps(response))
    try:
        article_id = request.POST.get('nid')
        val = int(request.POST.get('val'))
        obj = models.UpDown.objects.filter(user_id=user_id, article_id=article_id).first()
        print(obj)
        if obj:
            # 已经赞或者踩
            if val == 1:
                print('已赞')
                response['msg'] = '已经赞过了'
            else:
                print('已踩')
                response['msg'] = '已经踩过了'
        else:
        # 未赞或者踩
            with transaction.atomic():
                if val:
                    models.UpDown.objects.create(user_id=user_id, article_id=article_id, up=True)
                    models.Article.objects.filter(nid=article_id).update(up_count=F('up_count')+1)
                    response['status'] = 2
                else:
                    models.UpDown.objects.create(user_id=user_id, article_id=article_id, up=True)
                    models.Article.objects.filter(nid=article_id).update(down_count=F('down_count') + 1)
                    response['status'] = 3
    except Exception as e:
        response['status'] = False
        response['msg'] = str(e)
    return HttpResponse(json.dumps(response))

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

def ajax_comment(request, id):
    response = {"status":True, "msg":None, "data":None}
    try:
        msg_list = models.Comment.objects.filter(article__nid=id).values("nid", "content", "reply", "user__nickname", "create_time", "user__avatar")
        msg2list = []
        for i in msg_list:
            msg2list.append(i)
        print(msg2list)
        msg_list_dict = {}
        # 创建一个key
        for item in msg_list:
            item['child'] = []
            msg_list_dict[item['nid']] = item
        result = []
        # 有两个数据结构 msg_list，msg_list_dict
        for item in msg_list:
            pid = item['reply']
            if pid:
                msg_list_dict[pid]['child'].append(item)
            else:
                result.append(item)
        print('result:',result)
        response["data"] = result
    except Exception as e:
        response['msg'] = str(e)
    print(response)
    return HttpResponse(json.dumps(response, cls=DateEncoder))

def upload_img(request):

    #通过request ,可以获取上传文件类型
    upload_type = request.GET.get('dir')
    file_obj = request.FILES.get("imgFile")
    file_path = os.path.join('static/img', file_obj.name)
    with open(file_path, 'wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
    dic = {
        'error':0,
        'url':'/'+ file_path ,
        'message':'错误了'
    }
    return HttpResponse(json.dumps(dic))