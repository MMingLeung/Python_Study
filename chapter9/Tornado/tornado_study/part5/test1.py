import re
import copy
# ############## 定制插件（HTML） ##############
class TextInput(object):
    def __init__(self, attrs=None):
        if attrs:
            self.attrs = attrs
        else:
            self.attrs = {}

    def __str__(self):
        data_list = []
        for k, v in self.attrs.items():
            tpm = "{0}='{1}'" .format(k,v)
            data_list.append(tpm)
        tpl = '<input type="text" {0} />'.format(''.join(data_list))
        return tpl

class EmailInput(object):
    def __init__(self, attrs=None):
        if attrs:
            self.attrs = attrs
        else:
            self.attrs = {}

    def __str__(self):
        data_list = []
        for k, v in self.attrs.items():
            tpm = "{0}='{1}'" .format(k,v)
            data_list.append(tpm)
        tpl = '<input type="email" {0} />'.format(''.join(data_list))
        return tpl

class PassWordInput(object):
    def __init__(self, attrs=None):
        if attrs:
            self.attrs = attrs
        else:
            self.attrs = {}

    def __str__(self):
        data_list = []
        for k, v in self.attrs.items():
            tpm = "{0}='{1}'" .format(k,v)
            data_list.append(tpm)
        tpl = '<input type="password" {0} />'.format(''.join(data_list))
        return tpl

# obj = TextInput(attrs={'class':'btn'})
# print(obj)


# ############## 定制字段（正则） ##############

class Field(object):


    def __str__(self):
        if self.value:
            self.widget.attrs['value'] = self.value
        return str(self.widget)


class CharField(Field):

    default_widget = TextInput
    regex = "\w+"

    def __init__(self, widget=None):
        self.value = None
        self.widget = widget if widget else self.default_widget()

    def valid_field(self, value):
        if re.match(self.regex, value):
            self.value = value
            return True
        else:
            return False


class EmailField(Field):

    default_widget = EmailInput
    regex = "\w+@\w+"

    def __init__(self, widget=None):
        self.value = None
        self.widget = widget if widget else self.default_widget()

    def valid_field(self, value):
        if re.match(self.regex, value):
            self.value = value
            return True
        else:
            return False


# ############## 定制Form（正则） ##############
class BaseForm(object):
    def __init__(self, data):
        self.data = data
        self.fields = {}
        print(type(self).__dict__)
        #{'user': <__main__.CharField object at 0x101981710>, 'email': <__main__.EmailField object at 0x101981828>, '__doc__': None, '__module__': '__main__'}
        for name, field in type(self).__dict__.items():
            print(name, field)
            # 如果字段是Field这个类，就要拷贝一份
            if isinstance(field, Field):
                # 在对象设置，以便对象能够获取
                print(111)
                new_field = copy.deepcopy(field)
                setattr(self, name, new_field)
                self.fields[name] = new_field

    def is_valid(self):
        flag = True
        for name ,field in self.fields.items():
            user_input_val = self.data.get(name)
            result = field.valid_field(user_input_val)
            if not result:
                flag = False
        return flag



# ############## 使用 ##############
class LoginForm(BaseForm):
    user = CharField()

    email = EmailField()

# request.POST 本质是字典
form = LoginForm({'user':'matt', 'email':'matt@gmail.com'})
print(form.user)
print(form.email)
print(form.is_valid())