#!/usr/bin/env python
# -*- coding:utf-8 -*-
import copy
from CaroForm3.Field import Field


class BaseForm(object):
    def __init__(self, handler):
        self.handler = handler
        self.value_dict = {}
        self.error_dict = {}
        self.valid_status = True
        self.fields = {}

        self.initialize()

    def initialize(self):
        for name, value in type(self).__dict__.items():
            if isinstance(value, Field):
                copy_field = copy.deepcopy(value)
                copy_field.name = name
                copy_field.widget.attrs['name'] = name
                self.fields[name] = copy_field
        self.__dict__.update(self.fields)

    def is_valid(self):
        for name, field in self.fields.items():
            field.valid_field(self.handler)
            if field.status:
                self.value_dict[name] = field
            else:
                print(field.error)
                self.error_dict[name] = field.error
                self.valid_status = False
        return self.valid_status

    def initialize_field_value(self, value_dict):
        for name, field in self.fields.items():
            field.set_value(value_dict.get(name, None))
