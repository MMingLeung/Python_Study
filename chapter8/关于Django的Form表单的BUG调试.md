## 1、需求

在个人博客文章的新建文章页面，分类、标签的获取需要根据当前登录用户的id或者用户名进行数据库的查询，所以在后台视图函数中,请求方法是GET请求时，实例化Form表单时需要传入request用来获取session里面当前用户id的值。

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/django-form-bug.png?raw=true)

## 2、实现方法

### 局部代码
	
	#views.py
	def manager_new_article(request, nid):
	     
    if request.method == "GET":
        obj = ArticleForm(request) #传入request
        return render(request, 'new_article.html', 
						{'obj': obj, 'nid':nid})




	#forms.py
	class ArticleForm(Form):
	
		#正则的匹配不需要针对某用户个人的标签，直接查询全表的标签作为匹配标准
		title = fields.CharField(max_length=64)
		content = fields.CharField(
				  widget=widgets.Textarea(
				  attrs={'id': 't1', 'name': "content"})
				  )
		type_list = fields.MultipleChoiceField(
					widget=widgets.SelectMultiple,
					choices=models.Article.type_choices,
					)
		tag_list = fields.MultipleChoiceField(
				   widget=widgets.SelectMultiple,
				   choices=models.Tag.objects.all().values_list("nid", "title")
					)
		category_list = fields.MultipleChoiceField(
						widget=widgets.SelectMultiple,
						choices=models.Category.objects.all().values_list("nid", "title")
						)
		#接收request
		#注：如果不填入request，使用args[0]获取会报错
		def __init__(self, request, *args, **kwargs):
		super(ArticleForm, self).__init__(*args, **kwargs)
		self.nid = request.session.get('user_id')
		#根据用户id查询对应的标签等列表并填充至fields中
		self.fields['type_list'].widget.choices = models.Article.type_choices
		self.fields['category_list'].widget.choices =models.Category.objects.filter(
								blog__user__nid=self.nid).values_list("nid", "title")
		self.fields['tag_list'].widget.choices = models.Tag.objects.filter(
								blog__user__nid=self.nid).values_list("nid", "title")
	
