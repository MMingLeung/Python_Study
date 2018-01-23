# 自定义 Form 组件

## 简介：

&emsp;&emsp;本组件为 Tornado 框架提供类似 Django Form 组件的字段验证及生成 html 标签功能。

<br>

- [快速使用](#1)

  - [环境](#1_1)
  - [试用](#1_2)
  - [使用方式](#1_3)

- [系统详解](#2)

  - [架构](#2_1)
  - [组件功能及原理](#2_2)

  <br>

## <a id='1'>快速使用</a>：

### 1、<a id='1_1'>环境</a>

#### Python: 3.5

#### Packages:

&emsp;&emsp;使用 pip install -r requirement.txt 所需的包。

```python
# requirement.txt
tornado==4.5.3
```



### 2、<a id='1_2'>试用</a>

&emsp;&emsp;运行 apps.py， 输入 url ，进入测试页面

&emsp;&emsp;

<br>

------

**=========== 整体效果 ==========**

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/form_initial/form_initialize_index.png?raw=true)

<br>

------

**=========== 默认值 ===========**

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/form_initial/default_value.png?raw=true)

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/form_initial/multi_select_default.png?raw=true)

<br>

------

**=========== 错误提示 ===========**

1. 默认错误提示

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/form_initial/origin_error_msg.png?raw=true)

2. 自定义错误提示

![](https://github.com/MMingLeung/Markdown-Picture/blob/master/form_initial/customize_error_msg.png?raw=true)

------



### 3、<a id='1_3'>使用方式</a>

<br>

3.1、导入包

在 Tornado 视图函数中导入 Widget, Field, BaseForm

````python
from CaroForm3.Widget import MultiSelectBox, MultiCheckBox, TextInput, SingleSelectBox
from CaroForm3.Field import CharField, StringListField
from CaroForm3.Form import BaseForm
````

<br>

3.2、实例化 Form

&emsp;&emsp;本例子中定义了属性（需要验证的字段名称同时也是 html 标签中的 name 属性）、自定义错误信息、多选的选择及默认值。

​	**更多参数解释：[参数详解](#2_2)**

````python
# 例子：
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
````

<br>

3.3、前端页面

````html
// 显示标签
{% raw form.属性 %}

// 显示错误
{% raw form.error_dict.get('属性名称', '') %}
````

<br>

## <a id='2'>系统详解</a>：

### 1、<a id='2_1'>架构</a>

<br>

- Widget
  - Input 系列
    - 文本
    - CheckBox 系列
  - Select 系列
    - 单选
    - 多选
- Field
  - NormalField
    - CharField
    - EmailField
  - StringListFIeld
- Form



### 2、<a id='2_2'>组件功能及原理</a>

**Widget**

&emsp;&emsp;用于前端页面生成标签，接受用户传入的 attrs 字典参数，通过 \_\_str\_\_ 属性，打印输出带有自定义属性的标签。 

````Python
# ################################# Input 类参数说明 #################################
# attrs: 接收字典，其内容作为 html 标签的属性 （所有 widget 都有）

# text_value_list/select_value_list: 接收列表，其中每一个元素是字典，
# 									 根据 key, value 生成多选项 html 标签

# check_value_list: 接收列表，其中每一个元素是字符串对应 text_value_list 的 value 值，根据当前
#					参数为 html 标识为“选中状态”

# check_value/selected_value(): 接收字符串，类似 check_value_list, 但是单个值。

# 例子：
# 1、TextInput 添加属性
TextInput(attrs={'class':'form-control', 'id':'a1'})

# 2、MultiCheckBox 添加多项和默认值
MultiCheckBox(
  text_value_list=[
  {'text':'第一项', 'value':'1'},
  {'text':'第二项', 'value':'2'},
  {'text':'第三项', 'value':'3'},
],
  check_value_list=['1']
)

# 对应生成以下标签
"""
<div>
	<span>第一项</span><input checked='checked'  value='1'>
	....
</div>
"""
````

<br>

**Field**

````Python
# 类型
# NormalField(CharField/EmailField): 针对单个的值，作验证
# StringListField: 针对列表中多个元素，元素类型是字符串，对每一个元素作字段的验证
# ################################# Field 类参数说明 #################################
# required: 能否为空
# max_length/ele_max_length: 字段/元素最大长度
# min_length/ele_min_length: 字段/元素最小长度
# error: 自定义错误字典，key 包括：required、invalid（匹配正则失败）、max_length/ele_max_length、#							   min_length/ele_min_length

# 例子：
# 不能为空
# 最大/小值设置
# 错误信息自定义
EmailField(
  required=True,
  max_length=32, 
  min_length=8,
  error={
    'required':'不能为空',
  	'invalid':'字段不合法',
  	'max_length':'邮箱长度超出限制',
    'min_length':'邮箱长度必须大于8位',
  })
````

<br>

**Form**

````Python
# ################################# Form 的使用 #################################
# 综合上述插件，自定义 Form 类
class MyForm(BaseForm):
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

# ################################# 嵌入 Tornado #################################
# Tornado 部分代码
class LoginController(tornado.web.RequestHandler):
    def get(self):
      	# 实例化自定义的 form 类
        form = MyForm(self)
        
        # 动态赋予默认值操作
        form.initialize_field_value({'username': 'initialize_username'})
        
        # 传到前端
        self.render('login.html', msg='', form=form)

    def post(self, *args, **kwargs):
        form = LoginForm(self)
        # 验输入段合法性
        if form.is_valid():
            print('合法')
        else:
          	print('不合法')
            # 传入 form 使页面显示错误信息
            self.render('login.html', msg='', form=form)
````



<br>

````Html
// 前端部分代码
<form method="POST">

    <div>
        <h3>用户名</h3>
        <div>
            {% raw form.username %}
        </div>

        <div>
            错误信息：{% raw form.error_dict.get('username', '') %}
        </div>

    </div>
    <div>
        <h3>密码</h3>
        <div>
            {% raw form.password %}
        </div>
        <div>
            错误信息：{% raw form.error_dict.get('password', '') %}
        </div>

    </div>
    <div>
        <h3>性别</h3>
        <div>
            {% raw form.gender %}
        </div>
        <div>
            错误信息：{% raw form.error_dict.get('gender', '') %}
        </div>

    </div>
        <div>
            <h3>科目</h3>
        <div>
            {% raw form.subject %}
        </div>
        <div>
            错误信息：{% raw form.error_dict.get('subject', '') %}
        </div>

    </div>
        <div>
            <h3>爱好(多选)</h3>
        <div>
            {% raw form.hobby %}
        </div>
        <div>
            错误信息：{% raw form.error_dict.get('hobby', '') %}
        </div>
    </div>
    <input type="submit">{{ msg }}
</form>
````

