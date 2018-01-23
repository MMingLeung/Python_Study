import tornado.web
from controller.account import LoginController
from controller.index import IndexController



settings = {
    'template_path': 'templates',
    'static_path': 'static',
    'static_prefix': '/sss/',
    'xsrf_token': True,
    'cookie_secret': 'aaa',
    'login_url': '/login',
}

application = tornado.web.Application([
    (r'/login', LoginController),
    (r'/index', IndexController),
], **settings)

if __name__ == '__main__':
    import CaroForm3
    CaroForm3.setup('tornado')

    application.listen(8800)
    tornado.ioloop.IOLoop.instance().start()
