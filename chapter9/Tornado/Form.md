# 自定义Form

# 一、定制插件

在Django Form中，打印实例化Form里面自定义的字段对象显示其对应的标签，也就是定义了\_\_str\_\_方法。并且根据传入的attrs字典为其添加对应数据（字符串格式化）

````
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

obj = TextInput(attrs={'class':'btn'})
print(obj)
````



## 二、定义字段（正则）



````
class Field(object):
	# 正则匹配通过，打印这个类就返回插件对象的__str__
    def __str__(self):
        if self.value:
            self.widget.attrs['value'] = self.value
        return str(self.widget)


class CharField(Field):
	# 定义默认插件
    default_widget = TextInput
    # 正则
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
````



## 三、定义Form



````
class BaseForm(object):
    def __init__(self, data):
    	# django中传入的request.POST实际就是一个字典
        self.data = data
        # 
        self.fields = {}
        # 通过对象的类型，获取这个类的所有属性
        for name, field in type(self).__dict__.items():
            # {'user': <__main__.CharField object at 0x101981710>, 'email': <__main__.EmailField object at 0x101981828>,
            if isinstance(field, Field):
			# 如果属性是Field类，就要拷贝一份，因为每一次实例化Form都是独立的，如果不拷贝赋值会相互覆盖
                new_field = copy.deepcopy(field)
                # 在Form对象中设置，以便Form对象能够获取
                setattr(self, name, new_field)
                # 用于is_valid判断
                self.fields[name] = new_field
	
	# 判断是否匹配
    def is_valid(self):
        flag = True
        # {'user': <__main__.CharField object at 0x101981710>, 'email': <__main__.EmailField object at 0x101981828>
        for name ,field in self.fields.items():
        	# 获取输入的值{'user':'matt', 'email':'matt@gmail.com'}
            user_input_val = self.data.get(name)
            # 调用对象的valid_field方法
            result = field.valid_field(user_input_val)
            if not result:
                flag = False
        return flag
````

