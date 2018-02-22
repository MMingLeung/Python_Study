# 自定义 ORM 组件 

````Python
#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
自定义 ORM 组件
通过 __new__ 方法控制类的构造过程
'''


class Field(object):
    def __init__(self, name, col_type, required, field_type):
        '''
        :param name: 列名
        :param col_type: 数据库中的类型
        :param required: 能否为空
        :param field_type: python 中的数据类型
        '''
        self.name = name
        self.col_type = col_type
        self.required = required
        self.field_type = field_type

    def __str__(self):
        return "%s: %s" % (self.__class__.__name__, self.name)


class StringField(Field):
    def __init__(self, name, required):
        super(StringField, self).__init__(
            name=name,
            col_type='varchar(100)',
            required=required,
            field_type=str,
        )


class IntField(Field):
    def __init__(self, name, required):
        super(IntField, self).__init__(
            name=name,
            col_type='varchar(100)',
            required=required,
            field_type=int,
        )


class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        mappings = dict()
        requireds = dict()
        field_types = dict()
        for key, value in attrs.items():
            if isinstance(value, Field):
                mappings[key] = value
                field_types[key] = value.field_type
                if value.required:
                    requireds[key] = value
        attrs['__mappings__'] = mappings
        attrs['__requireds__'] = requireds
        attrs['__field_types__'] = field_types
        return type.__new__(cls, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kwargs):
        self.fields = kwargs
        if self.check_fields():
            super(Model, self).__init__(**kwargs)

    def check_fields(self):
        '''
        检验字段是否合法
        1、必填字段是否填写
        2、字段类型与内容是否一致
        :return: 
        '''
        print(type(self).__dict__)
        requireds = set(type(self).__dict__['__requireds__'])
        applys = set(self.fields)
        not_input_fields = requireds - applys
        field_types = type(self).__dict__['__field_types__']
        if len(not_input_fields) == 0:
            # 字段全部填写
            # 验证类型
            for key, value in self.fields.items():
                if isinstance(self.fields[key], field_types[key]):
                    continue
                else:
                    raise TypeError('字段类型错误 %s' % self.fields[key])
            return True
        else:
            raise AttributeError('缺少字段 %s' % not_input_fields)


    def __getattr__(self, item):
        try:
            return self[item]
        except Exception as e:
            raise AttributeError('item not in fileds')

    def __setattr__(self, key, value):
        self[key] = value



class User(Model):
    name = StringField('姓名', required=False)
    age = IntField('年龄', required=True)

if __name__ == '__main__':
    u = User(name='Matt', age=15)
    print(u['name'], u['age'])
````



