import time
import tornado.web
from CaroForm3.Widget import MultiSelectBox, MultiCheckBox, TextInput, SingleSelectBox
from CaroForm3.Field import CharField, StringListField
from CaroForm3.Form import BaseForm


class LoginForm(BaseForm):
    username = CharField(error={'required': '不能为空'})
    password = CharField(error={'required': '不能为空'})
    gender = CharField(widget=SingleSelectBox(
        select_value_list=[
            {'text': '男', 'value': '1'},
            {'text': '女', 'value': '2'},
        ]
    ))
    subject = StringListField(
        widget=MultiCheckBox(
            text_value_list=[
                {'text': '语文', 'value': '1'},
                {'text': '数学', 'value': '2'},
                {'text': '英语', 'value': '3'},
                {'text': '地理', 'value': '4'},
            ],
            check_value_list=['1', '2']
        ))
    hobby = CharField(
        widget=MultiSelectBox(
            select_value_list=[
                {'text':'C 语言','value':'1'},
                {'text':'C++ 语言','value':'2'},
                {'text':'C# 语言','value':'3'},
                {'text':'Python 语言','value':'4'},
                {'text':'Java 语言','value':'5'},
            ],
            selected_value_list=['4',]
        )
    )


class LoginController(tornado.web.RequestHandler):
    def get(self):
        form = LoginForm(self)
        form.initialize_field_value({'username': 'initialize_username'})
        self.render('login.html', msg='', form=form)

    def post(self, *args, **kwargs):
        form = LoginForm(self)

        if form.is_valid():
            print('合法')
        else:
            self.render('login.html', msg='', form=form)
