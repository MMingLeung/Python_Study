#!/usr/bin/env python
#! -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class Framework(object):
    '''
    单例模式形式为用户提供设置和获取类
    '''

    __framwork = None

    @staticmethod
    def set_framwork(name):
        Framework.__framwork = name

    @staticmethod
    def get_framwork():
        return Framework.__framwork()


class BaseFramework(metaclass=ABCMeta):
    '''
    抽象类
    get_argument: 获取单个输入
    get_arguments: 获取多个输入
    '''
    @abstractmethod
    def get_argument(self, handler, name, default=None):
        raise NotImplementedError

    @abstractmethod
    def get_arguments(self, handler, name, default=None):
        raise NotImplementedError


class Tornado(BaseFramework):
    def get_argument(self, handler, name, default=None):
        return handler.get_argument(name, default)

    def get_arguments(self, handler, name, default=None):
        return handler.get_arguments(name, default)
