# Django ORM 操作

## 一、简介

ORM：对象关系映射。类 -> 数据表，属性 -> 列， 对象 -> 一条数据

<br>

## 二、配置

````python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_name',
        'USER': 'xxx',
      	'PASSWORD': 'pwd',
      	'HOST': 'localhost',
      	'PORT': 3306,
    }
}
````

<br>

````python
# __init__.py
import pymysql
pymysql.install_as_MySQLdb()
````



## 三、Model 类

### 1、字段

````Python
# 综合
models.EmailField
models.URLField
models.UUIDField
models.FileField
models.FilePathField
models.ImageField
models.IPAddressField
models.CommaSeparatedIntegerField

# 数字
models.FloatField()
models.DecimalField(decimal_places=, max_digits=)

# 时间
models.DateTimeField()

# 枚举
color_tuple = (
    ('1',"黑"),('2','白'),('3','蓝')
)
color = models.IntegerField(choices=color_tuple)
````

<br>

### 2、索引

````
# 联合唯一索引
unique_together = (
	('username', 'email'),
	)

# 联合索引
index_together = (
	('username', 'email'),
	)
````

<br>

### 3、自定义错误

```
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator, URLValidator, DecimalValidator, \
   MaxLengthValidator, MinLengthValidator, MaxValueValidator, MinValueValidator


test = models.CharField(
   max_length=32,
   error_messages={
       'c1': '优先错信息1',
       'c2': '优先错信息2',
       'c3': '优先错信息3',
   },
   validators=[
       RegexValidator(regex='root_\d+', message='错误了', code='c1'),
       RegexValidator(regex='root_112233\d+', message='又错误了', code='c2'),
       EmailValidator(message='又错误了', code='c3'), ]
)
```

<br>

### 4、CURD 操作

 **增：**

````python
# 方法一
models.ModelName.objects.create(属性=xx)

# 方法二
obj = models.ModelName(属性=xx)
obj.save()
````

<br>

**删：**

````python
models.ModelName.objects.filter(条件).delete()
````

<br>

改：

````python
models.ModelName.objects.filter(条件).update(属性=xx)
````

<br>

**查：**

````python
# ############################## 正向 ##############################
data_list = models.ModelName.objects.all() # 获取的是 queryset

# ############################## 反向 ##############################
obj = models.ModelName.objects.all().first()
# 外键所在表名_set()
obj.userinfo_set()

# ##################### values\values_list #####################
# values: 获取字典格式的数据
# values_list: 获取元组格式的数据
# 跨表： 表名/外键属性名__另一张表的属性
models.UserGroup.objects.values('id', 'group_name', 'userinfo__password')

# ############################## filter ##############################
# filter 内条件以 and 相连
# 可以跨表，同 value

# 有关比较的参数
# 大于 属性__gt=
# 小于 属性__lt=
# 在...之内 属性__in=[]
# 在一定范围内 属性__range[x,y]
# 以...开头 属性__startwith
# 包含 属性__contains
# 不包括 exclude(属性=xx) 

# ############################### 排序 ###############################
order_by('属性')
order_by('-属性') # 倒序

# ############################### 分组 ###############################
from django.db.models import Count


models.UserInfo.objects.values("user_group_id").annotate(x=Count("nid")).filter(x__gt=1)
````



### 5、高级用法

````python
# ############################### F ###############################
# 用于让所有属性自加的情况
from django.db.models import F
# 让所有 age 属性自加1
models.UserInfo.objects.all().update(age=F('age') + 1)
````

<br>

````python
# ############################### Q ###############################
from django.db.models import Q

models.UserInfo.objects.filter(Q(nid=1) |  Q(username="matt")) # and
models.UserInfo.objects.filter(Q(nid=1) &  Q(username="matt")) # or

# 常见用法
item_dict = {
    'k1':[1,2,3,4,],
    'k2':[2,],
    'k3':[4,],
}
con = Q
for k,v in item_dict.items():
    q = Q()
    q.connector = 'AND'
    for i in v:
        q.children.append(i)
    con.add(q, 'OR')
````

<br>

````python
# ############################### extra ###############################
# 额外的复杂查询
# 参数解析：
# 参数详解：
# 第一组：select , select_params
# SQL语句：select 此处 from table
# 例子：
# SQL语句：select id, name, (select count(1) from student)as n from class
v = models.UserInfo.objects.all().extra(
   select={
       'n':'select count(1) from app01_usergroup where nid>%s and nid<%s',
       'm':'select count(1) from app01_usergroup where nid>%s and nid<%s',
          }, select_params=[1,3,3,5])

# #####################################################################
# 第二组：where , params
# SQL语句：select * from table where 此处
# where=['','']通过and连接
v1 = models.UserInfo.objects.all().extra(
   where=['nid=1 or nid=2','username="%s"'],
   params=["matt",],
   order_by=['-nid','username'],
)

# #####################################################################
# 第三组：
# tables
# select * from 表,此处
# SQL语句：select * from userinfo , usergroup (笛卡尔积)
v1 = models.UserInfo.objects.all().extra(
    tables=['app01_usergroup'],
    where=['app01_userinfo.user_group_id=app01_usergroup.id']
)
````

<br>

### 6、原生 SQL 语句

````python
from django.db import connection, connections


cursor = connection.cursor()
cursor.execute("select * from app01_usergroup ")
row = cursor.fetchall()
print(row)
````

<br>

### 7、操作一览

| all    | filter    | distinct  | only        | exisit        |
| ------ | --------- | --------- | ----------- | ------------- |
|        |           | 去重        | 取部分值        | 判断是否存在        |
| dates  | detetimes | aggregate | bulk_create | get_or_create |
|        |           | 聚合        | 批量增加        | 存在取之，否则创建     |
| defer  |           |           |             |               |
| 同 only |           |           |             |               |

<br>

### 8、多对多

````python
# 假设有三个表 
# teacher: tid tname
# course: cid cname
# teacher_course: teacher course

# 方法一：
#获取老师Ella的信息
teacher_obj = models.Teacher.objects.filter(tname="Ella").first()

#反向查询与老师表关联的teacher_course的信息的对象
teacher_class_list = teacher_obj.teacher_course_set.all() 
for row in teacher_class_list:  
    print(row.course.cname)
# ######################################################################

# 方法二：
value_list = models.teacher_course.objects.filter(teacher__tname='Ella').values("course__name")

value_list = models.teacher_course.objects.filter(teacher__tname='Ella')
for row in value_list:
    print(row.course.name)
    
# ######################################################################
````

<br>

````python
# 假设有两个表，第三章表由 ManyToMany 创建 
# teacher: tid tname
# course: cid cname
# 注意！自动生成的第三张表无法像方法一中对其进行操作

# models.py
class Teacher(models.Model):
    tid = models.AutoField(primary_key=True)
    tname = models.CharField(max_length=64)
    c = models.ManyToManyField('Course')  
    
# views.py
obj = models.Teacher.objects.filter(tname="Ella").first()
obj.c.add(3,4) # 在 c 表增加跟 ella 对应的值，为3,4(跟 teacher_course 表类似关系)
obj.c.add(*[1,])  # 添加列表
obj.c.remove(*[1,])  # 移除
obj.c.set([1,])  # 修改全部重置变成1了
course_list = obj.m.all() # 获取 ella 全部的对应关系的课程，是一个 Course 的对象
course_list = obj.m.filter(只可以输入Course里面的列名)



````

