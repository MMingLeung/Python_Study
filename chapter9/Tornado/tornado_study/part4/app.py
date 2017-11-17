import tornado.ioloop
import tornado.web
from tornado.web import RequestHandler
from session_code import SessionFactory



class IndexHandler(RequestHandler):
    def initialize(self):
        # 钩子
        print('initial')
        cls = SessionFactory.get_session()
        self.session = cls(self) # 把IndexHandler对象传入，可以使用其方法，如set_cookie等


    def get(self):
        user = self.session['user']
        if user:
            self.write("欢迎登录")

class LoginHandler(RequestHandler):
    def initialize(self):
        # 钩子
        print('initial')
        cls = SessionFactory.get_session()
        self.session = cls(self) # 把IndexHandler对象传入，可以使用其方法，如set_cookie等


    def get(self):
        self.render('login.html')

    def post(self):
        user = self.get_argument('user')
        pwd = self.get_argument('pwd')
        if user == 'matt' and pwd == '123':
            self.session['user'] = user
            self.redirect('/index')
        else:
            self.redirect('/login')

settings = {
    'template_path':'tpl',
    'static_path':'static'
}

application = tornado.web.Application([
    #                           反向生成
    (r'/index', IndexHandler),
    (r'/login', LoginHandler),
], **settings)


# 模板的静态文件




# 域名匹配
# application.add_handlers('www.lala.com',[
# (r'/index', IndexHandler),
# ])




if __name__ == '__main__':
    application.listen(8800)
    tornado.ioloop.IOLoop.instance().start()