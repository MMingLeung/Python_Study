# Django Form

## 一、Model  
操作数据库 

## 二、Form 
数据验证，生成html标签 
	# 基本使用方法
	from django.forms import Form, widgets as wdg, fields as flds, ModelForm
	class TestForm(Form):
	    user = flds.CharField()
	    email = flds.EmailField()
	    group_id = flds.ChoiceField(
	        widget=wdg.Select,
	        choices=models.UserGroup.objects.values_list('id', 'title')
	    )
	
	    def __init__(self, *args, **kwargs):
	        super(TestForm, self).__init__(*args, **kwargs)
	        self.fields['group'].choices = models.UserGroup.objects.values_list('id', 'title')
	



## 三、ModelForm  
应用场景：大型不使用 
操作数据库， 验证+生成html 

	# 使用及简单自定制
	class TestModelForm(ModelForm):
	    # 如果和model重复了，此处优先级更高
	    user = flds.EmailField(label='用户名')
	
	    class Meta:
	        model = models.UserInfo
	        fields = '__all__'
		# 自定制错误信息
	        error_messages = {
	            'user':{'required':'用户名不能为空'},
	            'email':{'required':'邮箱不能为空', 'invalid':'格式错误'}
	        }
	        #定制显示名称
	        labels = {
	            'user':'用户名',
	            'email':'邮箱'
	        }
	        help_texts = {
	            'user':'666'
	        }
		# 为字段定义输入框样式
	        # widgets = {
	        #     'user':wdg.Textarea(attrs={'class':'c1'})
	        # }
	
	        # 为字段定义验证规则,定制性不大
	        field_classes = {
	            'user':flds.EmailField
	        }
	
	    # 钩子
	    def clean_user(self):
	        pass
	
	# 对应视图处理
	def edit(request, nid):
	    obj = models.UserInfo.objects.filter(id=nid).first()
	    if request.method == "GET":
		# 实例化
	        form = TestModelForm(instance=obj)
	        context = {
	            'form':form
	        }
	        return render(request, 'edit.html', context)
	    else:
		# 获取用户提交的结果
	        form = TestModelForm(instance=obj, data=request.POST, files=request.FILES)
		# 验证输入是否合法
	        if form.is_valid():
	            # 写入数据库
	            form.save()
	            return redirect('http://www.baidu.com')
	        else:
	            return render(request, 'edit.html', {'form':form})

