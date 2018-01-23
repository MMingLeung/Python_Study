#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
字段的正则匹配及打印输出对应 Widget 的 html 标签
'''
import re
from CaroForm3.Widget import MultiSelectBox, MultiCheckBox, SingleSelectBox, SingleCheckbox, TextInput
from CaroForm3.FramworkFactory import Framework


class Field(object):
    def __init__(self, widget):
        self.widget = widget
        self.status = False
        self.name = None
        self.error = None
        self.value = None # 当前字段的值

    def valid_field(self, handler):
        '''
        
        :param handler:  不同框架获取前端输入的句柄
        :return: 
        '''
        raise NotImplementedError

    def __str__(self):
        if not self.value:
            return str(self.widget)

        if isinstance(self.widget, MultiSelectBox):
            self.widget.selected_value_list = self.value
        elif isinstance(self.widget, MultiCheckBox):
            self.widget.text_value_list = self.value
        elif isinstance(self.widget, SingleSelectBox):
            self.widget.select_value_list = self.value
        elif isinstance(self.widget, SingleCheckbox):
            self.widget.text_value_dict = self.value
        else:
            self.widget.attrs['value'] = self.value
        return str(self.widget)

    def set_value(self, value):
        '''
        用于动态设置 Field 对象的值
        :param value: 
        :return: 
        '''
        self.value = value


class NormalField(Field):
    '''
    CharField, PasswordField, EmailField 的父类
    '''
    DEFAULT_WIDGET = TextInput()

    REGEX = ''

    def __init__(self, required=True, max_length=None, min_length=None, error=None, widget=None):
        self.custom_errors_dict = {}
        if error:
            self.custom_errors_dict.update(error)

        self.required = required
        self.max_length = max_length
        self.min_length = min_length

        widget = widget if widget else self.DEFAULT_WIDGET
        super(NormalField, self).__init__(widget)

    def valid_field(self, handler):
        input_value = Framework.get_framwork().get_argument(handler, self.name, None)

        self.value = input_value

        if not self.value:
            if not self.required:
                self.status = True
                return
            if self.custom_errors_dict.get('required', None):
                self.error = self.custom_errors_dict['required']
            else:
                self.error = "{} is required".format(self.name)
            return

        if not re.match(self.REGEX, input_value):
            if self.custom_errors_dict.get('invalid', None):
                self.error = self.custom_errors_dict['invalid']
            else:
                self.error = "{} is invalid".format(self.name)
            return

        if self.max_length:
            if len(input_value) > self.max_length:
                if self.custom_errors_dict.get('max_length', None):
                    self.error = self.custom_errors_dict['max_length']
                else:
                    self.error = "{}'s length is longer than {}".format(self.name, self.max_length)
                return

        if self.min_length:
            if len(input_value) < self.min_length:
                if self.custom_errors_dict.get('max_length', None):
                    self.error = self.custom_errors_dict['min_length']
                else:
                    self.error = "{}'s length is shorter than {}".format(self.name, self.min_length)
                return

        self.status = True


class CharField(NormalField):

    REGEX = '^.*$'


class EmailField(NormalField):

    REGEX = '^\w+@\w+\.\w+$'


class StringListField(Field):
    '''
    字符串列表
    针对其中每一个值作正则匹配
    '''

    REGEX = '^.$'

    DEFAULT_WIDGET = MultiCheckBox()

    def __init__(self, widget=None, required=True, ele_max_length=None, ele_min_length=None, error=None):
        self.custom_errors_dict = {}
        if error:
            self.custom_errors_dict.update(error)

        self.required = required
        self.ele_max_length = ele_max_length
        self.ele_min_length = ele_min_length

        widget = widget if widget else self.DEFAULT_WIDGET

        super(StringListField, self).__init__(widget)


    def valid_field(self, handler):
        input_value = Framework.get_framwork().get_argument(handler, self.name, None)

        self.value = input_value

        if not self.value:
            if not self.required:
                self.status = True
                return
            if self.custom_errors_dict.get('required', None):
                self.error = self.custom_errors_dict['required']
            else:
                self.error = "{} is required".format(self.name)
            return

        if not re.match(self.REGEX, input_value):
            if self.custom_errors_dict.get('invalid', None):
                self.error= self.custom_errors_dict['invalid']
            else:
                self.error = "{} is invalid".format(self.name)
            return

        for value in self.value:
            if self.ele_max_length:
                if len(value) > self.ele_max_length:
                    if self.custom_errors_dict.get('max_length', None):
                        self.error = self.custom_errors_dict['max_length']
                    else:
                        self.error = "{}'s length is longer than {}".format(self.name, self.ele_max_length)
                    return

            if self.ele_min_length:
                if len(value) < self.ele_min_length:
                    if self.custom_errors_dict.get('max_length', None):
                        self.error = self.custom_errors_dict['min_length']
                    else:
                        self.error = "{}'s length is shorter than {}".format(self.name, self.ele_min_length)
                    return

        self.status = True








