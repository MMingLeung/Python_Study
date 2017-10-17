from django.forms import Form, fields, widgets
from django.core.exceptions import ValidationError
from cms import settings

class LoginForm(Form):
    username = fields.CharField(
        max_length=32,
        widget=widgets.TextInput(attrs={'class':'form-control'}),
        min_length=5,
        required=True,
        error_messages={
            'required':'不能为空',
            'max_length':'账号过长',
            'min_length':'账号过短',
        }
        )
    password = fields.CharField(
        max_length=64,
        widget=widgets.PasswordInput(attrs={'class':'form-control'}),
        min_length=5,
        required=True,
        error_messages={
            'required':'不能为空',
            'max_length':'密码过长',
            'min_length':'密码过短',
        }
        )
    code = fields.CharField(
        widget=widgets.TextInput(
            attrs={'class': 'form-control'})
    )

    def __init__(self, request, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.request = request

        # 定义clean方法，比对用户输入和session的值

    def clean_code(self):
        input_code = self.cleaned_data['code']
        session_code = self.request.session.get(settings.CHECK_CODE_SESSION_KEY)
        print(input_code, session_code)
        if input_code.upper() == session_code.upper():
            return input_code
        raise ValidationError('验证码错误')


class RegisterForm(Form):
    username = fields.CharField(widget=widgets.TextInput(attrs={'class': 'form-control'}))
    nickname = fields.CharField(widget=widgets.TextInput(attrs={'class': 'form-control'}))
    email = fields.EmailField(widget=widgets.EmailInput(attrs={'class': 'form-control'}))
    password = fields.CharField(widget=widgets.PasswordInput(attrs={'class': 'form-control'}))
    password2 = fields.CharField(widget=widgets.PasswordInput(attrs={'class': 'form-control'}))
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

    def clean(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')
        if p1 == p2:
            return self.cleaned_data
        self.add_error('password2', ValidationError("密码不一致"))


class AddUserForm(Form):
    username = fields.CharField(
        max_length=32,
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        min_length=3,
        required=True,
        error_messages={
            'required': '不能为空',
            'max_length': '账号过长',
            'min_length': '账号过短',
        }
    )
    password = fields.CharField(
        max_length=64,
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        min_length=3,
        required=True,
        error_messages={
            'required': '不能为空',
            'max_length': '密码过长',
            'min_length': '密码过短',
        }
    )
    nickname = fields.CharField(widget=widgets.TextInput(attrs={'class': 'form-control'}))
    email = fields.EmailField(widget=widgets.EmailInput(attrs={'class': 'form-control'}))


class AddGroupForm(Form):
    title = fields.CharField(
        max_length=64,
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        min_length=3,
        required=True,
        error_messages={
            'required': '不能为空',
            'max_length': '账号过长',
            'min_length': '账号过短',
        }
    )