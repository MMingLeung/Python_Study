import tornado.web
from tornado.web import authenticated


class BaseController(object):
    def get_current_user(self):
        return self.get_secure_cookie('xxx')

class IndexController(BaseController, tornado.web.RequestHandler):
    @authenticated
    def get(self, *args, **kwargs):
        data_list = [
            {'name':'aaa', 'age':16},
            {'name':'bbb', 'age':12},
            {'name':'ccc', 'age':32},
        ]
        self.render('index.html', data_list=data_list)
