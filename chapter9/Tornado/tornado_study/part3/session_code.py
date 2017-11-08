# import importlib
#
#
# path = 'scrapy.middlerware.C1'
#
# md,cls_name = path.rsplit('.', maxsplit=1)
# print(cls_name)
#
# importlib.import_module(md)


class Foo(object):
    def __getitem__(self, item):
        return "123"

    def __setitem__(self, key, value):
        pass

    def __delitem__(self):
        pass

obj = Foo()
# b = obj['k1']
# print(b)

# obj['k1'] = 666
#
# del obj['k1']

class CacheSession(object):
    def __getitem__(self, item):
        return '123'

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

class RedisSession(object):
    def __getitem__(self, item):
        return '123'


class SessionFactory(object):

    @staticmethod
    def get_session():
        import settings
        md, cls_name = settings.SESSION_ENGINE.rsplit('.', maxsplit=1)
        import importlib
        md = importlib.import_module(md)
        cls = getattr(md, cls_name)
        return cls
