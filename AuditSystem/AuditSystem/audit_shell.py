#! -*-coding:utf8-*-
from audit.backend import user_interactive
import sys
import os
import django

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AuditSystem.settings")
    django.setup() #手动注册django所有APP
    obj = user_interactive.UserShell(sys.argv)
    obj.start()