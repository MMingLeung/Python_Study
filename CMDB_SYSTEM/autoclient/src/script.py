#!/usr/bin/env python
# -*- coding:utf-8 -*-
from lib.conf.config import settings
from .client import Agent, SSHSALT


def run():
    if settings.MODE == 'agent':
        obj = Agent()
    else:
        obj = SSHSALT()

    return obj.execute()