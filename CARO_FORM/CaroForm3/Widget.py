#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
HTML 插件
功能：生成对应 HTML 标签 
'''


class Input(object):
    def __init__(self, attrs=None):
        self.attrs = attrs if attrs else {}

    def __str__(self):
        attrs_list = []
        input_tag = "<input {attrs}>"
        for key, value in self.attrs.items():
            temp = "{key}='{value}'".format(key=key, value=value)
            attrs_list.append(temp)
        input_tag = input_tag.format(attrs=' '.join(attrs_list))
        return input_tag


class TextInput(Input):
    def __init__(self, attrs=None):
        attr_dict = {'type': 'text'}
        if attrs:
            self.attrs = attr_dict.update(attrs)
        super(TextInput, self).__init__(attr_dict)


class EmailInput(Input):
    def __init__(self, attrs=None):
        attr_dict = {'type': 'email'}
        if attrs:
            attr_dict.update(attrs)
        super(EmailInput, self).__init__(attr_dict)


class PasswordInput(Input):
    def __init__(self, attrs=None):
        attr_dict = {'type': 'password'}
        if attrs:
            attr_dict.update(attrs)
        super(PasswordInput, self).__init__(attr_dict)


class SingleCheckbox(Input):
    def __init__(self, attrs=None, text_value_list=None, check_value=None):
        attr_dict = {'type': 'checkbox'}
        self.text_value_list = text_value_list if text_value_list else {}
        self.check_value = check_value
        if attrs:
            attr_dict.update(attrs)
        super(SingleCheckbox, self).__init__(attr_dict)

    def __str__(self):
        html_tag = """
                    <div>
                        <span>{text}</span>
                        {input}
                    <div>
                    """
        attrs_list = []
        for key, value in self.attrs.items():
            temp = "{key}='{value}'".format(key=key, value=value)
            attrs_list.append(temp)

        if self.text_value_list['value'] == self.check_value:
            input_tag = "<input 'checked'='checked' {attrs}>".format(attrs=' '.join(attrs_list))
        else:
            input_tag = "<input {attrs}>".format(attrs=' '.join(attrs_list))

        html_tag = html_tag.format(text=self.text_value_list['text'], input=input_tag)
        return html_tag


class MultiCheckBox(Input):
    def __init__(self, attrs=None, text_value_list=None, check_value_list=None):
        attr_dict = {'type': 'checkbox'}
        if attrs:
            attr_dict.update(attrs)

        self.text_value_list = text_value_list if text_value_list else []
        self.check_value_list = check_value_list if check_value_list else []
        super(MultiCheckBox, self).__init__(attr_dict)

    def __str__(self):
        html_tag = """
                    <div>
                        {tags}
                    </div>
                   """
        attrs_list = []
        for key, value in self.attrs.items():
            temp = "{key}='{value}'".format(key=key, value=value)
            attrs_list.append(temp)

        tag_list = []
        for item in self.text_value_list:
            if item['value'] in self.check_value_list:
                tags = "<span>{text}</span><input checked='checked' {attrs} value='{value}'>"
            else:
                tags = "<span>{text}</span><input {attrs} value='{value}'>"
            tags = tags.format(text=item['text'], value=item['value'],attrs=' '.join(attrs_list))
            tag_list.append(tags)

        html_tag = html_tag.format(tags=' '.join(tag_list))
        return html_tag


class SingleSelectBox(object):
    def __init__(self, attrs=None, select_value_list=None, selected_value=None):
        self.attrs = attrs if attrs else {}
        self.select_value_dict = select_value_list if select_value_list else []
        self.selected_value = selected_value

    def __str__(self):
        '''
        :return: 
        '''
        html_tag = """
        <select {attrs}>{options}</select>
        """
        attrs_list = []
        for key, value in self.attrs.items():
            temp = "{key}='{value}'".format(key=key, value=value)
            attrs_list.append(temp)

        option_list = []
        for item in self.select_value_dict:
            if item['value'] == self.selected_value:
                temp = "<option selected='selected' value={value}>{text}</option>"
            else:
                temp = "<option value={value}>{text}</option>"
            option = temp.format(value=item['value'], text=item['text'])
            option_list.append(option)

        html_tag = html_tag.format(attrs=' '.join(attrs_list), options=' '.join(option_list))
        return html_tag


class MultiSelectBox(object):
    def __init__(self, attrs=None, select_value_list=None, selected_value_list=None):
        attr_dict = {"multiple": "multiple"}
        if attrs:
            attr_dict.update(attrs)
        self.attrs = attr_dict

        self.select_value_list = select_value_list if select_value_list else []
        self.selected_value_list = selected_value_list if selected_value_list else []

    def __str__(self):
        '''
        :return: 
        '''
        html_tag = """
        <select {attrs}>{options}</select>
        """
        attrs_list = []
        for key, value in self.attrs.items():
            temp = "{key}='{value}'".format(key=key, value=value)
            attrs_list.append(temp)

        option_list = []
        for item in self.select_value_list:
            if item['value'] in self.selected_value_list:
                temp = "<option selected='selected' value={value}>{text}</option>"
            else:
                temp = "<option value={value}>{text}</option>"
            option = temp.format(value=item['value'], text=item['text'])
            option_list.append(option)

        html_tag = html_tag.format(attrs=' '.join(attrs_list), options=' '.join(option_list))
        return html_tag
