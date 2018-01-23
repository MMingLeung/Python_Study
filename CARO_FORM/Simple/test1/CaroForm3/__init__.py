#!/usr/bin/env python
#! -*- coding: utf-8 -*-
from CaroForm3.FramworkFactory import Tornado, Framework


def setup(framework_name='tornado'):
    framework_dict = {
        'tornado':Tornado,
        'django':'',
    }
    framework_class = framework_dict.get(framework_name)
    if not framework_class:
        raise Exception('请设置正确的 web 框架 {}'.format(' / '.join(framework_dict)))
    return Framework().set_framwork(framework_class)
