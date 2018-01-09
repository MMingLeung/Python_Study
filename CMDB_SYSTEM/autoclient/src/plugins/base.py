'''
如果不使用__init__.py中的判断模式类型的逻辑，可以用继承的方式替代
'''
class BasePlugin(object):

    def command(self, cmd):
        if 'salt':
            pass