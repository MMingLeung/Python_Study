from django.shortcuts import render, redirect
from django.db import transaction
from app01.forms import ArticleForm
from app01 import models
from project_1 import settings
from utils import xss


def manager(request, *args, **kwargs):
    if request.method == 'GET':
        user_id = request.session.get("user_id")
        print(kwargs)
        condition = {}
        for k, v in kwargs.items():
            kwargs[k] = int(v)
            if v != "0":
                condition[k] = v
        print(condition)

        # 大分类
        type_list = models.Article.type_choices
        # 个人分类category
        category_list = models.Category.objects.filter(blog_id=1)
        # 个人标签
        tag_list = models.Tag.objects.filter(blog_id=1)
        #####筛选文章
        condition['blog_id'] = 1
        article_list = models.Article.objects.filter(**condition)
        print(type_list, article_list)
        return render(request, 'manager.html', {
            "type_list": type_list,
            "category_list": category_list,
            "article_list": article_list,
            "tag_list": tag_list,
            "kwargs": kwargs,
            "nid":1,
        })

def article_management(request, *args, **kwargs):
    if request.method == 'GET':
        user_id = request.session.get(settings.LOGIN_USER_INFO_SESSION_KEY)[settings.USER_ID_SESSION]
        print('kwargs',kwargs)
        condition = {}
        for k, v in kwargs.items():
            kwargs[k] = int(v)
            if v != "0":
                condition[k] = v
        print("condition", condition)

        # 大分类
        type_list = models.Article.type_choices
        # 个人分类category
        category_list = models.Category.objects.filter(blog_id=1)
        # 个人标签
        tag_list = models.Tag.objects.filter(blog_id=1)
        #####筛选文章
        condition['blog_id'] = user_id
        article_list = models.Article.objects.filter(**condition)
        article_list_count = models.Article.objects.filter(**condition).count()
        print("article_list_count", article_list_count)
        return render(request, 'article_management.html', {
            "type_list": type_list,
            "category_list": category_list,
            "article_list": article_list,
            "tag_list": tag_list,
            "kwargs": kwargs,
            "nid":1,
            "article_list_count":article_list_count
        })

def manager_new_article(request, nid):
    '''
    :param request: 
    :param nid: 文章id号
    :return: 
    '''

    #获取session中用户的值
    user_id = request.session.get(settings.LOGIN_USER_INFO_SESSION_KEY)[settings.USER_ID_SESSION]
    if request.method == "GET":
        #实例化form表单并传入request
        obj = ArticleForm(request=request)
        return render(request, 'new_article.html', {'obj': obj, 'nid':nid})
    else:
        #接收form提交的值
        form = ArticleForm(request=request, data=request.POST)
        #判断是否合法
        if form.is_valid():
            #事务处理
            with transaction.atomic():
                #从cleaned_data获取文章内容
                content = form.cleaned_data.pop('content')
                #防止xss攻击
                content = xss.xss(content)
                #获取tags，值是list
                tags = form.cleaned_data.pop('tags')
                #获取用户blog_id，用于Article表的数据增加
                blog_id = models.Blog.objects.filter(user__nid=user_id).values('nid').first()
                form.cleaned_data['blog_id'] = blog_id['nid']
                #插入数据，并获取刚插入数据的对象
                article_id = models.Article.objects.create(**form.cleaned_data)
                #插入文章内容
                models.ArticleDetail.objects.create(article_id=article_id.nid,content=content)
                #根据tags的值，构建列表
                tag_list = []
                for tag_id in tags:
                    tag_id = int(tag_id)
                    tag_list.append(models.Article2Tag(article_id=article_id.nid, tag_id=tag_id))
                models.Article2Tag.objects.bulk_create(tag_list)
                return redirect('/back_stage/'+str(user_id)+'/manager/article_management/choice-0-0-0/')
        else:
            print(form.errors)
            return render(request, 'new_article.html', {'obj': form, 'nid':nid})

def manager_filter(request, nid, key):
    if key == 'category':
        categroy_list = models.Category.objects.filter(blog__user__nid=nid)
        categroy_list_count = models.Category.objects.filter(blog__user__nid=nid).count()
        return render(request, 'category.html',
                      {"categroy_list": categroy_list, 'categroy_list_count': categroy_list_count, 'nid': nid})
    elif key == 'tag':
        tag_list = models.Tag.objects.filter(blog__user__nid=nid)
        tag_list_count = models.Tag.objects.filter(blog__user__nid=nid).count()
        return render(request, 'tag.html', {"tag_list": tag_list, 'tag_list_count': tag_list_count, 'nid': nid})
    elif key == 'user':
        avatar = models.UserInfo.objects.filter(nid=nid).values("avatar").first()
        return render(request, 'user.html', {'nid': nid, "avatar": avatar})

def delete_article(request, art_id):
    user_id = request.session.get(settings.LOGIN_USER_INFO_SESSION_KEY)[settings.USER_ID_SESSION]
    models.Article.objects.filter(nid=art_id).delete()
    return redirect('/back_stage/'+str(user_id)+'/manager/article_management/choice-0-0-0/')

def edit_article(request, art_id):
    print("art_id",art_id)
    user_id = request.session.get(settings.LOGIN_USER_INFO_SESSION_KEY)[settings.USER_ID_SESSION]
    if request.method == 'GET':
        obj = models.Article.objects.filter(nid=art_id, blog__user__nid=user_id).first()
        if not obj:
            return render(request, 'edit_article.html')
        tags = obj.tags.values_list('nid')
        if tags:
            tags = list(zip(*tags))[0]
        init_dict = {
            'nid':int(art_id),
            'title':obj.title,
            'summary':obj.summary,
            'category_id':obj.category_id,
            'article_type_id':obj.article_type_id,
            'content': obj.articledetail.content,
            'tags': tags
        }
        print(init_dict)
        form = ArticleForm(request=request, data=init_dict)
        return render(request, 'edit_article.html',{'form':form, 'art_id':art_id})
    elif request.method == 'POST':
        print('修改文章')
        form = ArticleForm(request=request, data=request.POST)
        if form.is_valid():
            obj = models.Article.objects.filter(nid=art_id, blog__user__nid=user_id).first()
            if not obj:
                return render(request, 'edit_article.html')
            with transaction.atomic():
                content = form.cleaned_data.pop('content')
                content = xss.xss(content)
                tags = form.cleaned_data.pop('tags')
                models.Article.objects.filter(nid=obj.nid).update(**form.cleaned_data)
                models.ArticleDetail.objects.filter(article=obj).update(content=content)
                num = models.Article2Tag.objects.filter(article=obj).delete()
                tag_list = []
                for tag_id in tags:
                    tag_id = int(tag_id)
                    a = models.Article2Tag(article_id=obj.nid, tag_id=tag_id)
                    print('循环',a.article, a.tag)
                    tag_list.append(models.Article2Tag(article_id=obj.nid, tag_id=tag_id))
                models.Article2Tag.objects.bulk_create(tag_list)
                return redirect('/back_stage/'+str(user_id)+'/manager/article_management/choice-0-0-0/')