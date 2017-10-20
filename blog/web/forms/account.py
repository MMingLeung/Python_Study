from django.forms import Form, fields, widgets
from django.core.exceptions import ValidationError

class RegisterForm(Form):
    username = fields.CharField(widget=widgets.TextInput(attrs={'class': 'form-control'}))
    nickname = fields.CharField(widget=widgets.TextInput(attrs={'class': 'form-control'}))
    email = fields.EmailField(widget=widgets.EmailInput(attrs={'class': 'form-control'}))
    password = fields.CharField(widget=widgets.PasswordInput(attrs={'class': 'form-control'}))
    password2 = fields.CharField(widget=widgets.PasswordInput(attrs={'class': 'form-control'}))
    avatar = fields.FileField(
        required=False,
        widget=widgets.FileInput(attrs={'id': "imgSelect", 'class': 'i1'}))
    code = fields.CharField(widget=widgets.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, request, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.request = request

    def clean_code(self):
        input_code = self.cleaned_data['code']
        session_code = self.request.session.get('code')
        if input_code.upper() == session_code.upper():
            return input_code
        raise ValidationError('验证码错误')

    # def clean_password2(self):
    #     # 两个密码校验，注意顺序
    #     p1 = self.cleaned_data['password']
    #     p2 = self.cleaned_data['password2']
    #     print(p1,p2)

    def clean(self):
        # 两个密码校验，注意顺序
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')
        if p1 == p2:
            return self.cleaned_data
        # else:
        #     raise ValidationError("密码不一致")
        self.add_error('password2', ValidationError("密码不一致"))

class LoginForm(Form):

    username = fields.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        max_length=18,
        min_length=2,
        required=True,
        error_messages={
            'required': '不能为空',
            'max_length': '太长了',
            'min_length': '太短了',
        },
    )

    password = fields.CharField(
        widget=widgets.PasswordInput(attrs={'class': 'form-control'}),
        max_length=18,
        min_length=2,
        required=True,
        error_messages={
            'required': '不能为空',
            'max_length': '太长了',
            'min_length': '太短了',
        })

    code = fields.CharField(widget=widgets.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, request, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.request = request

    #定义clean方法，比对用户输入和session的值
    def clean_code(self):
        input_code = self.cleaned_data['code']
        session_code = self.request.session.get('code')
        if input_code.upper() == session_code.upper():
            return input_code
        raise ValidationError('验证码错误')

