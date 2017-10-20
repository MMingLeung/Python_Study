from django.forms import Form, fields, widgets
from app01 import models
from project_1 import settings


class ArticleForm(Form):
    title = fields.CharField(max_length=64,
                             widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '文章标题'})
                             )
    content = fields.CharField(
        widget=widgets.Textarea(attrs={'id': 't1', 'name': 'content', 'class': 'kind-content'})
    )
    summary=fields.CharField(
        widget=widgets.Textarea(attrs={'class': 'form-control', 'placeholder': '文章简介', 'rows': '3'})
    )
    article_type_id = fields.IntegerField(
        widget=widgets.RadioSelect(choices=models.Article.type_choices)
    )
    tags = fields.MultipleChoiceField(
        choices=models.Tag.objects.all().values_list("nid", "title"),
        widget=widgets.CheckboxSelectMultiple
    )
    category_id = fields.ChoiceField(
        choices=models.Category.objects.all().values_list("nid", "title"),
        widget=widgets.RadioSelect,
    )

    def __init__(self, request, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.nid = request.session.get(settings.LOGIN_USER_INFO_SESSION_KEY)[settings.USER_ID_SESSION]
        a = models.Category.objects.filter(
            blog__user__nid=self.nid).values_list("nid", "title")
        print('a',a)
        self.fields['category_id'].widget.choices = models.Category.objects.filter(
            blog__user__nid=self.nid).values_list("nid", "title")
        self.fields['tags'].widget.choices = models.Tag.objects.filter(blog__user__nid=self.nid).values_list("nid",
                                                                                                                 "title")

    def clean_content(self):
        old = self.cleaned_data['content']
        from utils.xss import xss
        return xss(old)
