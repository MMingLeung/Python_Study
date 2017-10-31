from django.shortcuts import render, HttpResponse, redirect
from django.template.response import TemplateResponse
from app01 import models
from django.forms import Form, widgets as wdg, fields as flds, ModelForm
# Create your views here.
#判断是否有值没有就用自己的
# test_template = None


class TestModelForm(ModelForm):
    # 如果和model重复了，此处优先级更高
    user = flds.EmailField(label='用户名')

    class Meta:
        model = models.UserInfo
        fields = '__all__'
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


def test(request):
    '''
    对用户表操作
    :param request: 
    :return: 
    '''
    if request.method == 'GET':
        form = TestModelForm()
        context = {'form':form}
        return render(request, 'test.html',context)
    else:
        form = TestModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('http://www.baidu.com')
        return render(request, 'test.html', {'form':form})

    # return TemplateResponse(request, [] or ['111.html','my_change_list_template.html'], {'k1':'v1'})

def edit(request, nid):
    obj = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = TestModelForm(instance=obj)
        context = {
            'form':form
        }
        return render(request, 'edit.html', context)
    else:
        form = TestModelForm(instance=obj, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('http://www.baidu.com')
        else:
            return render(request, 'edit.html', {'form':form})